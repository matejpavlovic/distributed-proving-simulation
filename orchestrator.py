# The orchestrator is the "brain" of the (simulated) proof system implementation.
# It keeps track of the progress of the whole system and, the (simulated) modules, and collects their outputs.

from collections import defaultdict

import modules
import eventloop
import workqueue

# These values determine how many inputs are aggregated at each level of the proof tree
# by, respectively, the witness generators and the provers.
witness_gen_fan_in = 2

# Set the number of available workers for each relevant module type.
workqueue.init_workers("witness_generator", 50)
workqueue.init_workers("intermediate_prover", 10)
workqueue.init_workers("witness_vector_generator", 20)

# The total number of witnesses, witness vectors, and proofs for each level.
# E.g., proof_tree_width[2] stores the proof tree width at level 2.
proof_tree_width = {}

# For each level, set of computed proofs by index.
# E.g., proofs[2][5] stores the proof at level 2, index 5.
proofs = defaultdict(lambda: {})


def process_batch(batch):
    # Generate the proof tree structure, i.e., for each level of the proof tree,
    # calculate the number of witness vectors and proofs that will be computed at that level.

    # At level 0, the number of witness vectors is determined by batch size.
    proof_tree_width[0] = batch.size

    # Add more levels until there is only one proof.
    level = 0
    while proof_tree_width[level] > 1:
        # One witness vector per witness_gen_fan_in inputs plus one witness vector for the rest (if any)
        proof_tree_width[level + 1] = (proof_tree_width[level] // witness_gen_fan_in +
                                       (1 if proof_tree_width[level] % witness_gen_fan_in > 0 else 0))
        level += 1

    # Now that the proof tree structure is known, start the basic witness generator
    # to trigger the actual (simulated) proof computation.
    modules.basic_witness_generator(batch)


def process_witness(witness):

    # A witness generator just finished working. Give it a new task if any are pending.
    workqueue.free("witness_generator", witness.ts)

    # Feed the witness to a witness vector generator.
    def generate_witness_vector(timestamp):
        modules.witness_vector_generator(witness, timestamp)
    workqueue.submit("witness_vector_generator", generate_witness_vector, witness.ts)


def process_witness_vector(witness_vector):

    # A witness vector generator just finished working. Give it a new task if any are pending.
    workqueue.free("witness_vector_generator", witness_vector.ts)

    # Pass the witness vector to a prover.
    if proof_tree_width[witness_vector.level] == 1:
        modules.root_prover(witness_vector)
    else:
        def prove(timestamp):
            modules.intermediate_prover(witness_vector, timestamp)
        workqueue.submit("intermediate_prover", prove, witness_vector.ts)


def process_intermediate_proof(proof):

    # A prover just finished working. Give it a new proving task if any are pending.
    # Note that this code must be executed before this function has a chance to return.
    # That is why we do it before processing the proof.
    workqueue.free("intermediate_prover", proof.ts)

    # Convenience variables
    level = proof.level
    index = proof.index

    # Register computed proof.
    if index in proofs[level]:
        raise Exception("Proof with index {0} at level {1} already processed.".format(index, level))
    proofs[level][index] = proof

    # Collect the inputs for witness computation.
    # (One witness is computed for a segment of witness_gen_fan_in consecutive proofs.)
    start_proof = (index // witness_gen_fan_in) * witness_gen_fan_in
    end_proof = min(start_proof + witness_gen_fan_in, proof_tree_width[level])
    inputs = []
    for i in range(start_proof, end_proof):
        if i in proofs[level]:
            inputs.append(proofs[level][i])
        else:
            return

    # Feed the proofs in the next level of witness generation.
    def generate_witness(timestamp):
        modules.witness_generator(inputs, index // witness_gen_fan_in, timestamp)
    workqueue.submit("witness_generator", generate_witness, proof.ts)


def init():
    eventloop.set_handler("batch", process_batch)
    eventloop.set_handler("witness", process_witness)
    eventloop.set_handler("witness_vector", process_witness_vector)
    eventloop.set_handler("intermediate_proof", process_intermediate_proof)
    eventloop.set_handler("root_proof", lambda event: None)  # Do nothing with the root proof.
