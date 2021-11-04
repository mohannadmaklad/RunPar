import unittest
from task import *

#Runnables 
r1 = Runnable(3, 1)
r2 = Runnable(4, 2)
r3 = Runnable(2, 3)
r4 = Runnable(1, 4)
r5 = Runnable(4, 5)
r6 = Runnable(2, 6)
r7 = Runnable(1, 7)

#Dependencies 
dag = [(1,2), (1,3), (2,5), (2,6), (4,5),(5,8)]
        
class testTask(unittest.TestCase):
    
    def test_Task1(self):
        #Prepare & Act
        task1_runnables = [r1,r3,r4]
        task1 = Task(task1_runnables, dag, "task1")
        
        #Assert
        self.assertEqual(task1.get_self_dag() , [(1,3)])
        self.assertEqual(task1.get_source_runnables() , [r1])
        self.assertEqual(task1.get_d_runnables() , [r3])
        self.assertEqual(task1.get_i_runnables() , [r4])
        
    def test_Task2(self):
        #Prepare & Act
        task2_runnables = [r2, r5, r6]
        task2 = Task(task2_runnables, dag, "task2")
        
        #Assert
        self.assertEqual(task2.get_self_dag() , [(2,5),(2,6)])
        self.assertEqual(task2.get_source_runnables() , [r2])
        self.assertEqual(task2.get_d_runnables() , [r5,r6])
        self.assertEqual(task2.get_i_runnables() , [])
        
    def test_Task3(self):
        #Prepare & Act
        task3 = Task([r7],dag, "task3")
        
        #Assert
        self.assertEqual(task3.get_self_dag() , [])
        self.assertEqual(task3.get_source_runnables() , [])
        self.assertEqual(task3.get_d_runnables() , [])
        self.assertEqual(task3.get_i_runnables() , [r7])
        pass



if __name__ == '__main__':
    unittest.main()