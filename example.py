from runpar import *

#Runnables (WCET, id)
r1 = Runnable(3, 1)
r2 = Runnable(4, 2)
r3 = Runnable(2, 3)
r4 = Runnable(1, 4)

#DAG pairs
dag = [(1,2), (1,3) ,(2,4)]

#Only one task, for now
task1 = Task([r1,r2,r3,r4], dag, "task1")

#We have 2 cores
core_0 = Core(0)
core_1 = Core(1)
cores = [core_0 ,core_1]

#Run the algorithm
rp = RunPar(task1, dag, cores)


#now print the schedule : 
rp.print_schedule()