# encoding: utf-8

# (c) 2017-2019 Open Risk (https://www.openriskmanagement.com)
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

""" Converter utilities to help switch between various formats """

import pandas as pd


def datetime_to_float(dataframe):
    """
    .. _Datetime_to_float:

    Converts dates from string format to the canonical float format

    :param dataframe: Pandas dataframe with dates in string format
    :return: Pandas dataframe with dates in float format
    :rtype: object

    .. note:: The date string must be recognizable by the pandas to_datetime function.

    """
    start_date = dataframe['Time'].min()
    end_date = dataframe['Time'].max()
    total_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    dataframe['Time'] = dataframe['Time'].apply(lambda x: (pd.to_datetime(x) - pd.to_datetime(start_date)).days / total_days)
    return [start_date, end_date, total_days], dataframe
