

from HypoModPy.hypodat import pdata



class AgentDat():
    def __init__(self, storesize):
        self.storesize = storesize

        # initialise arrays for recording model variables (or any model values)
        self.energy = pdata(self.storesize + 1)
        self.appetite = pdata(self.storesize + 1)
        self.glyco = pdata(self.storesize + 1)
        self.insulin = pdata(self.storesize + 1)
        self.chamber = pdata(self.storesize + 1)
        self.gut = pdata(self.storesize + 1)
        self.feed = pdata(self.storesize + 1)
        self.food = pdata(self.storesize + 1)
        self.reward = pdata(self.storesize + 1)
        self.reward_def = pdata(self.storesize + 1)
        self.fullness = pdata(self.storesize + 1)
        self.ghrelin = pdata(self.storesize + 1)
        self.energyLong = pdata(self.storesize + 1)
        self.rewardLong = pdata(self.storesize + 1)
        self.reward_oral = pdata(self.storesize + 1)
        self.reward_gut = pdata(self.storesize + 1)
        self.reward_new = pdata(self.storesize + 1)
        self.food1 = pdata(self.storesize + 1)
        self.food2 = pdata(self.storesize + 1)
        self.gut1 = pdata(self.storesize + 1)
        self.gut2 = pdata(self.storesize + 1)
        self.taste1 = pdata(self.storesize + 1)
        self.taste2 = pdata(self.storesize + 1)
    


class FoodDat():
    def __init__(self, storesize):
        self.storesize = storesize

        # parameters
        self.amount = 0
        self.step = 0
        self.interval = 0
        self.density = 0
        self.reward = 0
        self.taste = 0
        self.cost = 0
        self.basereward = 0
        self.desens = 0
        self.gut = 0
        self.start = 0
        self.stop = 0

        # recording arrays
        self.consumed = pdata(self.storesize + 1)

    def GetReward(self):
        return self.reward


class FoodChoice():
    def __init__(self):
        self.reward = 0
        self.type = 0
        self.prob = 0


class FoodGut():
    def __init__(self):
        self.reward = 0
        self.type = 0
        self.amount = 0
        self.density = 0
        self.proportion = 0