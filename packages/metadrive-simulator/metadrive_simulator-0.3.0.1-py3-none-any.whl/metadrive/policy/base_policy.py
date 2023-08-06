import logging
import numpy as np

import gym

from metadrive.base_class.configurable import Configurable
from metadrive.base_class.randomizable import Randomizable
from metadrive.engine.engine_utils import get_engine


class BasePolicy(Randomizable, Configurable):
    def __init__(self, control_object, random_seed=None, config=None):
        Randomizable.__init__(self, random_seed)
        Configurable.__init__(self, config)
        # self.engine = get_engine()
        self.control_object = control_object
        self.action_info = dict()

    def act(self, *args, **kwargs):
        """
        Return action [], policy implement information (dict) can be written in self.action_info, which will be
        retrieved automatically
        """
        pass

    def get_action_info(self):
        """
        Get current action info for env.step() retrieve
        """
        return self.action_info

    def reset(self):
        pass

    def destroy(self):
        logging.debug("{} is released".format(self.__class__.__name__))
        super(BasePolicy, self).destroy()
        self.control_object = None
        # self.engine = None

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.name

    @property
    def engine(self):
        return get_engine()

    @classmethod
    def get_input_space(cls):
        """
        It defines the input space of this class of policy
        """
        logging.warning(
            "No input space set for this policy! If you are querying an action space, "
            "the agent policy may not take any external input from env.step() and thus the env.action_space is None"
        )
        return gym.spaces.Box(-1.0, 1.0, shape=(2, ), dtype=np.float32)
