import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.client import Client
import pdb
from actions.bot_action_generator import BotActionGenerator
from builders.unit_builder import *
from actions.action_manager import *
from units.unit_classifier import UnitClassifier
from utils.file_wrapper import FileWrapper
from builders.dependencies import *
from units.zergling import Zergling
from units.squad import Squad


class ZergBot(sc2.BotAI):
    def __init__(self, id):
        self.id = id
        self.drone_counter = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = False
        self.queeen_started = False
        self.mboost_started = False
        self.action_generator = None
        self.evolution_chamber_started = False
        self.zergling_weapon_1_started = False
        self.lair_started = False
        self.hydralisk_chamber_started = False
        self.curr_unit_names = set()
        self.curr_units = set()
        self.wrapped_zergling = []
        self.squads = []
        self.hatcheries = []

    async def on_step(self, iteration):
        if iteration == 0:
            self.action_generator = BotActionGenerator.build(self)
            await self.chat_send("(glhf)")
        for _i in range(3):
            self.squads.append(Squad(self))

        
        # print("#######")
        # print("Squads:")
        # l = []
        for squad in self.squads:
            for unit in squad.wrapped_units:
                # print(unit)
                # print(self.curr_units)
                if not unit.unit in self.curr_units:
                    # l.append(unit)
                    squad.remove(unit)
                # else:
        # print(l)

        new_units = set(self.units()) - self.curr_units
        for unit in new_units:
            UnitClassifier.classify(unit, self)
        
        self.curr_units = set(self.units())
        curr_unit_names = set(map(lambda x: x.name, self.units))
        new_names = curr_unit_names - self.curr_unit_names
        for key in BUILDING_DEPENDENCIES.keys():
            unit = BUILDING_DEPENDENCIES[key]
            if unit and unit[0] in new_names:
                BUILDING_DEPENDENCIES[key] = []
        for key in UNIT_DEPENDENCIES.keys():
            if unit and unit[0] in new_names:
                UNIT_DEPENDENCIES[key] = []

        # ActionManager.inject_larva(self)
        for squad in self.squads:
            for func in squad.action_generator.get_actions():
                await func(self)
        for func in self.action_generator.get_actions():
            await func(self)
        self.action_generator.rebalance_weights()

    
    def on_end(self, game_result):
        if game_result == game_result.Victory:
            FileWrapper.write(f"./weights{self.id}.csv", self.action_generator.weights)
    
    def find_empty_hatchery(self):
        for hatchery in self.hatcheries:
            if hatchery.queen == None:
                return hatchery