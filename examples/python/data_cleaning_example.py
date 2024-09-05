# encoding: utf-8

# (c) 2017-2024 Open Risk (https://www.openriskmanagement.com)
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

import pprint as pp

import pandas as pd

from transitionMatrix.utils.converters import frame_to_array, datetime_to_float
from transitionMatrix.utils.preprocessing import transitions_summary, validate_absorbing_state

""" Examples of using transitionMatrix to prepare data sets (data cleansing). The functionality is primarily based on pandas, with transition data specific procedures supported by the utils sub-package. For some operations (and large datasets) it might be advisable to work with numpy arrays

"""

# Load the raw data into a pandas frame
raw_data = pd.read_csv('../../datasets/rating_data_raw.csv')

# Print a generic summary based on pandas describe() method
print(raw_data.describe())

# Bring the column names to a standard convention
raw_data.rename(columns={"RatingNum": "State", "Date": "Time", "CustomerId": "ID"}, inplace=True)

print(raw_data.head())

# Print a summary of transition statistics
pp.pprint(transitions_summary(raw_data))

# Drop redundant column
raw_data = raw_data.drop(columns=['Rating'])

# Move the NR column to the end
reorder_dict = {
    0: 8,
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7
}
raw_data = raw_data.replace({"State": reorder_dict})

print(raw_data.head(10))

# Convert date strings to floats
[start_date, end_date, total_days], converted_data = datetime_to_float(raw_data, time_column='Time')
print([start_date, end_date, total_days])

# NB: In the below the D = 7, NR = 8 special states are hardwired

# remove an initial observation for an entity if it is classified as D
# Reason: an initial defaulted observation is unusual / non-sensical
rows = []
entity_id, event_time, entity_state = frame_to_array(converted_data)
for i in range(len(entity_id)):
    if entity_id[i - 1] != entity_id[i] and entity_state[i] == 7:
        pass
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
clean_data0 = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])

# remove an initial observation for an entity if it is classified as NR
# Reason: left truncation of observations must be handled consistently

rows = []
entity_id, event_time, entity_state = frame_to_array(clean_data0)
for i in range(len(entity_id)):
    if entity_id[i - 1] != entity_id[i] and entity_state[i] == 8:
        pass
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
clean_data1 = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])


# remove an intermediate observation for an entity if it is classified as NR
# Reason: it is non-informative and it complicates the handling of NR state (non-absorbing)
rows = []
entity_id, event_time, entity_state = frame_to_array(clean_data1)
for i in range(len(entity_id) - 1):
    if entity_id[i + 1] == entity_id[i] and entity_state[i] == 8 and entity_state[i + 1] != 8:
        pass
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
clean_data2 = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])

# remove an intermediate observation for an entity if it is classified as D
# Reason: this is (presumably) a 're-emergence from default' type event. complicates the handling of D state (non-absorbing)
rows = []
entity_id, event_time, entity_state = frame_to_array(clean_data2)
for i in range(len(entity_id) - 1):
    if entity_id[i + 1] == entity_id[i] and entity_state[i] == 7 and entity_state[i + 1] != 7:
        pass
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
clean_data3 = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])

# remove NR observations of defaulted entities
# Reason: non-informative, ensure D is truly an absorbing state
# (NB: the labels 0, 8 are hardwired for this data set)
rows = []
entity_id, event_time, entity_state = frame_to_array(clean_data3)

for i in range(len(entity_id)):
    if entity_state[i] == 8 and entity_state[i - 1] == 7:
        pass
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
clean_data4 = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])

# check that NR and D are absorbing states
print(validate_absorbing_state(clean_data4, 7))
print(validate_absorbing_state(clean_data4, 8))

pp.pprint(transitions_summary(clean_data4))

# if the first entry is not at the earliest global observation timepoint, add the initial observation
# this assumption removes left truncation condition but may bias the data
# NB: 0.0 is hardwired as left observation window
rows = []
entity_id, event_time, entity_state = frame_to_array(clean_data4)
for i in range(len(entity_id)):
    if entity_id[i - 1] != entity_id[i] and event_time[i] > 0:
        rows.append((entity_id[i], event_time[i], entity_state[i]))
        rows.append((entity_id[i], 0.0, entity_state[i]))
    else:
        rows.append((entity_id[i], event_time[i], entity_state[i]))

clean_data = pd.DataFrame(rows, columns=['ID', 'Time', 'State'])

# Sort by entity ID, then event Time
sorted_data = clean_data.sort_values(['ID', 'Time'], ascending=[True, True])

pp.pprint(transitions_summary(sorted_data))
sorted_data.to_csv('../../datasets/rating_data.csv', index=False)
