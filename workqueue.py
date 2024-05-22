from collections import defaultdict


# For each worker type (identified by a string name),
# the number of workers currently available to perform a task
# (such as computing a proof).
available_workers = {}

# For each worker type (identified by a string name),
# a queue (represented as a slice) of module invocations of the corresponding module.
# An invocation is stored as a function receiving a single timestamp argument
# representing the logical time at which the work is starting to be performed.
queues = defaultdict(lambda: [])


def init_workers(module, n):
    available_workers[module] = n


def submit(module, work, timestamp):
    if available_workers[module] > 0:
        # If there are available workers, perform work immediately
        available_workers[module] -= 1
        work(timestamp)
    else:
        # Otherwise, enqueue work item for later.
        queues[module].append(work)


def free(module, timestamp):
    if len(queues[module]) > 0:
        # If there are tasks in the work queue, start the next one.
        queues[module][0](timestamp)
        queues[module] = queues[module][1:]
    else:
        # Otherwise, register another free worker.
        available_workers[module] += 1
