# -*- coding: utf-8 -*-

# (c) 2017-2019 Open Risk, all rights reserved
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
import statsmodels.stats.proportion as st

from transitionMatrix.estimators import BaseEstimator


class CohortEstimator(BaseEstimator):

    """
    Class for implementing a Cohort estimator for the transition matrix
    under the assumption of time homogeneity

    """

    def __init__(self, cohort_intervals=None, states=None, ci=None):
        BaseEstimator.__init__(self)
        # if not (0 < alpha <= 1.):
        #     raise ValueError('alpha parameter must be between 0 and 1.')
        self.cohort_intervals = cohort_intervals
        if states is not None:
            self.states = states
        if ci is not None:
            assert (ci['method'] in ['goodman', 'sison-glaz', 'binomial'])
            assert (0 < ci['alpha'] <= 1.0)
            self.ci_method = ci['method']
            self.ci_alpha = ci['alpha']

    def fit(self, data, labels=None):
        '''
        Parameters
        ----------
        data : array-like
            The data to use for the estimation

        labels: a dictionary for relabeling column names

        Returns
        -------
        matrix : estimated transition matrix
        confint_lower: lower confidence interval
        confint_upper: upper confidence interval

        Notes
        ------
        '''

        # loop over data (id, period, state)
        # calculate population count N^i_k per state i per period k
        # calculate migrations count N^{ij}_{kl} from i to j from period k to period l
        # calculate transition matrix as ratio T^{ij}_{kl} = N^{ij}_{kl} / N^i_k

        if labels is not None:
            state_label = labels['State']
            timestep_label = labels['Timestamp']
            id_label = labels['ID']
        else:
            state_label = 'State'
            id_label = 'ID'
            timestep_label = 'Timestep'

        state_dim = self.states.cardinality
        cohort_labels = data[timestep_label].unique()
        cohort_dim = len(cohort_labels) - 1
        event_count = data[id_label].count()

        # store data in 1d arrays for fast processing
        # capture nan events for missing observations
        event_exists = np.empty(event_count, int)
        event_id = np.empty(event_count, int)
        event_state = np.empty(event_count, int)
        event_time = np.empty(event_count, int)
        nan_count = 0
        i = 0
        # TODO read data by labels, not column location
        for row in data.itertuples():
            try:
                event_state[i] = int(row[3])
                event_id[i] = row[1]
                event_time[i] = int(row[2])
                event_exists[i] = 1
            except ValueError:
                nan_count += 1
            i += 1
        self.nans = nan_count

        # storage of counts
        # number of entities observed in given state per period
        tm_count = np.ndarray((state_dim, cohort_dim), int)
        # number of entities observed to transition from state to state per period
        tmn_count = np.ndarray((state_dim, state_dim, cohort_dim), int)
        tm_count.fill(0)
        tmn_count.fill(0)
        # normalized frequencies
        tmn_values = np.ndarray((state_dim, state_dim, cohort_dim), float)
        tmn_values.fill(0.0)

        # TODO Capture case if entity with only one observation (hence no transition count)

        for i in range(1, event_count - 1):
            if event_exists[i] == 1:
                # while processing event data from same entity
                if event_id[i + 1] == event_id[i]:
                    tm_count[(event_state[i], event_time[i])] += 1
                    tmn_count[(event_state[i], event_state[i + 1], event_time[i])] += 1
                # last data point from entity data
                # elif event_id[i + 1] != event_id[i] and event_id[i] == event_id[i - 1]:
                #     tm_count[(event_state[i], event_time[i])] += 1
                #     tmn_count[(event_state[i - 1], event_state[i], event_time[i])] += 1
                # elif event_id[i + 1] != event_id[i] and event_id[i] != event_id[i - 1]:
                #     sys.exit("Isolated observation in data")

        # boundary cases
        #
        i = 0
        if event_exists[i] == 1:
            if event_id[i + 1] == event_id[i]:
                tm_count[(event_state[i], event_time[i])] += 1
                tmn_count[(event_state[i], event_state[i + 1], event_time[i])] += 1
        #
        # i = event_count - 1
        # if event_exists[i] == 1:
        #     if event_id[i] == event_id[i - 1]:
        #         tm_count[(event_state[i], event_time[i])] += 1
        #         tmn_count[(event_state[i - 1], event_state[i], event_time[i])] += 1

        self.counts = int(tm_count.sum())

        # Confidence Interval Estimation (Based on Counts)
        confint_lower = np.ndarray((state_dim, state_dim, cohort_dim))
        confint_upper = np.ndarray((state_dim, state_dim, cohort_dim))
        for k in range(cohort_dim):
            for s1 in range(state_dim):
                intervals = st.multinomial_proportions_confint(tmn_count[s1, :, k], alpha=self.ci_alpha,
                                                               method=self.ci_method)
                for s2 in range(state_dim):
                    confint_lower[s1, s2, k] = intervals[s2][0]
                    confint_upper[s1, s2, k] = intervals[s2][1]
            self.confint_lower = confint_lower
            self.confint_upper = confint_upper

        # Normalization of counts to produce family of probability matrices
        for s1 in range(state_dim):
            for s2 in range(state_dim):
                for k in range(cohort_dim):
                    if tm_count[(s1, k)] > 0:
                        tmn_values[(s1, s2, k)] = tmn_count[(s1, s2, k)] / tm_count[(s1, k)]
                        # print(s1, s2, k, tmn_values[(s1, s2, k)], tmn_count[(s1, s2, k)], tm_count[(s1, k)])

        # Return a list of transition matrices
        for k in range(cohort_dim):
            self.matrix_set.append(tmn_values[:, :, k])
            self.count_set.append(tmn_count[:, :, k])
            self.count_normalization.append(tm_count[:, k])

        return self.matrix_set
