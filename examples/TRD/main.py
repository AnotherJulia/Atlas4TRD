import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from core import Environment, Factory, SimAnalyzer
from patient import Patient
# from utilities import generate_networkx_graph
# import pandas as pd

# What states to plot
states = ["intake", "remission", "relapse"]
steps = ["ad", "ap", "ad_ap", "esketamine", "ect"]

capacities = {
     "total": 50,
      "ad": 0.4,
      "ad_ap": 0.15,
      "ap": 0.10,
      "esk": 0.2,
      "ect": 0.05
}

def vary_capacities(capacities):

    total_value = 0
    for key, value in capacities.items():
        if key !=  "total":
            total_value += value

    if total_value != 1:
        difference = 1 - total_value

        # re-distribute the capacities again based on existing proportions
        print(difference)


def get_capacity(name):
    total = capacities["total"]
    return round(total * capacities[name], 0)

def run_simulation(simulation_id):
    env = Environment(time=0, dt=1)  # dt = 1week

    env.create_state(slug="intake", description="Patients coming into the TRD care pathway", depth=0, env=env)
    env.create_state(slug="remission", description="Patients coming out of the pathway", depth=0, env=env)
    env.create_state(slug="relapse", description="Patients relapsing from the remission bubble", depth=0, env=env)
    env.create_state(slug="recovery", description="Patients relapsing from the remission bubble", depth=0, env=env)

    env.create_connection("remission", "recovery")
    env.create_connection("remission", "relapse")
    env.create_connection("recovery", "relapse")
    env.create_connection("relapse", "intake")

    # LEVEL 1 : AUGMENTED THERAPIES

    env.create_step(slug="ad", description="AD Treatment, 8wks", capacity=get_capacity("ad"), config="config/ad_config.json",
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad")
    env.create_connection("ad", "remission")

    env.create_step(slug="ap", description="AP treatment, 8wks", capacity=get_capacity("ap"), config="config/ap_config.json",
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ap")
    env.create_connection("ap", "remission")

    env.create_step(slug="ad_ap", description="AP+AD treatment, 8wks", capacity=get_capacity("ad_ap"),
                    config="config/ad_ap_config.json", depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad_ap")
    env.create_connection("ad_ap", "remission")

    # LEVEL 2: ESKETAMINE TREATMENT

    env.create_step(slug="esketamine", description="Esketamine treatment, 12wks", capacity=get_capacity("esk"),
                    config="config/esketamine_config.json", depth=2, env=env)
    env.create_connection(start_slug="ad", end_slug="esketamine")
    env.create_connection(start_slug="ap", end_slug="esketamine")
    env.create_connection(start_slug="ad_ap", end_slug="esketamine")

    # LEVEL 3: ECT

    env.create_step(slug="ect", description="ECT Treatment, 28wks", capacity=get_capacity("ect"), config="config/ect_config.json",
                    depth=3, env=env)
    env.create_connection("esketamine", "ect")
    env.create_connection("ect", "remission")
    env.create_connection("ect", "ad")

    # generate_networkx_graph(env)

    factory = Factory(config="config/agent_params.json", agent_class_type=Patient)
    env.connect_factory(factory)

    # Set up the initial conditions of the pathway
    # env.create_agent("ad", 5)
    # env.create_agent("ap", 2)
    # env.create_agent("ad_ap", 3)
    # env.create_agent("esketamine", 3)
    env.create_agent("intake", 1000)

    env.set_patient_rate(1)  # this means 1 patient a week coming into the trd pathway

    env.run(until=200, verbose=False)

    # env.plot_occupancies()
    env.plot_waiting_queues(steps)

    from core import SimulationInstance
    instance = SimulationInstance(run_id=simulation_id, agents=env.agents)
    simulation_instances.append(instance)


if __name__ == "__main__":
    num_sims = 1
    simulation_instances = []

    for index in range(num_sims):
        print(f"Simulation {index}")
        run_simulation(simulation_id=index)

    analyzer = SimAnalyzer(simulation_instances)
    # analyzer.print_logs()

    analyzer.run()
