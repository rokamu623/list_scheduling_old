from dag import DAG, Node
import networkx
from yaml_dag_reader import YamlDagReader

class DAG_rta_fcp(DAG):
    def __init__(self, weights: list[int], edges: list[(int, int)], deadline: int):
        # add src dammy
        weights.append(0)
        # add snk dammy
        weights.append(0)

        # DiGraph
        self.G = networkx.DiGraph()
        self.G.add_nodes_from(range(len(weights)))
        self._nodes = [Node(w) for w in weights]
        self.G.add_edges_from(edges)

        # link src dammy
        for s in self.src:
            if s != len(self.nodes)-2 and s != len(self.nodes)-1:
                self.G.add_edge(len(self.nodes)-2, s)
        # link snk dammy
        for s in self.snk:
            if s != len(self.nodes)-2 and s != len(self.nodes)-1:
                self.G.add_edge(s, len(self.nodes)-1)

        # member
        self._deadline = deadline
        self._culc_laxity()
        self._c_path = self._culc_c_path()

        # culc priority
        self._culc_priority_rta_fcp()

    def ancestor(self, n: int) -> list[int]:
        ans_set = set()
        for s in self.predecessors(n):
            ans_set |= set(self.ancestor(s))
            ans_set.add(s)

        return list(ans_set)

    def _culc_priority_rta_fcp(self):
        priority = 0
        # assign highest with c_path
        for cp in self.c_path:
            self.nodes[cp].p = priority
            priority += 1
        priority -= 2

        # each c_path ordered
        for cp in self.c_path:
            # get un-assigned ancestor
            branchs: list[list[int]] = []
            for a in [a for a in self.predecessors(cp) if self.nodes[a].p == -1]:
                branch = [a]
                branch.extend([t for t in self.ancestor(a) if self.nodes[t].p == -1])
                branchs.append(sorted(branch))
            # WCET ordered
            for branch in sorted(branchs,key=lambda x: sum([self.nodes[i].c for i in x]), reverse=True):
                # define ancestor subgraph
                wcets = [self.nodes[n].c for n in branch]
                edges = [(branch.index(e[0]), branch.index(e[1])) for e in self.G.edges if e[0] in branch and e[1] in branch]
                # assign priority with subgraph (recursive)
                tmp = DAG_rta_fcp(wcets, edges, self._deadline)
                # copy priority subgraph -> graph
                for i, b in enumerate(branch):
                    self.nodes[b].p = tmp.nodes[i].p + priority
                priority += len(branch)

        # remove dummy nodes
        self.G.remove_node(len(self.nodes)-2)
        self.G.remove_node(len(self.nodes)-1)
        self._nodes.pop(-1)
        self._nodes.pop(-1)
        # re-culc status
        self._culc_laxity()
        self._c_path = self._culc_c_path()

# test use-case
"""
# read node, edge, deadline from yaml
reader = YamlDagReader("./dag_sample.yaml")
wcets, edges, deadline = reader.read()

# make dag from wcets, edges, deadline
dag = DAG_rta_fcp(wcets, edges, deadline)

print([n.p for n in dag.nodes])
"""
