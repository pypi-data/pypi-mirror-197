"""
---------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------
"""

import abc
import numbers
import typing

import gym
import numpy as np

from corl.libraries.plugin_library import PluginLibrary
from corl.libraries.property import BoxProp, DiscreteProp, MultiBinary
from corl.simulators.base_parts import BaseController, BasePlatformPartValidator, BaseSensor


class MemoryStoreValidator(BasePlatformPartValidator):
    """Validator for memory store"""

    default_value: typing.Optional[typing.Any]


class MemoryStore(BaseController, BaseSensor, abc.ABC):
    """Platform part for storing data in the env

    Parameters
    ----------
    """

    def __init__(self, parent_platform, config, property_class) -> None:
        self.config: MemoryStoreValidator
        super().__init__(parent_platform, config, property_class)
        self._properties_config = str(config["properties"])

        space = self._properties.create_space()
        if self.config.default_value is not None:
            if isinstance(space, gym.spaces.Box):
                if not isinstance(self.config.default_value, typing.Sequence):
                    self.config.default_value = [self.config.default_value]
                self._data = np.array(list(self.config.default_value), dtype=space.dtype)
            elif isinstance(space, gym.spaces.Discrete):
                self._data = self.config.default_value
            elif isinstance(space, gym.spaces.MultiBinary):
                self._data = np.array(list(self.config.default_value), dtype=space.dtype)
            else:
                raise RuntimeError("Invalid space: unable to default initialize")
        else:

            if isinstance(space, gym.spaces.Box):
                self._data = (space.low + space.high) / 2.0
            elif isinstance(space, gym.spaces.Discrete):
                self._data = 0  # type: ignore
            elif isinstance(space, gym.spaces.MultiDiscrete):
                self._data = space.sample() * 0
            else:
                raise RuntimeError("Invalid space: unable to default initialize")

        self._last_measurement = self.get_applied_control()  # type: ignore

        self.set_invalid()

    @property
    def get_validator(self) -> typing.Type[BasePlatformPartValidator]:
        """
        return the validator that will be used on the configuration
        of this part
        """
        return MemoryStoreValidator

    def apply_control(self, control: np.ndarray) -> None:
        """
        The generic method to apply the control for this controller.

        Parameters
        ----------
        control
            The control to be executed by the controller
        """
        self.set_valid()
        self._data = control

    def get_applied_control(self) -> typing.Union[np.ndarray, numbers.Number]:
        """
        Get the previously applied control that was given to the apply_control function
        Returns
        -------
        previously applied control that was given to the apply_control function
        """
        return self._data

    def _calculate_measurement(self, state) -> typing.Union[np.ndarray, typing.Tuple, typing.Dict]:
        if isinstance(self.control_properties, (BoxProp, DiscreteProp)):  # pylint: disable=no-else-return
            return typing.cast(np.ndarray, self.get_applied_control())
        elif isinstance(self.control_properties, (DiscreteProp)):
            return np.asarray([self.get_applied_control()], dtype=np.int32)

        raise TypeError(
            "Only supports {BoxProp.__name__} and {DiscreteProp.__name__} -- got a type of {type(self.config.properties).__name__}"
        )

    def calculate_and_cache_measurement(self, state):
        """
        Calculates the measurement and caches the result in the _last_measurement variable

        Parameters
        ----------
        state: BaseSimulatorState
            The current state of the environment used to obtain the measurement
        """
        super().calculate_and_cache_measurement(state)
        if isinstance(self.control_properties, (DiscreteProp)) and isinstance(self._last_measurement, int):
            self._last_measurement = np.asarray([self._last_measurement], dtype=np.int32)


PluginLibrary.AddClassToGroup(MemoryStore.embed_properties(BoxProp), "BoxPropMemoryStore", {})
PluginLibrary.AddClassToGroup(MemoryStore.embed_properties(MultiBinary), "MultiBinaryPropStore", {})
PluginLibrary.AddClassToGroup(MemoryStore.embed_properties(DiscreteProp), "DiscretePropStore", {})
