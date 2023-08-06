import csv
import statistics

class Utils:

    def __init__(self, rules):
        self.rules = rules

    def calculate_fitness(self, support, confidence):
        return (support + confidence) / 2

    def rules_to_csv(self, filename):
        r"""Store rules to CSV file."""
        with open(filename, 'w',) as csvfile:
            writer = csv.writer(csvfile)
            # header of our csv file
            writer.writerow(['Antecedent', 'Consequent', 'Fitness', 'Support', 'Confidence'])
            for rule in self.rules:
                # calculate fitness (for comparison purposes)
                fitness = self.calculate_fitness(rule.support, rule.confidence)

                writer.writerow(
                    [rule.antecedent, rule.consequent, fitness, rule.support, rule.confidence])

    def generate_statistics(self):
        r"""Generate statistics for experimental purposes"""
        fitness = 0.0
        support = 0.0
        confidence = 0.0
        for rule in self.rules:
            fitness += self.calculate_fitness(rule.support, rule.confidence)
            support += rule.support
            confidence += rule.confidence

        print("Total rules: ", len(self.rules))
        print("Average fitness: ", fitness / len(self.rules))
        print("Average support: ", support / len(self.rules))
        print("Average confidence: ", confidence / len(self.rules))

    def generate_stats_report(self, num_rules):
        fitness = []
        support = []
        confidence = []

        for i in range(num_rules):
            fitness.append(self.calculate_fitness(self.rules[i].support, self.rules[i].confidence))
            support.append(self.rules[i].support)
            confidence.append(self.rules[i].confidence)

        print ("-----------------------------------")
        print(f"Fitness:\n"
                f"Max: {round(max(fitness), 3)}\n"
                f"Min: {round(min(fitness), 3)}\n"
                f"Mean: {round(statistics.mean(fitness), 3)}\n"
                f"Median: {round(statistics.median(fitness), 3)}\n"
                f"Std: {round(statistics.stdev(fitness), 3)}\n")
        print ("-----------------------------------")
