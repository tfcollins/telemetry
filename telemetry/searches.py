import telemetry
import datetime
import os


class searches:
    use_test_index = False

    def __init__(self, mode="elastic", server="alpine"):
        if mode == "elastic":
            self.db = telemetry.elastic(server=server)

    def _get_schema(self, name):
        loc = os.path.dirname(__file__)
        return os.path.join(loc, "resources", name)

    def ad9361_tx_quad_cal_test(self, test_name=None, device=None, channel=None):
        """ Query AD9361 tx quad cal test data to elasticsearch """
        index = "ad936x_tx_quad_cal" if not self.use_test_index else "dummy"
        s = []
        if test_name:
            s.append({"match": {"test_name": test_name}})
        if device:
            s.append({"match": {"device": device}})
        if channel:
            s.append({"match": {"channel": str(channel)}})
        # Create query
        if s:
            query = {
                "sort": [{"date": {"order": "asc"}}],
                "query": {"bool": {"must": s}},
            }
        else:
            query = {"sort": [{"date": {"order": "asc"}}], "query": {"match_all": {}}}
        res = self.db.es.search(index=index, size=1000, body=query)

        x = [val["_source"]["date"] for val in res["hits"]["hits"]]
        y = [val["_source"]["failed"] for val in res["hits"]["hits"]]
        t = [val["_source"]["iterations"] for val in res["hits"]["hits"]]
        return x, y, t

    def github_stats(self, repo=None, date=None):
        """ Query github stats from elasticsearch """
        index = "github_stats" if not self.use_test_index else "dummy"
        s = []
        if repo:
            s.append({"match": {"repo": repo}})
        if date:
            s.append({"match": {"date": date}})
        # Create query
        if s:
            query = {
                "sort": [{"date": {"order": "asc"}}],
                "query": {"bool": {"must": s}},
            }
        else:
            query = {"sort": [{"date": {"order": "asc"}}], "query": {"match_all": {}}}
        res = self.db.es.search(index=index, size=1000, body=query)

        dates = [val["_source"]["date"] for val in res["hits"]["hits"]]
        repo = [val["_source"]["repo"] for val in res["hits"]["hits"]]
        views = [val["_source"]["views"] for val in res["hits"]["hits"]]
        clones = [val["_source"]["clones"] for val in res["hits"]["hits"]]
        view_unique = [val["_source"]["view_unique"] for val in res["hits"]["hits"]]
        clones_unique = [val["_source"]["clones_unique"] for val in res["hits"]["hits"]]
        return {
            repo[i]: {
                "date": dates[i],
                "views": views[i],
                "clones": clones[i],
                "view_unique": view_unique[i],
                "clones_unique": clones_unique[i],
            }
            for i in range(len(dates))
        }
