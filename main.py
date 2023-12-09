import examples.emergency.main

import matplotlib.pyplot as plt


def plot_bubble_occupancies(data):
    plt.figure(figsize=(10, 6))
    for name, occupancies in data['bubble_occupancies'].items():
        plt.plot(data['time'], occupancies, label=name)
    plt.xlabel('Time')
    plt.ylabel('Occupancy')
    plt.title('Bubble Occupancies Over Time')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    sim_data = examples.emergency.main.emergency_room_sim()
    plot_bubble_occupancies(sim_data)
