# encoding: utf-8

# (c) 2017-2022 Open Risk, all rights reserved
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

from __future__ import print_function

import numpy as np

import transitionMatrix as tm
from transitionMatrix.estimators import DurationEstimator


class AalenJohansenEstimator(DurationEstimator):

    """
    Class for implementing the Aalen-Johansen estimator for the transition matrix

    Documentation: `Aalen-Johansen Estimator <https://www.openriskmanual.org/wiki/Aalen-Johansen_Estimator>`_

    """

    def __init__(self, states=None):
        DurationEstimator.__init__(self)
        # if not (0 < alpha <= 1.):
        #     raise ValueError('alpha parameter must be between 0 and 1.')
        if states is not None:
            self.states = states
        self.etm = None
        self.times = None

    def fit(self, data, labels=None):
        """
        Parameters
        ----------
        data : dataframe - The data to use for the estimation provided in a pandas data frame in long format,with one row per observed transition. The data frame must contain the following columns (or pass a label object that will assign accordingly:

            * ID: A unique entity identification number
            * TIME Time when a transition occurs
            * FROM: State from where a transition occurs
            * TO: State to which a transition occurs

        labels: an optional dictionary for relabeling column names if those deviate from the convention

            * TODO constraint possible transitions (absorbing states)
            * TODO censored data
            * TODO partial dates
            * TODO covariance calculation
            * TODO confidence intervals

        Returns
        -------
        etm.values : estimated empirical transition matrix throughout the observed interval. This is a three dimensional array object (From State, To State, Timepoint)
        observation_times: a list of observation times etm.observation_times


        * TODO Store counts as well as frequencies
        * TODO Optional Binning of close observation times


        .. note::
            The input data MUST be pre-sorted in ascending time order. This is easily done using pandas functionality.

        References
        ----------

        """

        if labels is not None:
            from_label = labels['From']
            to_label = labels['To']
            timestep_label = labels['Time']
            id_label = labels['ID']
        else:
            from_label = 'From'
            to_lable = 'To'
            id_label = 'ID'
            timestep_label = 'Time'

        # The dimension of the transition matrix
        state_dim = self.states.cardinality

        # extract observation times
        observation_times = tm.utils.unique_timestamps(data)

        # Store event data in 1d arrays for faster processing
        event_count = data[id_label].count()
        event_id = np.empty(event_count, int)
        event_from_state = np.empty(event_count, int)
        event_to_state = np.empty(event_count, int)
        event_time = np.empty(event_count, float)
        event_timepoint = np.empty(event_count, int)
        event_exists = np.empty(event_count, bool)
        event_exists.fill(False)

        # Capture nan events for potentially missing observations
        nan_count = 0
        i = 0  # count of events
        t = 0  # count of distinct timepoints

        # TODO remove row hardwiring

        for row in data.itertuples():
            try:
                event_id[i] = row[1]
                event_time[i] = row[2]
                event_from_state[i] = int(row[3])
                event_to_state[i] = int(row[4])
                # Identify migrations
                if event_to_state[i] != event_from_state[i]:
                    event_exists[i] = True # indicates valid (complete) data row
                # Identify timepoint index
                if i == 0:
                    event_timepoint[i] = 0
                elif i > 0 and event_time[i] > event_time[i - 1]:
                    t += 1  # we have moved to next distinct event time
                    event_timepoint[i] = t
                elif i > 0 and event_time[i] == event_time[i - 1]:
                    event_timepoint[i] = t  # we are still in the same event time

            except ValueError:
                nan_count += 1
            i += 1

        self.nans = nan_count
        self.counts = event_count
        self.timepoint_count = t

        Debug = False
        if Debug:
            print('Events ', self.counts)
            print('NaNs ', self.nans)

        # Find the initial states of all entities
        unique_ids = list(data[id_label].unique())
        y_initial_count = np.zeros((state_dim,), dtype=int)
        for i in range(0, event_count - 1):
            if event_id[i] in unique_ids:
                item = unique_ids.index(event_id[i])
                y_initial_count[int(event_from_state[i])] += 1
                unique_ids.pop(item)

        # Initialize empirical transition matrix
        etm = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=float)
        etm[:, :, 0] = np.eye(state_dim, state_dim)

        # Initialize Migration counts
        dN = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=int)

        # Initialize State Occupation counts
        y = np.zeros((state_dim, self.timepoint_count), dtype=int)
        y[:, 0] = y_initial_count

        # Initialize transition densities
        dA = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=float)

        #
        # Loop over data (id, time, from_state, to_state)
        #
        # 1. calculate migrations count dN^{mn}_{k} from m to n at timepoint k
        #
        for i in range(0, event_count - 1):
            # if we have a valid data point
            if event_exists[i]:
                # if we have an observed transition
                if event_timepoint[i] > 0:
                    dN[event_from_state[i], event_to_state[i], event_timepoint[i]] += 1

        #
        # 2. calculate population count Y^m_k per state m at timepoint k
        #
        for k in range(1, self.timepoint_count - 1):
            for m in range(0, state_dim):
                migration_to_m = 0
                migration_from_m = 0
                for n in range(0, state_dim):
                    if n != m:
                        migration_to_m += dN[n, m, k]
                        migration_from_m += dN[m, n, k]
                y[m, k] = y[m, k - 1] + migration_to_m - migration_from_m
                dN[m, m, k] = migration_from_m

        #
        # 3. calculate off-diagonal element dA^{mn}_{k} from m to n at timepoint k
        # 4. calculate diagonal element dA^{n}_{k} at timepoint k
        #
        for k in range(1, self.timepoint_count - 1):
            for m in range(0, state_dim):
                for n in range(0, state_dim):
                    if y[m, k] != 0:
                        if m != n:
                            dA[m, n, k] = dN[m, n, k] / y[m, k]
                        else:
                            dA[m, m, k] = - dN[m, m, k] / y[m, k]
                    else:
                        dA[m, n, k] = 0

        #
        # 5. calculate transition matrix T^{mn}_{k} at timepoint k
        #
        identity = np.eye(state_dim, dtype=float)
        for k in range(1, self.timepoint_count):
            # for k in range(1, 4):
            for m in range(0, state_dim):
                for n in range(0, state_dim):
                    for q in range(0, state_dim):
                        etm[m, n, k] += etm[m, q, k - 1] * (identity[q, n] + dA[q, n, k])

        # The empirical transition matrix
        self.etm = etm
        self.times = observation_times

        return self.etm, self.times
