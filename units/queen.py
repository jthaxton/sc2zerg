from sc2.constants import *
class Queen:
  def __init__(self, unit, hatchery, bot):
    self.unit = unit
    self.hatchery = hatchery
    self.bot = bot

  async def inject_larva(self):
    abilities = await self.bot.get_available_abilities(self.unit)
    if AbilityId.EFFECT_INJECTLARVA in abilities:
      await self.bot.do(self.unit(EFFECT_INJECTLARVA, self.hatchery))