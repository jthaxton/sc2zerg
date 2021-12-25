import random
from actions.squad_action_generator import SquadActionGenerator

class Squad:
  def __init__(self, bot):
    self.wrapped_units = []
    self.bot = bot
    self.action_generator = SquadActionGenerator.build(bot)

  def __add(self, unit_wrapper):
    self.wrapped_units.append(unit_wrapper)
  
  async def __attack(self, target):
    for unit in self.wrapped_units:
      unit.attack_target(target)
  
  async def __upgrade(self):
    for unit in self.wrapped_units:
      unit.upgrade_random()

  def remove(self, unit):
    new_units = []
    for wrapped_unit in self.wrapped_units:
      if wrapped_unit.unit != unit:
        new_units.append(wrapped_unit)
    self.wrapped_units = new_units
  
  @staticmethod
  def assign_random(bot, unit_wrapper):
    idx = random.randint(0,len(bot.squads) - 1)
    bot.squads[idx].__add(unit_wrapper)

  @staticmethod
  async def attack_random(bot):
    idx = random.randint(0,len(bot.squads) - 1)
    target = bot.known_enemy_structures.random_or(bot.enemy_start_locations[0]).position
    await bot.squads[idx].__attack(target)
  
  @staticmethod
  async def upgrade_random(bot):
    idx = random.randint(0,len(bot.squads) - 1)
    await bot.squads[idx].__upgrade()