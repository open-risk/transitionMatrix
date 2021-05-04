# encoding: utf-8

# (c) 2017-2021 Open Risk (https://www.openriskmanagement.com)
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


""" Characterize datasets (Summary statistics etc)

"""

import pandas as pd
import pprint as pp
import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.creditratings.predefined import SP02, SP02NR
from transitionMatrix.utils import print_matrix
from transitionMatrix.utils import transitions_summary

dataset_path = source_path + "datasets/"

dataset_list = [
    'rating_data_raw.csv',
    'rating_data.csv',
    'scenario_data.csv',
    'synthetic_data.csv',
    'synthetic_data1.csv',
    'synthetic_data2.csv',
    'synthetic_data3.csv',
    'synthetic_data4.csv',
    'synthetic_data5.csv',
    'synthetic_data6.csv',
    'synthetic_data7.csv',
    'synthetic_data8.csv',
    'synthetic_data9.csv',
    'test.csv'
]

for dataset in dataset_list:
    input_data = pd.read_csv('../../datasets/' + dataset)
    print(dataset)
    pp.pprint(transitions_summary(input_data))
    print(80 * '-')


def main():
    print("Done")


if __name__ == "__main__":
    main()
