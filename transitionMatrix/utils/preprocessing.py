# encoding: utf-8

# (c) 2017-2023 Open Risk, all rights reserved
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

'''
module transitionMatrix.utils - helper classes and functions

'''

from __future__ import print_function, division

import numpy as np
import pandas as pd
import pprint as pp
from transitionMatrix.utils.converters import frame_to_array


def validate_absorbing_state(dataframe, state):
    """ Validate whether a given state is actually absorbing (there should be no transitions to another state)

    :param dataframe: an input data frame
    :param state: the state to validate
    :type state: int

    :return: a list of exceptions
    """

    exceptions = []
    entity_id, event_time, entity_state = frame_to_array(dataframe)
    for i in range(len(entity_id) - 1):
        if entity_id[i + 1] == entity_id[i] and entity_state[i] == state and entity_state[i + 1] != state:
            exceptions.append((entity_id[i], entity_state[i], entity_state[i + 1]))
    return exceptions


def transitions_summary(dataframe):
    """
    Calculate some summary statistics about transitions
    :param dataframe: input dataframe
    :return: dict
    """
    statistics = {}
    try:
        statistics['unique_entities'] = len(list(unique_entities(dataframe)))
    except Exception as e:
        statistics['unique_entities'] = 'Could not parse entities'

    try:
        statistics['unique_states'] = len(list(unique_states(dataframe)))
    except Exception as e:
        statistics['unique_states'] = 'Could not parse states'

    try:
        statistics['unique_timestamps'] = len(list(unique_timestamps(dataframe)))
    except:
        statistics['unique_timestamps'] = 'Could not parse timestamps'

    try:
        statistics['total_timestamps'] = total_timestamps(dataframe)
    except:
        statistics['total_timestamps'] = 'Could not parse timestamps'

    return statistics


def unique_entities(data):
    """
    Identify unique entities in a dataframe

    :param data: dataframe. The 'ID' column is used by default

    :returns: returns a numpy array

    """
    unique_entities = data['ID'].unique()
    return unique_entities


def unique_states(data):
    """
    Identify unique states in a dataframe

    :param data: dataframe. The 'State' column is used by default for Compact formats, 'From' column as fallback for Canonical format

    :returns: returns a numpy array

    """
    try:
        unique_states = data['State'].unique()
    except Exception as e:
        unique_states = data['From'].unique()
    return unique_states


def total_timestamps(data):
    """
    Count total number  of timestamps in a dataframe

    :param data: dataframe. The 'Time' column is used by default

    :returns: returns an integer

    """
    total_timestamps = data['Time'].count()
    return total_timestamps


def unique_timestamps(data):
    """
    Identify unique timestamps in a dataframe

    :param data: dataframe. The 'Time' column is used by default

    :returns: returns a sorted numpy array

    """
    unique_timestamps = sorted(data['Time'].unique())
    return unique_timestamps


def generate_cohort_bounds(data, cohorts):
    """Generate cohort intervals given an input transition dataframe and the desired number of cohorts. The function finds the range of timestamps and divides it equally

    :param data: a pandas dataframe
    :param cohorts:  the number of cohorts
    :type cohorts: int
    :return: cohort_bounds
    :return: dt

    .. warning:: the Time column must be in float format

    """
    # Find the temporal range of observed event times
    t_min = data['Time'].min()
    t_max = data['Time'].max()

    # Divide the temporal range into equal intervals (dt)
    dt = (t_max - t_min) / cohorts
    # Capture the degenerate case that t_max = t_min
    if not dt > 0:
        dt = 1.0
    cohort_bounds = [t_min + dt * i for i in range(0, cohorts + 1)]
    return dt, cohort_bounds


def generate_event_dict(data, dt, cohort_bounds):
    """
    Loop over all events and construct a dictionary in the following format:

    .. code::

        event_dict = {
          (entity_id, cohort interval) : [(time, state), ..., (time, state)]
          (entity_id, cohort interval) : (time, state), ..., (time, state)]
        }

    * Create a unique key as per (entity, interval)
    * Find the interval of each event (the cohort it belongs it)
    * Add (time, state) pairs as variable length list

    This data structure allows applying arbitrary state assignment to each cohort interval

    :param data: a pandas dataframe
    :param dt: the cohort interval
    :param cohort_bounds: the boundaries of the cohort intervals
    :return: dict

    """

    initial_time = cohort_bounds[0]

    event_dict = {}
    for row in data.itertuples():

        entity_id = row.ID
        event_time = row.Time
        entity_state = row.State

        # insert initial state observation events
        # ATTN equality check
        if event_time == initial_time:
            event_key = (entity_id, 0)
            event_dict[event_key] = [(event_time, entity_state)]
        else:
            # Find the interval of the event (the cohort it belongs it)
            c = 0
            for i in range(len(cohort_bounds)):
                if event_time > cohort_bounds[i]:
                    c = i
            event_key = (entity_id, c + 1)
            if event_key in event_dict.keys():  # append observation if (i, c) key exists
                event_dict[event_key].append((event_time, entity_state))
            else:  # create new key if (i, c) key does not exist
                event_dict[event_key] = [(event_time, entity_state)]

    return event_dict


def remove_stale_events(data):
    """
    Parse an event dictionary and remove transitions to the same state:

    .. code::

        event_dict = {
          (entity_id, cohort interval) : [(time, state), ..., (time, state)]
          (entity_id, cohort interval) : (time, state), ..., (time, state)]
        }

    :param data: a pandas dataframe
    :return: dict

    """
    event_dict = {}
    for event_key in data.keys():
        # Pull the list of all events for this entity in this time
        event_list = data[event_key]
        new_event_list = []
        # Iterate over all events and only keep those leading to changed state
        for i in range(len(event_list) - 1):
            if event_list[i][1] != event_list[i + 1][1]:
                new_event_list.append(event_list[i])
        # Last event added by default
        i = len(event_list) - 1
        new_event_list.append(event_list[i])
        event_dict[event_key] = new_event_list

    return event_dict


def bin_timestamps(sorted_data, cohorts, output_format=0, remove_stale=False):
    """
    Bin timestamped data in a dataframe so as to have ingoing and outgoing states per cohort interval

    :param data: the dataframe to cohort
    :param cohorts: the number of cohorts
    :param output_format: how to structure the outputs (0=cohorts, 1=event_list)
    :param remove_stale: whether to remove successive observations with identical state
    :type data: pandas dataframe
    :type dimension: int
    :type output_format: int
    :type remove_stale: bool

    :returns: returns dataframe with cohorted data and cohort intervals

    .. note:: The 'ID' and 'Time' column labels are used by default.

    .. warning:: Cohorting is a 'lossy' operation: Timestamps are discretised (binned) and any intermediate state transitions are lost.

    .. warning:: The data must be sorted already

    """

    # STEP 1
    # Construct regular intervals on the basis of minimum / maximum observation times
    #
    dt, cohort_bounds = generate_cohort_bounds(sorted_data, cohorts)
    # print(80 * '=')
    # print(cohort_bounds)
    # print(80 * '=')

    # TODO Optionally construct intervals by hand
    # dt = 1.0
    # cohort_bounds = [0.0, 1.0]

    # Identify unique entities in the frame
    unique_ids = sorted_data['ID'].unique()

    # Array storage for processed data
    cohort_assigned_state = np.empty((len(unique_ids), len(cohort_bounds)), str)
    cohort_assigned_state.fill(np.nan)
    cohort_event = np.empty((len(unique_ids), len(cohort_bounds)))
    cohort_event.fill(np.nan)
    cohort_count = np.empty((len(unique_ids), len(cohort_bounds)))
    cohort_count.fill(np.nan)

    # STEP 2
    # Generate the full event dictionary
    #
    event_dict = generate_event_dict(sorted_data, dt, cohort_bounds)

    # pp.pprint(event_dict)

    if remove_stale:
        event_dict = remove_stale_events(event_dict)

    # STEP 3
    # Loop over all possible entity / cohort interval pairs
    # assign a state to the cohort interval
    # compute counts of events within cohort inteval
    # ATTN we loop over all possibilities, not all actual realizations.
    # We use integer indexes for entities / cohort intervals

    for id in unique_ids:
        for time in range(len(cohort_bounds)):

            # Construct the event key
            entity_id = list(unique_ids).index(id)
            event_key = (id, time)
            # Intervals are associated with bounds starting at 0
            # 0 Interval between 0 and 1 Timestep
            # 1 Interval between 1 and 2 Timestep etc.

            interval = time

            # Case A: We have events for the entity in this time
            # (If the key exists there should be at least one event for this entity in this time)
            if event_key in event_dict.keys():

                # Pull the list of all events for this entity in this time
                event_list = event_dict[(id, interval)]

                # Assign state to cohort
                # Here we are using the LAST observation in interval
                # TODO Generalize to user specified function (first observation, average state in interval etc)
                if time == 0:
                    # The first time point is a special (initial state)
                    cohort_assigned_state[entity_id, time] = event_list[0][1]  # the initial state
                    cohort_event[entity_id, time] = event_list[0][0]  # the actual time of the initial state
                    cohort_count[entity_id, time] = 1  # by default only one count at initial state
                    #
                    # # Assign to the first cohort interval the last observed state
                    # cohort_assigned_state[entity_id, time + 1] = event_list[len(event_list) - 1][1]
                    # # Pick time of last event (informative)
                    # cohort_event[entity_id, time + 1] = event_list[len(event_list) - 1][0]
                    # # Add the count of events for that entity in the cohort (informative)
                    # cohort_count[entity_id, time + 1] = int(len(event_list))

                    # print('A00', event_key, time, cohort_event[entity_id, time])
                    # print('A01', event_key, time, cohort_event[entity_id, time + 1])
                else:
                    # Assign to the cohort interval the last observed state
                    cohort_assigned_state[entity_id, time] = event_list[len(event_list) - 1][1]
                    # Pick time of last event (informative)
                    cohort_event[entity_id, time] = event_list[len(event_list) - 1][0]
                    # Add the count of events for that entity in the cohort (informative)
                    cohort_count[entity_id, time] = int(len(event_list))

                    # print('AXX', event_key, time, cohort_assigned_state[entity_id, time])

            # Case B: We don't have events for the entity in this interval and it is the first interval
            # If we don't have observation for an entity in the first interval we assign NaN state
            elif event_key not in event_dict.keys() and time == 0:

                cohort_assigned_state[entity_id, time] = np.nan
                cohort_event[entity_id, time] = np.nan
                cohort_count[entity_id, time] = np.nan

                # print('BXX', event_key, time, cohort_count[entity_id, time])

            # Case C: We don't have events for the entity in this interval but maybe we have in the previous one
            # if there are no events and the previous state is available assign the last known state, else NaN
            elif event_key not in event_dict.keys() and time > 0:

                if cohort_assigned_state[entity_id, time - 1]:
                    cohort_assigned_state[entity_id, time] = cohort_assigned_state[entity_id, time - 1]
                    cohort_event[entity_id, time] = cohort_event[entity_id, time - 1]
                    cohort_count[entity_id, time] = cohort_count[entity_id, time - 1]
                else:
                    cohort_assigned_state[entity_id, time] = np.nan
                    cohort_event[entity_id, time] = np.nan
                    cohort_count[entity_id, time] = np.nan

                # print('CXX', event_key, time, cohort_count[entity_id, time])

    # Convert to pandas dataframe
    cohort_data = []
    for i in range(len(unique_ids)):
        for c in range(len(cohort_bounds)):
            cohort_data.append((unique_ids[i], c, cohort_assigned_state[i][c], cohort_event[i][c], cohort_count[i][c]))

    # The time index spans the cohort intervals (bounds - 1)
    # The measurement time point is the
    cohort_data = pd.DataFrame(cohort_data, columns=['ID', 'Time', 'State', 'EventTime', 'Count'])

    if output_format == 0:
        return cohort_data, cohort_bounds
    elif output_format == 1:
        return event_dict, cohort_bounds
