from typing import Any
from builders.unit_builder import *
from actions.action_manager import *
import random
import pdb

from utils.file_wrapper import FileWrapper

class BotActionGenerator:
  def __init__(self, bot: Any):
    self.weights = []
    self.actions = []

  @staticmethod
  def build(bot):
    bag = BotActionGenerator(bot)
    bag.generate_weighted_actions(bot, bot.id)
    return bag

  def generate_weighted_actions(self, bot: Any, id: int) -> None:
    self.weights =  FileWrapper.read(f"./weights{id}.csv")[0]#10 * [1/10]
    self.actions = [
      lambda _: UnitBuilder.research_metabolic_boost(bot),
      lambda _: ActionManager.move_workers_from_gas(bot),
      lambda _: UnitBuilder.build_overlord(bot),
      lambda _: UnitBuilder.build_zergling(bot),
      lambda _: ActionManager.move_workers_to_gas(bot),
      lambda _: UnitBuilder.expand_base(bot),
      lambda _: UnitBuilder.build_worker(bot),
      lambda _: UnitBuilder.build_extractor(bot),
      lambda _: UnitBuilder.build_spawning_pool(bot),
      lambda _: UnitBuilder.build_queen(bot),
      lambda _: UnitBuilder.build_evolution_chamber(bot),
      lambda _: UnitBuilder.research_zergling_weapon_1(bot),
      lambda _: UnitBuilder.convert_hatchery_to_lair(bot),
      lambda _: UnitBuilder.build_hydralisk_den(bot),
      lambda _: UnitBuilder.build_hydralisk(bot),
      lambda _: ActionManager.units_attack_location(bot)
    ]
  
  def get_actions(self):
    rand_int = random.randint(0,len(self.actions) - 1)
    return random.choices(self.actions, self.weights, k=rand_int)

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
    