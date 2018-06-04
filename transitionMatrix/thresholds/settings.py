GRID_POINTS = 2000
PRECISION = 1.e-8
SCALE = 7.0
DELTA = 2000

# Select the autoregressive model AR(1) to fit
# Mu is the process drift
# Phi is the process autocorrelation parameter
# [X_0, X_1] are th process initial conditions

AR_Model = {
    "Mu": 0.0,
    "Phi": [1.0],
    "Initial Conditions": [1.0, 0.0]
}