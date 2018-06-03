## Kudos to StevenBrown
# This is a scripted bot experiment to try the new release of pysc2
# The original tutorial by Steven Brown with Terran can be found here
# https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c

# The bot has been built with Protoss race
## At this point this scripted bot is able to select a probe and build a pylon

"""A base agent to write custom scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.lib import actions
from pysc2.agents import base_agent
from pysc2.lib import features
import time
import numpy

# Functions
_BUILD_PYLON = actions.FUNCTIONS.Build_Pylon_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_MOVE_CAMERA = actions.FUNCTIONS.move_camera.id
_BUILD_GATEWAY = actions.FUNCTIONS.Build_Gateway_screen.id

# Features
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_POWER = features.SCREEN_FEATURES.power.index
_PLAYER_SELF = 1

# Unit IDs
_PROTOSS_NEXUS = 59
_PROTOSS_PROBE = 84
_PROTOSS_PYLON = 60
_PROTOSS_GATEWAY = 62

# Parameters
_PLAYER_SELF = 1
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]


class SimpleAgent(base_agent.BaseAgent):
    base_top_left = None
    pylon_built = False
    probe_selected = False
    gateway_built = False
    gateway_selected = False
    gateway_rallied = False

    def _xy_locs(mask):
        """Mask should be a set of bools from comparison with a feature layer."""
        y, x = mask.nonzero()
        return list(zip(x, y))

    def step(self, obs):
        super(SimpleAgent, self).step(obs)

        def _xy_locs(mask):
            """Mask should be a set of bools from comparison with a feature layer."""
            y, x = mask.nonzero()
            return list(zip(x, y))


        if self.base_top_left is None:
            PLAYER_RELATIVE = obs.observation.feature_screen.player_relative
            player_ = _xy_locs(PLAYER_RELATIVE == _PLAYER_SELF)
            self.base_top_left = numpy.mean(player_, axis=0).round() <= 31

        if not self.pylon_built:
            if not self.probe_selected:
                unit_type = obs.observation.feature_screen[_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _PROTOSS_PROBE).nonzero()
                target = [unit_x[0], unit_y[0]]

                self.probe_selected = True

                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

            elif _BUILD_PYLON in obs.observation["available_actions"]:
                unit_type = obs.observation.feature_screen[_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _PROTOSS_NEXUS).nonzero()

                if self.base_top_left[0] == True:
                    target = [unit_x[0] + 5, unit_y[0] + 5]
                else:
                    target = [unit_x[0] + 10, unit_y[0] - 5]

                self.pylon_built = True

                return actions.FunctionCall(_BUILD_PYLON, [_NOT_QUEUED, target])
        if not self.gateway_built and self.pylon_built and _BUILD_GATEWAY in obs.observation["available_actions"]:
            print('try building gateway')
            area = obs.observation.feature_screen[_POWER].nonzero()
            if len(area[0]) != 0:
                print(area)
                unit_type = obs.observation.feature_screen[_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _PROTOSS_PYLON).nonzero()
                print(unit_x)

                if self.base_top_left[0] == True:
                    print("area is top left")
                    target = [unit_x[0]+12, unit_y[0]]
                else:
                    print("area is bottom right")
                    target = [unit_x[0]+12, unit_y[0]]

                self.gateway_built = True

                return actions.FunctionCall(_BUILD_GATEWAY, [_NOT_QUEUED, target])

        return actions.FunctionCall(_NOOP, [])
