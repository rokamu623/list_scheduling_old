from numpy import argmin

from .dag import DAG

class Scheduler():
    def __init__(self, dag: DAG, core_num: int):
        self._dag = dag
        self._core_num = core_num
        self._priority_queue = []
        self._sim_time = 0

    # pop most priory node
    def _select_node(self, priority_queue: list[int]) -> tuple([list[int], int]):
        priority_queue.sort(key=lambda x : self._dag.nodes[x].laxity)
        poped_node = priority_queue[0]
        priority_queue.pop(0)

        return priority_queue, poped_node

    # get fastest free core
    def _select_core(self) -> tuple([int, int]):
        # find node latest finish for each core
        ft = [0 for n in range(self._core_num)]
        for c in range(self._core_num):
            for node in self._dag.nodes:
                if node.core is not None and node.core == c and node.FT is not None and ft[c] < node.FT:
                    ft[c] = node.FT

        # get fastest free core
        selected_core = int(argmin(ft))
        core_avail_time = min(ft)

        return selected_core, core_avail_time

    def scheduling(self):
        # initialize by src nodes
        self._priority_queue = [n for n in self._dag.src]
        
        while(1):
            self._priority_queue, poped_node = self._select_node(self._priority_queue)

            # culc release time
            if len(self._dag.predecessors(poped_node)):
                release_time = max([self._dag.nodes[p].FT for p in self._dag.predecessors(poped_node)])
            else:
                release_time = 0

            selected_core, core_avail_time = self._select_core()

            start_time = max(release_time, core_avail_time)

            # assign scheduling info
            self._dag.nodes[poped_node].ST = start_time
            self._dag.nodes[poped_node].FT = self._dag.nodes[poped_node].ST + self._dag.nodes[poped_node].c
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
