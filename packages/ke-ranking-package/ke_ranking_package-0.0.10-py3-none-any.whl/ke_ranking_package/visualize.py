import base64
from io import BytesIO

import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
import requests
from IPython.display import HTML
from PIL import Image

import ke_ranking_package.queries


def get_thumbnail(path):
    path = (
        "\\\\?\\" + path
    )  # This "\\\\?\\" is used to prevent problems with long Windows paths
    i = Image.open(path)
    return i


def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, "jpeg")
        return base64.b64encode(buffer.getvalue()).decode()


def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'


def load_images_by_skg(sku_group_ids, connection_str):
    """
    Load images from DB by sku group ids.

    Args:
        sku_group_ids (list of int): list of sku group ids
        connection_str (str): connection string to postgres db

    Returns:
        pd.DataFrame: dataFrame with resized images
    """
    pg_connection = psycopg2.connect(connection_str)
    images = sqlio.read_sql_query(
        queries.get_images,
        pg_connection,
        params={"sku_group_ids": tuple(sku_group_ids)},
    )
    images["image"] = images.url_prefix + images.key + "/original.jpg"

    images.loc[:, "image"] = images.image.apply(
        lambda x: Image.open(requests.get(x, stream=True).raw)
    )
    images.loc[:, "image"] = images.im.apply(
        lambda x: x.resize((80, 100), Image.Resampling.LANCZOS)
    )
    return images


def print_df_with_images(df, columns_to_print, connection_str):
    """Print dataframe with images.

    Args:
        df (pd.DataFrame): df with skg ids and any data to print
        columns_to_print (list of str): name of columns to print in final DataFrame
        connection_str (_type_): connection string to postgres db

    Returns:
        HTML: DataFrame with skg images and any data.
    """
    images = load_images_by_skg(
        [int(i) for i in df.sku_group_id.unique()], connection_str
    )

    df = df.merge(images[["sku_group_id", "image"]], how="left", on="sku_group_id")
    df = df[~df.image.isna()]

    result_columns_dict = {}
    for col in columns_to_print:
        result_columns_dict[col] = df[col]
        df_images = pd.DataFrame(result_columns_dict)

    return HTML(df_images.to_html(formatters={"image": image_formatter}, escape=False))


def print_reranked_items_with_image(
    query_items,
    columns_to_print,
    connection_str,
    score_col="score",
    top_k=10,
    position=None,
):
    """Print dataframe with skg images and reranked skg images for query.

    Args:
        query_items (pd.DataFrame): df with query, sku_group_id and any data
        columns_to_print (list of str): name of columns to print in final DataFrame
        connection_str (_type_): connection string to postgres db
        score_col (str, optional): score to sort sku_group_ids
        top_k (int, optional): number of top items to print
        position (_type_, optional): position of initial ranking

    Returns:
        _type_: _description_
    """
    query_items_reranked = query_items.sort_values(by=score_col, ascending=False)[
        :top_k
    ]
    sku_group_ids_reranked = query_items_reranked.sku_group_id.unique()

    skg_unique = [int(i) for i in query_items.sku_group_id.unique()]
    skg_unique_reranked = [int(i) for i in sku_group_ids_reranked.sku_group_id.unique()]

    images = load_images_by_skg(skg_unique, connection_str)
    query_items = query_items.merge(
        images[["sku_group_id", "image"]], how="left", on="sku_group_id"
    )
    query_items = query_items[~query_items.image.isna()]

    query_items_reranked = load_images_by_skg(skg_unique_reranked, connection_str)
    query_items_reranked = query_items.merge(
        images[["sku_group_id", "image"]], how="left", on="sku_group_id"
    )
    query_items_reranked = query_items[~query_items.image.isna()]

    if position:
        query_items_init = query_items.sort_values(by="position")
        sku_group_ids_init = query_items_init.sku_group_id.unique()
        images_pos = load_images_by_skg(query_items_init, sku_group_ids_init)
        query_items_init = query_items_init.merge(
            images_pos[["sku_group_id", "image"]], how="left", on="sku_group_id"
        )

        query_items_images = pd.DataFrame(
            {
                "sku_group_id": query_items_init["sku_group_id"],
                "image": query_items_init["im"],
                "imps": query_items_init["impressions"],
                "clicks": query_items_init["clicks"],
                "atcs": query_items_init["atcs"],
                "sku_group_id_ranked": query_items_reranked["sku_group_id"],
                "image_reranked": query_items_reranked["im"],
                "imps_reranked": query_items_reranked["impressions"],
                "clicks_reranked": query_items_reranked["clicks"],
                "atcs_reranked": query_items_reranked["atcs"],
            }
        )

    else:
        result_columns_dict = {
            "sku_group_id": query_items["sku_group_id"],
            "image": query_items["im"],
            "sku_group_id_ranked": query_items_reranked["sku_group_id"],
            "image_reranked": query_items_reranked["im"],
        }
        for column in columns_to_print:
            result_columns_dict[f"{column}_reranked"] = query_items_reranked[column]

        query_items_images = pd.DataFrame(result_columns_dict)

    return HTML(
        query_items_images.to_html(
            formatters={"image": image_formatter, "image_reranked": image_formatter},
            escape=False,
        )
    )
