import os
import requests
import json
from elasticsearch import Elasticsearch


def resp_msg(msg, resp, throw=True, ignore=[]):
    rsc = resp.status_code
    print("{} [Status: {}]".format(msg, rsc))
    if rsc >= 400 and rsc not in ignore:
        if throw:
            raise RuntimeError(resp.text)


class ElasticClient:
    """ """

    def __init__(self, url, configs_dir="."):
        self.docker = os.environ.get("LTR_DOCKER") != None
        self.configs_dir = configs_dir  # location of elastic configs
        self.url = url
        if self.docker:
            self.host = "elastic"
        else:
            self.host = "localhost"

        print(f"{self.url}:9200")
        self.elastic_ep = f"{self.url}:9200/_ltr"
        self.es = Elasticsearch(f"{self.url}:9200")

    def get_host(self):
        return self.host

    def check_index_exists(self, index):
        return self.es.indices.exists(index=index)

    def reset_ltr(self, index):
        resp = requests.delete(self.elastic_ep)
        resp_msg(
            msg="Removed Default LTR feature store".format(), resp=resp, throw=False
        )
        resp = requests.put(self.elastic_ep)
        resp_msg(msg="Initialize Default LTR feature store".format(), resp=resp)

    def create_featureset(self, index, name, ftr_config):
        resp = requests.post(
            "{}/_featureset/{}".format(self.elastic_ep, name), json=ftr_config
        )
        resp_msg(msg="Create {} feature set".format(name), resp=resp)

    def submit_model(self, featureset, index, model_name, model_payload):
        model_ep = "{}/_model/".format(self.elastic_ep)
        print(model_ep)
        create_ep = "{}/_featureset/{}/_createmodel".format(self.elastic_ep, featureset)
        print(create_ep)

        resp = requests.delete("{}{}".format(model_ep, model_name))
        print(resp.text)
        print("Delete model {}: {}".format(model_name, resp.status_code))

        resp = requests.post(create_ep, json=model_payload)
        resp_msg(msg="Created Model {}".format(model_name), resp=resp)

    def submit_xgboost_model(self, featureset, index, model_name, model_payload):
        params = {
            "model": {
                "name": model_name,
                "model": {"type": "model/xgboost+json", "definition": model_payload},
            }
        }
        self.submit_model(featureset, index, model_name, params)
