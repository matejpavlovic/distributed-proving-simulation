# This file defines events that serve as inputs and outputs to the distributed prover modules.
# Each event has a type and a timestamp used by the eventloop implementation to decide in which order
# and by which modules the events are to be processed.
#
# Concrete events carry additional event-specific data (e.g. size of the simulated payload).
# The idea is to observe all these events as they are processed by the event loop
# and obtain insights about the execution, such as total data transmitted between (specific kinds of) modules.

class Event:
    def __init__(self, ts, event_type):
        self.ts = ts
        self.type = event_type

    def __lt__(self, other):
        if self.ts < other.ts:
            return True
        return self.type < other.type

    def __str__(self):
        return "Event(ts={0}, type={1})".format(self.ts, self.type)


class Batch(Event):
    def __init__(self, ts, size):
        Event.__init__(self, ts, "batch")
        self.size = size

    def __lt__(self, other):
        if Event.__lt__(self, other):
            return True
        return self.size < other.size

    def __str__(self):
        return "Batch(ts={0}, size={1})".format(self.ts, self.size)


class Witness(Event):
    def __init__(self, ts, level, index):
        Event.__init__(self, ts, "witness")
        self.level = level
        self.index = index

    def __lt__(self, other):
        if Event.__lt__(self, other):
            return True
        if Event.__lt__(other, self):
            return False
        if self.level < other.level:
            return True
        if self.level > other.level:
            return False
        return self.index < other.index

    def __str__(self):
        return "Witness(ts={0}, level={1}, index={2})".format(self.ts, self.level, self.index)


class WitnessVector(Event):
    def __init__(self, ts, level, index):
        Event.__init__(self, ts, "witness_vector")
        self.level = level
        self.index = index

    def __lt__(self, other):
        if Event.__lt__(self, other):
            return True
        if Event.__lt__(other, self):
            return False
        if self.level < other.level:
            return True
        if self.level > other.level:
            return False
        return self.index < other.index

    def __str__(self):
        return "WitnessVector(ts={0}, level={1}, index={2})".format(self.ts, self.level, self.index)


class IntermediateProof(Event):
    def __init__(self, ts, level, index):
        Event.__init__(self, ts, "intermediate_proof")
        self.level = level
        self.index = index

    def __lt__(self, other):
        if Event.__lt__(self, other):
            return True
        if Event.__lt__(other, self):
            return False
        if self.level < other.level:
            return True
        if self.level > other.level:
            return False
        return self.index < other.index

    def __str__(self):
        return "IntermediateProof(ts={0}, level={1}, index={2})".format(self.ts, self.level, self.index)


class IntermediateProofTimeout(Event):
    def __init__(self, ts, witness_vector):
        Event.__init__(self, ts, "intermediate_proof_timeout")
        self.witness_vector = witness_vector

    def __lt__(self, other):
        if Event.__lt__(self, other):
            return True
        if Event.__lt__(other, self):
            return False
        return self.witness_vector < other.witness_vector

    def __str__(self):
        return "IntermediateProofTimeout(ts={0}, witness_vector={1})".format(self.ts, self.witness_vector)


class RootProof(Event):
    def __init__(self, ts):
        Event.__init__(self, ts, "root_proof")

    def __lt__(self, other):
        return Event.__lt__(self, other)

    def __str__(self):
        return "RootProof(ts={0})".format(self.ts)
