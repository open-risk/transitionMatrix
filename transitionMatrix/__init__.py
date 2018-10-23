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


""" transitionMatrix - Python package for statistical analysis and visualization of state space transition events """

from .model import *
from .estimators import *
from .utils import *
from .thresholds import *
from .portfolio_model_lib import *

__version__ = '0.4.0'

package_name = 'transitionMatrix'
module_path = os.path.dirname(__file__)
source_path = module_path[:-len(package_name)]
dataset_path = os.path.join(source_path, '/datasets/')
