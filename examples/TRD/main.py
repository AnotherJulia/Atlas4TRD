import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from examples.TRD.run_sim import run_simulation
from core.analyzis import SimAnalyzer

import json

def load_simulation_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config


def run_simulation_w_config(name, sim_instances, config_path):
    num_sims = 5
    simulation_instances = []

    config = load_simulation_config(config_path)
    capacity_distribution = {step['slug']: step['capacity_ratio'] for step in config['steps']}
    
    # Don't forget to add the total capacity
    capacity_distribution['total'] = config['total_capacity']

    for index in range(num_sims):
        print(f"Simulation {index}")
        run_simulation(simulation_id=index, config=config,cap_dist=capacity_distribution, simulation_instances=simulation_instances)

    analyzer = SimAnalyzer(simulation_instances)
    analyzer.run(plot=True)

    sim_instances[name] = analyzer.simulation_instances
    return sim_instances


if __name__ == "__main__":
    sim_instances = {}

    sum_instances = run_simulation_w_config(name="esketamine @ 0.2", sim_instances=sim_instances, config_path="config/structure_esketamine_2.json")

