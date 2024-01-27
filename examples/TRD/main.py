import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from core import Environment, Factory, SimAnalyzer
from utilities import Capacity
from patient import Patient
# from utilities import generate_networkx_graph

# What states to plot
states = ["intake", "remission", "recovery", "relapse"]
steps = ["ad", "ap", "ad_ap", "esketamine", "ect"]

capacity_distribution = {
    "total": 50,
    "ad": 0.3,
    "ap": 0.2,
    "ad_ap": 0.2,
    "esketamine": 0.2, 
    "ect": 0.1
}

capacity = Capacity(capacity_distribution)
print(f"{capacity}")

def run_simulation(simulation_id):
    env = Environment(time=0, dt=1)  # dt = 1 week

    env.create_state(slug="intake", description="Patients coming into the TRD care pathway", depth=0, env=env)
    env.create_state(slug="remission", description="Patients coming out of the pathway", depth=0, env=env)
    env.create_state(slug="relapse", description="Patients relapsing from the remission bubble", depth=0, env=env)
    env.create_state(slug="recovery", description="Patients relapsing from the remission bubble", depth=0, env=env)

    env.create_connection("remission", "recovery")
    env.create_connection("remission", "relapse")
    env.create_connection("recovery", "relapse")
    env.create_connection("relapse", "intake")

    # LEVEL 1 : AUGMENTED THERAPIES

    env.create_step(slug="ad", description="AD Treatment, 8wks", capacity=capacity.retrieve_capacity("ad"), config="config/ad_config.json",
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad")
    env.create_connection("ad", "remission")

    env.create_step(slug="ap", description="AP treatment, 8wks", capacity=capacity.retrieve_capacity("ap"), config="config/ap_config.json",
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ap")
    env.create_connection("ap", "remission")

    env.create_step(slug="ad_ap", description="AP+AD treatment, 8wks", capacity=capacity.retrieve_capacity("ad_ap"),
                    config="config/ad_ap_config.json", depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad_ap")
    env.create_connection("ad_ap", "remission")

    # LEVEL 2: ESKETAMINE TREATMENT

    env.create_step(slug="esketamine", description="Esketamine treatment, 12wks", capacity=capacity.retrieve_capacity("esketamine"),
                    config="config/esketamine_config.json", depth=2, env=env)
    env.create_connection(start_slug="ad", end_slug="esketamine")
    env.create_connection(start_slug="ap", end_slug="esketamine")
    env.create_connection(start_slug="ad_ap", end_slug="esketamine")

    # LEVEL 3: ECT

    env.create_step(slug="ect", description="ECT Treatment, 28wks", capacity=capacity.retrieve_capacity("ect"), config="config/ect_config.json",
                    depth=3, env=env)
    env.create_connection("esketamine", "ect")
    env.create_connection("ect", "remission")
    env.create_connection("ect", "ad")

    # generate_networkx_graph(env)

    factory = Factory(config="config/agent_params.json", agent_class_type=Patient)
    env.connect_factory(factory)

    # setup initial patients
    env.create_agent("intake", 1000)
    env.set_patient_rate(1)  # this means 1 patient a week coming into the trd pathway

    env.run(until=250, verbose=False)

    # if simulation_id == 0:
    #     env.plot_occupancies(states)
    #     env.plot_waiting_queues(steps)
    #     pass

    from core import SimulationInstance
    instance = SimulationInstance(run_id=simulation_id, agents=env.agents,run_data=env.data)
    simulation_instances.append(instance)


if __name__ == "__main__":
    num_sims = 5
    simulation_instances = []

    for index in range(num_sims):
        print(f"Simulation {index}")
        run_simulation(simulation_id=index)

    analyzer = SimAnalyzer(simulation_instances)
    # analyzer.print_logs()

    analyzer.run(plot=True)
