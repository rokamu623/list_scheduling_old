from util.yaml_dag_reader import YamlDagReader
from util.json_exporter import JsonExporter

from src.dag import DAG
from src.scheduler import Scheduler

# read node, edge, deadline from yaml
reader = YamlDagReader("./DAG/dag_sample.yaml")
wcets, edges, deadline = reader.read()

# make dag from wcets, edges, deadline
dag = DAG(wcets, edges, deadline)

# do list scheduling
core_num = 2
scheduler = Scheduler(dag, core_num)
scheduler.scheduling()



### outputs ###
# dag info
print("===== info ======")
for i, node in enumerate(dag.nodes):
    print("idx: "+str(i)+", ST: "+str(node.ST)+", FT: "+str(node.FT)+", core: "+str(node.core))

# makespan
print("===== makespan ======")
print(dag.makespan)

# scheduling
# display_scheduling(core_num, dag)
print("===== json ======")
json_exporter = JsonExporter(dag)
json_exporter.export("./DAG/dag_sample.json")
print("export json")

