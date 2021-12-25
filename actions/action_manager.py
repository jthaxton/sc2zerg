import sc2
from sc2.constants import *
from typing import Any, List
from sc2.position import Point2
from sc2.unit import Unit

class ActionManager(sc2.BotAI):

  @staticmethod
  async def move_workers_from_gas(bot: Any):
    if bot.vespene >= 100:
      if not bot.moved_workers_from_gas:
        bot.moved_workers_from_gas = True
        for drone in bot.workers:
          m = bot.state.mineral_field.closer_than(10, drone.position)
          if m: await bot.do(drone.gather(m.random, queue=True))
  
  @staticmethod
  async def move_workers_to_gas(bot: Any):
    if bot.units(EXTRACTOR).ready.exists and not bot.moved_workers_to_gas:
      bot.moved_workers_to_gas = True
      extractor = bot.units(EXTRACTOR).first
      for drone in bot.workers.random_group_of(3):
          await bot.do(drone.gather(extractor))

  @staticmethod
  async def units_attack_location(bot: Any):
    target = bot.known_enemy_structures.random_or(bot.enemy_start_locations[0]).position
    units = bot.units(ZERGLING)
    for unit in units.idle:
      await bot.do(unit.attack(target))

  @staticmethod
  async def inject_larva(bot: Any):
    hatchery = bot.units(HATCHERY).ready.first
    for queen in bot.units(QUEEN).idle:
      abilities = await bot.get_available_abilities(queen)
      if AbilityId.EFFECT_INJECTLARVA in abilities:
        await bot.do(queen(EFFECT_INJECTLARVA, hatchery))