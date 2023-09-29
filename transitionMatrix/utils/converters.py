# encoding: utf-8

# (c) 2017-2023 Open Risk (https://www.openriskmanagement.com)
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

""" Converter utilities to help switch between various formats """

import pandas as pd
import numpy as np


def frame_to_array(dataframe):
    """
    Convert pandas to numpy array
    :param dataframe:
    :return:
    """
    event_count = dataframe.shape[0]
    entity_id = np.empty(event_count, int)
    entity_state = np.empty(event_count, int)
    event_time = np.empty(event_count, float)

    i = 0
    for row in dataframe.itertuples(index=False):
        entity_id[i] = row.ID
        event_time[i] = row.Time
        entity_state[i] = row.State
        i += 1
    return entity_id, event_time, entity_state


def datetime_to_float(dataframe, time_column='Time', format=None):
    """datetime_to_float() converts dates from string format to the canonical float format

    :param time_column: the column label of the observation times
    :param dataframe: Pandas dataframe with dates in string format
    :return: Pandas dataframe with dates in float format
    :rtype: object

    .. note:: The date string must be recognizable by the pandas to_datetime function.

    """

    dataframe[time_column] = dataframe[time_column].apply(
        lambda x: (pd.to_datetime(x, format=format)))

    # Find the start and end dates of the sample
    start_date = dataframe[time_column].min()
    end_date = dataframe[time_column].max()
    # Find the total days in the sample
    total_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days

    # Apply the transformation
    # If total_days == 0 simply set to zero
    if total_days > 0:
        dataframe[time_column] = dataframe[time_column].apply(
            lambda x: (pd.to_datetime(x) - pd.to_datetime(start_date)).days / total_days)
    else:
        dataframe[time_column] = dataframe[time_column].apply(
            lambda x: 0.0
        )

    return [start_date, end_date, total_days], dataframe


def to_canonical(dataframe):
    """to_canonical() converts a dataframe that is in compact form into a canonical form

    :param dataframe:
    :return: dataframe

    """

    event_count = dataframe.shape[0]
    entity_id = np.empty(event_count, int)
    state = np.empty(event_count, int)
    event_from_state = np.empty(event_count, int)
    event_to_state = np.empty(event_count, int)
    event_time = np.empty(event_count, float)

    i = 0
    for row in dataframe.itertuples(index=False):
        entity_id[i] = row.ID
        event_time[i] = row.Time
        state[i] = row.State
        i += 1

    rows = []
    # boostrap first event
    i = 0
    event_from_state[i] = state[i]
    event_to_state[i] = state[i]
    rows.append((entity_id[i], event_time[i], event_from_state[i], event_to_state[i]))
    for i in range(1, event_count):
        if entity_id[i - 1] == entity_id[i]:  # same entity transition
            event_from_state[i] = event_to_state[i - 1]
            event_to_state[i] = state[i]
        else:  # new entity
            event_from_state[i] = state[i]
            event_to_state[i] = state[i]

        rows.append((entity_id[i], event_time[i], event_from_state[i], event_to_state[i]))
    return pd.DataFrame(rows, columns=['ID', 'Time', 'From', 'To'])


def to_compact(dataframe):
    """to_compact() converts a dataframe that is in canonical form into a compact form

    :param dataframe:
    :return: dataframe

    """

    data = dataframe.drop(['From'], axis=1)
    data.rename(columns={'To': 'State'}, inplace=True)

    return data
