import networkx as nx

class DagProcessor:
    def __init__(self):
        pass
    
    @staticmethod
    def construct_Graph(self, dag):
        self.__graph = nx.DiGraph()
        self.__graph.add_edges_from(dag)
        return self.__graph

           
    def get_all_paths_ids(self, dag, source_node_id):

        roots = []
        leaves = []
        paths = []
        root = 0
        
        graph = self.construct_Graph(self,dag)
        
        for node in graph.nodes :
          if graph.in_degree(node) == 0 : # it's a root
            roots.append(node)
            
            if source_node_id not in roots :
                raise ValueError("Source node doesn't belong to the given dag")
                return []
            else :
                root = source_node_id
            
          elif graph.out_degree(node) == 0 : # it's a leaf
            leaves.append(node)
            
        for leaf in leaves :
            for path in nx.all_simple_paths(graph, root, leaf) :
                paths.append(path)
        return paths
        
    def calculate_path_cost(self, path):
        if len(path) == 0:
            return 0
            
        total_cost = 0
        
        #loop over all other nodes
        for p in path:
            total_cost += p.WCET

        return total_cost
        
    def get_runnable_providers(self, runnable, dag):
        providers = []
        
        for d in dag:
            if d[1] == runnable.Id :
                providers.append(d[0])
                
        return providers
        