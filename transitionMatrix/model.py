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
import os


class TransitionMatrix(np.matrix):
    """ The TransitionMatrix object inherits from numpy matrices and implements transition matrix properties

    """

    def __new__(cls, values=None, dimension=2, json_file=None, csv_file=None):
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

    def to_html(self, file):
        # TODO write matrix to html table format
        pass

    def fix_rowsums(self):
        # If the row sum is not identically unity, correct the diagonal element to enforce
        matrix = self
        matrix_size = matrix.shape[0]
        for i in range(matrix_size):
            diagonal = matrix[i, i]
            rowsum = matrix[i].sum()
            self[i, i] = diagonal + 1.0 - rowsum

    def fix_negativerates(self):
        # If a matrix entity is below zero, set to zero and correct the diagonal element to enforce
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
        """ Validate transition matrix
        1) check squareness
        2) check that all values are probabilities (between 0 and 1)
        3) check that all rows sum to one
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

    def print(self, format='Standard', accuracy=2):
        """ Pretty print a matrix

        """
        for s_in in range(self.shape[0]):
            for s_out in range(self.shape[1]):
                if format is 'Standard':
                    format_string = "{0:." + str(accuracy) + "f}"
                    print(format_string.format(self[s_in, s_out]) + ' ', end='')
                elif format is 'Percent':
                    print("{0:.2f}%".format(100 * self[s_in, s_out]) + ' ', end='')
            print('')
        print('')

    def remove(self, state, method):
        """ remove a transition matrix state and distribute its probability to other states according
        to prescribed method

        """
        new_matrix = tm.TransitionMatrix(dimension=self.shape[0]-1)
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
    """  The TransitionMatrices object stores a family of transition matrices as list


    """

    def __init__(self, dimension=2, values=None, periods=1, temporal_type=None, method=None, json_file=None, csv_file=None):
        """ Create a new matrix using provided values (or a default identity matrix)
        Parameters
        ----------
        temporal_type : str
            Incremental: Each period matrix reflects transitions for that period
            Cumulative: Each period matrix reflects cumulative transitions from start to that period

        Attributes
        ----------
        entries : str
            Human readable string describing the exception.
        temporal_type : str
            The temporal type of the set
        timesteps : list
            The timesteps of matrix observations

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
                self.timesteps = list(range(periods))
            # Create a multi-period matrix assuming Markov Chain
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
                self.timesteps = list(range(periods))
            # Use provided matrices as-is
            elif method is None:
                val_set = []
                for entry in values:
                    a = tm.TransitionMatrix(entry)
                    val_set.append(a)
                self.entries = val_set
                self.temporal_type = temporal_type
                self.timesteps = list(range(periods))
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
            self.timesteps = tenors
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
            self.timesteps = list(range(periods))
        else:
            # Default instance (2x2 identity matrix)
            # default = np.identity(dimension)
            val_set = []
            for k in range(periods):
                a = tm.TransitionMatrix(dimension=dimension)
                val_set.append(a)
            self.entries = val_set
            self.temporal_type = 'Incremental'
            self.timesteps = list(range(periods))

        self.validated = False
        return

    def __mul__(self, scale):
        """ Scale all entries by a factor
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
        :returns List of tuples with validation messages
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

    def print(self, format='Standard', accuracy=2):
        k = 0
        for entry in self.entries:
            print("Entry: ", k)
            entry.print(format=format, accuracy=accuracy)
            k +=1

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
