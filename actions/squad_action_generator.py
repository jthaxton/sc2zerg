import units.squad
import random

class SquadActionGenerator:
  def __init__(self):
    self.actions = []
    self.weights = [0.5, 0.5]

  @staticmethod
  def build(bot):
    sag = SquadActionGenerator()
    sag.generate_actions(bot)
    return sag

  def generate_actions(self, bot):
    self.actions = [
      lambda _: units.squad.Squad.attack_random(bot),
      lambda _: units.squad.Squad.upgrade_random(bot),
    ]
  
  def get_actions(self):
    rand_int = random.randint(0,len(self.actions) - 1)
    actions = random.choices(self.actions, self.weights, k=rand_int)
    self.rebalance_weights()
    return actions

  def rebalance_weights(self):
    length = len(self.weights) - 1
    i = random.randint(0, length)
    j = random.randint(0, length)
    while i == j:
      j = random.randint(0, length)

    if self.weights[i] <= self.weights[j]:
      to_modify = i
      delta = 1 - self.weights[to_modify] - random.random()
      self.weights[j] -= delta
      self.weights[i] += delta
    else:
      to_modify = j
      delta = 1 - self.weights[to_modify] - random.random()
      self.weights[j] += delta
      self.weights[i] -= delta