# -*- coding: utf-8 -*-

# (c) 2017-2024 Open Risk, all rights reserved
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


""" Run all examples for a high-level test that everything is working with the current version of the library

"""

import os

examples_path = os.path.join("examples", "python")
filelist = ['adjust_nr_state', 'credit_curves',
            'empirical_transition_matrix', 'fix_multiperiod_matrix', 'generate_synthetic_data',
            'generate_visuals', 'matrix_from_cohort_data', 'matrix_operations', 'matrix_set_operations']

# TODO additional examples
# 'matrix_from_duration_data', 'matrix_lendingclub', 'matrix_set_lendingclub',

if __name__ == '__main__':

    for example in filelist:
        try:
            print('\nExecuting example file: ', example.upper())
            print('-----------------------' + '-' * len(example))
            path = os.path.join(examples_path, example + ".py")
            exec(open(path).read())
        except:
            print('**********************' + '*' * len(example))
            print('ERROR in example file', example)
            print('**********************' + '*' * len(example))
            pass
