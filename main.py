# Runs a Boojum prover simulation for a single batch.
# Takes a single command-line argument: the number of witnesses to create from the batch.
# Currently, for simplicity, we encode this number as the "size" property of a batch.
#
# usage:
#          python3 main.py num_batches

import sys

import orchestrator
import events
import eventloop
import stats

orchestrator.init()
eventloop.add(events.Batch(0, int(sys.argv[1])))
num_events, elapsed_time = eventloop.run()

print("Number of events processed: {0}".format(num_events))
print("Elapsed logical time: {0}".format(elapsed_time))
stats.print_data()
