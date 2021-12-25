import sc2
from sc2.constants import *
from typing import Any
import pdb

class UnitBuilder(sc2.BotAI):

  @staticmethod
  async def build_zergling(bot: Any):
    if bot.units(SPAWNINGPOOL).ready.exists:
      larvae = bot.units(LARVA)
      if larvae.exists and bot.can_afford(ZERGLING):
          await bot.do(larvae.random.train(ZERGLING))

  @staticmethod
  async def build_worker(bot: Any):
    larvae = bot.units(LARVA)
    if bot.drone_counter < 3:
      if bot.can_afford(DRONE):
          bot.drone_counter += 1
          await bot.do(larvae.random.train(DRONE))

  @staticmethod
  async def build_queen(bot: Any):
    hatchery = UnitBuilder.find_empty_hatchery(bot)
    if hatchery: 
      hatchery = hatchery.unit
    else:
      print("QUEEN NOT BUILT")
      return
    if not bot.queeen_started and bot.units(SPAWNINGPOOL).ready.exists:
      if bot.can_afford(QUEEN):
          r = await bot.do(hatchery.train(QUEEN))
          if not r:
              bot.queeen_started = True

  @staticmethod
  async def build_overlord(bot: Any):
    larvae = bot.units(LARVA)
    if bot.supply_left < 2:
      if bot.can_afford(OVERLORD) and larvae.exists:
          await bot.do(larvae.random.train(OVERLORD))
  
  @staticmethod
  async def build_spawning_pool(bot: Any):
    hatchery = bot.hatcheries[0].unit
    if not bot.spawning_pool_started:
      if bot.can_afford(SPAWNINGPOOL) and bot.workers.exists:
        for d in range(4, 15):
          pos = hatchery.position.to2.towards(bot.game_info.map_center, d)
          if await bot.can_place(SPAWNINGPOOL, pos):
            drone = bot.workers.closest_to(pos)
            err = await bot.do(drone.build(SPAWNINGPOOL, pos))
            if not err:
              bot.spawning_pool_started = True
              break

  @staticmethod
  async def build_extractor(bot: Any):
    if not bot.extractor_started:
      if bot.can_afford(EXTRACTOR) and bot.workers.exists:
        drone = bot.workers.random
        target = bot.state.vespene_geyser.closest_to(drone.position)
        err = await bot.do(drone.build(EXTRACTOR, target))
        if not err:
          bot.extractor_started = True
  
  @staticmethod
  async def expand_base(bot: Any):
    hatchery = bot.units(HATCHERY).ready
    if hatchery:
      hatchery = hatchery.first
    else:
      print("CANNOT EXPAND BASE")
      return False
    if bot.minerals > 500 and bot.workers.exists:
      for d in range(4, 15):
        pos = hatchery.position.to2.towards(bot.game_info.map_center, d)
        if await bot.can_place(HATCHERY, pos):
          await bot.do(bot.workers.random.build(HATCHERY, pos))
          break
  
  @staticmethod
  async def research_metabolic_boost(bot: Any):
    if bot.vespene >= 100:
      sp = bot.units(SPAWNINGPOOL).ready
      if sp.exists and bot.minerals >= 100 and not bot.mboost_started:
        await bot.do(sp.first(RESEARCH_ZERGLINGMETABOLICBOOST))
        bot.mboost_started = True
  
  @staticmethod
  async def build_evolution_chamber(bot: Any):
    hatchery = bot.units(HATCHERY).ready
    if hatchery:
      hatchery = hatchery.first
    else:
      print("CAN NOT BUILD EVOLUTION CHAMBER")
      return False
    if not bot.evolution_chamber_started:
      if bot.can_afford(EVOLUTIONCHAMBER) and bot.workers.exists:
        for d in range(4, 15):
          pos = hatchery.position.to2.towards(bot.game_info.map_center, d)
          if await bot.can_place(EVOLUTIONCHAMBER, pos):
            drone = bot.workers.closest_to(pos)
            err = await bot.do(drone.build(EVOLUTIONCHAMBER, pos))
            if not err:
              bot.evolution_chamber_started = True
              break
  
  @staticmethod
  async def research_zergling_weapon_1(bot: Any):
    evolution_chamber = bot.units(EVOLUTIONCHAMBER).ready
    if bot.vespene >= 100 and bot.minerals >= 100 and evolution_chamber.exists and not bot.zergling_weapon_1_started:
        err = await bot.do(evolution_chamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL1))
        if not err:
          bot.zergling_weapon_1_started = True
  
  @staticmethod
  async def convert_hatchery_to_lair(bot: Any):
    hatchery = bot.units(HATCHERY).ready
    if hatchery:
      hatchery = hatchery.first
    else:
      print("CAN NOT BUILD lair")
      return False
    if hatchery and bot.vespene >= 100 and bot.minerals >= 150:
      if not bot.lair_started:
        err = await bot.do(hatchery(UPGRADETOLAIR_LAIR))
        if not err:
          bot.lair_started = True
  
  @staticmethod
  async def build_hydralisk_den(bot: Any):
    hatchery = bot.units(HATCHERY).ready
    if hatchery:
      hatchery = hatchery.first
    else:
      print("COULD NOT BUILD HYDRALISK DEN")
      return False
    if not bot.hydralisk_chamber_started:
      if bot.can_afford(HYDRALISKDEN) and bot.workers.exists:
        for d in range(4, 15):
          pos = hatchery.position.to2.towards(bot.game_info.map_center, d)
          if await bot.can_place(HYDRALISKDEN, pos):
            drone = bot.workers.closest_to(pos)
            err = await bot.do(drone.build(HYDRALISKDEN, pos))
            if not err:
              bot.hydralisk_chamber_started = True
              break

  @staticmethod
  async def build_hydralisk(bot: Any):
    if bot.units(HYDRALISKDEN).ready.exists:
      larvae = bot.units(LARVA)
      if larvae.exists and bot.can_afford(HYDRALISK):
          await bot.do(larvae.random.train(HYDRALISK))

  @staticmethod
  def find_empty_hatchery(bot):
    for hatchery in bot.hatcheries:
        if hatchery.queen == None:
            return hatchery