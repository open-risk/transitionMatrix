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

import unittest
import transitionMatrix as tm
from transitionMatrix import source_path
import pandas as pd

ACCURATE_DIGITS = 7


class TestPreprocessing(unittest.TestCase):

    def test_bin_timestamps(self):

        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data1.csv')
        event_count = data['ID'].count()
        cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
        cohort_data['Count'] = cohort_data['Count'].astype(int)
        self.assertEqual(event_count, cohort_data['Count'].sum())


class TestDataSetGenerators(unittest.TestCase):
    pass


if __name__ == "__main__":

    unittest.main()
