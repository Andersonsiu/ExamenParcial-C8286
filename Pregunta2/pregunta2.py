import asyncio
import marshal
import multiprocessing as mp
import pickle
from queue import Empty, Queue # PriorityQueue
import threading
import types
from multiprocessing import Process, Queue

work_queue = Queue()
results_queue = Queue()
results = {}


#AGREGAR MANEJO DE ERRRORES
async def submit_job(job_id, reader, writer):
    writer.write(job_id.to_bytes(4, 'little'))
    writer.close()
    code_size = int.from_bytes(await reader.read(4), 'little')
    my_code = marshal.loads(await reader.read(code_size))
    data_size = int.from_bytes(await reader.read(4), 'little')
    data = pickle.loads(await reader.read(data_size))
    work_queue.put_nowait((job_id, my_code, data))
    try:
        job_id, data = results_queue.get_nowait()
        results[job_id] = data
    except Empty:
        return


#AGREGAR MANEJO DE ERRRORES
def get_results_queue():
    while results_queue.qsize() > 0:
        try:
            job_id, data = results_queue.get_nowait()
            results[job_id] = data
        except Empty:
            return

async def get_results(reader, writer):
    get_results_queue()
    job_id = int.from_bytes(await reader.read(4), 'little')
    data = pickle.dumps(None)
    if job_id in results:
        data = pickle.dumps(results[job_id])
        del results[job_id]
    writer.write(len(data).to_bytes(4, 'little'))
    writer.write(data)


#AGREGAR MANEJO DE ERRRORES
async def accept_requests(reader, writer, job_id=[0]):
    op = await reader.read(1)
    if op[0] == 0:
        await submit_job(job_id[0], reader, writer) #Errors in async
        job_id[0] += 1
    elif op[0] == 1:
        await get_results(reader, writer)
    try:
        job_id, data = results_queue.get_nowait()
        results[job_id] = data
    except Empty:
        return


#REFACTORIZAR CONCURRENT.FUTURES

from concurrent.futures import ProcessPoolExecutor

def worker(): # daemon
    with ProcessPoolExecutor() as executor:
        while True:
            job_id, code, data = work_queue.get() # blocking
            func = types.FunctionType(code, globals(), 'mapper_and_reducer')
            mapper, reducer = func()
            counts = mr.map_reduce(pool, data, mapper, reducer, 100, mr.reporter)
            results_queue.put((job_id, counts))
        pool.close()
        pool.join()

async def main():
    server = await asyncio.start_server(accept_requests, '127.0.0.1', 1936)
    worker_thread = threading.Thread(target=worker) # Daemon
    worker_thread.start()
    async with server:
        await server.serve_forever()

asyncio.run(main())        
