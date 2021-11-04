from core import *
from task import *
from dagProcessor import DagProcessor

        
class RunPar:

    def __init__(self, task, dag, cores):
    
        self.sdr = task.dR
        self.sir = task.iR 
        self.source_runnables = task.source_runnables 
        self.task = task
        self.cores = cores
        self.allocated_runnables = []
        self.idle_runnable_id = 100000
        
        #Sort Runnables
        self.sort_runnables(self, self.sdr)
        self.sort_runnables(self, self.sir)
        self.sort_runnables(self, self.source_runnables)
        
        #Allocate Source Runnables
        self.allocate_source_runnables(self)
        
        #Allocate Dependent Runnables
        self.allocate_dependent_runnables(self, dag)
        
        #Allocate independent runnables
        self.allocate_independent_runnables(self)
            

        
    
    @staticmethod
    def allocate_source_runnables(self):
        for r in self.source_runnables:
            c = self.worstfit(self)
            
            self.allocate(r,c)
    
    @staticmethod
    def allocate_dependent_runnables(self, dag):
        max_depth = -1
        providers = self.get_allocated_providers(self, dag)
        
        r_largest = Runnable(0,0)
        r_largest_core = Core(-1)
        
        for r in providers:
            r_core = self.core_of_runnable(self,r)

            if r_core.utilization > max_depth :
                max_depth = r_core.utilization
                r_largest = r
                r_largest_core = r_core
        

        for r in self.sdr:                    
            c_index = self.worstfit_startdef(r, max_depth, r_largest_core)
            ideal_offset = r_largest_core.get_exec_time_after_runnable(r_largest)
            
            if ideal_offset > self.cores[c_index].utilization :
                r_idle = Runnable(ideal_offset - self.cores[c_index].utilization ,self.idle_runnable_id)
                self.idle_runnable_id = self.idle_runnable_id + 1
                self.task.runnables.append(r_idle)
                self.allocate(r_idle,c_index, True)
            
            self.allocate(r,c_index)
    
    @staticmethod
    def allocate_independent_runnables(self):
        for r in self.sir:
            for c in self.cores:
                found_idle_slot = 0
                ret = c.replace_idle_runnable(r)
                if ret != -1 :
                    found_idle_slot = 1
                    break;
                    
            if found_idle_slot == 0 :
                c = self.worstfit(self)
                self.allocate(r,c)
    @staticmethod
    def get_allocated_providers(self, dag):
        dp = DagProcessor()
        providers = []
        for r in self.sdr :
            all_providers = dp.get_runnable_providers(r, dag)
            for p in all_providers :
                for ar in self.allocated_runnables :  
                    if ar.Id == p :
                        providers.append(ar)
                        continue
                    
        return providers
    
    @staticmethod
    def core_of_runnable(self, r):
        for c in self.cores:
            if r in c.runnables:
                return c

           
    def calculate_runnable_uC(self,runnable):
        dp = DagProcessor()
        try :
            paths = dp.get_all_paths_ids(self.task.get_self_dag(), runnable.Id)
        except :
            return runnable.WCET
        
        if len(paths) == 0 :
            return runnable.WCET
            
        cU = []
        for p in paths:
            path_runnables = []
            for r in p :
                path_runnables.append(self.task.get_runnable(r))
                
            cU.append(dp.calculate_path_cost(path_runnables))
        
        return max(cU)
        
        
        
    @staticmethod
    def sort_runnables(self, runnables):
        runnables.sort(reverse=True, key=self.calculate_runnable_uC)
        pass
    
    
    @staticmethod
    def worstfit(self):
        cores_u = []
        for c in self.cores:
            cores_u.append(c.utilization)
            
        return cores_u.index(min(cores_u))
        
    def allocate(self, runnable, core, idle = False):
        self.cores[core].add_runnable(runnable, idle)
        self.allocated_runnables.append(runnable)

        
    def worstfit_startdef(self, runnable, max_depth, rlargest_core):
        if rlargest_core.utilization == max_depth :
            return self.cores.index(rlargest_core)
            
        else :
            return self.worstfit(self)
        
        

    def get_sdr(self):
        return self.sdr
        
    def get_sir(self):
        return self.sir

    def get_source_runnables(self):
        return self.source_runnables
        
            
    def print_sorted_runnables(self):
        print("sorted dependent runnables")
        print(self.sdr)
        print("sorted independent runnables")
        print(self.sir)

    
    def print_allocated_runnables(self):
        i = 0
        for c in self.cores:
            print("Core " + str(i) + " utilization : ")
            print(c.utilization)
            print("Core " + str(i) + " Runnables : ")
            i = i+1
            for r in c.runnables:
                print(r)
                
    def print_schedule(self):
        for c in self.cores:
            c.print_runnables()


def main() :
    pass
    
    
if __name__ == "__main__":
    main()
else:
    print(__name__)