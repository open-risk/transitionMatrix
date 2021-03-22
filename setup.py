# encoding: utf-8

# (c) 2017-2020 Open Risk (https://www.openriskmanagement.com)
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


from codecs import open

from setuptools import setup

__version__ = '0.4.7'

ver = __version__

long_descr = open('docs/source/description.rst', 'r', encoding='utf8').read()

setup(name='transitionMatrix',
      version=ver,
      description='A Python powered library for statistical analysis and visualization of state transition phenomena',
      long_description=long_descr,
      author='Open Risk',
      author_email='info@openrisk.eu',
      packages=['transitionMatrix', 'transitionMatrix.estimators', 'transitionMatrix.utils', 
                #'tests',
                #'transitionMatrix.thresholds', 
                #'transitionMatrix.portfolio_model_lib', 
                #'datasets', 
                #'examples.python'
                ],
      include_package_data=True,
      url='https://github.com/open-risk/transitionMatrix',
      install_requires=[
          'pandas',
          'numpy',
          'scipy',
          'statsmodels',
          'sympy',
          'matplotlib'
      ],
      zip_safe=False,
      provides=['transitionMatrix'],
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Financial and Insurance Industry',
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ]

      )
