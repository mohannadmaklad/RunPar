import unittest
from runnable import Runnable
from dagProcessor import DagProcessor


class testCore(unittest.TestCase):
    def test_get_all_paths_ids(self):
        dag_1 = [(1,2),(2,3),(2,4)]
        dp = DagProcessor()
        paths = dp.get_all_paths_ids(dag_1, 1)
        
        #expect the paths 
        self.assertEqual([[1,2,3],[1,2,4]],paths)
        
        #valueError is raised in case source doesn't belong to the dagProcessor
        self.assertRaises(ValueError,dp.get_all_paths_ids, dag_1,10)
    
    def test_calculate_path_cost(self):
        dp = DagProcessor()

        r1 = Runnable(5,1)
        r2 = Runnable(4,2)
        r3 = Runnable(9,2)
        
        path = [r1, r2, r3]
    
        self.assertEqual(dp.calculate_path_cost(path), 18)
        
    def test_get_runnable_providers(self):
        dp = DagProcessor()
        dag_1 = [(1,2),(2,3),(2,4)]

        self.assertEqual(dp.get_runnable_providers(Runnable(6,2),dag_1), [1])
        self.assertEqual(dp.get_runnable_providers(Runnable(6,4),dag_1), [2])
        self.assertEqual(dp.get_runnable_providers(Runnable(6,5),dag_1), [])


    
if __name__ == '__main__':
    unittest.main()