# This file defines the event-processing modules represented as simple functions.
# They simulate the actors in the system receiving inputs (such as witness vectors)
# and producing outputs (such as proofs).
# In the simulation, modules are invoked by the orchestrator, inputs being passed as arguments.
# This should correspond to some orchestration mechanism assigning tasks to remote actors in practice.

import eventloop
import events

witness_gen_delay = 100
witness_vec_gen_delay = 1000
prover_delay = 200


def basic_witness_generator(batch):
    for i in range(batch.size):
        eventloop.emit(events.Witness(batch.ts + witness_gen_delay, 0, i))


def witness_generator(inputs, index):
    # Stub. Simply add witness generation delay to the highest input timestamp.
    # Level is the same for all inputs, taking first and incrementing by 1.
    eventloop.emit(events.Witness(max(i.ts for i in inputs) + witness_gen_delay, inputs[0].level+1, index))


def witness_vector_generator(witness):
    eventloop.emit(events.WitnessVector(witness.ts + witness_vec_gen_delay, witness.level, witness.index))


def intermediate_prover(inputs, index):
    # Stub. Simply add prover delay to the highest input timestamp. Level is the same for all inputs.
    # The level is not incremented, as proving and witness generation are considered to be at the same level.
    eventloop.emit(events.IntermediateProof(max(i.ts for i in inputs) + prover_delay, inputs[0].level, index))


def root_prover(witness_vector):
    eventloop.emit(events.RootProof(witness_vector.ts + prover_delay))
