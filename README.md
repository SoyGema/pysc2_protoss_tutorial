## pysc2_protoss_tutorial

 Protoss Agent for pysc2 new release
```console
my-computer:~ me$ python -m pysc2.bin.agent --map Simple96 --agent_race protoss
```

```console
my-computer:~ me$ python -m pysc2.bin.agent --map Simple96 --agent pysc2.agents.custom_agent.SimpleAgent --agent_race protoss
```

## Debug method to check sc2 areas 
Debug values for print in an image sc2 areas
:param area : the array of tuples with positions
:param filename: the filename for the png value


#### Example of method documentation 

```python
_POWER = features.SCREEN_FEATURES.power.index
obs.observation.feature_screen[_POWER].nonzero()
```
Inside of Environment>Actions and Observations>Observation>Screen>Power

Returns --> array of tuples of power area perimeter from Protoss once it is built . 
.nonzero() is added due to show when the area is built 

#### Using Debug print method documentation

Will print the area of the called method 

```python
POWER_AREA = obs.observation.feature_screen[_POWER].nonzero()
print_area(POWER_AREA)
```
