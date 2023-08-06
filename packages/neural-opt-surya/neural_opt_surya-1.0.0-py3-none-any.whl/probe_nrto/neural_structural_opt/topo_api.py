# lint as python3
# Copyright 2019 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=missing-docstring

import autograd.numpy as np
from . import topo_physics


def specified_task(problem):
  """Given a problem, return parameters for running a topology optimization."""
  fixdofs = np.flatnonzero(problem.normals.ravel())
  alldofs = np.arange(2 * (problem.nelx + 1) * (problem.nely + 1))
  freedofs = np.sort(list(set(alldofs) - set(fixdofs)))

  params = {
      # material properties
      'young': 1,
      'young_min': 1e-9,
      'poisson': 0.3,
      'g': 0,
      # constraints
      'volfrac': problem.density,
      'xmin': 0.001,
      'xmax': 1.0,
      # input parameters
      'nelx': problem.nelx,
      'nely': problem.nely,
      'mask': problem.mask,
      'width': problem.width,
      'height': problem.height,
      'freedofs': freedofs,
      'fixdofs': fixdofs,
      'forces': problem.forces.ravel(),
      'penal': 3.0,
      'filter_width': 2, # TODO: May need to change this!
  }
  return params


class Environment:

  def __init__(self, args):
    self.args = args
    self.ke = topo_physics.get_stiffness_matrix(self.args) 

  def reshape(self, params):
    return params.reshape(self.args['nely'], self.args['nelx'])
# Main difference :  Rendering designs accepts volume constraint  [hard] keyword
# Mostly for tounn models
  def render(self, params, volume_contraint=True, cone_filter = True,
             den_proj=False, beta=1):
    return topo_physics.physical_density(
        self.reshape(params), self.args, volume_contraint=volume_contraint,
                                        cone_filter = cone_filter, den_proj=den_proj,
                                        beta =beta)

  def objective(self, params, volume_contraint=False, cone_filter=True, p=3.0,
                den_proj=False, beta=1):
    return topo_physics.objective(
                self.reshape(params), self.ke, self.args,
                volume_contraint=volume_contraint, cone_filter=cone_filter, p=p,
                den_proj = den_proj, beta=beta)

  def constraint(self, params, den_proj =False, beta=1):
    volume = topo_physics.mean_density(self.reshape(params), self.args, den_proj =den_proj,
                                       beta=1)
    return volume - self.args['volfrac']
