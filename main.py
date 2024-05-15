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

orchestrator.init()
eventloop.emit(events.Batch(0, int(sys.argv[1])))
eventloop.run()
