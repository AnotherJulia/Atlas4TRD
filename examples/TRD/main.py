<<<<<<< HEAD
from core import Environment, Factory
from utilities import generate_networkx_graph

if __name__ == '__main__':
    env = Environment(time=0, dt=1) # dt = 1week
=======
from core import Environment, Factory, SimAnalyzer
from patient import Patient
from utilities import generate_networkx_graph
import pandas as pd

# What states to plot
states = ["intake", "remission", "relapse"]
steps = ["ad", "ap", "ad_ap", "esketamine", "ect"]


def run_simulation(simulation_id):
    env = Environment(time=0, dt=1)  # dt = 1week
>>>>>>> origin/packaging/framework

    env.create_state(slug="intake", description="Patients coming into the TRD care pathway", depth=0, env=env)
    env.create_state(slug="remission", description="Patients coming out of the pathway", depth=0, env=env)
    env.create_state(slug="relapse", description="Patients relapsing from the remission bubble", depth=0, env=env)
<<<<<<< HEAD
=======
    env.create_state(slug="recovery", description="Patients relapsing from the remission bubble", depth=0, env=env)
>>>>>>> origin/packaging/framework

    # TODO: ADD STATE SUICIDE / DEATH
    # TODO: CURRENTLY = RELAPSE -> INTAKE; SHOULD CHANGE THIS TO SOMETHING MORE ACCURATE

<<<<<<< HEAD
    env.create_connection("remission", "relapse")
=======
    env.create_connection("remission", "recovery")
    env.create_connection("remission", "relapse")
    env.create_connection("recovery", "relapse")
>>>>>>> origin/packaging/framework
    env.create_connection("relapse", "intake")

    # LEVEL 1 : AUGMENTED THERAPIES

<<<<<<< HEAD
    env.create_step(slug="ad", description="AD Treatment, 12wks", capacity=10, config="../../config/ad_config.json",
=======
    env.create_step(slug="ad", description="AD Treatment, 8wks", capacity=14, config="../../config/ad_config.json",
>>>>>>> origin/packaging/framework
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad")
    env.create_connection("ad", "remission")

<<<<<<< HEAD
    env.create_step(slug="ap", description="AP treatment, 28wks", capacity=10, config="../../config/ap_config.json",
=======
    env.create_step(slug="ap", description="AP treatment, 8wks", capacity=12, config="../../config/ap_config.json",
>>>>>>> origin/packaging/framework
                    depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ap")
    env.create_connection("ap", "remission")

<<<<<<< HEAD
    env.create_step(slug="ad_ap", description="AP+AD treatment, 28wks", capacity=10,
=======
    env.create_step(slug="ad_ap", description="AP+AD treatment, 8wks", capacity=12,
>>>>>>> origin/packaging/framework
                    config="../../config/ad_ap_config.json", depth=1, env=env)
    env.create_connection(start_slug="intake", end_slug="ad_ap")
    env.create_connection("ad_ap", "remission")

    # LEVEL 2: ESKETAMINE TREATMENT

<<<<<<< HEAD
    env.create_step(slug="esketamine", description="Esketamine treatment, 28wks", capacity=10,
=======
    env.create_step(slug="esketamine", description="Esketamine treatment, 12wks", capacity=10,
>>>>>>> origin/packaging/framework
                    config="../../config/esketamine_config.json", depth=2, env=env)
    env.create_connection(start_slug="ad", end_slug="esketamine")
    env.create_connection(start_slug="ap", end_slug="esketamine")
    env.create_connection(start_slug="ad_ap", end_slug="esketamine")

    # LEVEL 3: ECT

<<<<<<< HEAD
    env.create_step(slug="ect", description="ECT Treatment, 28wks", capacity=10, config="../../config/ect_config.json",
=======
    env.create_step(slug="ect", description="ECT Treatment, 28wks", capacity=2, config="../../config/ect_config.json",
>>>>>>> origin/packaging/framework
                    depth=3, env=env)
    env.create_connection("esketamine", "ect")
    env.create_connection("ect", "remission")
    env.create_connection("ect", "ad")

<<<<<<< HEAD
    generate_networkx_graph(env)

    factory = Factory(config="../../config/agent_params.json")
    env.connect_factory(factory)

    # Set up the initial conditions of the pathway
    env.create_initial_agents(2, "ad")
    env.create_initial_agents(2, "ap")
    env.create_initial_agents(2, "ad_ap")
    env.create_initial_agents(2, "intake")
    env.create_initial_agents(2, "esketamine")
    env.create_initial_agents(2, "ect")

    env.set_patient_rate(1)         # this means 2 patients a week coming into the trd pathway

    env.run(until=52, verbose=True)

    states = ["intake", "remission", "relapse"]
    steps = ["ad", "ap", "ad_ap", "esketamine", "ect"]

    env.plot_occupancies(steps)
    env.plot_waiting_queues(steps)

=======
    # generate_networkx_graph(env)

    factory = Factory(config="../../config/agent_params.json", agent_class_type=Patient)
    env.connect_factory(factory)

    # Set up the initial conditions of the pathway
    # env.create_agent("ad", 5)
    # env.create_agent("ap", 2)
    # env.create_agent("ad_ap", 3)
    # env.create_agent("esketamine", 3)
    # env.create_agent("ect", 1)

    env.set_patient_rate(1)  # this means 1 patient a week coming into the trd pathway

    env.run(until=100, verbose=False)

    # env.plot_occupancies()
    # env.plot_waiting_queues()

    from core import SimulationInstance
    instance = SimulationInstance(run_id=simulation_id, agents=env.agents)
    simulation_instances.append(instance)


if __name__ == "__main__":
    num_sims = 1
    simulation_instances = []
    for index in range(num_sims):
        print(f"Simulation {index}")
        run_simulation(simulation_id=index)

    # Transform the dataframe into an Analyzer object that will help us get some data

    analyzer = SimAnalyzer(simulation_instances)
    analyzer.print_logs()

    analyzer.run()
>>>>>>> origin/packaging/framework
