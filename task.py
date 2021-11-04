from runnable import Runnable
import networkx as nx

class Task():    
    def __init__(self, runnables, dag, name):
        self.__relevant_dag = []
        self.dR = []
        self.iR = []
        self.source_runnables = []
        self.runnables = runnables
        self.temp_dR = []
        self.__task_name = name
        self.__runnablesIndices = []
        
        
        if name == '':
            self.task_name = "task" + str(self.task_num)
        
        
        #Fill runnables indices 
        for r in runnables :
            self.__runnablesIndices.append(r.Id)
        
        
        #Construct the relevant dag
        for d in dag :
            if d[0] in self.__runnablesIndices and d[1] in self.__runnablesIndices and d not in self.__relevant_dag:
                self.__relevant_dag.append(d)
        
        
        self.Populate_temp_runnables(self)
        self.Populate_independent_runnables(self)
        self.Populate_source_runnables(self)
        self.Populate_dependent_runnables(self)
        self.construct_Graph(self,self.__task_name)
        
        
    
    @staticmethod
    def Populate_temp_runnables(self):
        #Update all dependent runnables in temp list
        for r in self.__runnablesIndices:
            for d in self.__relevant_dag:
                if r == d[0]:
                    if d[1] in self.__runnablesIndices :
                        if r not in self.temp_dR :
                            self.temp_dR.append(r)
                elif r == d[1] :
                    if d[0] in self.__runnablesIndices :
                        if r not in self.temp_dR :
                            self.temp_dR.append(r)
        
        
    @staticmethod
    def Populate_independent_runnables(self):
        ''' Must be called after Populate_temp_runnables'''

        #Update independent runnables
        for r in self.__runnablesIndices:
            if r not in self.temp_dR:
                self.iR.append(self.get_runnable(r))
                
                
    @staticmethod
    def Populate_source_runnables(self):   
        #Update source runnables
        for r in self.__runnablesIndices:
            if self.get_runnable(r) in self.iR:
                continue
                
            provider = True
            for d in self.__relevant_dag:
                if d[1] == r :
                    provider = False
                    break
                    
            if provider == True:
                self.source_runnables.append(self.get_runnable(r))    
        
    @staticmethod
    def Populate_dependent_runnables(self):
        #Update dependent runnables (that are not only source of data)
        for t in self.temp_dR:
            if self.get_runnable(t) not in self.source_runnables:
                self.dR.append(self.get_runnable(t))
                
        delattr(self, "temp_dR")

    @staticmethod
    def construct_Graph(self, file_name):
        self.__graph = nx.DiGraph()
        self.__graph.add_edges_from(self.__relevant_dag)
        '''
        nx.draw_networkx(graph)
        plt.savefig(self.__task_name+".png", format="PNG")
        plt.clf()
        return graph
        '''
        
    def calculate_cU(self, runnables):
        roots = []
        leaves = []
        for node in self.__graph.nodes :
          if self.__graph.in_degree(node) == 0 : # it's a root
            roots.append(node)
          elif self.__graph.out_degree(node) == 0 : # it's a leaf
            leaves.append(node)

        for root in roots :
          for leaf in leaves :
            for path in nx.all_simple_paths(self.__graph, root, leaf) :
                print("@@@@@@@@@")
                print(path)
              
        pass
        
    def print_source_runnables(self):    
        print("Source runnables : ")          
        for r in self.source_runnables :
            print(r.Id)
        
    def print_d_runnables(self):
        print("Dependent runnables : ")
        for r in self.dR :
            print(r.Id)
            
        
    def print_i_runnables(self):    
        print("Inependent runnables : ")    
        for r in self.iR :
            print(r.Id)
    
    def print_self_dag(self): 
        print("Task DAG : ")        
        print(self.__relevant_dag)
        
        
    def print_info(self):
        print("Dumping Task info.........")
        self.print_source_runnables()
        self.print_d_runnables()
        self.print_i_runnables()
        self.print_self_dag()
        print("\n")


    def get_runnable(self,runnable_id):
        for r in self.runnables:
            if r.Id == runnable_id:
                return r
                
                
    def get_self_dag(self): 
        return self.__relevant_dag
        
    def get_source_runnables(self):
        return self.source_runnables
        
    def get_d_runnables(self):
        return self.dR
        
    def get_i_runnables(self):
        return self.iR
        
if __name__ == '__main__':

    r1 = Runnable(3, 1)
    r2 = Runnable(4, 2)
    r3 = Runnable(2, 3)
    r4 = Runnable(1, 4)
    r5 = Runnable(4, 5)
    r6 = Runnable(2, 6)
    r7 = Runnable(1, 7)
    dag = [(1,2), (1,3), (2,5), (2,6), (4,5),(5,8)]

    task2_runnables = [r2, r5, r6]
    task2 = Task(task2_runnables, dag, "task2")
    task2.print_info()
    pass