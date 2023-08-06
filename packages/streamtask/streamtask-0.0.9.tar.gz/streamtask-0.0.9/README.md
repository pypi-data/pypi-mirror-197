# Streamtask
**Streamtask** is a lightweight python parallel framework for parallelizing the computationally intensive pipelines. It is similar to Map/Reduce, while it is more lightweight. It parallelizes each module in the pipeline with a given processing number to make it possible to leverage the different speeds in different modules. It improves the performance especially there are some heavy I/O operations in the pipeline.

### Example
Suppose we want to process the data in a pipline with 3 blocks, f1, f2 and f3. We can use the following code to  parallelize the processing. We can also directly add a data list or give a file name by using `add_data`.

``` python
def f1(total):
    import time
    for i in range(total):
        time.sleep(0.002)
        yield i * 2

def f2(n, add, third = 0.01):
    time.sleep(0.02)
    return n + add + third

def f3_the_final(n):
    time.sleep(0.03)
    return n + 1

if __name__ == "__main__":
    total = 100000
    stk = StreamTask(total = total)
    stk.add_data(data = range(total), batch_size=10) # Also support directly stream reading file
    #stk.add_module(f1, 1, total = total)
    stk.add_module(f2, 2, args = [0.5], third = 0.02)
    stk.add_module(f3_the_final, 2)
    stk.run(parallel = True)
    stk.join()
    res = stk.get_results()
    print(stk.get_results())
```

```
stream_reader (1/1):  79%|██████████████████████████████████████████████▋            | 7923/10000 [00:05<00:01, 1567.68it/s]
f2 (2/2):  29%|████████████████████▉                                                   | 1927/6635 [00:04<00:09, 476.72it/s]
f3_the_final (2/2): 100%|█████████████████████████████████████████████████████████████▉| 1927/1928 [00:04<00:00, 476.55it/s]
```