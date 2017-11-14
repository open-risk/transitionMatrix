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

""" This module is part of the transitionMatrix package

"""
import numpy as np
import pandas as pd
from scipy.linalg import logm
import transitionMatrix as tm
import json


class TransitionMatrix(np.matrix):
    """ The TransitionMatrix object inherits from numpy matrices and implements transition matrix properties

    """
    def __new__(cls, values=None, dimension=2, json=None, csv=None):
        """ Create a new matrix. Different options for initialization are
        - using provided values as a list of list
        - using provided values as a numpy array
        - a default identity matrix
        - loading from a csv or json file
        NOTE: The initialization does not validate if the provided values form indeed a transition matrix
        """
        if values is not None:
            # Initialize with given values
            obj = np.asarray(values).view(cls)
        elif json is not None:
            # Initialize from file in json format
            q = pd.read_json(json)
            obj = np.asarray(q.values).view(cls)
        elif csv is not None:
            # Initialize from file in csv format
            q = pd.read_csv(csv, index_col=None)
            obj = np.asarray(q.values).view(cls)
        else:
            # Default instance (2x2 identity matrix)
            default = np.identity(dimension)
            obj = np.asarray(default).view(cls)
        obj.validated = False
        return obj

    def to_json(self, file):
        # Write to file in json format
        q = pd.DataFrame(self)
        q.to_json(file, orient='values')

    def to_csv(self, file):
        # Write to file in csv format
        q = pd.DataFrame(self)
        q.to_csv(file, index=None)

    def validate(self, accuracy=1e-3):
        """ Validate transition matrix
        1) check squareness
        2) check all values are probabilities (between 0 and 1)
        3) check all rows sum to one
        :returns List of tuples with validation messages
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
            return self.validated
        else:
            self.validated = False
            return validation_messages

    def generator(self, t=1.0):
        """ Compute the generator of a transition matrix

        """
        generator = logm(self) / t
        return generator

    def characterize(self):
        """ Analyse transition matrix
        1) diagonal dominance
        """
        # TODO further characterization
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

    # TODO implement matrix generation subject to various constraints
    def generate_random_matrix(self, n):
        pass

    def print(self):
        """ Pretty print a matrix

        """
        for s_in in range(self.shape[0]):
            for s_out in range(self.shape[1]):
                print("{0:.2f}%".format(self[s_in, s_out]) + ' ', end='')
            print('')
        print('')


class TransitionMatrixSet(object):
    """  The TransitionMatrices object stores a family of transition matrices as list


    """

    def __init__(self, dimension=2, values=None, periods=None, temporal_type=None, method=None, json=None, csv=None):
        """ Create a new matrix using provided values (or a default identity matrix)
        Temporal type
        Incremental: Each period matrix reflects transitions for that period
        Cumulative: Each period matrix reflects cumulative transitions from start to that period

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
            # Create a multi-period matrix assuming Markov Chain
            elif method is 'Power':
                val_set = []
                a = tm.TransitionMatrix(values)
                val_set.append(a)
                an = a
                for k in range(periods-1):
                    an = an*a
                    an = tm.TransitionMatrix(an)
                    val_set.append(an)
                self.entries = val_set
                self.temporal_type = 'Cumulative'
            # Use provided matrices as-is
            elif method is None:
                val_set = []
                for entry in values:
                    a = tm.TransitionMatrix(entry)
                    val_set.append(a)
                self.entries = val_set
                self.temporal_type = temporal_type
        else:
            # Default instance (2x2 identity matrix)
            # default = np.identity(dimension)
            val_set = []
            for k in range(periods):
                a = tm.TransitionMatrix(dimension=dimension)
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = 'Incremental'

        self.validated = False
        return

    def validate(self):
        """ Validate transition matrix set (validating individual entries)
        :returns List of tuples with validation messages
        """
        validation_messages = []
        for entry in self.entries:
            validation_messages.append(entry.validate())
        if all(validation_messages):
            self.validated = True
            return self.validated
        else:
            self.validated = False
            return validation_messages

    def cumulate(self):
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

    def incremental(self):
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
                anm1 = self.entries[k-1]
                anm1i = anm1.I
                a = anm1i * an
                a = tm.TransitionMatrix(a)
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = 'Incremental'
        return

    def print(self):
        for entry in self.entries:
            entry.print()

    def to_json(self, file=None):
        hold = []
        for k in range(len(self.entries)):
            hold.append(self.entries[k].tolist())
        serialized = json.dumps(hold, indent=2, separators=(',', ': '))
        if file is not None:
            file = open(file, 'w')
            file.write(serialized)
            file.close()

        return serialized

    def to_csv(self, file):
        pass


class StateSpace(object):
    """  The StateSpace object stores a state space structure as a List of tuples

    (value, description, optional, optional, ...)
    """
    # TODO approach to Absorbing States

    def __init__(self, description=[], sticky=False):
        # Description: List of tuples describing the state space
        self.description = description
        # The cardinality (size, number of states) of the state space
        self.cardinality = len(description)
        # Sticky = True, measurement data contain unchanged states
        # Default is False, only state changes are recorded
        # TODO Implement in estimators
        self.sticky = sticky

    def get_states(self):
        """ Return a list with the set of states

        """
        states = []
        for s in self.description:
            states.append(s[0])
        return states

    def get_state_labels(self):
        """
        Return a list of state descriptions
        """
        states = []
        for state in self.description:
            states.append(state[1])
        return states

    def generic(self, n=2):
        """
        Create a generic state space of size n
        """
        self.cardinality = n
        description = []
        for s in range(n):
            description.append((str(s), str(s)))
        self.description = description

    def validate_dataset(self, dataset, labels=None):
        """
        Check that dataset is consistend with a given state space
        1: all states in dataset exist in state space description (error otherwise)
        2: all states in state space exist in dataset (warning otherwise)
        3: successive states for the same entity are different, unless Sticky flag is True
        """
        if labels is not None:
            state_label = labels['State']
        else:
            state_label = 'State'

        dataset_states = dataset[state_label].unique()
        expected_states = []
        for state in self.description:
            expected_states.append(state[0])
        ds = set(dataset_states.tolist())
        es = set(expected_states)
        if ds.difference(es):
            validation_outcome = ds.difference(es)
            validation_message = "Dataset contains more states than expected. Check the following: "
        elif es.difference(ds):
            validation_outcome = es.difference(ds)
            validation_message = "Dataset contains fewer states than expected. Check the following: "
        else:
            validation_outcome = ''
            validation_message = "Dataset contains the expected states."

        return validation_message, validation_outcome

    def describe(self):
        for state in self.description:
            print("State Index/Label: ", state[0], " , ", state[1])
