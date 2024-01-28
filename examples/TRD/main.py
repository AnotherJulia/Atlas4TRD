import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from examples.TRD.run_sim import run_simulation
from core.analyzis import SimAnalyzer

import json

def load_simulation_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config


if __name__ == "__main__":
    num_sims = 5
    simulation_instances = []

    config = load_simulation_config('config/structure_esketamine.json')
    capacity_distribution = {step['slug']: step['capacity_ratio'] for step in config['steps']}
    # Don't forget to add the total capacity
    capacity_distribution['total'] = config['total_capacity']


    for index in range(num_sims):
        print(f"Simulation {index}")
        run_simulation(simulation_id=index, config=config,cap_dist=capacity_distribution)

    analyzer = SimAnalyzer(simulation_instances)
    analyzer.run(plot=True)
