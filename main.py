import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
import bots.zerg_bot
from sc2.player import Bot, Computer
import sc2
import bots
import pdb

def main():
  b1 = bots.zerg_bot.ZergBot(1)
  bot_1 = Bot(Race.Zerg, b1)
  
  bot_2 = Bot(Race.Zerg, bots.zerg_bot.ZergBot(2))
  sc2.run_game(sc2.maps.get("AcropolisLE"), [
      bot_1,
      bot_2
      # Computer(Race.Terran, Difficulty.Hard)
  ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
  main()
