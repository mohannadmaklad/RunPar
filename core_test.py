import unittest
from runnable import Runnable
from core import Core

class testCore(unittest.TestCase):

    def test_add_runnable(self):
        
        core_1 = Core(0)
        runnable_1 = Runnable(5,1)
        runnable_2 = Runnable(4,2)
        runnable_3 = Runnable(9,2)
        idle_runnable_1 = Runnable(4,3)
        idle_runnable_2 = Runnable(7,4)
        runnable_4 = Runnable(1,5)
        idle_runnable_3 = Runnable(2,6)

        #Utilization is zero @ init
        self.assertEqual(0, core_1.utilization)

        #check utilization after adding 1 runnable
        core_1.add_runnable(runnable_1)
        self.assertEqual(5, core_1.utilization)
        
        #check utilization after adding 2 runnables
        core_1.add_runnable(runnable_2)
        self.assertEqual(9, core_1.utilization)
        
        #Can not add runnables with duplicate id 
        self.assertRaises(ValueError, core_1.add_runnable, runnable_3)
        
        #Add one idle runnable 
        core_1.add_runnable(idle_runnable_1, True)
        self.assertEqual(13, core_1.utilization)
        self.assertEqual(4, core_1.idle_wcet)
        
        #Add another idle runnable 
        core_1.add_runnable(idle_runnable_2, True)
        self.assertEqual(20, core_1.utilization)
        self.assertEqual(11, core_1.idle_wcet)

        #Check consecutive idle runnables 
        core_1.add_runnable(runnable_4)
        self.assertEqual(21, core_1.utilization)

        core_1.add_runnable(idle_runnable_3, True)
        self.assertEqual(23, core_1.utilization)
        self.assertEqual(13, core_1.idle_wcet)
        
        self.assertEqual([2,11,5,2], core_1.get_idleSlots())
        
    def test_replace_idle_runnable(self):
        core_1 = Core(0)
        runnable_1 = Runnable(5,1)
        runnable_2 = Runnable(4,2)
        runnable_3 = Runnable(9,2)
        idle_runnable_1 = Runnable(4,3)
        idle_runnable_2 = Runnable(7,4)
        runnable_4 = Runnable(1,5)
        idle_runnable_3 = Runnable(2,6)
        runnable_5 = Runnable(1,7)
        runnable_6 = Runnable(12,8)
        runnable_7 = Runnable(10,8)
        runnable_8 = Runnable(2,9)


        core_1.add_runnable(runnable_1)
        core_1.add_runnable(runnable_2)
        core_1.add_runnable(idle_runnable_1, True)
        core_1.add_runnable(idle_runnable_2, True)
        core_1.add_runnable(runnable_4)
        core_1.add_runnable(idle_runnable_3, True)   
        
        #Replace with a small runnable
        core_1.replace_idle_runnable(runnable_5)
        self.assertEqual([3,10,6,2], core_1.get_idleSlots())
        
        #Replace with too big runnable (>)
        self.assertEqual(core_1.replace_idle_runnable(runnable_6) , -1)
        
        #Replace with a big runnable (=)
        self.assertEqual(core_1.replace_idle_runnable(runnable_7) , 0)
        self.assertEqual([5,2], core_1.get_idleSlots())
        
        #Let's replace the last sloth 
        self.assertEqual(core_1.replace_idle_runnable(runnable_8) , 0)
        self.assertEqual([], core_1.get_idleSlots())
        
        pass
        
    def test_get_exec_time_after_runnable(self):
        
        pass


if __name__ == '__main__':
    unittest.main()