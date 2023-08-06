import os
import asyncio
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = int(os.environ.get('MAX_WORKERS', '16'))

# Worker pool
worker_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

def tasks(s, jdata, func, output):
    return [run_analysis(s[i.get("account_id")][i.get("region")],i, func, output) for i in jdata]

def worker(func):
    """
    Runs blocking code asynchronously in worker thread from worker pool
    """
    @wraps(func)
    async def run(*args, **kwargs):
        pfunc = partial(func, *args, **kwargs)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(worker_pool, pfunc)
    return run

@worker
def run_analysis(s, record, func, output):
    if s: output.append(func(s,record))
