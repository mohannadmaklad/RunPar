class Core:
    def __init__(self, core_id):
        self.core_id = core_id
        self.runnables = []
        self.utilization = 0
        self.__idle_runnables = []
        self.idle_wcet = 0
        
    def add_runnable(self, runnable, idle = False):
        for r in self.runnables :
            if runnable.Id == r.Id :
                raise ValueError("Runnable with the same ID exists")
                
        self.runnables.append(runnable)
        self.utilization = self.utilization + runnable.WCET
        
        if idle == True :
            self.__idle_runnables.append(runnable.Id)
            self.idle_wcet = self.idle_wcet + runnable.WCET


    def get_idleSlots(self):
        ''' Returns list of consecuting idle slots in the format : start index 1,
        consecutive idle time 1,start index 2, consecutive idle time 2 '''
        idle_slots = []
        current_slot = 0
        runnables_len = len(self.runnables)
        
        i = 0
        
        while i < runnables_len:
            if self.runnables[i].Id in self.__idle_runnables :
                idle_slots.append(i)
                
                current_slot = current_slot + self.runnables[i].WCET
                while i < runnables_len -1 and self.runnables[i+1].Id in self.__idle_runnables :
                    i = i + 1
                    current_slot = current_slot + self.runnables[i].WCET
                    

                idle_slots.append(current_slot)
                current_slot = 0
            i = i + 1
        
        return idle_slots
    
    
    
    @staticmethod
    def deduct_idle(self,idle_id, to_deduct):
        if self.runnables[idle_id].WCET <= to_deduct :
            del self.runnables[idle_id]
        elif self.runnables[idle_id].WCET > to_deduct :
            self.runnables[idle_id].WCET = self.runnables[idle_id].WCET - to_deduct
            
        self.idle_wcet = self.idle_wcet - to_deduct
        
    def replace_idle_runnable(self,new_runnable):
        #Do we have a free space?
        if self.idle_wcet == 0:
            return -1
        
        #Get idle slots 
        idle_slots = self.get_idleSlots()
        
        
        #Get the maximum free space : 
        free_slot_id = -1
        for i in range(1,len(idle_slots),2):
            if idle_slots[i] >= new_runnable.WCET:
                free_slot_id = idle_slots[i-1]
                break
                
        if free_slot_id == -1:
            return -1
        
        #Now we assign the new runnable 
        self.runnables.insert(free_slot_id, new_runnable)
        self.utilization = self.utilization + new_runnable.WCET


        to_deduct = new_runnable.WCET       
        
        will_deduct = 0
        while to_deduct > 0 :
            will_deduct = self.runnables[free_slot_id + 1].WCET
            self.deduct_idle(self,free_slot_id + 1,to_deduct)
            to_deduct = to_deduct - will_deduct

                
        return 0
                
    def get_exec_time_after_runnable(self, runnable):
        if runnable not in self.runnables :
            return -1
        
        exec_sum = 0
        for r in self.runnables:
            exec_sum = exec_sum + r.WCET
            if r.Id == runnable.Id :
                return exec_sum
                
    def get_runnables(self):
        return self.runnables
        
        
    def print_runnables(self):
        for r in self.runnables :
            if r.Id in self.__idle_runnables :
                print(str(r.Id) +"[" + str(r.WCET) +"]" + "[i]" + " -> ", end = "")
            else : 
                print(str(r.Id) +"[" + str(r.WCET) +"]" + " -> ", end = "")

        print("********** Done **********")