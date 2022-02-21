# encoding: utf-8

# (c) 2017-2022 Open Risk (https://www.openriskmanagement.com)
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

""" This module provides objects related to credit curves

* CreditCurve_ implements the functionality of a collection of credit (default curves)

"""

import numpy as np
import pandas as pd


class CreditCurve(np.matrix):
    """ The _`CreditCurve` object implements a typical collection of `credit curves <https://www.openriskmanual.org/wiki/Credit_Curve>`_.
    The class inherits from numpy matrices and implements additional properties specific to curves.

    """

    def __new__(cls, values=None, json_file=None, csv_file=None):
        """ Create a new credit curve set. Different options for initialization are:

        * providing values as a list of list
        * providing values as a numpy array  (The rows are the different curves, the columns are different periods)
        * loading from a csv file
        * loading from a json file

        Without data, a default identity matrix is generated with user specified dimension

        :param values: initialization values
        :param json_file: a json file containing transition matrix data
        :param csv_file: a csv file containing transition matrix data
        :type values: list of lists or numpy array
        :returns: returns a CreditCurve object
        :rtype: object

        .. note:: The initialization in itself does not validate if the provided values form indeed a credit curve

        :Example:

        .. code-block:: python

            A = tm.CreditCurve(values=[[0.1, 0.2, 0.3], [0.2, 0.6, 0.8], [0.01, 0.02, 0.06]])

        """
        obj = None
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
        # validation flag is set to False at initialization
        obj.validated = False
        # temporary dimension assignment (must validated for squareness)
        obj.dimension = obj.shape[0]
        return obj

    def to_json(self, file):
        """
        Write credit curves to file in json format

        :param file: json filename
        """

        q = pd.DataFrame(self)
        q.to_json(file, orient='values')

    def to_csv(self, file):
        """
        Write credit curves to file in csv format

        :param file: csv filename
        """

        q = pd.DataFrame(self)
        q.to_csv(file, index=False)

    def to_html(self, file=None):
        html_table = pd.DataFrame(self).to_html()
        if file is not None:
            file = open(file, 'w')
            file.write(html_table)
            file.close()
        return html_table

    def validate(self, accuracy=1e-3):
        """ Validate required properties of a credit curve set. The following are checked

        1. check that all values are probabilities (between 0 and 1)
        2. check that values are non-decreasing

        :param accuracy: accuracy level to use for validation
        :type accuracy: float

        :returns: List of tuples with validation messages
        """
        validation_messages = []

        curve_set = self
        curve_set_size = curve_set.shape[0]
        curve_set_periods = curve_set.shape[1]

        # checking that values of curve_set are within allowed range
        for i in range(curve_set_size):
            for j in range(curve_set_periods):
                if curve_set[i, j] < 0:
                    validation_messages.append(("Negative Probabilities: ", (i, j, curve_set[i, j])))
                if curve_set[i, j] > 1:
                    validation_messages.append(("Probabilities Larger than 1: ", (i, j, curve_set[i, j])))
        # checking monotonicity
        for i in range(curve_set_size):
            for j in range(1, curve_set_periods):
                if curve_set[i, j] < curve_set[i, j - 1]:
                    validation_messages.append(("Curve not monotonic: ", (i, j)))

        if len(validation_messages) == 0:
            self.validated = True
            return self.validated
        else:
            self.validated = False
            return validation_messages

    def hazard_curve(self):
        """ Compute hazard rates

        .. Todo:: Compute hazard rates

        :return: TODO

        """
        pass

    def characterize(self):
        """ Analyse or classify a credit curve according to its properties

        * slope of hazard rate

        .. Todo:: Further characterization

        """

        pass

    def print_curve(self, format_type='Standard', accuracy=2):
        """ Pretty print a set of credit curves

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
