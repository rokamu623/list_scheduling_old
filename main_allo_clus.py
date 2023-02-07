from yaml_dag_reader import YamlDagReader
from json_exporter import JsonExporterAllcClus

from dag import DAG
from scheduler_allocate_clusters import SchedulerAllocateClusters

# read node, edge, deadline from yaml
reader = YamlDagReader("./dag_sample.yaml")
wcets, edges, deadline = reader.read()

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
json_exporter.export("dag_sample.json")
print("export json")

