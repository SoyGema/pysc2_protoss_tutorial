## Kudos StevenBrown 
"""A base agent to write custom scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.lib import actions
from pysc2.agents import base_agent
from pysc2.lib import features 


# Functions
_BUILD_PYLON = actions.Function.Build_Pylon_screen.id
_NOOP = actions.Function.no_op.id
_SELECT_POINT = actions.Function.select_point.id
_MOVE_CAMERA = actions.Function.move_camera.id
_BUILD_GATEWAY = actions.Function.Build_Gateway_screen.id

# Features
_PLAYER_RELATIVE = features.ScreenFeatures.player_relative.index
_UNIT_TYPE = features.ScreenFeatures.unit_type.index

#Unit IDs
_PROTOSS_NEXUS = 59
_PROTOSS_PROBE = 84
_PROTOSS_PYLON = 60
_PROTOSS_GATEWAY = 62

#Parameters
_PLAYER_SELF = 1
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]

class BaseAgent(object):
  base_top_left = None
  pylon_built = False
  probe_selected = False
  gateway_built = False
  gateway_selected = False
  gateway_rallied = False 
  
  def transformLocation(self, x, x_distance, y, y_distance):
      if not self.base_top_left:
          return [x - x_distance, y - y_distance]
        
      return [x + x_distance, y + y_distance]  
  
  
  def __init__(self):
    self.reward = 0
    self.episodes = 0
    self.steps = 0
    self.obs_spec = None
    self.action_spec = None

  def setup(self, obs_spec, action_spec):
    self.obs_spec = obs_spec
    self.action_spec = action_spec

  def reset(self):
    self.episodes += 1

  def step(self, obs):
      super(SimpleAgent, self).step(obs)
        
      time.sleep(0.5)
        
      if self.base_top_left is None:
          player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
          self.base_top_left = player_y.mean() <= 47
            
      if not self.supply_depot_built:
          if not self.scv_selected:
              unit_type = obs.observation["screen"][_UNIT_TYPE]
              unit_y, unit_x = (unit_type == _PROTOSS_PROBE).nonzero()
                
              target = [unit_x[0], unit_y[0]]
                
              self.probe_selected = True
                
              return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
          elif _BUILD_PYLON in obs.observation["available_actions"]:
              unit_type = obs.observation["screen"][_UNIT_TYPE]
              unit_y, unit_x = (unit_type == _PROTOSS_NEXUS).nonzero()
                
              target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                
              self.pylon_built = True
                
              return actions.FunctionCall(_BUILD_PYLON, [_NOT_QUEUED, target])
      elif not self.gateway_built and _BUILD_GATEWAY in obs.observation["available_actions"]:
          unit_type = obs.observation["screen"][_UNIT_TYPE]
          unit_y, unit_x = (unit_type == _PROTOSS_NEXUS).nonzero()
            
          target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
            
          self.pylon_built = True
            
          return actions.FunctionCall(_BUILD_GATEWAY, [_NOT_QUEUED, target])

      return actions.FunctionCall(_NOOP, [])
