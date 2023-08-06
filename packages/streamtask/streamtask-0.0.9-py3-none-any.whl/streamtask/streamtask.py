from __future__ import absolute_import
import multiprocessing
#multiprocessing.set_start_method('spawn', True) #Slow, debug only
from multiprocessing import Process, Queue, Pool, Manager
import time
import sys
import queue
import datetime
import traceback
import logging
from tqdm.auto import tqdm
import os
import itertools
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
STREAM_LINE_TAG = "[StreamTask]"

def stream_reader(file = None, data = None, batch_size = 50, format = "plain"):
    if file is not None and data is not None:
        logging.error(f"{STREAM_LINE_TAG} Only one of file/data should be set.")
    batch = []
    cnt = 0
    # gz file is 5x faster than bz2.
    if file is not None:
        if format == "plain":
            reader = open(file, "r")
        elif format == "byte":
            reader = open(file, "rb")
        elif format == "bz2":
            reader = os.popen("pbzip2 -dc %s "%file)
        elif format == "gz":
            reader = os.popen("pigz -dc %s"%file)
    elif data is not None:
        reader = data
    else:
        logging.error(f"{STREAM_LINE_TAG} Either file or data should be set a value.")
    for line in reader:
        batch.append(line)
        cnt += 1
        if batch_size is None:
            yield line
        elif len(batch) >= batch_size:
            res = batch
            batch = []
            yield res
    if batch_size is not None and batch:
        yield batch

def stream_writer(content, file = None, filemode = "w"):
    if file is not None:
        if not hasattr(stream_writer, 'f'):
            stream_writer.f = open(file, filemode)
        stream_writer.f.write(content)

def func_wrapper(func, q_in, q_out, layer, proc_num, finished, args, kwargs):
    if q_in is None:#First queue, without input
        for d in func(*args, **kwargs):
            q_out.put(d)
            with finished.lock:
                finished[layer] += 1
    else: # Others with input
        while True:
            try:
                input_data = q_in.get(timeout = 2)
                r = func(input_data, *args, **kwargs)
                q_out.put(r)
                with finished.lock:
                    finished[layer] += 1
            except queue.Empty:
                with proc_num.lock:
                    #print("empty!", func.__name__, q_in.qsize(), proc_num[layer - 1])
                    if q_in.qsize() == 0 and proc_num[layer - 1] <= 0:
                        logging.info(f"{STREAM_LINE_TAG} break")
                        break
            except Exception as error:
                q_in.put(input_data)#return back
                logging.error(f"{STREAM_LINE_TAG} {func.__name__} Error!")
                logging.error(f"{STREAM_LINE_TAG} {traceback.print_exc()}")

    with proc_num.lock:            
        proc_num[layer] -= 1
    logging.info(f"{STREAM_LINE_TAG} Finish {str(func)}")

def show_progress(proc_num, modules, buffers, finished, total):
    try:
        finished_prev = list(finished)
        st = time.time()
        st0 = st
        pbars = [tqdm(total=100, desc=f"{modules[i].__name__} ({proc_num[i]}/{proc_num[i]})") for i in range(len(modules))]
        total_proc_num = [proc_num[i] for i in range(len(modules))]
        while sum(proc_num) > 0:
            log_str = ""
            has_progress = False
            for i in range(len(modules)):
                finish_inc = finished[i] - finished_prev[i]
                has_progress = True if finish_inc > 0 else False
                if modules[i] is not None:
                    #log_str += "%s: [%d ⇦ %s, %.1f/s]; "%(modules[i].__name__, finished[i], str(buffers[i].qsize() * batch_sizes[i]) if buffers[i] and batch_sizes[i] else 'N/A', (finished[i]) / (time.time() - st0))
                    pbars[i].n = finished[i]
                    acnt = buffers[i].qsize() + proc_num[i] + finished[i] if buffers[i] else total
                    pbars[i].total = min(acnt, total)
                    pbars[i].desc = f"{modules[i].__name__} ({proc_num[i]}/{total_proc_num[i]})"
                    pbars[i].refresh()
            finished_prev = list(finished)
            st = time.time()
            if not has_progress:
                continue
            #logging.info(f"{STREAM_LINE_TAG} {log_str}")
            time.sleep(1)
            #sys.stdout.write('\x1b[2K\r')
            #print("", end='\r')
            #print(proc_num, finished, [b.qsize() if b is not None else 'na' for b in buffers])
            remain_seconds = (st - st0) / max(1, finished[-1]) * (finished[0] - finished[-1])
            #remain_time = time.strftime('%H:%M:%S', time.gmtime(remain_seconds))
            current_time = datetime.timedelta(seconds = int(st - st0))
            remain_time = datetime.timedelta(seconds = int(remain_seconds))
            #logging.info(f"{STREAM_LINE_TAG} {str(proc_num)} ETA: {current_time} ⇦ {remain_time}")
    except Exception as error:
        logging.error(f"{STREAM_LINE_TAG} show_progress Error! \n {error}")
        
class StreamTask():
    def __init__(self, total = None, parallel = True, verbose = False, aggregate = True):
        self.manager = Manager()
        self.modules = self._get_locked_list(self.manager)
        self.args = []
        self.kwargs = []
        self.buffers = [None]
        self.processes = []
        self.proc_num = self._get_locked_list(self.manager)
        self.finished = self._get_locked_list(self.manager)
        self.aggregate_results = []
        self.parallel = parallel
        self.total = total
        self.aggregate = aggregate
        if verbose:
            logger.setLevel(logging.INFO)

    def _get_locked_list(self, manager):
        l = manager.list()
        l.lock = manager.Lock()
        return l

    def add_module(self, func, proc_num = 1, args = [], **kwargs):
        self.modules.append(func)
        self.proc_num.append(proc_num)
        self.buffers.append(self.manager.Queue())
        self.finished.append(0)
        self.args.append(args)
        self.kwargs.append(kwargs)

    def add_data(self, data, batch_size = None):
        self.total = len(data) if batch_size is None else (len(data) // batch_size if len(data) % batch_size == 0 else len(data) // batch_size + 1)
        if batch_size is not None:
            self.batched_data = True
        self.add_module(stream_reader, args=[None, data, batch_size, format])

    def add_file(self, file = None, batch_size = None, format = "plain"):
        if batch_size is not None:
            self.batched_data = True
        self.add_module(stream_reader, args=[file, None, batch_size, format])


    def add_writer(self, file = None, filemode = "w"):
        self.add_module(stream_writer, args=[file, filemode])

    def run(self, parallel = None):
        if sys.gettrace():
            parallel = False
            logging.error(f"{STREAM_LINE_TAG} In Debug mode, force use serial.")
        parallel = parallel if parallel is not None else self.parallel
        if not parallel:
            self.run_serial()
        else:
            self.run_parallel()

    def run_parallel(self):
        self.run_mode = "run"
        for i in range(len(self.modules)):
            for _ in range(self.proc_num[i]):
                c = Process(target=func_wrapper, args=(self.modules[i], self.buffers[i], self.buffers[i + 1], i, self.proc_num, self.finished, self.args[i], self.kwargs[i]))
                c.start()
                self.processes.append(c)

        c = Process(target=show_progress, args = (self.proc_num, self.modules, self.buffers, self.finished, self.total))
        c.start()
        self.processes.append(c)
        
    def run_serial(self):
        self.run_mode = "run_serial"
        cnt = 0
        for d in self.modules[0](*self.args[0], **self.kwargs[0]):
            for i in range(1, len(self.modules)):
                #print(self.modules[i].__name__, len(d))
                d = self.modules[i](d, *self.args[i], **self.kwargs[i])
            self.buffers[-1].put(d)
            logging.info(f"{STREAM_LINE_TAG} Finish: {cnt}")
            cnt += 1
        
    def join(self):
        while True:
            while self.buffers[-1].qsize() > 0:
                res = self.buffers[-1].get()
                self.aggregate_results.append(res)
            if not any([p.is_alive() for p in self.processes]):
                break
        for p in self.processes:
            p.join()
            logging.info(f"{STREAM_LINE_TAG} {str(p)} Finish")

    def get_results(self):
        while self.buffers[-1].qsize() > 0:
            res = self.buffers[-1].get()
            self.aggregate_results.append(res)
        if hasattr(self, "batched_data") and self.batched_data:
            self.aggregate_results = list(itertools.chain(*self.aggregate_results))
        """if self.run_mode == "run_serial":
            pass
        else:
            self.aggregate_results = list(itertools.chain(*self.aggregate_results))"""
        return self.aggregate_results

    def get_finish_count(self):
        return self.buffers[-1].qsize() 

    
#=============================TEST=============================

def f1(total):
    import time
    for i in range(total):
        time.sleep(0.002)
        yield i * 2

def f2(n, add, third = 0.01):
    time.sleep(0.002)
    if type(n) is not list:
        return n + add + third
    else:
        return [nn + add + third for nn in n ]

def f3_the_final(n):
    time.sleep(0.003)
    if type(n) is not list:
        return n + 1
    else:
        return [nn + 1 for nn in n ]

if __name__ == "__main__":
    total = 100000
    stk = StreamTask(total = total)
    #stk.add_module(f1, 1, total = total)
    stk.add_data(data = range(total), batch_size=21)
    stk.add_module(f2, 2, args = [0.5], third = 0.02)
    stk.add_module(f3_the_final, 2)
    stk.run(parallel = True)
    stk.join()
    res = stk.get_results()
    #print(res)

