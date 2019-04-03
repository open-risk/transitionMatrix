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

'''
module transitionMatrix.utils - helper classes and functions

'''

from __future__ import print_function, division

import numpy as np
import pandas as pd


# def initial_states(data):
#     """
#     Identify the initial state for each entity in the dataframe
#
#     :param data: dataframe.
#
#     :returns: returns a numpy array
#
#     """
#     unique_timestamps = data['Time'].unique()
#     return unique_timestamps


def unique_timestamps(data):
    """
    Identify unique timestamps in a dataframe

    :param data: dataframe. The 'Time' column is used by default

    :returns: returns a numpy array

    """
    unique_timestamps = data['Time'].unique()
    return unique_timestamps


def bin_timestamps(data, cohorts):
    """
    Bin timestamped data in a dataframe so as to have ingoing and outgoing states per cohort interval

    The 'Time' column is used by default

    .. note:: This is a lossy operation: Timestamps are discretised and intermediate state \
    transitions are lost

    """
    # Find the range of observed event times
    t_min = data['Time'].min()
    t_max = data['Time'].max()

    # Divide the range into equal intervals
    dt = (t_max - t_min) / cohorts
    cohort_intervals = [t_min + dt * i for i in range(0, cohorts + 1)]
    sorted_data = data.sort_values(['Time', 'ID'], ascending=[True, True])

    # Identify unique states for validation
    unique_ids = sorted_data['ID'].unique()

    # Arrays to store processed data
    cohort_assigned_state = np.empty((len(unique_ids), len(cohort_intervals)), str)
    cohort_assigned_state.fill(np.nan)
    cohort_event = np.empty((len(unique_ids), len(cohort_intervals)))
    cohort_event.fill(np.nan)
    cohort_count = np.empty((len(unique_ids), len(cohort_intervals)))
    cohort_count.fill(np.nan)

    # Loop over all events and construct a dictionary
    # Create a unique key as per (entity, interval)
    # Add (time, state) pairs as variable length list
    event_dict = {}
    for row in sorted_data.itertuples():
        event_id = row[1]
        event_time = row[2]
        event_state = row[3]
        # Find the interval of the event
        c = int((event_time - event_time % dt) / dt)
        event_key = (event_id, c)
        if event_key in event_dict.keys():
            # append observation if key exists
            event_dict[event_key].append((event_time, event_state))
        else:
            # create new key if not
            event_dict[event_key] = [(event_time, event_state)]

    # Loop over all possible keys
    for i in range(len(unique_ids)):
        for k in range(len(cohort_intervals)):
            event_id = i
            event_cohort = k
            event_key = (i, k)
            # Do we have events in this interval?
            if event_key in event_dict.keys():
                event_list = event_dict[(i, k)]
                # Assign state using last observation in interval
                # TODO Generalize to user specified function
                cohort_assigned_state[event_id, event_cohort] = event_list[len(event_list) - 1][1]
                cohort_event[event_id, event_cohort] = event_list[len(event_list) - 1][0]
                cohort_count[event_id, event_cohort] = int(len(event_list))
                # print('A', cohort_count[event_id, event_cohort])
            elif event_key not in event_dict.keys() and event_cohort > 0:
                # Assign previous state if there are not events and previous state is available
                cohort_assigned_state[event_id, event_cohort] = cohort_assigned_state[event_id, event_cohort - 1]
                cohort_event[event_id, event_cohort] = cohort_event[event_id, event_cohort - 1]
                cohort_count[event_id, event_cohort] = cohort_count[event_id, event_cohort - 1]
                # print('B', cohort_count[event_id, event_cohort])
            elif event_key not in event_dict.keys() and event_cohort == 0:
                # If we don't have observation in first interval assign NaN state
                cohort_assigned_state[event_id, event_cohort] = np.nan
                cohort_event[event_id, event_cohort] = np.nan
                cohort_count[event_id, event_cohort] = np.nan
                # print('C', cohort_count[event_id, event_cohort])

    # Convert to pandas dataframe
    cohort_data = []
    for i in range(len(unique_ids)):
        for c in range(len(cohort_intervals)):
            cohort_data.append((i, c, cohort_assigned_state[i][c], cohort_event[i][c], cohort_count[i][c]))

    cohort_data = pd.DataFrame(cohort_data, columns=['ID', 'Cohort', 'State', 'EventTime', 'Count'])
    return cohort_data, cohort_intervals
