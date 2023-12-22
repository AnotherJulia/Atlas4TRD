from core import *
from patient import Patient

import networkx as nx
import matplotlib.pyplot as plt

from utilities.netx import plot_bubbles_and_connections
from utilities import ConfigLoader

def run_sim():

    Loader = ConfigLoader(config_file="env_config.json")
    print(Loader.bubbles[0])
    plot_bubbles_and_connections(Loader.bubbles, Loader.connections)



    # env.run(until=100, verbose=True)



if __name__ == '__main__':
    run_sim()
