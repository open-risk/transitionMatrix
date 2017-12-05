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


""" Example of using transitionMatrix adjust the NR state (not-rated)
Input data are the Standard and Poor's historical data (1981 - 2016) for corporate credit rating migrations

"""

import transitionMatrix as tm
from transitionMatrix import source_path
dataset_path = source_path + "datasets/"

import numpy as np


print("-- Loading multi-period transitional matrices (cumulative mode) from json file")
SnP_Set0 = tm.TransitionMatrixSet(json_file=dataset_path + "sp_1981-2016.json", temporal_type='Cumulative')
print(SnP_Set0.validate())

print("-- Remove NR transitions and redistribute to other states")
SnP_Set1 = SnP_Set0.remove(8, "noninform")
print(SnP_Set1.validate())

#
# Hurrah, we have an NR adjusted matrix set. Lets save it
#
SnP_Set1.to_json(dataset_path + 'sp_NR_adjusted.json', accuracy=5)

