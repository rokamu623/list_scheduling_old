from yaml_dag_reader import YamlDagReader

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














# outputs
# dag info
for i, node in enumerate(dag.nodes):
    print("idx: "+str(i)+", ST: "+str(node.ST)+", FT: "+str(node.FT)+", core: "+str(node.core))

# makespan
print(dag.makespan)

# scheduling
sched = []
for i in range(core_num):
    s = []
    for j in range(dag.makespan):
        s.append("-")
    sched.append(s)

for i, node in enumerate(dag.nodes):
    for j in range(node.ST, node.FT):
        sched[node.core][j] = str(i)

for s in sched:
    print("".join(s))
