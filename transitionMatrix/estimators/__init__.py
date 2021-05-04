# encoding: utf-8

# (c) 2017-2021 Open Risk, all rights reserved
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


class BaseEstimator(object):

    """ Base class for implementing any transition matrix estimator

    Offers basic methods common to all estimators

    """

    def __init__(self):
        self.states = None
        self.matrix_set = []
        self.count_set = []
        self.count_normalization = []
        self.average_matrix = []
        self.ci_alpha = None
        self.ci_method = None
        self.confint_lower = None
        self.confint_upper = None
        self.counts = None
        self.nans = None

    def get_matrix_set(self):
        return self.matrix_set

    def print(self, select='Frequencies', period=None):
        """
        Pretty print the estimated transition matrices
        :return:
        """
        if select == 'Counts':
            if period is not None:
                print("Period: ", period)
                print("Starting Count: ")
                print(self.count_normalization[period])
                print("Migration Counts: ")
                print(self.count_set[period][:, :])
            else:
                for k in range(len(self.count_set)):
                    print("Period: ", k)
                    print("Starting Count: ")
                    print(self.count_normalization[k])
                    print("Migration Counts: ")
                    print(self.count_set[k][:, :])
        elif select == 'Frequencies':
            if period is not None:
                print("Period: ", period)
                print(self.matrix_set[period][:, :])
            else:
                for k in range(len(self.matrix_set)):
                    print("Period: ", k)
                    print(self.matrix_set[k][:, :])

        return

    def summary(self, k=0):
        """
        Pretty-print a summary of estimation results (values and confidence intervals)
        """
        if self.ci_method:
            state_count = self.states.cardinality
            print('                      Transition Matrix Estimation Results                    ')
            print('==============================================================================')
            print('Confidence Level: ', self.ci_alpha)
            print('Confidence Level Method: ', self.ci_method)
            print('------------------------------------------------------------------------------')
            print('Row  Col  Lower Bound      Value   Upper Bound')
            for s1 in range(state_count):
                for s2 in range(state_count):
                    lv = self.confint_lower[s1, s2, k]
                    rv = self.confint_upper[s1, s2, k]
                    cv = self.matrix_set[k][s1, s2]
                    print('{0:3} {1:4} {2:12f} {3:10f} {4:12f}'.format(s1, s2, lv, cv, rv))
                print('..............................................................................')
            print('==============================================================================')
        else:
            state_count = self.states.cardinality
            print('                      Transition Matrix Estimation Results                    ')
            print('==============================================================================')
            print('Row  Col  Value')
            for s1 in range(state_count):
                for s2 in range(state_count):
                    cv = self.matrix_set[k][s1, s2]
                    print('{0:3} {1:4} {2:10f}'.format(s1, s2, cv))
                print('..............................................................................')
            print('==============================================================================')
        return


class DurationEstimator(BaseEstimator):

    """ Base class for implementing any duration based transition matrix estimator

    Offers methods common to all duration based estimators
    Two subclasses:

    * Time homogeneous estimator (constant transition rates)
    * Time inhomogeneous estimator (variable transition probabilities) Aalen-Johansen

    T(s, t) = T(0, t)  (transition from start=0)
    Compute transition_times(k) T^ij(t) numpy(i,j,k)

    Transitions at cohort intervals
    Approximate numpy(i,j, k_index : largest k-value that is less than t(boundary))

    """

    def __init__(self, cohort_intervals=None, states=None):
        BaseEstimator.__init__(self)
        self.cohort_intervals = cohort_intervals
        if states is not None:
            self.states = states
        self.timepoint_count = None
