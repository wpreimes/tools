# -*- coding: utf-8 -*-
import time
from multiprocessing import Process, Queue
import os

os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'
os.environ['OPENBLAS_NUM_THREADS'] = '1'


def parallelize(q, arg1, arg2, process_no):
    '''
    This function runs in parallel
    '''

    print('Process %i: Wait %i seconds' % (process_no, process_no))
    time.sleep(1 * process_no) # process 1 waits 1 second, process 2 waits 2 seconds etc.

    q.put(True)




def main(number_of_parallel_processes):
    args1 = range(number_of_parallel_processes) # each process gets different args
    args2 = range(number_of_parallel_processes, number_of_parallel_processes*2)


    processes = []
    q = Queue()
    finished_processes = []

    for i, process_no in enumerate(range(1, number_of_parallel_processes + 1)):
        arg1, arg2 = args1[i], args2[i]
        p = Process(target=parallelize, args=(q, arg1, arg2, process_no))

        processes.append(p)
        p.start()

    for i, process in enumerate(processes):
        finished_processes.append(q.get(True))
        print('Process %i finished' % i)

    for process in processes:
        process.join()


    print('Processes joined, continue as single process')


if __name__ == '__main__':
    main(number_of_parallel_processes=3)
