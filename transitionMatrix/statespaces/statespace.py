# encoding: utf-8

# (c) 2017-2024 Open Risk (https://www.openriskmanagement.com)
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

""" StateSpace holds information about the stochastic system state space


"""


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

    def __init__(self, definition=None, sticky=False, absorbing=None, originator=None, full_name=None, cqs_mapping=None,
                 transition_data=None):
        """

        :param definition: List of tuples describing the state space
        :param sticky: Sticky = True, measurement data may contain repeat measurements of unchanged states. The default is False, only state changes are recorded
        :param absorbing: List of states that are absorbing
        :param originator: Name of entity defining the State Space (e.g. A Credit Rating Agency)
        :param full_name: Full (formal) name for the State Space (e.g. Concrete Credit Rating Scale)
        :param cqs_mapping: For credit ratings that have a mapping to the simplified EU CQS Scale
        :param transition_data: pandas dataframe with transition data

        """

        if transition_data is not None:
            if definition is None and transition_data.empty:
                definition = []  # allow empty state space
            elif not transition_data.empty and not definition:
                definition = self._infer(transition_data)  # construct from data
            elif not transition_data.empty and definition:
                pass  # explicitly defined state space overrules implicit from data

        if definition:
            self.definition = definition
        else:
            definition = []

        self.cardinality = len(definition)
        self.sticky = sticky
        self.absorbing = absorbing
        self.originator = originator
        self.full_name = full_name
        self.cqs_mapping = cqs_mapping

    def _infer(self, transition_data):
        """ Infer the state space from the data. This uses the State column by default and does an automated sorting by default.

        :return: Definition list

        .. warning: If the state space include ascii characters the order will be arbitrary. If it is important for presentation purposes it needs to be adjusted manually (see examples/python/data_cleaning_example.py)
        """
        unique_states = sorted(transition_data['State'].unique())

        definition = []
        i = 0
        for s in unique_states:
            state = (i, s)
            definition.append(state)
            i += 1
        return definition

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

        1: all the states in dataset exist in the state space description (error otherwise)
        2: all the states in state space exist in dataset (warning otherwise)
        3: TODO successive states for the same entity are different, unless the Sticky flag is True

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
        # print(state_list_stringified)
        ds = set(state_list_stringified)
        # The expected states according to the state space
        expected_states = []
        for state in self.definition:
            expected_states.append(state[1])
        es = set(expected_states)

        if ds.difference(es):
            validation_outcome = ds.difference(es)
            print('Found ', ds)
            print('Expected', es)
            validation_message = "Dataset contains more states than expected. Check the following: " + str(
                validation_outcome)
        elif es.difference(ds):
            validation_outcome = es.difference(ds)
            validation_message = "Dataset contains fewer states than expected. Check the following: " + str(
                validation_outcome)
        else:
            validation_outcome = ''
            validation_message = "Dataset contains the expected states."

        return validation_message, validation_outcome

    def describe(self):
        """
        Print the State Space description

        """
        print(80 * '=')
        if self.full_name:
            print('State Space: ', self.full_name)
        else:
            print('State Space')
        print(80 * '-')
        for state in self.definition:
            print("State Index and Label: ", state[0], ", ", state[1])
        print(80 * '-')

    def cqs_map(self, label):
        """
        Produce a CQS for a given input label (the cqs_mapping dictionary must exist)

        """
        mapped = None
        for x in self.definition:
            if x[1] == label:
                mapped = self.cqs_mapping[x[0]]
        if mapped:
            return mapped
        else:
            print("ERROR: Mapping failed")
