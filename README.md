# RunPar - Implementation of RunPar Scheduling Algorithm
The project is divided into subclasses, each class in a single file and a test file, example : core, core_test
You can find the main algorithm class in runpar.py

Example :

First you need to import runpar :
```
from runpar import *
```

Then you need to create the runnables, each runnable is created using the following format
r = Runnable(WCET, runnable id) :
```
r1 = Runnable(3, 1)
r2 = Runnable(4, 2)
r3 = Runnable(2, 3)
r4 = Runnable(1, 4)
```

Then create the DAG :
```
dag = [(1,2), (1,3) ,(2,4)]
```

For instance,  (1,3) means that runnable with id of 3 depends on runnable with id of 1

Now create the tasks with associated runnables :

```
task1 = Task([r1,r2,r3,r4], dag, "task1")
```

The core class takes only the core number as a constructor input :

```
core_0 = Core(0)
core_1 = Core(1)
cores = [core_0 ,core_1]
```


You can now run the algorithm :

```
rp = RunPar(task1, dag, cores)
```

Please note that the algorithm works on one task at a time.If you have more than one task,
You will need to instantiate new cores for each task (Maybe I'm wrong but that's how I understood the algorithm :) )

The output should be something like that : 

```
1[3] -> 2[4] -> ********** Done **********
100000[3][i] -> 3[2] -> 4[1] -> ********** Done **********
```

Each line correpsonds to a core schedule. i.e. The first line represents the first core in the list, and so on..

each runnable is written in the form id[WCET]. 
For intance, the first line in the output represents the first core scheduling :
Runnable 1 with WCET of 3, Runnable 2 with WCET of 4
the [i] in the second line represents an idle runnable with WCET of 3, this means
that runnable 3 will run after runnable 1, because it depends on it.
Idle runnables are given ids during runtime, starting from 100000 and incrementing by 1

