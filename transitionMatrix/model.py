# encoding: utf-8

# (c) 2017-2018 Open Risk (https://www.openriskmanagement.com)
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

""" This module provides the key transition matrix objects

* TransitionMatrix_ implements the functionality of single period transition matrix
* TransitionMatrixSet_ provides a container for a multiperiod transition matrix collection
* StateSpace holds information about the stochastic system state space
* EmpiricalTransitionMatrix implements the functionality of a continuously observed transition matrix

"""

import json
import os

import numpy as np
import pandas as pd
from scipy.linalg import logm

import transitionMatrix as tm


class TransitionMatrix(np.matrix):
    """ The _`TransitionMatrix` object implements a typical (one period) `transition matrix <https://www.openriskmanual.org/wiki/Transition_Matrix>`_.
    The classs inherits from numpy matrices and implements additional properties specific transition matrices. It form the building block of the
    TransitionMatrixSet_ which holds a collection of matrices in increasing temporal order

    """

    def __new__(cls, values=None, dimension=2, json_file=None, csv_file=None):
        """ Create a new transition matrix. Different options for initialization are:

        * providing values as a list of list
        * providing values as a numpy array
        * loading from a csv file
        * loading from a json file

        Without data, a default identity matrix is generated with user specified dimension

        :param values: initialization values
        :param dimension: matrix dimensionality (default is 2)
        :param json_file: a json file containing transition matrix data
        :param csv_file: a csv file containing transition matrix data
        :type values: list of lists or numpy array
        :type dimension: int
        :returns: returns a TransitionMatrix object
        :rtype: object

        .. note:: The initialization in itself does not validate if the provided values form indeed a transition matrix

        :Example:

        .. code-block:: python

            A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])

        """
        if values is not None:
            # Initialize with given values
            obj = np.asarray(values).view(cls)
        elif json_file is not None:
            # Initialize from file in json format
            q = pd.read_json(json_file)
            obj = np.asarray(q.values).view(cls)
        elif csv_file is not None:
            # Initialize from file in csv format
            q = pd.read_csv(csv_file, index_col=None)
            obj = np.asarray(q.values).view(cls)
        else:
            # Default instance (2x2 identity matrix)
            default = np.identity(dimension)
            obj = np.asarray(default).view(cls)
        # validation flag is set to False at initialization
        obj.validated = False
        # temporary dimension assignment (must validated for squareness)
        obj.dimension = obj.shape[0]
        return obj

    def to_json(self, file):
        """
        Write transition matrix to file in json format

        :param file: json filename
        """

        q = pd.DataFrame(self)
        q.to_json(file, orient='values')

    def to_csv(self, file):
        """
        Write transition matrix to file in csv format

        :param file: csv filename
        """

        q = pd.DataFrame(self)
        q.to_csv(file, index=None)

    def to_html(self, file=None):
        html_table = pd.DataFrame(self).to_html()
        if file is not None:
            file = open(file, 'w')
            file.write(html_table)
            file.close()
        return html_table

    def fix_rowsums(self):
        """
        If the row sum is not identically unity, correct the diagonal element to enforce

        """

        matrix = self
        matrix_size = matrix.shape[0]
        for i in range(matrix_size):
            diagonal = matrix[i, i]
            rowsum = matrix[i].sum()
            self[i, i] = diagonal + 1.0 - rowsum

    def fix_negativerates(self):
        """
        If a matrix entity is below zero, set to zero and correct the diagonal element to enforce

        """

        matrix = self
        matrix_size = matrix.shape[0]
        # For all rows
        for i in range(matrix_size):
            maxval_index = self[i].argmax()
            row_adjust = 0.0
            # Search all cols for negative entries
            for j in range(matrix_size):
                if matrix[i, j] < 0.0:
                    row_adjust += matrix[i, j]
                    self[i, j] = 0.0
            # Add the adjustment to the diagonal
            self[i, maxval_index] += row_adjust

    def validate(self, accuracy=1e-3):
        """ Validate required properties of a transition matrix. The following are checked

        1. check squareness
        2. check that all values are probabilities (between 0 and 1)
        3. check that all rows sum to one

        :param accuracy: accuracy level to use for validation
        :type accuracy: float

        :returns: List of tuples with validation messages
        """
        validation_messages = []

        matrix = self
        # checking squareness of matrix
        if matrix.shape[0] != matrix.shape[1]:
            validation_messages.append(("Matrix Dimensions Differ: ", matrix.shape))
        else:
            matrix_size = matrix.shape[0]
            # checking that values of matrix are within allowed range
            for i in range(matrix_size):
                for j in range(matrix_size):
                    if matrix[i, j] < 0:
                        validation_messages.append(("Negative Probabilities: ", (i, j, matrix[i, j])))
                    if matrix[i, j] > 1:
                        validation_messages.append(("Probabilities Larger than 1: ", (i, j, matrix[i, j])))
            # checking row sums of matrix
            for i in range(matrix_size):
                rowsum = matrix[i].sum()
                if abs(rowsum - 1.0) > accuracy:
                    validation_messages.append(("Rowsum not equal to one: ", (i, rowsum)))

        if len(validation_messages) == 0:
            self.validated = True
            self.dimension = matrix.shape[0]
            return self.validated
        else:
            self.validated = False
            return validation_messages

    def generator(self, t=1.0):
        """ Compute the generator of a transition matrix

        :param t: the timescale parameter
        :type t: float

        :Example:

        G = A.generator()
        """
        generator = logm(self) / t
        return generator

    def characterize(self):
        """ Analyse or classify a transition matrix according to its properties

        * diagonal dominance

        .. Todo:: Further characterization
        """

        outcome_messages = []
        if self.validated is True:
            matrix = self
            matrix_size = matrix.shape[0]
            dominance = True
            for i in range(matrix_size):
                if matrix[i, i] < 0.5:
                    dominance = False
            if dominance:
                outcome_messages.append("Diagonally Dominant")
            else:
                outcome_messages.append("Not Diagonally Dominant")
        else:
            outcome_messages.append("Not a validated matrix. Use matrix.validate()")
        return outcome_messages

    def generate_random_matrix(self):
        """

        .. Todo:: Implement matrix generation subject to various constraints
        """
        pass

    def print(self, format_type='Standard', accuracy=2):
        """ Pretty print a transition matrix

        :param format_type: formatting options (Standard, Percent)
        :type format_type: str
        :param accuracy: number of decimals to display
        :type accuracy: int

        """
        for s_in in range(self.shape[0]):
            for s_out in range(self.shape[1]):
                if format_type is 'Standard':
                    format_string = "{0:." + str(accuracy) + "f}"
                    print(format_string.format(self[s_in, s_out]) + ' ', end='')
                elif format_type is 'Percent':
                    print("{0:.2f}%".format(100 * self[s_in, s_out]) + ' ', end='')
            print('')
        print('')

    def remove(self, state, method):
        """ Remove a transition matrix state and distribute its probability to other states according
        to prescribed method

        :param state: the state to remove
        :type state: int

        :returns: a transition matrix

        """
        new_matrix = tm.TransitionMatrix(dimension=self.shape[0] - 1)
        states = list(range(self.shape[0]))
        del states[state]
        # process all rows of the matrix except the state we remove
        for i in states:
            # probability to distribute
            xp = self[i, state]
            if 0.0 < xp < 1.0:
                # process all columns of the matrix except the state we remove
                w = xp / (1.0 - xp)
                for j in states:
                    # weight of state among remaining states
                    new_matrix[i, j] = self[i, j] * (1.0 + w)
        return new_matrix


class TransitionMatrixSet(object):
    """  The _`TransitionMatrixSet` object stores a family of TransitionMatrix_ objects as a time ordered list. Besides
    storage it allows a variety of simultaneous operations on the collection of matrices


    """

    def __init__(self, dimension=2, values=None, periods=1, temporal_type=None, method=None, json_file=None,
                 csv_file=None):
        """ Create a new matrix set. Different options for initialization are:

        * providing values as a list of list
        * providing values as a numpy array
        * loading from a csv file
        * loading from a json file

        Without data, a default identity matrix is generated with user specified dimension

        :param values: initialization values
        :param dimension: matrix dimensionality (default is 2)
        :param method: matrix dimensionality (default is 2)
        :param periods: List with the timesteps of matrix observations
        :param temporal_type: matrix dimensionality (default is 2)

        * Incremental: Each period matrix reflects transitions for that period
        * Cumulative: Each period matrix reflects cumulative transitions from start to that period

        :param json_file: a json file containing transition matrix data
        :param csv_file: a csv file containing transition matrix data

        :type values: list of lists or numpy array
        :type dimension: int
        :type temporal_type: str
        :type json_file: str
        :type csv_file: str

        :returns: returns a TranstionMatrix object
        :rtype: object

        .. note:: The initialization in itself does not validate if the provided values form indeed a transition matrix set

        :Example:

        Instantiate a transition matrix set directly using a list of matrices

        .. code-block:: python

            C_Vals = [[[0.75, 0.25], [0.0, 1.0]],  [[0.75, 0.25], [0.0, 1.0]]]

            C_Set = tm.TransitionMatrixSet(values=C_Vals, temporal_type='Incremental')

        """

        if values is not None:
            # Copy a single matrix to all periods
            if method is 'Copy':
                val_set = []
                for k in range(periods):
                    a = tm.TransitionMatrix(values)
                    val_set.append(a)
                self.entries = val_set
                self.temporal_type = 'Incremental'
                self.periods = list(range(periods))
                self.dimension = val_set[0].shape[0]
            # Create a multi-period matrix assuming a Markov Chain
            elif method is 'Power':
                val_set = []
                a = tm.TransitionMatrix(values)
                val_set.append(a)
                an = a
                for k in range(periods - 1):
                    an = an * a
                    an = tm.TransitionMatrix(an)
                    val_set.append(an)
                self.entries = val_set
                self.temporal_type = 'Cumulative'
                self.periods = list(range(periods))
                self.dimension = val_set[0].shape[0]
            # Use provided matrices as-is
            elif method is None:
                val_set = []
                for entry in values:
                    a = tm.TransitionMatrix(entry)
                    val_set.append(a)
                self.entries = val_set
                self.temporal_type = temporal_type
                self.periods = list(range(periods))
                self.dimension = val_set[0].shape[0]
        elif values is None and csv_file is not None:
            # Initialize from file in csv format
            # First row is meta data labels (From States, To States, Periods, Tenor List)
            # Second row is meta data values (comma separated)
            # Subsequent rows are Periods x Matrices in sequence
            if not os.path.isfile(csv_file):
                print("Input File Does not Exist")
                exit()
            f = open(csv_file)
            header_dict = f.readline()
            header_data = f.readline().split(',')
            val_set = []
            from_states = int(header_data.pop(0))
            to_states = int(header_data.pop(0))
            periods = int(header_data.pop(0))
            tenors = [int(x) for x in header_data]
            q = pd.read_csv(f, header=None, usecols=range(to_states))
            for k in range(periods):
                raw = q.iloc[k * from_states:(k + 1) * from_states]
                a = tm.TransitionMatrix(raw.as_matrix())
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = temporal_type
            self.periods = tenors
            self.dimension = val_set[0].shape[0]
            f.close()
        elif values is None and json_file is not None:
            # Initialize from file in json format
            if not os.path.isfile(json_file):
                print("Input File Does not Exist")
                exit()
            val_set = []
            q = json.load(open(json_file))
            periods = len(q)
            for k in range(periods):
                a = tm.TransitionMatrix(q[k])
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = temporal_type
            self.periods = list(range(periods))
            self.dimension = val_set[0].shape[0]
        else:
            # Default instance (2x2 identity matrix)
            # default = np.identity(dimension)
            val_set = []
            for k in range(periods):
                a = tm.TransitionMatrix(dimension=dimension)
                val_set.append(a)
            self.entries = val_set
            if temporal_type is not None:
                self.temporal_type = temporal_type
            else:
                self.temporal_type = 'Incremental'
            self.periods = list(range(periods))
            self.dimension = 2

        self.validated = False
        return

    def __mul__(self, scale):
        """ Scale all entries of the set by a factor


        """
        scaled = self
        val_set = []
        for entry in self.entries:
            a = entry * scale
            val_set.append(a)
        scaled.entries = val_set
        return scaled

    def validate(self):
        """ Validate transition matrix set (validating individual entries)

        :returns: List of tuples with validation messages
        """
        validation_messages = []
        validation_status = []
        for entry in self.entries:
            validation_messages.append(entry.validate())
            validation_status.append(entry.validated)
        if all(validation_status):
            self.validated = True
            return self.validated
        else:
            self.validated = False
            return validation_messages

    def cumulate(self):
        """ Cumulate a transition matrix set from an incremental set

        """
        if self.temporal_type is 'Cumulative':
            print("Transition Matrix Set is already cumulated")
            return
        else:
            val_set = []
            periods = len(self.entries)
            a = self.entries[0]
            val_set.append(a)
            an = a
            for k in range(periods - 1):
                an = an * a
                an = tm.TransitionMatrix(an)
                val_set.append(an)
            self.entries = val_set
            self.temporal_type = 'Cumulative'
        return

    def remove(self, state, method):
        """ remove a transition matrix state and distribute its probability to other states according
        to prescribed method

        """
        updated = self
        val_set = []
        for entry in self.entries:
            a = entry.remove(state, method)
            val_set.append(a)
        updated.entries = val_set
        return updated

    def incremental(self):
        """ Create an incremental transition matrix set from a cumulative set

        """
        if self.temporal_type is 'Incremental':
            print("Transition Matrix Set is already incremental")
            return
        else:
            val_set = []
            periods = len(self.entries)
            anm1 = self.entries[0]
            val_set.append(anm1)
            for k in range(1, periods):
                an = self.entries[k]
                anm1 = self.entries[k - 1]
                anm1i = anm1.I
                a = anm1i * an
                a = tm.TransitionMatrix(a)
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = 'Incremental'
        return

    def print_matrix(self, format_type='Standard', accuracy=2):
        """ Pretty Print a Transition Matrix Set

        """
        k = 0
        for entry in self.entries:
            print("Entry: ", k)
            entry.print(format_type=format_type, accuracy=accuracy)
            k += 1

    def to_json(self, file=None, accuracy=5):
        hold = []
        for k in range(len(self.entries)):
            entry = np.around(self.entries[k], accuracy)
            hold.append(entry.tolist())
        serialized = json.dumps(hold, indent=2, separators=(',', ': '))
        if file is not None:
            file = open(file, 'w')
            file.write(serialized)
            file.close()

        return serialized

    def to_csv(self, file):
        pass

    def to_html(self, file=None):
        table_set = ''
        for table in self.entries:
            html_table = pd.DataFrame(table).to_html()
            table_set += html_table
        if file is not None:
            file = open(file, 'w')
            file.write(table_set)
            file.close()
        return table_set

    def default_curves(self, rating):
        """ Calculate the incremental probability of crossing the absorbing barrier,
        and the corresponding cumulative probabilities, hazard rates and survival rates

        """

        # TODO Make absorbing state an attribute of Matrix and MatrixSet
        # Default state hardwired to be highest matrix element
        Default = self.entries[0].dimension - 1
        Periods = len(self.periods)

        iPD = np.zeros(Periods)
        cPD = np.zeros(Periods)
        hR = np.zeros(Periods)
        sR = np.zeros(Periods)
        if self.temporal_type is 'Cumulative':
            for k in range(0, Periods):
                cPD[k] = self.entries[k][rating, Default]
                sR[k] = 1.0 - cPD[k]
            iPD[0] = cPD[0]
            hR[0] = cPD[0]
            for k in range(1, Periods):
                iPD[k] = cPD[k] - cPD[k - 1]
                hR[k] = iPD[k] / (1.0 - cPD[k - 1])
        elif self.temporal_type is 'Incremental':
            pass
        return iPD, cPD, hR, sR


class StateSpace(object):
    """  The StateSpace object stores a state space structure as a List of tuples
    The first two elements of each tuple contain the index (base-0) and label of the
    state space respectively.

    Additional fields reserved for further characterisation

    [(index 1, label 1, optional, optional, ...),
     (index 2, label 2, optional, optional, ...)]

    .. Todo:: Implement Absorbing States

    .. Todo:: Implement in estimators

    """

    def __init__(self, definition=[], sticky=False, absorbing=None, originator=None, full_name=None, cqs_mapping=None):
        """

        :param definition: List of tuples describing the state space
        :param sticky: Sticky = True, measurement data contain unchanged states. The default is False, only state changes are recorded
        :param absorbing: List of states that are absorbing
        :param originator: Name of entity defining the State Space (e.g. A Credit Rating Agency)
        :param full_name: Full (formal) name for the State Space (e.g. Concrete Credit Rating Scale)
        :param cqs_mapping: For credit ratings that have a mapping to the simplified EU CQS Scale

        """
        # Description:
        self.definition = definition
        # The cardinality (size, number of states) of the state space
        self.cardinality = len(definition)

        self.sticky = sticky
        self.absorbing = absorbing

        self.originator = originator
        self.full_name = full_name
        self.cqs_mapping = cqs_mapping

    def get_states(self):
        """ Return a list with the set of states

        """
        states = []
        for s in self.definition:
            states.append(s[0])
        return states

    def get_state_labels(self):
        """ Return a list of state descriptions

        """
        states = []
        for state in self.definition:
            states.append(state[1])
        return states

    def generic(self, n=2):
        """ Create a generic state space of size n

        """
        self.cardinality = n
        description = []
        for s in range(n):
            description.append((str(s), str(s)))
        self.definition = description

    def validate_dataset(self, dataset, labels=None):
        """  Check that a dataset column is consistent with a given state space. The following tests are implemented

        1: all the states in dataset exist in state space description (error otherwise)
        2: all the states in state space exist in dataset (warning otherwise)
        3: successive states for the same entity are different, unless the Sticky flag is True

        :param dataset: the dataset to test
        :param labels: the labels of the state space

        :returns: a list of validation messages

        """

        # Select the appropriate State label
        # This covers for case of relabeling or multiple columns with state data
        if labels is not None:
            state_label = labels['State']
        else:
            state_label = 'State'

        # The unique states in the data set
        dataset_states = dataset[state_label].unique()
        state_list = dataset_states.tolist()
        state_list_stringified = [str(s) for s in state_list]
        print(state_list_stringified)
        ds = set(state_list_stringified)
        # The expected states according to the state space
        expected_states = []
        for state in self.definition:
            expected_states.append(state[0])
        es = set(expected_states)
        if ds.difference(es):
            validation_outcome = ds.difference(es)
            print('Found ', ds)
            print('Expected', es)
            validation_message = "Dataset contains more states than expected. Check the following: "
        elif es.difference(ds):
            validation_outcome = es.difference(ds)
            validation_message = "Dataset contains fewer states than expected. Check the following: "
        else:
            validation_outcome = ''
            validation_message = "Dataset contains the expected states."

        return validation_message, validation_outcome

    def describe(self):
        """
        Print the State Space description

        """
        for state in self.definition:
            print("State Index/Label: ", state[0], " , ", state[1])


class EmpiricalTransitionMatrix(object):
    """  The EmpiricalTransitionMatrix object stores a continuously observed Transition Matrix. It stores matrices
    estimated using duration methods

    The EmpiricalTransitionMatrix object is different from the TransitionMatrixSet in that it stores detailed event time
    of observations and the transition densities in addition to the transition probabilities

    An EmpiricalTransitionMatrix can be converted into a TransitionMatrixSet by sampling on a temporal grid (but not
    vice-versa)


    """

    def __init__(self, dimension=2, values=None, observation_times=None, json_file=None,
                 csv_file=None):
        """ Create a new probability matrix. Different options for initialization are:

        * providing values as a 3D numpy array of signature (S, S, T) and observation times as a list or numpy array of length T
        * loading from a csv file
        * loading from a json file

        Without data, a default identity matrix is generated with user specified dimension

        :param values: initialization values
        :param dimension: matrix dimensionality (default is 2)
        :param observation_times: List with the timesteps (support) of transition observations
        :param json_file: a json file containing transition matrix data
        :param csv_file: a csv file containing transition matrix data

        :type values: 3D numpy array
        :type dimension: int
        :type observations: int
        :type json_file: str
        :type csv_file: str

        :returns: returns a EmpiricalTransitionMatrix object
        :rtype: object

        .. note:: The initialization in itself does not validate if the provided values form indeed a transition matrix set

        :Example:

        Instantiate a transition probability matrix

        .. code-block:: python

        """

        self.values = values
        self.observation_times = observation_times

        return
