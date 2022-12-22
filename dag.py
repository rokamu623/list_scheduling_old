from typing import Optional

import networkx

class Node:
    def __init__(self, c: int):
        self._c = c
        self._ft = None
        self._st = None
        self._core = None
        self._laxity = 0

    @property
    def c(self) -> int:
        return self._c

    @property
    def FT(self) -> Optional[int]:
        return self._ft

    @FT.setter
    def FT(self, n: int):
        self._ft = n

    @property
    def ST(self) -> Optional[int]:
        return self._st

    @ST.setter
    def ST(self, n: int):
        self._st = n

    @property
    def core(self) -> Optional[int]:
        return self._core

    @core.setter
    def core(self, n: int):
        self._core = n

    @property
    def laxity(self) -> int:
        return self._laxity

    @laxity.setter
    def laxity(self, n: int):
        self._laxity = n

class DAG:
    def __init__(self, weights: list[int], edges: list[(int, int)], deadline: int):
        # DiGraph
        self.G = networkx.DiGraph()
        self.G.add_nodes_from(range(len(weights)))
        self._nodes = [Node(w) for w in weights]
        self.G.add_edges_from(edges)

        # member
        self._deadline = deadline
        self.__culc_laxity()
        self._c_path = self.__culc_c_path()

    # return index list [1, ..., n]
    @property
    def c_path(self) -> list[int]:
        return self._c_path

    def predecessors(self, n: int) -> list[int]:
        return list(self.G.predecessors(n))

    def successors(self, n: int) -> list[int]:
        return list(self.G.successors(n))

    # return index list
    @property
    def src(self) -> list[int]:
        return [i for i, node in enumerate(self.G.nodes) if len(list(self.predecessors(i))) == 0]

    # return index list
    @property
    def snk(self) -> list[int]:
        return [i for i, node in enumerate(self.G.nodes) if len(list(self.successors(i))) == 0]

    @property
    def deadline(self) -> int:
        return self._deadline

    @property
    def makespan(self) -> int:
        m=0
        for n in self.nodes:
            if n.FT > m:
                m = n.FT
        return m

    def __culc_laxity(self):
        def culc(n: int, l: int):
            self.nodes[n].laxity = l
            for s in list(self.G.predecessors(n)):
                culc(s, l-self.nodes[s].c)

        for n in self.snk:
            culc(n, self.deadline-self.nodes[n].c)

    @property
    def nodes(self):
        return self._nodes


    def __culc_c_path(self) -> list[int]:
        cp = []
        length = 0
        for s in self.src:
            for d in self.snk:
                for path in list(networkx.all_simple_paths(self.G, s, d)):
                    print(path)
                    tmp_length = sum([self.nodes[n].c for n in path])
                    print(tmp_length)
                    print("===")
                    if tmp_length > length:
                        cp = path
                        length = tmp_length
        print(cp)
        return cp
