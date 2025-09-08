import numpy as np

import scipy.fftpack
from scipy.ndimage import gaussian_filter
from scipy.fft import fft, ifft

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cmasher

from typing import Any