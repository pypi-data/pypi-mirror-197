from niaarm import NiaARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType

class Compare:
    def __init__(self, dataset, output):
        self.dataset = dataset
        self.output = output

    def compare_niaarm(self, np, evaluations):
        data = Dataset(self.dataset)

        self.problem = NiaARM(data.dimension, data.features, data.transactions, metrics=('support', 'confidence'), logging=True)

        task = Task(problem=self.problem, max_evals=evaluations, optimization_type=OptimizationType.MAXIMIZATION)

        algo = DifferentialEvolution(population_size=np, differential_weight=0.5, crossover_probability=0.9)

        best = algo.run(task=task)

        self.problem.rules.sort()

        self.problem.rules.to_csv(self.output)

    def get_rules(self):
        return self.problem.rules
