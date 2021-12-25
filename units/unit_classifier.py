from units.hatchery import Hatchery
from units.hydralisk import Hydralisk
from units.queen import Queen
from units.zergling import Zergling
from units.squad import Squad

class UnitClassifier:
  @staticmethod
  def classify(unit, bot):
    if unit.name == "Zergling":
      zergling = Zergling.build(unit, bot)
      Squad.assign_random(bot, zergling)
    elif unit.name == "Hatchery":
      bot.hatcheries.append(Hatchery(unit))
    elif unit.name == "Queen":
      hatchery = bot.find_empty_hatchery()
      queen = Queen(unit, hatchery, bot)
      hatchery.assign_queen(queen)
    elif unit.name == "Hydralisk":
      hydralisk = Hydralisk(unit, bot)
      Squad.assign_random(bot, hydralisk)