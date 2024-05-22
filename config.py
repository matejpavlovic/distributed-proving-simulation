import yaml

# This variable stores the all the configuration data directly as loaded from the YAML config file.
# For simplicity, it is directly accessed by the simulation code, and it is the user's responsibility
# to provide a well-formed config file containing all required values.
data = None


def load(filename):
    global data

    with open(filename) as file:
        data = yaml.safe_load(file)
