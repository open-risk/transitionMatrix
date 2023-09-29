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


""" Examples of using transitionMatrix to adjust the NR (not-rated) statistics.

Input data are the Standard and Poor's historical data (1981 - 2016) for corporate credit rating migrations

"""

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.creditratings.predefined import SP02, SP02NR
from transitionMatrix.utils import print_matrix

dataset_path = source_path + "datasets/"

example = 1

if example == 1:
    a = tm.TransitionMatrix(values=SP02NR)
    b = tm.TransitionMatrix(values=SP02)
    a = 0.01 * a
    b = 0.01 * b
    a = a.remove(8, method='noninform')
    print_matrix(a, format_type='Standard', accuracy=5)
    print_matrix(b, format_type='Standard', accuracy=5)


elif example == 2:

    print("> Load multi-period transitional matrices (cumulative mode) from json file")
    SnP_Set0 = tm.TransitionMatrixSet(json_file=dataset_path + "sp_1981-2016.json", temporal_type='Cumulative')
    print("> Valid Input Matrix? ", SnP_Set0.validate())

    print("> Remove NR transitions and redistribute to other states")
    SnP_Set1 = SnP_Set0.remove(8, "noninform")
    print("> Valid Output Matrix? ", SnP_Set1.validate())

    #
    # Hurrah, we have an NR adjusted matrix set. Lets save it
    #
    SnP_Set1.to_json(dataset_path + 'sp_NR_adjusted.json', accuracy=5)

    # Compare before / after
    SnP_Set0.print_matrix(period=2)
    SnP_Set1.print_matrix(period=2)


def main():
    print("Done")


if __name__ == "__main__":
    main()
