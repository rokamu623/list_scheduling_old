from numpy import argmin

from dag import DAG, Node
from scheduler import Scheduler

from amdahl import amdahl

CORE_NUM_IN_CLUSTER = 16

class SchedulerAllocateClusters(Scheduler):
    def __init__(self, dag: DAG, core_num: int):
        self._dag = dag

        assert core_num % CORE_NUM_IN_CLUSTER == 0
        self._core_clusters = [[cc*CORE_NUM_IN_CLUSTER+c for c in range(CORE_NUM_IN_CLUSTER)] for cc in range(int(core_num/CORE_NUM_IN_CLUSTER))]
        self._cluster_num = len(self._core_clusters)

        self._priority_queue = []
        self._sim_time = 0

    def aaa(self):
        self.__select_core()

    # get fastest free core
    def __select_core(self) -> tuple([int, int]):
        # find node latest finish for each core
        ft = [[0 for _ in range(CORE_NUM_IN_CLUSTER)] for _ in range(self._cluster_num)]
        for node in [node for node in self._dag.nodes if node.core is not None]:
            for cc in range(self._cluster_num):
                for c in range(CORE_NUM_IN_CLUSTER):
                    core_idx = 16 * cc + c
                    if core_idx in node.core and node.FT is not None and ft[cc][c] < node.FT:
                        ft[cc][c] = node.FT

        # # get fastest free core
        # selected_core = int(argmin(ft))
        # core_avail_time = min(ft)

        # return selected_core, core_avail_time

    def scheduling(self):
        # initialize by src nodes
        self._priority_queue = [n for n in self._dag.src]
        
        while(1):
            self._priority_queue, poped_node = self.__select_node(self._priority_queue)

            # culc release time
            if len(self._dag.predecessors(poped_node)):
                release_time = max([self._dag.nodes[p].FT for p in self._dag.predecessors(poped_node)])
            else:
                release_time = 0

            selected_core, core_avail_time = self.__select_core() # NOTE: mainly, changes are in select_core function

            start_time = max(release_time, core_avail_time)

            # assign scheduling info
            self._dag.nodes[poped_node].ST = start_time
            self._dag.nodes[poped_node].FT = self._dag.nodes[poped_node].ST + amdahl(self._dag.nodes[poped_node].c, 16) # TODO: 16 -> self._dag.nodes[poped_node].core_num?
            self._dag.nodes[poped_node].core = selected_core

            # if all node is scheduled, finish
            if len([n for n in self._dag.nodes if (n.FT is None)]) == 0:
                break

            # update priority queue
            while True:
                # listing not schediling and not in priority queue 
                for i in [i for i in range(len(self._dag.nodes)) if self._dag.nodes[i].FT is None and i not in self._priority_queue]:
                    append_flag = True
                    ft = 0
                    # enqueue node which release "sim_time" (all predecessors finish until "sim_time")
                    for pre in [self._dag.nodes[p] for p in self._dag.predecessors(i)]:
                        if pre.FT is None or (pre.FT is not None and pre.FT > self._sim_time):
                            append_flag = False
                    if append_flag is True:
                        self._priority_queue.append(i)

                # if all node in queue is allocated, wait for time when earliest node finish
                if len(self._priority_queue) != 0:
                    break
                else:
                    ft = [n.FT for n in self._dag.nodes if n.FT is not None and n.FT > self._sim_time]
                    if len(ft) > 0:
                        self._sim_time = min(ft)

dag = DAG([], [], 0)
node0 = Node(10)
node0.FT = 20
node0.core = [i for i in range(16)]
node1 = Node(20)
node1.FT = 30
node1.core = [i+32 for i in range(16)]
dag._nodes = [node0, node1]
scheduler = SchedulerAllocateClusters(dag, 80)
scheduler.aaa()
