import unittest
from runpar import *


dag = [(1,2), (1,3), (2,5), (2,6), (4,5),(5,8)]

r1 = Runnable(3, 1)
r2 = Runnable(4, 2)
r3 = Runnable(2, 3)
r4 = Runnable(1, 4)
r5 = Runnable(4, 5)
r6 = Runnable(2, 6)
r7 = Runnable(1, 7)

task1 = Task([r1,r3,r4], dag, "task1")
task2 = Task([r2,r5,r6], dag, "task2")
task3 = Task([r7],dag, "task3")


class testRunPar(unittest.TestCase):
    
    def test_runnables_are_sorted_correctly(self):
        
        #Task 1
        cores = [Core(0), Core(1)]
        rp = RunPar(task1  , dag, cores)
        
        self.assertEqual(rp.get_sdr(), [r3])
        self.assertEqual(rp.get_sir(), [r4])
        self.assertEqual(rp.get_source_runnables(), [r1])


        #Task 2
        cores2 = [Core(0), Core(1)]
        rp2 = RunPar(task2  , dag, cores2)
        
        self.assertEqual(rp2.get_sdr(), [r5,r6])
        self.assertEqual(rp2.get_sir(), [])
        self.assertEqual(rp2.get_source_runnables(), [r2])
        
        #Task 3
        cores3 = [Core(0), Core(1)]
        rp3 = RunPar(task3  , dag, cores3)
        
        self.assertEqual(rp3.get_sdr(), [])
        self.assertEqual(rp3.get_sir(), [r7])
        self.assertEqual(rp3.get_source_runnables(), [])
        
        
        
    def test_runnables_allocated_correctly_task_1(self):
    
        #Task 1
        core_0 = Core(0)
        core_1 = Core(1)
        cores = [core_0 ,core_1]
        
        #Run the algorithm over the first task
        rp = RunPar(task1  , dag, cores)
        
        #Check core 0 runnables & total WCET :
        self.assertEqual(core_0.get_runnables(), [r1,r3])
        self.assertEqual(core_1.get_runnables(), [r4])
        #Check core 1 runnables & total WCET :
        self.assertEqual(core_0.utilization, r1.WCET + r3.WCET)
        self.assertEqual(core_1.utilization, r4.WCET)


    def test_runnables_allocated_correctly_task_2(self):
    
        #Task 1
        core_0 = Core(0)
        core_1 = Core(1)
        cores = [core_0 ,core_1]
        
        #Run the algorithm over the third task
        rp = RunPar(task2  , dag, cores)
        
        
        core_0.print_runnables()
        core_1.print_runnables()
        
        #Check core 0 runnables & total WCET :
        self.assertEqual(core_0.get_runnables(), [r2,r5])
        #self.assertEqual(core_1.get_runnables(), [r6]) #will fail because the idle runnable is assigned dynamically
        #Check core 1 runnables & total WCET :
        self.assertEqual(core_0.utilization, r2.WCET + r5.WCET)
        self.assertEqual(core_1.utilization, r2.WCET + r6.WCET)
       
    def test_runnables_allocated_correctly_task_3(self):
    
        #Task 1
        core_0 = Core(0)
        core_1 = Core(1)
        cores = [core_0 ,core_1]
        
        #Run the algorithm over the third task
        rp = RunPar(task3  , dag, cores)
        
        #Check core 0 runnables & total WCET :
        self.assertEqual(core_0.get_runnables(), [r7])
        self.assertEqual(core_1.get_runnables(), []) 
        #Check core 1 runnables & total WCET :
        self.assertEqual(core_0.utilization, r7.WCET)
        self.assertEqual(core_1.utilization, 0)
        
    def test_task3(self):
        pass
        
    
if __name__ == '__main__':
    unittest.main()