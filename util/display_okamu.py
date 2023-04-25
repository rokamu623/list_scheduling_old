from src.dag import DAG

def display_scheduling(core_num: int, dag: DAG):
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