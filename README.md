# Project Atlas: Modeling MDD Treatment Pathways

---

## Description
This project is a simulation of a healthcare system where patients move through different stages of treatment. The simulation models patients as agents who navigate through various treatment points (bubbles) and undergo events that affect their health status

## Features

* Agent-Based Modelling: Patients are simulated as individual agents with unique characteristics
* Discrete-Event Simulation: Key events in the healthcare pathway are simulated at specific times
* Treatment Pathway: Patients moe through different stages of treatment, represented by bubbles
* Data Collection: The simulation collects data on patient flow, bubble occupancy and waiting times.

## Structure

* `agent.py` defines the Agent class, representing the patients
* `bubble.py` contains the Bubble class, representing the treatment stages
* `event.py` defines the Event class
* `environment.py` defines the Core of the simulation environment, which manages the different Agents, Events and Bubbles

Under examples, you can find the simulation method in action. 