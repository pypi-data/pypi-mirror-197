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
"""A suite of topology optimization problems."""
from typing import Optional, Union

import dataclasses

import numpy as np
import skimage.draw
import sys

X, Y = 0, 1


@dataclasses.dataclass
class Problem:
  """Description of a topology optimization problem.

  Attributes:
    normals: float64 array of shape (width+1, height+1, 2) where a value of 1
      indicates a "fixed" coordinate, and 0 indicates no normal force.
    forces: float64 array of shape (width+1, height+1, 2) indicating external
      applied forces in the x and y directions.
    density: fraction of the design region that should be non-zero.
    mask: scalar or float64 array of shape (height, width) that is multiplied by
      the design mask before and after applying the blurring filters. Values of
      1 indicate regions where the material can be optimized; values of 0 are
      constrained to be empty.
    name: optional name of this problem.
    width: integer width of the domain.
    height: integer height of the domain.
    mirror_left: should the design be mirrored to the left when displayed?
    mirror_right: should the design be mirrored to the right when displayed?
    nelx: Number of elements in the FEM grid along width
    nely: Number of elements in the FEM grid along height
  """
  normals: np.ndarray
  forces: np.ndarray
  density: float
  width: int =  2 # Domain size
  height: int = 1 # Domain size
  mask: Union[np.ndarray, float] = 1
  name: Optional[str] = None
  nelx: int = dataclasses.field(init=False)
  nely: int = dataclasses.field(init=False)
  mirror_left: bool = dataclasses.field(init=False)
  mirror_right: bool = dataclasses.field(init=False)

  def __post_init__(self):
    self.nelx = self.normals.shape[0] - 1
    self.nely = self.normals.shape[1] - 1
    print("nely has been set to {}".format(self.nely))
    
    if self.normals.shape != (self.nelx + 1, self.nely + 1, 2):
      raise ValueError(f'normals has wrong shape: {self.normals.shape}')
    if self.forces.shape != (self.nelx + 1, self.nely + 1, 2):
      raise ValueError(f'forces has wrong shape: {self.forces.shape}')
    if (isinstance(self.mask, np.ndarray)
        and self.mask.shape != (self.nelx, self.nely)):
      raise ValueError(f'mask has wrong shape: {self.mask.shape}')

    self.mirror_left = (
        self.normals[0, :, X].all() and not self.normals[0, :, Y].all()
    )
    self.mirror_right = (
        self.normals[-1, :, X].all() and not self.normals[-1, :, Y].all()
    )

def cantilever_beam_two_point(  # checked # problem parameters changed from hoyer's
    nelx=64, density=0.15, width = 64, height =32, support_position=0.0,
    force_position=0.5):
  """Cantilever supported by two points. For fine features"""
  # https://link.springer.com/content/pdf/10.1007%2Fs00158-010-0557-z.pdf
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[0, round(nely*(1-support_position)), :] = 1
  normals[0, round(nely*support_position), :] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[-1, round((1 - force_position)*nely), Y] = -1

  return Problem(normals, forces, density, width, height, 1,'cantilever_fine')

def tensile_rod(
    nelx=64, density=0.2, width = 64, height =32, force_position=0.5): # Newly added
  """Cantilever supported with a tensile load at the end intended to produce a rod like structure"""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[0, :, :] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[-1, round((1 - force_position)*nely), X] = 1

  return Problem(normals, forces, density, width, height, 1, 'tensile_rod')

def causeway_bridge(nelx=64, density=0.1, width = 64, height =64, deck_level=0.5): #checked
  """A bridge supported by columns at a regular interval."""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[-1, -1, Y] = 1
  normals[-1, :, X] = 1
  normals[0, :, X] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[:, round(nely * (1 - deck_level)), Y] = -1 / nelx
  return Problem(normals, forces, density, width, height, 1, 'causeway_bridge')


def mbb_beam(nelx=64, density=0.2, width = 64, height =32): # checked!
  """Textbook beam example."""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")  
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[-1, -1, Y] = 1
  normals[0, :, X] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[0, 0, Y] = -1

  return Problem(normals, forces, density, width, height, 1 ,'mbb')

def l_shape(nelx=64, density=0.1, width = 64,
            height =64, aspect=0.4, force_position=0.5): # checked
  """An L-shaped structure, with a limited design region."""
  # Topology Optimization Benchmarks in 2D
  # Doesn't work for assymetrical width and height
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[:round(aspect*nelx), 0, :] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[-1, round((1 - aspect*force_position)*nely), Y] = -1

  mask = np.ones((nelx, nely))
  mask[round(nely*aspect):, :round(nelx*(1-aspect))] = 0

  return Problem(normals, forces, density, width, height, mask.T, 'lshape')

def dam(nelx=64, density=0.25, width = 32, height =64):
  """Support horizitonal forces, proportional to depth."""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[:, -1, X] = 1
  normals[:, -1, Y] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[0, :, X] = 2 * np.arange(1, nely+2) / nely ** 2
  return Problem(normals, forces, density, width, height, 1, 'dam')

def multistory_building(nelx=64, density=0.3, width = 32, height =64, interval=32):
  """A multi-story building, supported from the ground."""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[:, -1, Y] = 1
  normals[-1, :, X] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[:, ::interval, Y] = -1 / nelx
  return Problem(normals, forces, density, width, height, 1,'multistory')

def michell_centered_both(nelx=64, density=0.1, 
                          width = 64, height =32, position=0.05):#checked
  """A single force down at the center, with support from the side."""
  # https://en.wikipedia.org/wiki/Michell_structures#Examples
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[round(position*nelx), round(nely/2), Y] = 1
  normals[-1, :, X] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[-1, round(nely/2), Y] = -1

  return Problem(normals, forces, density, width, height, 1, "michell")

def pure_bending_moment( # checked
    nelx=64, density=0.15, width = 32, height =16, support_position=0.45):
  """Pure bending forces on a beam."""
  # Figure 28 from
  # http://naca.central.cranfield.ac.uk/reports/arc/rm/3303.pdf
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[-1, :, X] = 1
  # for numerical stability, fix y forces here at 0
  normals[0, round(nely*(1-support_position)), Y] = 1
  normals[0, round(nely*support_position), Y] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  forces[0, round(nely*(1-support_position)), X] = 1
  forces[0, round(nely*support_position), X] = -1

  return Problem(normals, forces, density, width, height, 1, 'bending')

def staggered_points(nelx=32, density=0.3, width = 32, height =16, interval=16,
                      break_symmetry=False):
  """A staggered grid of points with downward forces, supported from below."""
  nely = int(height*nelx/width)
  try:
      assert nely == height*nelx/width
  except:
      sys.exit("nely is not an integer")
  normals = np.zeros((nelx + 1, nely + 1, 2))
  normals[:, -1, Y] = 1
  normals[0, :, X] = 1
  normals[-1, :, X] = 1

  forces = np.zeros((nelx + 1, nely + 1, 2))
  f = interval ** 2 / (nelx * nely)
  # intentionally break horizontal symmetry?
  forces[interval//2+int(break_symmetry)::interval, ::interval, Y] = -f
  forces[int(break_symmetry)::interval, interval//2::interval, Y] = -f
  return Problem(normals, forces, density, width, height,1, 'staggered')


PROBLEMS_BY_NAME = {'tensile_rod': tensile_rod, 
                    'causeway_bridge' : causeway_bridge, 
                    'cantilever_fine': cantilever_beam_two_point,
                    'michell': michell_centered_both,
                    'mbb':mbb_beam,
                    'lshape':l_shape,
                    'dam':dam,
                    'multistory':multistory_building,
                    'bending': pure_bending_moment,
                    'staggered': staggered_points}

# def cantilever_beam_full(
#     nelx=60, density=0.5, width = 2, height =1, force_position=0): # Checked
#   """Cantilever supported everywhere on the left."""
#   # https://link.springer.com/content/pdf/10.1007%2Fs00158-010-0557-z.pdf
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[0, :, :] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[-1, round((1 - force_position)*nely), Y] = -1

#   return Problem(normals, forces, density, width, height)



# def michell_centered_both(nelx=32, density=0.5, width = 2, height =1, position=0.05):#checked
#   """A single force down at the center, with support from the side."""
#   # https://en.wikipedia.org/wiki/Michell_structures#Examples
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[round(position*nelx), round(nely/2), Y] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[-1, round(nely/2), Y] = -1

#   return Problem(normals, forces, density, width, height)


# def michell_centered_below(nelx=32, density=0.5, width = 2, height =1, position=0.25): # checked
#   """A single force down at the center, with support from the side below."""
#   # https://en.wikipedia.org/wiki/Michell_structures#Examples
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[round(position*nelx), 0, Y] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[-1, 0, Y] = -1

#   return Problem(normals, forces, density, width, height)


# def ground_structure(nelx=32, density=0.5, width = 2, height =1, force_position=0.5): # checkdd
#   """An overhanging bridge like structure holding up two weights."""
#   # https://link.springer.com/content/pdf/10.1007%2Fs00158-010-0557-z.pdf
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[-1, :, X] = 1
#   normals[0, -1, :] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[round(force_position*nely), -1, Y] = -1

#   return Problem(normals, forces, density, width, height)


# def crane(nelx=32, density=0.3, width = 1, height =1, aspect=0.5, force_position=0.9):# checked
#   """A crane supporting a downward force, anchored on the left."""
#   # Needs a symmetric physical domain
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, :] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[round(force_position*nelx), round(1-aspect*nely), Y] = -1

#   mask = np.ones((nelx, nely))
#   # the extra +2 ensures that entire region in the vicinity of the force can be
#   # be designed; otherwise we get outrageously high values for the compliance.
#   mask[round(aspect*nelx):, round(nely*aspect)+2:] = 0

#   return Problem(normals, forces, density, width, height, mask.T)


# def tower(nelx=32, density=0.5, width = 2, height =1):
#   """A rather boring structure supporting a single point from the ground."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, Y] = 1
#   normals[0, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[0, 0, Y] = -1
#   return Problem(normals, forces, density, width, height)


# def center_support(nelx=32, density=0.3, width = 2, height =1):
#   """Support downward forces from the top from the single point."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[-1, -1, Y] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, 0, Y] = -1 / nelx
#   return Problem(normals, forces, density, width, height)


# def column(nelx=32, density=0.3, width = 2, height =1): #checked
#   """Support downward forces from the top across a finite width."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, Y] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, 0, Y] = -1 / nelx
#   return Problem(normals, forces, density, width, height)


# def roof(nelx=32, density=0.5, width = 2, height =1): #checked
#   """Support downward forces from the top with a repeating structure."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[0, :, X] = 1
#   normals[-1, :, X] = 1
#   normals[:, -1, Y] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, 0, Y] = -1 / nelx
#   return Problem(normals, forces, density, width, height)


# def two_level_bridge(nelx=32, density=0.3, width = 2, height =1, deck_height=0.2): #checked
#   """A causeway bridge with two decks."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nelx + 1, 2))
#   normals[0, -1, :] = 1
#   normals[0, :, X] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nelx + 1, 2))
#   forces[:, round(nely * (1 - deck_height) / 2), :] = -1 / (2 * nelx)
#   forces[:, round(nely * (1 + deck_height) / 2), :] = -1 / (2 * nelx)
#   return Problem(normals, forces, density, width, height)


# def suspended_bridge(nelx=60, density=0.3, width = 2, height =1,
#                      span_position=0.2,
#                      anchored=False):
#   """A bridge above the ground, with supports at lower corners."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[-1, :, X] = 1
#   normals[:round(span_position*nelx), -1, Y] = 1
#   if anchored:
#     normals[:round(span_position*nelx), -1, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, -1, Y] = -1 / nelx
#   return Problem(normals, forces, density, width, height)


# def canyon_bridge(nelx=60, density=0.3, width = 2, height =1, deck_level=1):
#   """A bridge embedded in a canyon, without side supports."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   deck_nely = round(nely * (1 - deck_level))

#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[-1, deck_nely:, :] = 1
#   normals[0, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, deck_nely, Y] = -1 / nelx
#   return Problem(normals, forces, density, width, height)


# def thin_support_bridge(
#     nelx=32, density=0.25, width = 2, height =1, design_width=0.25):
#   """A bridge supported from below with fixed nelx supports."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, Y] = 1
#   normals[0, :, X] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, 0, Y] = -1 / nelx

#   mask = np.ones((nelx, nely))
#   mask[-round(nelx*(1-design_width)):, :round(nely*(1-design_width))] = 0
#   return Problem(normals, forces, density, width, height, mask)


# def drawbridge(nelx=32,  density=0.25, width = 2, height =1):
#   """A bridge supported from above on the left."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[0, :, :] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   forces[:, -1, Y] = -1 / nelx

#   return Problem(normals, forces, density, width, height)


# def hoop(nelx=32, density=0.25, width = 1, height =2): # checked
#   """Downward forces in a circle, supported from the ground."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   if 2 * nelx != nely:
#     raise ValueError('hoop must be circular')

#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[-1, :, X] = 1
#   normals[:, -1, Y] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   i, j, value = skimage.draw.circle_perimeter_aa(
#       nelx, nelx, nelx, forces.shape[:2]
#   )
#   forces[i, j, Y] = -value / (2 * np.pi * nelx)

#   return Problem(normals, forces, density, width, height)


# # def multipoint_circle(
# #     nelx=140, density=0.333, width = 2, height =1, radius=6/7,
# #     weights=(1, 0, 0, 0, 0, 0), num_points=12):
# #   """Various load scenarios at regular points in a circle points."""
# #   # From: http://www2.mae.ufl.edu/mdo/Papers/5219.pdf
# #   # Note: currently unused in our test suite only because the optimization
# #   # problems from the paper are defined based on optimizing for compliance
# #   # averaged over multiple force scenarios.
# #   c_x = nelx // 2
# #   c_y = nely // 2
# #   normals = np.zeros((nelx + 1, nely + 1, 2))
# #   normals[c_x - 1 : c_x + 2, c_y - 1 : c_y + 2, :] = 1
# #   assert normals.sum() == 18

# #   c1, c2, c3, c4, c_x0, c_y0 = weights

# #   forces = np.zeros((nelx + 1, nely + 1, 2))
# #   for position in range(num_points):
# #     x = radius * c_x * np.sin(2*np.pi*position/num_points)
# #     y = radius * c_y * np.cos(2*np.pi*position/num_points)
# #     i = int(round(c_x + x))
# #     j = int(round(c_y + y))
# #     forces[i, j, X] = + c1 * y + c2 * x + c3 * y + c4 * x + c_x0
# #     forces[i, j, Y] = - c1 * x + c2 * y + c3 * x - c4 * y + c_y0

# #   return Problem(normals, forces, density, width, height)


# def ramp(nelx=32, density=0.25, width = 2, height =1):
#   """Support downward forces on a ramp."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   return staircase(nelx, nely, density, num_stories=1)


# def staircase(nelx=32, density=0.25, width = 2, height =1, num_stories=2):
#   """A ramp that zig-zags upward, supported from the ground."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, :] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   for story in range(num_stories):
#     parity = story % 2
#     start_coordinates = (0, (story + parity) * nely // num_stories)
#     stop_coordiates = (nelx, (story + 1 - parity) * nely // num_stories)
#     i, j, value = skimage.draw.line_aa(*start_coordinates, *stop_coordiates)
#     forces[i, j, Y] = np.minimum(
#         forces[i, j, Y], -value / (nelx * num_stories)
#     )

#   return Problem(normals, forces, density, width, height)


# def staggered_points(nelx=32, density=0.3, width = 2, height =1, interval=16,
#                      break_symmetry=False):
#   """A staggered grid of points with downward forces, supported from below."""
#   nely = int(height*nelx/width)
#   try:
#       assert nely == height*nelx/width
#   except:
#       sys.exit("nely is not an integer")
#   normals = np.zeros((nelx + 1, nely + 1, 2))
#   normals[:, -1, Y] = 1
#   normals[0, :, X] = 1
#   normals[-1, :, X] = 1

#   forces = np.zeros((nelx + 1, nely + 1, 2))
#   f = interval ** 2 / (nelx * nely)
#   # intentionally break horizontal symmetry?
#   forces[interval//2+int(break_symmetry)::interval, ::interval, Y] = -f
#   forces[int(break_symmetry)::interval, interval//2::interval, Y] = -f
#   return Problem(normals, forces, density, width, height)





# pylint: disable=line-too-long
# PROBLEMS_BY_CATEGORY = {
#     # idealized beam and cantilevers
#     'mbb_beam': [
#         mbb_beam(96, 32, density=0.5),
#         mbb_beam(192, 64, density=0.4),
#         mbb_beam(384, 128, density=0.3),
#         mbb_beam(192, 32, density=0.5),
#         mbb_beam(384, 64, density=0.4),
#     ],
#     'cantilever_beam_full': [
#         cantilever_beam_full(96, 32, density=0.4),
#         cantilever_beam_full(192, 64, density=0.3),
#         cantilever_beam_full(384, 128, density=0.2),
#         cantilever_beam_full(384, 128, density=0.15),
#     ],
#     'cantilever_beam_two_point': [
#         cantilever_beam_two_point(64, 48, density=0.4),
#         cantilever_beam_two_point(128, 96, density=0.3),
#         cantilever_beam_two_point(256, 192, density=0.2),
#         cantilever_beam_two_point(256, 192, density=0.15),
#     ],
#     'pure_bending_moment': [
#         pure_bending_moment(32, 64, density=0.15),
#         pure_bending_moment(64, 128, density=0.125),
#         pure_bending_moment(128, 256, density=0.1),
#     ],
#     'ground_structure': [
#         ground_structure(64, 64, density=0.12),
#         ground_structure(128, 128, density=0.1),
#         ground_structure(256, 256, density=0.07),
#         ground_structure(256, 256, density=0.05),
#     ],
#     'michell_centered_both': [
#         michell_centered_both(32, 64, density=0.12),
#         michell_centered_both(64, 128, density=0.12),
#         michell_centered_both(128, 256, density=0.12),
#         michell_centered_both(128, 256, density=0.06),
#     ],
#     'michell_centered_below': [
#         michell_centered_below(64, 64, density=0.12),
#         michell_centered_below(128, 128, density=0.12),
#         michell_centered_below(256, 256, density=0.12),
#         michell_centered_below(256, 256, density=0.06),
#     ],
#     # simple constrained designs
#     'l_shape_0.2': [
#         l_shape(64, 64, aspect=0.2, density=0.4),
#         l_shape(128, 128, aspect=0.2, density=0.3),
#         l_shape(256, 256, aspect=0.2, density=0.2),
#     ],
#     'l_shape_0.4': [
#         l_shape(64, 64, aspect=0.4, density=0.4),
#         l_shape(128, 128, aspect=0.4, density=0.3),
#         l_shape(256, 256, aspect=0.4, density=0.2),
#     ],
#     'crane': [
#         crane(64, 64, density=0.3),
#         crane(128, 128, density=0.2),
#         crane(256, 256, density=0.15),
#         crane(256, 256, density=0.1),
#     ],
#     # vertical support structures
#     'center_support': [
#         center_support(64, 64, density=0.15),
#         center_support(128, 128, density=0.1),
#         center_support(256, 256, density=0.1),
#         center_support(256, 256, density=0.05),
#     ],
#     'column': [
#         column(32, 128, density=0.3),
#         column(64, 256, density=0.3),
#         column(128, 512, density=0.1),
#         column(128, 512, density=0.3),
#         column(128, 512, density=0.5),
#     ],
#     'roof': [
#         roof(64, 64, density=0.2),
#         roof(128, 128, density=0.15),
#         roof(256, 256, density=0.4),
#         roof(256, 256, density=0.2),
#         roof(256, 256, density=0.1),
#     ],
#     # bridges
#     'causeway_bridge_top': [
#         causeway_bridge(64, 64, density=0.3),
#         causeway_bridge(128, 128, density=0.2),
#         causeway_bridge(256, 256, density=0.1),
#         causeway_bridge(128, 64, density=0.3),
#         causeway_bridge(256, 128, density=0.2),
#     ],
#     'causeway_bridge_middle': [
#         causeway_bridge(64, 64, density=0.12, deck_level=0.5),
#         causeway_bridge(128, 128, density=0.1, deck_level=0.5),
#         causeway_bridge(256, 256, density=0.08, deck_level=0.5),
#     ],
#     'causeway_bridge_low': [
#         causeway_bridge(64, 64, density=0.12, deck_level=0.3),
#         causeway_bridge(128, 128, density=0.1, deck_level=0.3),
#         causeway_bridge(256, 256, density=0.08, deck_level=0.3),
#     ],
#     'two_level_bridge': [
#         two_level_bridge(64, 64, density=0.2),
#         two_level_bridge(128, 128, density=0.16),
#         two_level_bridge(256, 256, density=0.12),
#     ],
#     'free_suspended_bridge': [
#         suspended_bridge(64, 64, density=0.15, anchored=False),
#         suspended_bridge(128, 128, density=0.1, anchored=False),
#         suspended_bridge(256, 256, density=0.075, anchored=False),
#         suspended_bridge(256, 256, density=0.05, anchored=False),
#     ],
#     'anchored_suspended_bridge': [
#         suspended_bridge(64, 64, density=0.15, span_position=0.1, anchored=True),
#         suspended_bridge(128, 128, density=0.1, span_position=0.1, anchored=True),
#         suspended_bridge(256, 256, density=0.075, span_position=0.1, anchored=True),
#         suspended_bridge(256, 256, density=0.05, span_position=0.1, anchored=True),
#     ],
#     'canyon_bridge': [
#         canyon_bridge(64, 64, density=0.16),
#         canyon_bridge(128, 128, density=0.12),
#         canyon_bridge(256, 256, density=0.1),
#         canyon_bridge(256, 256, density=0.05),
#     ],
#     'thin_support_bridge': [
#         thin_support_bridge(64, 64, density=0.3),
#         thin_support_bridge(128, 128, density=0.2),
#         thin_support_bridge(256, 256, density=0.15),
#         thin_support_bridge(256, 256, density=0.1),
#     ],
#     'drawbridge': [
#         drawbridge(64, 64, density=0.2),
#         drawbridge(128, 128, density=0.15),
#         drawbridge(256, 256, density=0.1),
#     ],
#     # more complex design problems
#     'hoop': [
#         hoop(32, 64, density=0.25),
#         hoop(64, 128, density=0.2),
#         hoop(128, 256, density=0.15),
#     ],
#     'dam': [
#         dam(64, 64, density=0.2),
#         dam(128, 128, density=0.15),
#         dam(256, 256, density=0.05),
#         dam(256, 256, density=0.1),
#         dam(256, 256, density=0.2),
#     ],
#     'ramp': [
#         ramp(64, 64, density=0.3),
#         ramp(128, 128, density=0.2),
#         ramp(256, 256, density=0.2),
#         ramp(256, 256, density=0.1),
#     ],
#     'staircase': [
#         staircase(64, 64, density=0.3, num_stories=3),
#         staircase(128, 128, density=0.2, num_stories=3),
#         staircase(256, 256, density=0.15, num_stories=3),
#         staircase(128, 512, density=0.15, num_stories=6),
#     ],
#     'staggered_points': [
#         staggered_points(64, 64, density=0.3),
#         staggered_points(128, 128, density=0.3),
#         staggered_points(256, 256, density=0.3),
#         staggered_points(256, 256, density=0.5),
#         staggered_points(64, 128, density=0.3),
#         staggered_points(128, 256, density=0.3),
#         staggered_points(32, 128, density=0.3),
#         staggered_points(64, 256, density=0.3),
#         staggered_points(128, 512, density=0.3),
#         staggered_points(128, 512, interval=32, density=0.15),
#     ],
#     'multistory_building': [
#         multistory_building(32, 64, density=0.5),
#         multistory_building(64, 128, interval=32, density=0.4),
#         multistory_building(128, 256, interval=64, density=0.3),
#         multistory_building(128, 512, interval=64, density=0.25),
#         multistory_building(128, 512, interval=128, density=0.2),
#     ],
#     'causeway_bridge_top2': [causeway_bridge(128, 128, density=0.1)],
#     'causeway_bridge_middle2':[causeway_bridge(256, 256, density=0.1, deck_level=0.5)],
#     'multistory_building2': [multistory_building(128, 256, interval=16, density=0.3)],
#     'causeway_bridge_mid':[causeway_bridge(64, 64, density=0.1),
#                                causeway_bridge(32, 32, density=0.1)],
#     'l_shape_2':[l_shape(128, 128, aspect=0.4, density=0.4)],
#     'crane_2': [crane(256, 256, density=0.2)]
    
# }

# PROBLEMS_BY_NAME = {}
# for problem_class, problem_list in PROBLEMS_BY_CATEGORY.items():
#   for problem in problem_list:
#     name = f'{problem_class}_{problem.nelx}x{problem.nely}_{problem.density}'
#     problem.name = name
#     assert name not in PROBLEMS_BY_NAME, f'redundant name {name}'
#     PROBLEMS_BY_NAME[name] = problem
