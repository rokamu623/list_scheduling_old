from util.yaml_dag_reader import YamlDagReader
from util.json_exporter import JsonExporterAllcClus

from src.dag import DAG
from src.scheduler_allocate_clusters import SchedulerAllocateClusters

# read node, edge, deadline from yaml
reader = YamlDagReader("./data/dag_sample.yaml")
wcets, edges, deadline = reader.read()
# wcets = [wcet*10000 for wcet in wcets]

# make dag from wcets, edges, deadline
dag = DAG(wcets, edges, deadline)

# do list scheduling
core_num = 80
scheduler = SchedulerAllocateClusters(dag, core_num)
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
json_exporter = JsonExporterAllcClus(dag)
json_exporter.export("./data/dag_sample.json")
print("export json")

