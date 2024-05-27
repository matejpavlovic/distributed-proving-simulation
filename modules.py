# This file defines the event-processing modules represented as simple functions.
# They simulate the actors in the system receiving inputs (such as witness vectors)
# and producing outputs (such as proofs).
# In the simulation, modules are invoked by the orchestrator, inputs being passed as arguments.
# This should correspond to some orchestration mechanism assigning tasks to remote actors in practice.
# Each module records statistics about spent resources.
import random

import config
import eventloop
import events
import stats


def basic_witness_generator(batch):
    for i in range(batch.size):
        eventloop.add(events.Witness(batch.ts + config.data["witness"]["generation_time"], 0, i))

        # Record spent resources.
        stats.record_send("basic_witness_gen", config.data["witness"]["size"])
        stats.record_compute("basic_witness_gen", config.data["witness"]["generation_time"])


def witness_generator(inputs, index, timestamp):
    # Stub. Simply add witness generation delay to the highest input timestamp.
    # Level is the same for all inputs, taking first and incrementing by 1.
    eventloop.add(events.Witness(timestamp + config.data["witness"]["generation_time"], inputs[0].level + 1, index))

    # Record spent resources.
    stats.record_receive("witness_gen", len(inputs) * config.data["proof"]["size"])
    stats.record_send("witness_gen", config.data["witness"]["size"])
    stats.record_compute("witness_gen", config.data["witness"]["generation_time"])


def witness_vector_generator(witness, timestamp):
    eventloop.add(events.WitnessVector(
        timestamp + config.data["witness_vector"]["generation_time"],
        witness.level,
        witness.index,
    ))

    # Record spent resources.
    stats.record_receive("witness_vector_generator", config.data["witness"]["size"])
    stats.record_send("witness_vector_generator", config.data["witness_vector"]["size"])
    stats.record_compute("witness_vector_generator", config.data["witness_vector"]["generation_time"])


def intermediate_prover(witness_vector, timestamp):

    # Flip a coin to schedule a timeout event instead of computing a proof.
    # Since this is a fault of the prover, we do not record any resources spent.
    if random.random() < config.data["proof"]["omission_probability"]:
        eventloop.add(events.IntermediateProofTimeout(
            timestamp + config.data["proof"]["timeout"],
            witness_vector,
        ))
        return

    # If no omission occurs, produce a proof after the configured delay.
    eventloop.add(events.IntermediateProof(
        timestamp + config.data["proof"]["generation_time"],
        witness_vector.level,
        witness_vector.index,
    ))

    # Record spent resources.
    stats.record_receive("prover", config.data["witness_vector"]["size"])
    stats.record_send("prover", config.data["proof"]["size"])
    stats.record_compute("prover", config.data["proof"]["generation_time"])


def root_prover(witness_vector):
    eventloop.add(events.RootProof(witness_vector.ts + config.data["proof"]["generation_time"]))

    # Record spent resources.
    stats.record_receive("root_prover", config.data["witness_vector"]["size"])
    stats.record_send("root_prover", config.data["proof"]["size"])
    stats.record_compute("root_prover", config.data["proof"]["generation_time"])
