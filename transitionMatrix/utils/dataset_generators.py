# encoding: utf-8

# (c) 2017-2019 Open Risk, all rights reserved
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

# library to create synthetic state transition datasets
#
# TODO Full simulation in continuous time for arbitrary Markov Chain

import numpy as np
import pandas as pd
from scipy import stats as stats


def exponential_transitions(statespace, n, sample, rate, data_format='Compact'):
    """
    Generate continuous time events from exponential distribution and uniform sampling from state space. Suitable
    for testing cohorting algorithms and duration based estimators.

    The data are sorted by entity ID, then by time of occurrence T. The first entry per entity indicates the state up
    to that timepoint. The format is a sequence of triples (ID, Time, State)

    :param statespace: The state space to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int sample: The number of events to simulate
    :param float rate: The event rate
    :return: transition events
    :rtype: pandas dataframe

    .. note:: May generate successive events in the same state

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
    Generate discrete events from a markov chain matrix in Compact data format
    Suitable for testing cohort based estimators

    :type statespace: The state space to use for the simulation
    :type transitionmatrix: The transitionMatrix to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int timesteps: The number of timesteps to simulate (including initial state)
    :return: the message id
    :rtype: pandas dataframe

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


def long_format(statespace, transitionmatrix, n, timesteps):
    """
    Generate continuous events from a markov chain matrix in Long data format
    Suitable for testing duration based estimators

    :type statespace: The state space to use for the simulation
    :type transitionmatrix: The transitionMatrix to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int timesteps: The number of timesteps to simulate (including initial state)
    :return: the message id
    :rtype: pandas dataframe

    .. note: The observation time within timesteps is calculated using a uniform \
    distribution assumption

    """
    states = statespace.get_states()
    matrix = transitionmatrix
    # collect the data in a list of tuples (ID, Time, From, To)
    data = []
    # loop over all entities
    for i in range(n):
        # calculate a random initial entity state
        from_state = np.random.choice(len(states))

        # flag to keep track of migration event
        migrated = False

        # the transition probabilities for the initial state
        p = matrix[from_state]

        # iterate of the required periods
        for k in range(1, timesteps):

            # Draw the next state for this entity
            # NB: we sample the state index, not the state label
            to_state = np.random.choice(len(states), p=p)

            if to_state != from_state:
                migrated = True
                # event time is current timestep minus a uniformly distributed number
                event_time = k - np.random.uniform(low=0.0, high=1.0, size=None)
                data.append((i, event_time, states[from_state], states[to_state]))
                # Calculate next transition probabilities
                p = matrix[to_state]
                # Shift state
                from_state = to_state
        # Create static entry if no migration event took place for this entity
        if not migrated:
            data.append((i, 0, states[from_state], states[from_state]))

    return pd.DataFrame(data, columns=['ID', 'Time', 'From', 'To'])
