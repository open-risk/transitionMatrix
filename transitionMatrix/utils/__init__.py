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

""" This module contains various helper classes and functions that do not fit
into any of the main modules of the library

"""

from __future__ import print_function, division

from .preprocessing import *
from .converters import *


def print_matrix(A, format_type='Standard', accuracy=2):
    """ Pretty print a matrix

    :param format_type: formatting options (Standard, Percent)
    :type format_type: str
    :param accuracy: number of decimals to display
    :type accuracy: int

    """
    for s_in in range(A.shape[0]):
        for s_out in range(A.shape[1]):
            if format_type is 'Standard':
                format_string = "{0:." + str(accuracy) + "f}"
                print(format_string.format(A[s_in, s_out]) + ' ', end='')
            elif format_type is 'Percent':
                print("{0:.2f}%".format(100 * A[s_in, s_out]) + ' ', end='')
        print('')
    print('')
