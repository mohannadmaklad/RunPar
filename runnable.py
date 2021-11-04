class Runnable():
    def __init__(self, worst_case_time, runnable_id):
        self.WCET = worst_case_time
        self.cU = 0
        self.Id = runnable_id
        
    def set_cU(self,accumulative_utilization):
        self.cU = accumulative_utilization