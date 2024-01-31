import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from tqdm import tqdm

from examples.TRD.run_sim import run_simulation
# from core.analyzis import SimAnalyzer
from examples.TRD.analyse import analyse_instances
from utilities.tom import capacity_allocation

import json

def load_simulation_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config


def run_simulation_w_config(name, config_path, esketamine_fraction):
    num_sims = 10
    simulation_instances = []

    config = load_simulation_config(config_path)
    simulation_duration = config["simulation_duration"]

    config_path_cap = "config/capacities.json"
    config_cap = load_simulation_config(config_path_cap)

    capacity_distribution = capacity_allocation(config_cap, esketamine_fraction=esketamine_fraction)
    capacity_distribution['total'] = config['total_capacity']
    # print(f"{name}: {capacity_distribution}")

    # analyzer = SimAnalyzer(simulation_instances)
    # analyzer.run(plot=False)
    
    # Whoop whoop, fancy progress bar
    for index in tqdm(range(num_sims), desc=f"Running Simulations for '{name}'"):
        instance = run_simulation(simulation_id=index, config=config, cap_dist=capacity_distribution, simulation_duration=simulation_duration)
        simulation_instances.append(instance)

    return simulation_instances

if __name__ == "__main__":
    sim_instances = {}

    # sim_instances["esketamine @ 10%"] = run_simulation_w_config(name="esketamine @ 10%",
    #         config_path="config/structure_esketamine.json", esketamine_fraction=0.1)
    sim_instances["esketamine @ 20%"] = run_simulation_w_config(name="esketamine @ 20%",
            config_path="config/structure_esketamine.json", esketamine_fraction=0.2)
    # sim_instances["esketamine @ 40%"] = run_simulation_w_config(name="esketamine @ 40%",
    #         config_path="config/structure_esketamine.json", esketamine_fraction=0.4)
    # sim_instances["no esketamine"] = run_simulation_w_config(name="no esketamine",
    #         config_path="config/structure_default.json", esketamine_fraction=0.0)
    

    # instance = sim_instances["esketamine @ 20%"][0]
    # agents = instance.agents
    # print(agents[500].medical_history)

    analyse_instances(sim_instances)
