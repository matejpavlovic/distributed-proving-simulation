# Distributed Proving Simulation

This code simulates the computation of proofs for a ZK rollup at a fine-grained level.
It is under development and currently only focuses on Boojum.
The aim is to generalize it to be easily used for simulating other proof systems.

The outcome of the simulation are insights into the behavior of the system under faults, various system-wide metrics
such as latency, data transmitted, total computation overhead, cost, etc...
Once generalized, different strategies to deal with failing components should be easy to try and evaluate.

## Usage

Currently, only one parameter can be set on the command line - the number of witnesses produced from one incoming batch.
The simulation of proving a single batch is started by running

```shell
python3 main.py <num_witnesses>
```

Other parameters, such as the sizes of proofs and witnesses, computation delays, etc., are hard-coded in
[modules.py](/modules.py) for now.

The degree of the proof tree (separately for provers and witness generators) is hard-coded in the corresponding
variables in [orchestrator.py](/orchestrator.py).

## Statistics

At the end of the run, the simulator prints basic statistics about how much computation and communication has been
performed (in simulation) by each type of component.

## See also

The proof tree being simulated is sketched in [this Notion document](https://www.notion.so/matterlabs/Boojum-Fault-Injection-Simulation-2d6b04bbd55d4215b96c9185e432b91d?pvs=4).
(The simulation only covers the bottom part of it for now.)