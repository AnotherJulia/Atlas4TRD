
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
        # Check if it totals up to 0
        
        if not self.capacities_distribution["total"]:
            raise ValueError("No total capacity filled in.")

        total_capacity = self.capacities_distribution["total"]
        # print(f"Total Capacity: {total_capacity}")
        capacities = {}
        
        sum = 0
        for key, value in self.capacities_distribution.items():
            if key != "total": 
                sum += value
        
        # print(f"Sum: {sum}")

        if sum == 1:
            for key, value in self.capacities_distribution.items():
                if key != "total":
                    capacities[key] = round(value * total_capacity, 0)
        
        else:
            difference = 1 - sum
            # print(f"Difference: {difference}")
            
            for key, value in self.capacities_distribution.items():
                if key != "total":
                    prop = value / total_capacity
                    capacities[key] = round((value + prop*difference) * total_capacity, 0)

        # print(capacities)


        # double check if total capacities match
        sum = 0
        for _, value in capacities.items():
            sum += value
        # print(f"Final capacities: {sum}")

        if sum != total_capacity:
            raise ValueError("Capacities don't match.")


        return capacities

