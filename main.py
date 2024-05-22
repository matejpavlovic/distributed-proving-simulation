# Runs a Boojum prover simulation for a single batch.
# Takes a single command-line argument: the number of witnesses to create from the batch.
# Currently, for simplicity, we encode this number as the "size" property of a batch.
#
# usage:
#          python3 main.py num_batches

import sys

import config
import orchestrator
import events
import eventloop
import stats

# Load configuration file.
if len(sys.argv) > 1:
    config.load(sys.argv[1])
else:
    config.load("config.yaml")

# Initialize and run the simulation.
orchestrator.init()
eventloop.add(events.Batch(0, config.data["batch"]["num_witnesses"]))
num_events, elapsed_time = eventloop.run(True)

# Print simulation results.
stats.print_data()
print("Number of events processed: {0}".format(num_events))
print("Elapsed logical time: {0}".format(elapsed_time))
