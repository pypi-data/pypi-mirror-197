# neural_opt
Tools for analyzing the optimization dynamics in neural reparameterization of objectives

The tools used here as derived from the following repositories
- Hoyer
- PyHessian
- GradVis

The available tools are:
1. Visualization of loss landscapes
  - Linear interpolation plots
  - 2D random filter normalized plots
  - 2D Hessian eigenvector / PCA component plots
  - t-SNE (To be done)
2. Hessian based tools
  - Hessian trace and frobenius norm
  - Eigenvalue Density Spectrum
  - Hessian top & Bottom k eigenvalues and their combinations
3. Trajectory based tools
  - Angles between various important directions (gradient, minima direction, successive steps etc.)
  - Distance travelled by optimizer

Apart from these tools, two optimizers derived from L-BFGS (Hessian descent and Gradient descent with line_search) are available

Note:
In order to save the weights of the model when using L-BFGS, a script has to be added to the lbfgsb.py file in your environment's Scipy package file.
