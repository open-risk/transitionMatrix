# encoding: utf-8

# (c) 2017 Open Risk, all rights reserved
#
# TransitionMatrix is licensed under the Apache 2.0 license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

# lib to create synthetic state transition datasets

import numpy as np
import pandas as pd
from scipy import stats as stats


def exponential_transitions(statespace, n, sample, rate):
    """
    Generate continuous time events from exponential distribution and uniform sampling from state space
    :type statespace: The state space to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int sample: The number of events to simulate
    :param float rate: The event rate
    :return: transition events
    :rtype: pandas dataframe
    :raises TODO

    NOTES: May generate successive events in the same state
    """
    states = statespace.get_states()
    data = []
    for i in range(n):
        # calculate number of migration events per entity
        t = stats.expon.rvs(scale=rate, size=sample)
        # build up the event timestamps
        t = t.cumsum()
        # select random state per entity
        s = np.random.choice(states, sample)
        for e in range(sample):
            data.append((i, t[e], s[e]))
    return pd.DataFrame(data, columns=['ID', 'Time', 'State'])


def markov_chain(statespace, transitionmatrix, n, timesteps):
    """
    Generate discrete events from a markov chain matrix
    :type statespace: The state space to use for the simulation
    :type transitionmatrix: The transitionMatrix to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int timesteps: The number of timesteps to simulate (inlcuding initial state)
    :param float rate: The event rate
    :return: the message id
    :rtype: pandas dataframe
    :raises TODO
    """
    states = statespace.get_states()
    matrix = transitionmatrix
    data = []
    # for all entities
    for i in range(n):
        # calculate initial state
        initial_state = np.random.choice(len(states))
        k = 0
        data.append((i, k, states[initial_state]))
        p = matrix[initial_state]
        for k in range(1, timesteps):
            # we sample the state index, not the state label
            state = np.random.choice(len(states), p=p)
            p = matrix[state]
            data.append((i, k, states[state]))
    return pd.DataFrame(data, columns=['ID', 'Timestep', 'State'])
