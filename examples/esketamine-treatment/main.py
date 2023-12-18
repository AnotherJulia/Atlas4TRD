from core import *
from patient import Patient

import networkx as nx
import matplotlib.pyplot as plt

from utilities.netx import plot_bubbles_and_connections


def run_sim():
    env = Environment(name="Simple Esketamine Treatment", dt=1)

    intake = Bubble(name="intake", capacity=0, type="step")
    induction = Bubble(name="induction", capacity=5, type="step")
    maintenance = Bubble(name="maintenance", capacity=20, type="step")

    remission = Bubble(name="remission", capacity=0, type="state")
    relapse = Bubble(name="relapse", capacity=0, type="state")
    death = Bubble(name="death", capacity=0, type="state")
    no_response = Bubble(name="no response", capacity=0, type="state")

    env.add_bubble(intake)
    env.add_bubble(induction)
    env.add_bubble(maintenance)
    env.add_bubble(remission)
    env.add_bubble(relapse)
    env.add_bubble(death)
    env.add_bubble(no_response)

    env.add_connection(from_bubble=intake, to_bubble=induction)
    env.add_connection(from_bubble=induction, to_bubble=maintenance)
    env.add_connection(from_bubble=induction, to_bubble=no_response)
    env.add_connection(from_bubble=induction, to_bubble=death)
    env.add_connection(from_bubble=maintenance, to_bubble=death)

    env.add_connection(from_bubble=maintenance, to_bubble=remission)
    env.add_connection(from_bubble=maintenance, to_bubble=relapse)

    # plot_bubbles_and_connections(env.bubbles, env.connections)

    patient_1 = Patient(name="Bassie", start=intake, initial_madrs=20)
    env.add_agent(patient_1)

    env.run(until=100, verbose=True)






if __name__ == '__main__':
    run_sim()
