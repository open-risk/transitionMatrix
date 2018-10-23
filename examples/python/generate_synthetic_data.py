# encoding: utf-8

# (c) 2017-2018 Open Risk, all rights reserved
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


"""
Example workflows using transitionMatrix to generate synthetic data

The first three examples produce "duration" type data. Estimating transitions
for duration data is done directly with duration type estimators or after
cohorting (binning) the data for cohort (frequency) type estimators

The subsequent three examples product cohort type data using markov chain simulation

"""

import transitionMatrix as tm
from datasets import Generic
from transitionMatrix import source_path
from transitionMatrix.utils import dataset_generators

dataset_path = source_path + "datasets/"

# DURATION TYPE DATASETS (Compact format)
# 1-> This dataset simulates single entity transitions
# 2-> Multiple Entities with simple state space observed over continuous short time interval
# 3-> Multiple Entities with Medium sized State space observed over continuous long time interval

# COHORT TYPE DATASETS
# 4-> S&P Credit Rating Migration Matrix
# 5-> Single entity observed over discrete short time interval
# 6-> Simplest absorbing state case for validation purposes

# DURATION TYPE DATASETS (Long format)
# 7-> S&P Credit Rating Migration Matrix

dataset = 7

#
# Duration type datasets in Compact Format
#
if dataset == 1:
    # This dataset simulates single entity transitions
    # State Space description
    myState = tm.StateSpace([('0', "A"), ('1', "B"), ('2', "C"), ('3', "D")])
    # myState.describe()
    # n: number of entities
    # s: number of samples per entity
    data = dataset_generators.exponential_transitions(myState, n=1, sample=100, rate=0.1)
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data1.csv', index=False)

elif dataset == 2:
    # Second example: Multiple Entities observed over continuous short time interval
    myState = tm.StateSpace([('0', "Basic"), ('1', "Default")])
    data = dataset_generators.exponential_transitions(myState, n=1000, sample=10, rate=0.1)
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data2.csv', index=False)

elif dataset == 3:
    # Third example: Multiple Entities with Medium sized State space observed over continuous long time interval
    myState = tm.StateSpace([('0', "A"), ('1', "B"), ('2', "C"), ('3', "D"), ('4', "E"), ('5', "F"), ('6', "G")])
    data = dataset_generators.exponential_transitions(myState, n=100, sample=20, rate=0.1)
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data3.csv', index=False)

#
# Cohort type datasets
#
elif dataset == 4:
    # Fourth example: S&P Credit Rating Migration Matrix
    # S&P Ratings State Space
    description = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                   ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]

    matrix = Generic
    myState = tm.StateSpace(description)
    # Fourth example: Single entity observed over discrete short time interval
    data = dataset_generators.markov_chain(myState, matrix, n=1000, timesteps=10)
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data4.csv', index=False)

elif dataset == 5:
    # Fifth example: An IFRS 9 style Migration Matrix for migrations between Stages
    description = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]

    matrix = [[0.8, 0.15, 0.05],
              [0.1, 0.7, 0.2],
              [0.0, 0.0, 1.0]]

    myState = tm.StateSpace(description)
    data = dataset_generators.markov_chain(myState, transitionmatrix=matrix, n=10000, timesteps=5)
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data5.csv', index=False)

elif dataset == 6:
    # Simplest absorbing state case for validation purposes
    myState = tm.StateSpace()
    myState.generic(2)
    myState.describe()
    matrix = [[0.5, 0.5],
              [0.0, 1.0]]
    data = dataset_generators.markov_chain(myState, transitionmatrix=matrix, n=1000, timesteps=20)
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    data.to_csv(dataset_path + 'synthetic_data6.csv', index=False)

#
# Duration type datasets in Long Format
#

elif dataset == 7:
    # Seventh example: Credit Rating Migrations in Long Format
    description = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                   ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]
    myState = tm.StateSpace(description)
    matrix = Generic
    # Timesteps are the interval periods over which to repeatedly simulate the single period migration matrix
    data = dataset_generators.long_format(myState, transitionmatrix=matrix, n=1000, timesteps=10)
    sorted_data = data.sort_values(['Time', 'ID', 'From'], ascending=[True, True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data7.csv', index=False)

elif dataset == 8:
    # Simplest absorbing state case for validation purposes (Duration estimator)
    # Single timestep
    description = [('0', "G"), ('1', "B")]
    myState = tm.StateSpace()
    myState.generic(2)
    myState.describe()
    matrix = [[0.5, 0.5],
              [0.0, 1.0]]
    data = dataset_generators.long_format(myState, transitionmatrix=matrix, n=10000, timesteps=2)
    sorted_data = data.sort_values(['Time', 'ID', 'From'], ascending=[True, True, True])
    data.to_csv(dataset_path + 'synthetic_data8.csv', index=False)

print("> Synthetic Dataset:", dataset, " has been created and stored in the filesystem.")
