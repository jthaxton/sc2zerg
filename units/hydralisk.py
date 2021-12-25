from sc2.constants import *
import random

class Hydralisk:
  def __init__(self, unit, bot):
    self.unit = unit
    self.bot = bot
    self.available_upgrades = []
    self.upgrade_dependencies = {
      ZERGMISSILEWEAPONSLEVEL1: [],
      ZERGMISSILEWEAPONSLEVEL2: [ZERGMISSILEWEAPONSLEVEL1],
      ZERGMISSILEWEAPONSLEVEL3: [ZERGMISSILEWEAPONSLEVEL2],
      ZERGGROUNDARMORSLEVEL1: [],
      ZERGGROUNDARMORSLEVEL2: [ZERGGROUNDARMORSLEVEL1],
      ZERGGROUNDARMORSLEVEL3: [ZERGGROUNDARMORSLEVEL2]
    }

  @staticmethod
  def build(unit, bot):
    hydralisk = Hydralisk(unit, bot)
    hydralisk.setup_available_upgrades()
    return hydralisk

  def setup_available_upgrades(self):
    for key in RESEARCH_DEPENDENCIES.keys():
      if not self.dependencies_remaining(key):
        self.available_upgrades.append(key)

  def dependencies_remaining(self, upgrade):
    ground = set([ZERGMELEEWEAPONSLEVEL1, ZERGMELEEWEAPONSLEVEL2, ZERGMELEEWEAPONSLEVEL3])
    return RESEARCH_DEPENDENCIES[upgrade] == [] and upgrade not in ground and self.upgrade_dependencies[upgrade] == []
  
  def upgrade_random(self):
    idx = random.randint(0,len(self.available_upgrades) - 1)
    upgrade = self.available_upgrades[idx]
    if not self.dependencies_remaining(upgrade):
      self.upgrade(upgrade)

  def upgrade(self, upgrade):
    if self.bot.can_afford(upgrade):
      self.unit.research(upgrade)
      self.filter_dependencies(upgrade)
      self.setup_available_upgrades()
      return True
  
  def filter_dependencies(self, upgrade):
    self.available_upgrades.remove(upgrade)

    for key in self.upgrade_dependencies.keys():
      if self.upgrade_dependencies[key] == []:
        self.upgrade_dependencies = None
      elif self.upgrade_dependencies[key] == [upgrade]:
        self.upgrade_dependencies[key] = []
  
  async def attack(self):
    target = self.bot.known_enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
    if self.unit.idle:
      await self.bot.do(self.unit.attack(target))
  
  async def attack_target(self, target):
    if self.unit.idle:
      await self.bot.do(self.unit.attack(target))