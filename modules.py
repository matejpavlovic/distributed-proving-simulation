# This file defines the event-processing modules represented as simple functions.
# They simulate the actors in the system receiving inputs (such as witness vectors)
# and producing outputs (such as proofs).
# In the simulation, modules are invoked by the orchestrator, inputs being passed as arguments.
# This should correspond to some orchestration mechanism assigning tasks to remote actors in practice.
# Each module records statistics about spent resources.

import eventloop
import events
import stats

witness_size = 5
witness_gen_delay = 100

witness_vec_size = 5000
witness_vec_gen_delay = 1000

proof_size = 2
prover_delay = 200


def basic_witness_generator(batch):
    for i in range(batch.size):
        eventloop.add(events.Witness(batch.ts + witness_gen_delay, 0, i))

        stats.record_send("basic_witness_gen", witness_size)
        stats.record_compute("basic_witness_gen", witness_gen_delay)


def witness_generator(inputs, index):
    # Stub. Simply add witness generation delay to the highest input timestamp.
    # Level is the same for all inputs, taking first and incrementing by 1.
    eventloop.add(events.Witness(max(i.ts for i in inputs) + witness_gen_delay, inputs[0].level + 1, index))

    stats.record_receive("witness_gen", len(inputs) * proof_size)
    stats.record_send("witness_gen", witness_size)
    stats.record_compute("witness_gen", witness_gen_delay)


def witness_vector_generator(witness):
    eventloop.add(events.WitnessVector(witness.ts + witness_vec_gen_delay, witness.level, witness.index))

    stats.record_receive("witness_vector_generator", witness_size)
    stats.record_send("witness_vector_generator", witness_vec_size)
    stats.record_compute("witness_vector_generator", witness_vec_gen_delay)


def intermediate_prover(witness_vector, index):
    # Stub. Simply add prover delay to the highest input timestamp. Level is the same for all inputs.
    # The level is not incremented, as proving and witness generation are considered to be at the same level.
    eventloop.add(events.IntermediateProof(witness_vector.ts + prover_delay, witness_vector.level, index))

    stats.record_receive("prover", witness_vec_size)
    stats.record_send("prover", proof_size)
    stats.record_compute("prover", prover_delay)


def root_prover(witness_vector):
    eventloop.add(events.RootProof(witness_vector.ts + prover_delay))

    stats.record_receive("root_prover", witness_vec_size)
    stats.record_send("root_prover", proof_size)
    stats.record_compute("root_prover", prover_delay)
