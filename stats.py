from collections import defaultdict

data_received = defaultdict(lambda: 0)
data_sent = defaultdict(lambda: 0)
computation_performed = defaultdict(lambda: 0)


def record_receive(key, val):
    data_received[key] += val


def record_send(key, val):
    data_sent[key] += val


def record_compute(key, val):
    computation_performed[key] += val


def print_data():
    keys = data_received.keys() | data_sent.keys() | computation_performed.keys()
    for k in keys:
        print(k+":")
        print("            data received: {0}".format(data_received[k]))
        print("                data sent: {0}".format(data_sent[k]))
        print("    computation performed: {0}".format(computation_performed[k]))
        print()
