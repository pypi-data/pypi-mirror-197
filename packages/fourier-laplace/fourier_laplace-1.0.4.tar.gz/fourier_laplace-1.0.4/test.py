from numpy import arange
from src.fourier_laplace import FourierProfile

from matplotlib import pyplot as plt

# 0.1 <= Bo <= 0.35
estimator = FourierProfile(bond_number=0.35)

# 0 <= z <= 5
z = arange(0, 2, 1e-1)
x = estimator.estimate(z=z) # Predicted x

# # Normalize profile (so that true x_max = 1)
# max_x = estimator.get_max_x()
# z = z / max_x
# x = x / max_x

fig, ax = plt.subplots()

ax.plot(z, x)
ax.set_aspect("equal")

plt.show()