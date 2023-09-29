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


""" Example of using the transitionMatrix data generator methods to generate a full multi-period matrix set
The input data are processed Standard and Poor's matrices for a selection of cumulative observation points

.. note:: This example requires a substantial amount of custom code!

"""

from scipy.linalg import expm

import transitionMatrix as tm
from transitionMatrix import source_path

dataset_path = source_path + "datasets/"

print("> Loading multi-period transitional matrices (cumulative mode) from json file")
SnP_Set0 = tm.TransitionMatrixSet(json_file=dataset_path + "sp_NR_adjusted.json", temporal_type='Cumulative')
print("> Validate")
print(SnP_Set0.validate())
# SnP_Set0.print(format='Percent')

print("> Set the timesteps at which we have matrix observations")
# We skip the 15 and 20 year time points as they require further processing
SnP_Set0.timesteps = [1, 2, 3, 5, 7, 10]
print(SnP_Set0.timesteps)

# we will store the results here
timesteps = SnP_Set0.timesteps[len(SnP_Set0.timesteps) - 1]
SnP = tm.TransitionMatrixSet(dimension=8, periods=timesteps)

print("> Fill in the gaps between periods")
t_list = SnP_Set0.timesteps
# TODO Assumption is that first entry starts at 1
# First matrix
ts = 1
SnP.entries[ts - 1] = SnP_Set0.entries[0]
# Loop over timestep list
for k in t_list:
    i = t_list.index(k)
    # While not at the final matrix
    if i < len(t_list) - 1:
        # compute the gap period
        gap = t_list[i + 1] - t_list[i]
        # If the gap to next timestep is larger than one period
        if gap > 1:
            # Divide right matrix by left matrix to derive forward gap transition matrix the for gap-periods
            lm = SnP_Set0.entries[i]
            lm.fix_rowsums()
            rm = SnP_Set0.entries[i + 1]
            rm.fix_rowsums()
            # TODO Fix Negative probabilities for gap transition matrix
            q = rm * lm.I
            q.fix_rowsums()
            #   From gap transition matrix derive gap one-year matrices (via generator)
            #   Fill in gap years with cumulative matrices
            q.fix_negativerates()
            G = q.generator(t=gap)
            for gap_period in range(1, gap + 1):
                gm = expm(gap_period * G)
                cm = gm * lm
                cm.fix_negativerates()
                ts += 1
                SnP.entries[ts - 1] = cm
        # There is no gap, store matrix as is
        else:
            ts += 1
            SnP.entries[ts - 1] = SnP_Set0.entries[i + 1]
    # Final matrix
    else:
        ts = timesteps
        SnP.entries[ts - 1] = SnP_Set0.entries[i]

SnP.timesteps = t_list
SnP.temporal_type = 'Cumulative'
SnP.print_matrix(accuracy=4)
# TODO Handle strictly zero transition probabilities
# TODO Handle non-monotonic transition probabilities
SnP.to_json(dataset_path + "sp_multiperiod.json", accuracy=8)


def main():
    print("Done")


if __name__ == "__main__":
    main()
