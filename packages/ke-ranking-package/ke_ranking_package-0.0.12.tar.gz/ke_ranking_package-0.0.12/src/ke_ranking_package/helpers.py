import datetime
import json
import os
import re
import sys
from itertools import groupby
from multiprocessing import Manager

import joblib
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
import requests
from clickhouse_driver import Client
from joblib import Parallel, delayed
from tqdm import tqdm

import ke_ranking_package.config as config
import ke_ranking_package.queries as queries
from ke_ranking_package.elastic_client import ElasticClient
from ke_ranking_package.paths import Paths


def load_and_store_sesions_with_conversion_event(
    connection_str, data_dir, date_str, event_name, query, platform, min_version
):
    """Load and store sessions with atcs or clicks.

    Args:
        connection_str (str): connection string to db
        data_dir (str): path to save data
        date_str (str): date
        event_name (str): name of conversion event (clicks/atcs)
        query (str): sql query
        platform (str): platform to get data from (ANDROID/WEB/IOS)
        min_version (str): app version
    """
    clickhouse_client = Client.from_url(connection_str)
    sessions_with_conv_event = []

    for fold_id in range(config.TOTAL_FOLDS):
        sessions_with_conv_event_fold = clickhouse_client.query_dataframe(
            query,
            params={
                "date": date_str,
                "platform": platform,
                "min_version": min_version,
                "fold_id": fold_id,
                "total_folds": config.TOTAL_FOLDS,
            },
        )
        sessions_with_conv_event.append(sessions_with_conv_event_fold)
    sessions_with_conv_event = pd.concat(sessions_with_conv_event)
    sessions_with_conv_event[["session_id", "install_id"]] = sessions_with_conv_event[
        ["session_id", "install_id"]
    ].astype(str)

    os.makedirs(f"{data_dir}", exist_ok=True)
    sessions_with_conv_event.reset_index(inplace=True, drop=True)
    sessions_with_conv_event['date'] = sessions_with_conv_event['date'].apply(lambda x: pd.to_datetime(x))
    sessions_with_conv_event.to_parquet(
        f"{data_dir}/sessions_with_{event_name}_{platform.lower()}.parquet"
    )


def load_and_store_sessions_with_orders(
    connection_str, root_dir, start_date, end_date, platform
):
    """Load and store sessions with orders.

    Args:
        connection_str (str): connection string to db
        root_dir (_type_): path to save data
        platform (str): platform to get data from (ANDROID/WEB/IOS)
    """
    clickhouse_client = Client.from_url(connection_str)
    end_date_orders = pd.to_datetime(end_date) + datetime.timedelta(
        days=config.NUM_DAYS_AHEAD
    )

    session_with_orders = clickhouse_client.query_dataframe(
        queries.get_session_with_orders,
        params={
            "start_date": start_date,
            "end_date": end_date_orders,
            "platform": platform,
        },
    )
    session_with_orders["order_created_at"] = pd.to_datetime(
        session_with_orders["order_created_at"]
    )
    session_with_orders["date"] = session_with_orders["order_created_at"].dt.date
    session_with_orders = (
        session_with_orders.groupby(["date", "query", "session_id"])
        .agg({"ordered_sku_group_id": list})
        .reset_index()
    )
    session_with_orders[["session_id", "date"]] = session_with_orders[
        ["session_id", "date"]
    ].astype(str)
    session_with_orders.to_parquet(
        f"{root_dir}/sessions_with_orders_{platform.lower()}_{start_date}_{end_date}.parquet"
    )


def query_transform(df):
    """Transformation of query string.

    Args:
        df (pd.DataFrame): dataframe with queries

    Returns:
        pd.DataFrame: dataframe with transformed queries
    """
    df["query"] = df["query"].str.lower()
    df["query"] = df["query"].apply(lambda x: re.sub("[^ \w+]", "", x))
    df["query"] = df["query"].apply(lambda x: x.strip())
    df = df[df["query"] != ""]
    return df


def upload_data_to_es(sku_group_ids, connection_string):
    """Upload data to Elasticsearch

    Args:
        sku_group_ids (list of str): list of sku_group ids
    """
    # Фичи sku групп для добавления в индекс эластика
    clickhouse_client = Client.from_url(connection_string)
    sku_group_features = clickhouse_client.query_dataframe(
        queries.get_skg_features_to_es
    )
    sku_group_features["full_category_title"] = sku_group_features[
        "full_category_title"
    ].apply(lambda x: "; ".join(x))

    sku_groups_to_es = sku_group_features[
        sku_group_features.sku_group_id.isin(sku_group_ids)
    ]

    batch_size = 10000
    for i in tqdm(range(0, sku_groups_to_es.shape[0] // batch_size + 1)):
        payload = ""
        for ind, row in sku_groups_to_es.iloc[
            i * batch_size : (i * batch_size) + batch_size
        ].iterrows():
            data = [
                {
                    "index": {
                        "_index": config.INDEX,
                        "_type": "_doc",
                        "_id": str(row.sku_group_id),
                    }
                },
                {
                    "sku_group": {
                        "id": int(row.sku_group_id),
                        "price": {"full": 0, "sell": 0},
                        "rating": 0,
                        "orders_quantity": 0,
                        "random_order": 0,
                    },
                    "product": {
                        "id": int(row.product_id),
                        "title": row.title,
                        "is_adult_category": False,
                        "date_created": "2022-08-18T18:43:37.251804058+03:00",
                        "orders_quantity": 0,
                        "rating": 0,
                        "random_order": 0,
                    },
                    "category": {
                        "id": int(row.category_id),
                        "path": [],
                        "title": row.category_title,
                        "full_title": row.full_category_title,
                        "is_adult": False,
                    },
                    "offers": [],
                    "shop": {"id": 0, "rating": 0},
                    "skus": [],
                    "facets": [],
                    "score": 0,
                    "ab_score": 0,
                },
            ]
            payload = payload + "\n".join([json.dumps(line) for line in data]) + "\n"

        requests.put(
            f"{config.ES_URL}:9200/_bulk",
            headers={"Content-Type": "application/x-ndjson"},
            data=payload,
        )


def create_index_es(es_url, index):
    """Create ElasticSearch index

    Args:
        es_url (str): ElasticSearch url
        index (str): index name
    """
    # подключаемся к ElasticSearch
    client = ElasticClient(url=es_url)
    # сбрасываем индекс ltr и создаем новый
    client.reset_ltr(index)

    # создаем индекс для bm25 фичей
    with open("featureset_bm25_config.json", "r") as openfile:
        featureset_bm25_config = json.load(openfile)

    client.create_featureset(
        index=index, name="bm25_features", ftr_config=featureset_bm25_config
    )
    return client


def get_unique_skgs(dates, root_dir, platforms=["android", "ios"]):
    """Get list of sku group ids from conversions.

    Args:
        root_dir (str): root directory
    Returns:
        pd.DataFrame: df with query and list of skgs
    """
    # Собираем данные за все дни (query -> [sku_group_id, sku_group_id, ...])
    query_with_skgs = []
    for d in dates:
        for platform in platforms:
            data_dir = Paths.data_dir(root_dir, d)
            query_with_skgs.append(
                pd.read_parquet(
                    f"{data_dir}/conversions_grouped_by_query_{platform}.parquet"
                )[["query", "sku_group_ids_imps"]]
            )

    query_with_skgs = pd.concat(query_with_skgs)
    query_with_skgs = query_transform(query_with_skgs)

    # группируем запросы за все дни для отправки только уникальных в эластик
    query_with_skgs = (
        query_with_skgs.groupby("query").agg({"sku_group_ids_imps": list}).reset_index()
    )
    query_with_skgs["sku_group_ids_imps"] = query_with_skgs[
        "sku_group_ids_imps"
    ].parallel_apply(lambda x: list(set([item for sublist in x for item in sublist])))
    query_with_skgs.reset_index(drop=True, inplace=True)
    unique_sku_group_ids = list(
        set(
            [
                int(item)
                for sublist in query_with_skgs.sku_group_ids_imps.values
                for item in sublist
            ]
        )
    )
    print(f"Unique sku groups: {len(unique_sku_group_ids)}")
    return query_with_skgs


def get_bm25_features_from_es(dates, root_dir):
    """Get bm25 features from ElasticSearch"""
    manager = Manager()
    query_sku_feat_dict = manager.dict()

    def get_bm25_features(sku_group_ids, keywords):
        params = {
            "keywords": keywords,
            "fuzzy_keywords": " ".join([x + "~" for x in keywords.split(" ")]),
            "keywordsList": [keywords],
        }
        ids = [int(i) for i in sku_group_ids]
        client = create_index_es(config.ES_URL, config.INDEX)
        res = client.log_query(config.INDEX, "bm25_features", ids, params)

        if res != 0:
            sku_features = {}
            for doc in res:
                sku_features[str(doc["sku_group"]["id"])] = doc["ltr_features"]
            query_sku_feat_dict[keywords] = sku_features

    query_with_skgs = get_unique_skgs(dates)

    batch_size = 2000
    for i in tqdm(range(0, query_with_skgs.shape[0] // batch_size + 1)):
        keywords = (
            query_with_skgs["query"]
            .iloc[i * batch_size : (i * batch_size) + batch_size]
            .values
        )
        sku_groups = query_with_skgs.sku_group_ids_imps.iloc[
            i * batch_size : (i * batch_size) + batch_size
        ].values

        _ = Parallel(n_jobs=32, prefer="threads")(
            delayed(get_bm25_features)(sku_group_ids, keyword)
            for sku_group_ids, keyword in zip(sku_groups, keywords)
        )

    query_sku_bm25_features_dict = query_sku_feat_dict.copy()
    joblib.dump(
        query_sku_bm25_features_dict, f"{root_dir}/query_sku_bm25_features_dict.joblib"
    )


def find_min(tree):
    """Finds the minimum leaf value in a tree.

    Args:
        tree (dict): dictionary of trees
        df (_type_): _description_
        n_jobs (int, optional): _description_. Defaults to 32.

    Returns:
        dict: minimum leaf
    """
    if "leaf" in tree.keys():
        return tree["leaf"]
    else:
        mapped = list(map(lambda t: find_min(t), tree["children"]))
        return min(mapped)


def find_first_feature(tree):
    """Finds the first feature in a tree, we then use this in the split condition
        It doesn't matter which feature we use, as both of the leaves will add the same value

    Args:
        tree (dict):
    """
    if "split" in tree.keys():
        return tree["split"]
    elif "children" in tree.keys():
        return find_first_feature(tree["children"][0])
    else:
        raise Exception("Unable to find any features")


def create_correction_tree(correction_value, feature_to_split_on):
    """Creates new tree with the given correction amount.

    Args:
        correction_value (float): leaf values for new tree
        feature_to_split_on (string): feature name for the new tree

    Returns:
        dict: correction tree
    """
    return {
        "children": [
            {"leaf": correction_value, "nodeid": 1},
            {"leaf": correction_value, "nodeid": 2},
        ],
        "depth": 0,
        "missing": 1,
        "no": 2,
        "nodeid": 0,
        "split": feature_to_split_on,
        "split_condition": 1,
        "yes": 1,
    }


def get_correction_tree(trees):
    """Calculate and return a tree that will provide a positive final score.

    Args:
        trees : dict
    """
    summed_min_leafs = sum(map(lambda t: find_min(t), trees))
    correction_value = abs(summed_min_leafs)
    print("Correction value: {}".format(correction_value))
    if summed_min_leafs < 0:
        feature_to_split_on = find_first_feature(trees[0])

        # define an extra tree that produces a positive value so that the sum of all the trees is > 0
        extra_tree = create_correction_tree(correction_value, feature_to_split_on)
        return extra_tree
    else:
        print("Not modifying tree, scores are already positive")
        return None
