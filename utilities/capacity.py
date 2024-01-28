
class Capacity:

    def __init__(self, capacities_distribution):
        self.capacities_distribution = capacities_distribution
        self.capacities = self.assign_updated_capacity()

    def __repr__(self):
        return f"Capacities: {self.capacities}"

    def retrieve_capacity(self, slug=""):
        # get the capacity for a specific "slug"
        if self.capacities is None:
            raise ValueError(f"Capacities not assigned.")

        if self.capacities[slug]:
            return self.capacities[slug]
        else:
            raise ValueError(f"ValueError: Unable to retrieve capacity for {slug}; slug not found")

    def assign_updated_capacity(self):
        print("Assigning Capacities")

        # Validate that "total" is present in capacities_distribution
        if "total" not in self.capacities_distribution:
            raise ValueError("No total capacity provided.")

        # Validate that "total" is a number
        if not isinstance(self.capacities_distribution["total"], (int, float)):
            raise ValueError("Total capacity must be a number.")

        # # Ensure the sum of all proportions equal to 1
        # proportions_sum = sum(val for key, val in self.capacities_distribution.items()
        #                       if key != "total")
        # if proportions_sum != 1:
        #     raise ValueError(f"Capacities' proportions must add up to 1. => {proportions_sum}")

        total_capacity = self.capacities_distribution["total"]
        capacities = {key: round(val * total_capacity, 0)
                      for key, val in self.capacities_distribution.items()
                      if key != "total"}

        # Validate that the individual capacities add up to the total
        if sum(capacities.values()) != total_capacity:
            raise ValueError(f"Capacities don't match the total.=> {sum(capacities.values())}")

        return capacities

