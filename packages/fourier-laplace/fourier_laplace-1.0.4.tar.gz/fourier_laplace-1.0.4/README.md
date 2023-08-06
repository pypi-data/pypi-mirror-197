# Installation

`pip install fourier-laplace`

# Usage

```python
from numpy import arange
from fourier_laplace import FourierProfile

# 0.1 <= Bo <= 0.35
estimator = FourierProfile(bond_number=0.2)

# 0 <= z <= 5
z = arange(0, 2, 1e-1)
x = estimator.estimate(z=z) # Predicted x

# Normalize profile (so that true x_max = 1)
max_x = estimator.get_max_x()
z = z / max_x
x = x / max_x
```

# Background

The Young-Laplace equation describes the pressure difference across a curved interface between two immiscible fluids, 
such as a liquid drop or bubble.

$$\Delta P = \frac{1}{\gamma}(\frac{1}{R_1} + \frac{1}{R_2})$$

In the case of axis-symmetric drops, 
the above equation can be translated into a system of first order differential equation.

$$\frac{d \phi}{d s} = 2 - Bo z - \frac{\sin \phi}{x}$$

$$\frac{d x}{d s} = \cos \phi$$

$$\frac{d z}{d s} = \sin \phi$$

With the boundary condition

$$\phi(s=0)=x(s=0)=z(s=0)=0$$

The bond number, $Bo$, represents the balance of forces between gravity and surface tension.

$$Bo = \frac{\Delta \rho g a^2}{\gamma}$$

Where $a$ is the characteristic length. 
Then to  calculate a point map (x, z) from the equations above,
the set of differential equations have to be solved through numerical means.

# Improved Method

The surface tension can only accurately be calculated from the $Bo$ range of [0, 1]. 
Otherwise, gravity is the dominating force and not surface tension.
In practice, the true $Bo$ should be in the range [0.1, 0.35] for the most accurate measurements.
For any drop, the following relationship can written.

$$x = f(z, Bo)$$

Where $f(z, Bo)$ is some generic function can be calculated from the equations above.
Using a fourier series, a generic function for $f(z, Bo)$ can be calculated.

$$f(z, Bo) = \frac{a_0}{2} + \sum_{n=1}^{\infty} a_n \cos \left( \frac{2 \pi n z}{P} \right)+ b_n \sin \left( \frac{2 \pi n z}{P} \right)$$

$$a_n = \frac{2}{P} \int^{P}_{0} f(z, Bo) \cos \left( \frac{2 \pi n z}{P} \right) dz$$

$$b_n = \frac{2}{P} \int^{P}_{0} f(z, Bo) \sin \left( \frac{2 \pi n z}{P} \right) dz$$

$P$ is some artibary period at which the function is defined over, 
but $z$ can theoretically be defined over any range.
In reality, z is typically only defined over the range [0, 5].
Often times $z < 2$, 
but there are some cases where z is defined at a larger values.
Thus, it is safe to assume that $P=5$.
But it can be seen above that $a_n$ and $b_n$ are only dependant on $Bo$,
since the dependance on z is integrated out.

$$a_n = a_n(Bo)$$

$$b_n = b_n(Bo)$$

Since the range for $Bo$ is known, 
a table can easily be made all the fourier constants for many $Bo$ values.
Then interplotion can be used to calculate the new constants for a given Bo.
This means that generating the table is computationally very expensive,
but using it is very computationally cheap.
This is the basis for this codebase, and how a sigificant speed up is achieved.