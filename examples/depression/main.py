from examples.depression.config import DepressionSimulationConfig
from core import Environment, Agent, Bubble, MoveAgentEvent, AgentFactory

# Set up the configuration/data file for the simulation
simulation_config = DepressionSimulationConfig(
    name="Depression Pathway Simulation",
    waiting_capacity=None,
    intake_capacity=10,
    diagnosis_capacity=5,
    therapy_capacity=5,
    medication_capacity=5
)


def depression_sim():
    env = Environment(config=simulation_config)
    print("Running: ", env.name, " -------------")

    # lets create some bubbles
    waiting = Bubble("waiting", simulation_config.waiting_capacity)
    intake = Bubble("intake", simulation_config.intake_capacity)
    diagnosis = Bubble("diagnosis", simulation_config.diagnosis_capacity)
    medical_treatment = Bubble("medical_treatment", simulation_config.medication_capacity)
    therapy_treatment = Bubble("therapy_treatment", simulation_config.therapy_capacity)

    env.add_bubble(waiting)
    env.add_bubble(intake)
    env.add_bubble(diagnosis)
    env.add_bubble(medical_treatment)
    env.add_bubble(therapy_treatment)

    # lets create some patients (agents)
    # patient_1 = Agent(id=1, initial_depression_score=12, initial_bubble="intake")
    # patient_2 = Agent(id=2, initial_depression_score=8, initial_bubble="intake")
    # patient_3 = Agent(id=3, initial_depression_score=9, initial_bubble="diagnosis")


    # Initialize the patients inside the system
    patient_factory = AgentFactory(50)
    patients = patient_factory.build()
    for patient in patients:
        env.add_agent(patient)

    # let's manually schedule some events
    # env.schedule_event(MoveAgentEvent(name="moving patient 1", time=0, agent_id=1, from_bubble="intake", to_bubble="diagnosis"))
    # env.schedule_event(MoveAgentEvent(name="moving patient 2", time=1, agent_id=2, from_bubble="intake", to_bubble="diagnosis"))
    # env.schedule_event(MoveAgentEvent(name="moving patient 3", time=3, agent_id=3, from_bubble="diagnosis", to_bubble="medical_treatment"))

    env.run(20, verbose=True)

    return env.data
