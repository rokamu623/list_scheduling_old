import json
from dag import DAG


class JsonExporter():
    def __init__(self, dag: DAG):
        self._dag = dag

    def _get_data(self):
        json_data = {
            "makespan": self._dag.makespan,
            "taskSet": []
        }

        for i, node in enumerate(self._dag.nodes):
            data = {
                "coreID": node.core,
                "taskID": i,
                #"jobID": 0,  # optional
                #"releaseTime": 0,  # optional
                #"deadline": 0,  # optional
                "startTime": node.ST,
                "finishTime": node.FT,
                "preemption": False,  # optional
                "deadlineMiss": False  # optional
            }
            json_data["taskSet"].append(data)

        return json_data

    def export(self, file_name: str="output.json"):
        json_data = self._get_data()

        json_file = open(file_name, "w")
        json.dump(json_data, json_file)
        json_file.close()

class JsonExporterAllcClus(JsonExporter):
    def __init__(self, dag: DAG):
        self._dag = dag

    def _get_data(self):
        json_data = {
            "makespan": self._dag.makespan,
            "taskSet": []
        }

        for i, node in enumerate(self._dag.nodes):
            for c in node.core:
                data = {
                    "coreID": c,
                    "taskID": i,
                    #"jobID": 0,  # optional
                    #"releaseTime": 0,  # optional
                    #"deadline": 0,  # optional
                    "startTime": node.ST,
                    "finishTime": node.FT,
                    "preemption": False,  # optional
                    "deadlineMiss": False  # optional
                }
                json_data["taskSet"].append(data)

        return json_data