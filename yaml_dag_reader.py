import yaml

class YamlDagReader:
    def __init__(self, file_path):
        with open(file_path, 'r') as yml:
            self.dict = yaml.safe_load(yml)

    def read(self) -> tuple([[int], [(int, int)], int]):
        nodes_yaml = self.dict["nodes"]
        # wcets = [3,12,7,5,13,2,5,16,3,5,7,2]
        wcets = [n["Execution_time"] for n in sorted(nodes_yaml, key=lambda x: x["id"])]

        # deadline = 100
        for n in nodes_yaml:
            if "End_to_end_deadline" in n:
                deadline = n["End_to_end_deadline"]

        edge_yaml = self.dict["links"]
        # edges = [(0,1),(0,2),(0,3),(1,5),(1,6),(2,4),(3,7),(4,7),(4,8),(5,9),(6,10),(7,10),(8,10),(8,11),(9,11),(10,11)]
        edges = [(e["source"], e["target"]) for e in edge_yaml]

        return wcets, edges, deadline
