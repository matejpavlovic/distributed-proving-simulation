# The orchestrator is the "brain" of the (simulated) proof system implementation.
# It keeps track of the progress of the whole system and, the (simulated) modules, and collects their outputs.

from collections import defaultdict

import modules
import eventloop

# These values determine how many inputs are aggregated at each level of the proof tree
# by, respectively, the witness generators and the provers.
witness_gen_fan_in = 2
prover_fan_in = 2

# For each level, set of computed witness vectors by index.
# E.g., witness_vectors[2][5] stores the witness vector at level 2, index 5.
witness_vectors = defaultdict(lambda: {})

# For each level, set of computed proofs by index.
# E.g., proofs[2][5] stores the proof at level 2, index 5.
proofs = defaultdict(lambda: {})

# The total number of witness vectors for each level.
# E.g., num_witness_vectors[2] stores the total number of witness vectors stored at level 2.
num_witness_vectors = {}

# The total number of proofs for each level.
# E.g., num_proofs[2] stores the total number of witness vectors stored at level 2.
num_proofs = {}


def process_batch(batch):

    # Collect
    num_witness_vectors[0] = batch.size
    num_proofs[0] = batch.size // prover_fan_in + (1 if batch.size % prover_fan_in > 0 else 0)
    items = num_proofs[0]
    level = 1
    while items > 1:
        num_witness_vectors[level] = items // witness_gen_fan_in + (1 if items % witness_gen_fan_in > 0 else 0)
        items = num_witness_vectors[level]

        num_proofs[level] = items // prover_fan_in + (1 if items % prover_fan_in > 0 else 0)
        items = num_proofs[level]

        level += 1

    print(num_witness_vectors)
    print(num_proofs)

    modules.basic_witness_generator(batch)


def process_witness(witness):
    modules.witness_vector_generator(witness)


def process_witness_vector(witness_vector):

    # Convenience variables
    level = witness_vector.level
    index = witness_vector.index

    # Register computed witness vector.
    if index in witness_vectors[level]:
        raise Exception("Witness vector with index {0} at level {1} already processed.".format(index, level))
    witness_vectors[level][index] = witness_vector

    # Collect the inputs for proof computation.
    # (One proof is computed for a segment of prover_fan_in consecutive witness vectors.)
    start_wv = (index // prover_fan_in) * prover_fan_in
    stop_wv = min(start_wv+prover_fan_in, num_witness_vectors[level])
    inputs = []
    for i in range(start_wv, stop_wv):
        if i in witness_vectors[level]:
            inputs.append(witness_vectors[level][i])
        else:
            return

    # Process witness vectors
    if num_proofs[level] == 1:
        modules.root_prover(witness_vector)
    else:
        modules.intermediate_prover(inputs, index // prover_fan_in)


def process_intermediate_proof(proof):
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
    end_proof = min(start_proof+witness_gen_fan_in, num_proofs[level])
    inputs = []
    for i in range(start_proof, end_proof):
        if i in proofs[level]:
            inputs.append(proofs[level][i])
        else:
            return

    # Feed the proofs in the next level of witness generation.
    modules.witness_generator(inputs, index // witness_gen_fan_in)


def init():
    eventloop.set_handler("batch", process_batch)
    eventloop.set_handler("witness", process_witness)
    eventloop.set_handler("witness_vector", process_witness_vector)
    eventloop.set_handler("intermediate_proof", process_intermediate_proof)
    eventloop.set_handler("root_proof", lambda event: None)
