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

from __future__ import print_function

import numpy as np
import statsmodels.stats.proportion as st

import transitionMatrix
from transitionMatrix.estimators import BaseEstimator


class CohortEstimator(BaseEstimator):
    """
    Class for implementing a Cohort Estimator for the transition matrix

    Documentation: `Cohort Estimator <https://www.openriskmanual.org/wiki/Cohort_Estimator>`_

    """

    def __init__(self, cohort_bounds=None, states=None, ci=None):
        BaseEstimator.__init__(self)
        # if not (0 < alpha <= 1.):
        #     raise ValueError('alpha parameter must be between 0 and 1.')
        self.cohort_bounds = cohort_bounds
        if states is not None:
            self.states = states
        if ci is not None:
            assert (ci['method'] in ['goodman', 'sison-glaz', 'binomial'])
            assert (0 < ci['alpha'] <= 1.0)
            self.ci_method = ci['method']
            self.ci_alpha = ci['alpha']

    def get_average(self):
        return self.average_matrix

    def fit(self, data, labels=None):
        """
        Parameters
        ----------
        data : dataframe - The data to use for the estimation (in sorted by ID in compact format)

        labels: an optional dictionary for relabeling column names

        Returns
        -------
        matrix_set : An estimated transition matrix set

        Notes
        ------

        * loop over data rows (id, timepoint, state)
        * at least two distinct timepoints are required (initial and final)
        * calculate population count N^i_k per state i per timepoint k
        * calculate migrations count N^{ij}_{kl} from i to j from timepoint k to timepoint l
        * calculate transition matrix as ratio T^{ij}_{kl} = N^{ij}_{kl} / N^i_k
        * calculate also count-averaged matrix

        References
        ----------


        """

        # Allow for flexible labelling for dataframe columns
        if labels is not None:
            state_label = labels['State']
            timestep_label = labels['Time']
            id_label = labels['ID']
        else:
            state_label = 'State'
            id_label = 'ID'
            timestep_label = 'Time'

        # Old way of enumerating cohort intervals was using labels
        # cohort_labels = data[timestep_label].unique()
        # cohort_dim = len(cohort_labels) - 1

        # The size of the state space
        state_dim = self.states.cardinality
        # The number of cohorts is the number of intervals
        # Minimally two (initial and final)
        cohort_dim = len(self.cohort_bounds) - 1
        event_count = data[id_label].count()

        # store data in 1d arrays for faster processing
        # capture nan events for missing observations
        event_exists = np.empty(event_count, int)
        entity_id = np.empty(event_count, int)
        entity_state = np.empty(event_count, int)
        event_time = np.empty(event_count, int)
        nan_count = 0

        i = 0
        for index, row in data.iterrows():
            entity_id[i] = row[id_label]
            try:
                entity_state[i] = row[state_label]
                event_time[i] = row[timestep_label]
                event_exists[i] = 1  # indicates a valid (complete) data row
            except ValueError:
                entity_state[i] = -99999
                event_time[i] = -99999
                event_exists[i] = 0
                nan_count += 1
            i += 1
        self.nans = nan_count

        # store number of entities observed in given state per time step
        tm_count = np.ndarray((state_dim, cohort_dim + 1), int)
        # store number of entities observed to transition from state (From) to state (To) per period
        tmn_count = np.ndarray((state_dim, state_dim, cohort_dim), int)
        # store normalized frequencies
        tmn_values = np.ndarray((state_dim, state_dim, cohort_dim), float)
        # matrix to store average transitions
        tmn_average = np.ndarray((state_dim, state_dim), float)

        # initialize to zero (TODO ?)
        tm_count.fill(0)
        tmn_count.fill(0)
        tmn_values.fill(0)
        tmn_average.fill(0)

        # TODO Capture case if entity with only one observation (hence no transition count)
        # TODO Capture case with stale observations (no transitions)

        for i in range(0, event_count - 1):  # the last point handled separately
            if event_exists[i] == 1:
                # while processing valid event data from same entity
                # increment state count
                tm_count[(entity_state[i], event_time[i])] += 1
                if entity_id[i + 1] == entity_id[i]:
                    # increment migration count if there is subsequent observation
                    # NB: It does not have to be different
                    tmn_count[(entity_state[i], entity_state[i + 1], event_time[i])] += 1

        # handle boundary cases
        # the last event must be evaluated in comparison with its previous one
        i = event_count - 1
        if event_exists[i] == 1:
            # ATTN we must shift the time index of the tm_count, tmn_count
            tm_count[(entity_state[i], event_time[i] - 1)] += 1
            if entity_id[i] == entity_id[i - 1]:
                tmn_count[(entity_state[i - 1], entity_state[i], event_time[i] - 1)] += 1

        # print(tm_count)
        # print(tm_count.sum())
        # print(tmn_count[:, :, 0])

        self.counts = int(tm_count.sum())

        # Normalization of counts to produce a family of probability matrices
        for s1 in range(state_dim):
            for s2 in range(state_dim):
                for k in range(cohort_dim):
                    if tm_count[(s1, k)] > 0:
                        tmn_values[(s1, s2, k)] = tmn_count[(s1, s2, k)] / tm_count[(s1, k)]

        # for k in range(cohort_dim):
        #     m = transitionMatrix.TransitionMatrix(tmn_values[:, :, k])
        #     m.print_matrix(accuracy=3)

        # Average transition matrix (assuming temporal homogeneity)
        for s1 in range(state_dim):
            for s2 in range(state_dim):
                tm_total_count = 0
                for k in range(cohort_dim):
                    tmn_average[(s1, s2)] += tmn_count[(s1, s2, k)]
                    tm_total_count += tm_count[(s1, k)]
                if tm_total_count > 0:
                    tmn_average[(s1, s2)] /= tm_total_count
        self.average_matrix = tmn_average

        # Confidence Interval Estimation (Based on Counts)
        confint_lower = np.ndarray((state_dim, state_dim, cohort_dim))
        confint_upper = np.ndarray((state_dim, state_dim, cohort_dim))
        for k in range(cohort_dim - 1):
            for s1 in range(state_dim):
                intervals = st.multinomial_proportions_confint(tmn_count[s1, :, k], alpha=self.ci_alpha,
                                                               method=self.ci_method)
                for s2 in range(state_dim):
                    confint_lower[s1, s2, k] = intervals[s2][0]
                    confint_upper[s1, s2, k] = intervals[s2][1]
            self.confint_lower = confint_lower
            self.confint_upper = confint_upper

        # Return a list of transition matrices
        # Both absolute (frequency) and relative (probability) format
        for k in range(cohort_dim):
            self.matrix_set.append(tmn_values[:, :, k])
            self.count_set.append(tmn_count[:, :, k])


        # Return absolute counts at time points
        for k in range(cohort_dim + 1):
            self.count_normalization.append(tm_count[:, k])

        # print(self.count_normalization)

        return self.matrix_set
