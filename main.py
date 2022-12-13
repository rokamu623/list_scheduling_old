from yaml_dag_reader import YamlDagReader
from display_okamu import display_scheduling

from dag import DAG
from scheduler import Scheduler

# read node, edge, deadline from yaml
reader = YamlDagReader("./dag_sample.yaml")
wcets, edges, deadline = reader.read()

# make dag from wcets, edges, deadline
dag = DAG(wcets, edges, deadline)

# do list scheduling
core_num = 2
scheduler = Scheduler(dag, core_num)
scheduler.scheduling()



### outputs ###
# dag info
for i, node in enumerate(dag.nodes):
    print("idx: "+str(i)+", ST: "+str(node.ST)+", FT: "+str(node.FT)+", core: "+str(node.core))

# makespan
print(dag.makespan)

# scheduling
display_scheduling(core_num, dag)
