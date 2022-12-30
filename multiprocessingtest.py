import multiprocessing
import concurrent.futures
import time


processes = []

def do_something(sec: int):
    print('do something')
    time.sleep(sec)
    return 'done'

start = time.perf_counter()

# phase 1
for _ in range(0,10):
    # do_something(1)
    p = multiprocessing.Process(target=do_something, args=[1]) # serializing args (python object) with pickle
    p.start()
    processes.append(p)

for pr in processes:
    pr.join()

end = time.perf_counter()


print(f'finished in {end - start}')


# switch from multiprocessing module to concurrent.futures module (using ProcessPool(with context manager) instead of multiprocessing.Process)
# phase 2

with concurrent.futures.ProcessPoolExecutor() as executor:
    f = executor.submit(do_something, 1) # create future(scheduled function to be executed) object that encapsulate execution of function
    # '_state': 'RUNNING', '_result': None, '_exception': None, '_waiters': [], '_done_callbacks': []}
    print(type(f))
    print(f.__dict__)
    print(f.result)

with concurrent.futures.ProcessPoolExecutor() as executor:
    results = [executor.submit(do_something, 1) for _ in range(0,10)]
    for f in concurrent.futures.as_completed(results):
        # '_state': 'FINISHED'
        print(f.result())
    
#using map run target on each item
with concurrent.futures.ProcessPoolExecutor() as executor: #(context manager will automatically join the processes)
    secs = [1,2,3,4]
    results = executor.map(do_something, secs)  #return future.result 

    for result in results:
        print(result) # you can handle error here