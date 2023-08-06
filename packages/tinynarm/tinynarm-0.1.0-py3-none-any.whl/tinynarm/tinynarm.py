from itertools import permutations, combinations
from niaarm import Dataset, Feature, Rule
from tinynarm.item import Item

class TinyNarm:
    r"""Main class for tinyNARM approach.

   Args:
       dataset (csv file): Dataset stored in csv file.
       num_intervals (int): Number which defines how many intervals we create for numerical features.
   """

    def __init__(self, dataset):
        # load dataset from csv
        self.data = Dataset(dataset)
        self.num_features = len(self.data.features)

        self.feat = []
        self.rules = []

    def prepare(self):
        for feature in self.data.features:
            intervals = feature.categories
            occurences = [0] * len(feature.categories)

            self.feat.append(
                Item(
                    feature.name,
                    feature.dtype,
                    intervals,
                    occurences))

    # create item/attribute map
    def calculate_frequencies(self):
        r"""Count the occurences"""
        item_map = []
        transactions = self.data.transactions.to_numpy()
        for transaction in transactions:
            for i in range(len(transaction)):
                for j in range(len(self.feat[i].intervals)):
                    if transaction[i] == self.feat[i].intervals[j]:
                        self.feat[i].occurences[j] += 1

    def ant_con(self, combination, cut):
        ant = combination[:cut]
        ant1 = []
        for i in range(len(ant)):
            ant1.append(ant[i])
        con = combination[cut:]
        con1 = []
        for i in range(len(con)):
            con1.append(con[i])

        return ant1, con1

    def create_rules(self):
        r"""Create new association rules."""

        self.prepare()
        self.calculate_frequencies()

        items = []
        for item in self.feat:
            max_index = item.occurences.index(max(item.occurences))
            items.append(Feature(item.name,item.dtype,categories=[item.intervals[max_index]]))

        # create rules for the combination of 3...,num_features
        for i in range(2, self.num_features):
            comb = combinations(items, i)
            if i == 2:
                for j in list(comb):
                    rule = Rule([j[0]], [j[1]],
                                transactions=self.data.transactions)
                    if rule.support > 0.0:
                        self.rules.append(rule)
            else:
                for j in list(comb):
                    for cut in range(1, i - 1):
                        ant, con = self.ant_con(j, cut)
                        rule = Rule(
                            ant, con, transactions=self.data.transactions)
                        if rule.support > 0.0:
                            self.rules.append(rule)

        self.rules.sort(key=lambda x: x.support, reverse=True)

    def generate_report(self):
        for f in self.feat:
            print(f"Feat INFO:\n"
                  f"Name: {f.name}\n"
                  f"Bins: {f.intervals}")
