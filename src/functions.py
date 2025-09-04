from src.config import *


def getRandomStreamFunction(N: int, sigma: float) -> np.ndarray:
    """Generate a random stream function.

    The function creates a random field, applies a Gaussian filter, and 
    normalizes the result to lie in the range [-1, 1].

    Args:
        N: The size of the square output array (N x N).
        sigma: Standard deviation passed to the Gaussian filter.

    Returns:
        A NumPy array of shape ``(N, N)`` containing the stream function.

    Raises:
        ValueError: If the maximum of the generated pattern is zero (to avoid
            division by zero during normalization).
    """
    pattern = gaussian_filter(2 * np.random.rand(N, N) - 1, sigma, mode='wrap')
    max_val = np.max(np.abs(pattern))
    if max_val == 0:
        raise ValueError("Generated pattern has zero maximum; cannot normalize")
    psi = pattern / max_val
    return psi


def spectralDeriv(array: np.ndarray) -> np.ndarray:
    """Compute the spectral derivative of a 1D array using FFT.

    This uses the Fourier representation of the derivative: multiply the
    Fourier coefficients by ``i*k`` and transform back to real space.

    Args:
        array: 1D real-valued array representing a periodic function.

    Returns:
        A real-valued 1D NumPy array containing the derivative with respect
        to the array index (assumes unit spacing).
    """
    N = array.shape[0]
    freqs = np.fft.fftfreq(N, d=1) * 2 * np.pi
    return np.real(ifft(1j * freqs * fft(array)))


def ddx(array: np.ndarray) -> np.ndarray:
    """Compute the derivative along the first axis (rows) of a 2D array.

    The derivative is computed row-by-row using :func:`spectralDeriv`.

    Args:
        array: 2D real-valued array with shape ``(N, M)``.

    Returns:
        A 2D NumPy array of the same shape as ``array`` containing the
        derivative along the x-direction (i.e., derivative of each row).
    """
    deriv = spectralDeriv(array[0]).reshape(1, -1)
    for slice_ in array[1:]:
        deriv = np.concatenate([deriv, spectralDeriv(slice_).reshape(1, -1)])
    return deriv


def ddy(array: np.ndarray) -> np.ndarray:
    """Compute the derivative along the second axis (columns) of a 2D array.

    The computation is performed by transposing the array and applying
    :func:`spectralDeriv` to each row, then transposing the result back.

    Args:
        array: 2D real-valued array with shape ``(N, M)``.

    Returns:
        A 2D NumPy array of the same shape as ``array`` containing the
        derivative along the y-direction (i.e., derivative of each column).
    """
    array_T = array.T
    deriv = spectralDeriv(array_T[0]).reshape(1, -1)
    for slice_ in array_T[1:]:
        deriv = np.concatenate([deriv, spectralDeriv(slice_).reshape(1, -1)])
    return deriv.T


def getVorticity(vx: np.ndarray, vy: np.ndarray) -> np.ndarray:
    """Compute the vorticity field from velocity components.

    The vorticity is defined as ``omega = dv/dx - du/dy`` and is computed
    spectrally using :func:`ddx` and :func:`ddy`.

    Args:
        vx: x-component of velocity, 2D array of shape ``(N, N)``.
        vy: y-component of velocity, 2D array of shape ``(N, N)``.

    Returns:
        A 2D NumPy array containing the vorticity field.
    """
    omega = ddx(vy) - ddy(vx)
    return omega


def getOkuboWeiss(psi: np.ndarray) -> np.ndarray:
    """Compute the Okubo–Weiss field from a stream function.

    The Okubo–Weiss parameter is computed from second derivatives of the
    stream function ``psi``:

        Q = psi_xy**2 - psi_xx * psi_yy

    where derivatives are computed in spectral space.

    Args:
        psi: 2D stream function array of shape ``(N, N)``.

    Returns:
        A 2D NumPy array of shape ``(N, N)`` containing the Okubo–Weiss
        field.
    """
    N = psi.shape[0]
    kx = np.fft.fftfreq(N).reshape(-1, 1)
    ky = np.fft.fftfreq(N).reshape(1, -1)
    kx, ky = np.meshgrid(kx, ky)

    psi_hat = scipy.fftpack.fft2(psi)
    psi_xy = np.real(scipy.fftpack.ifft2((2 * np.pi * 1j * kx) * (2 * np.pi * 1j * ky) * psi_hat))
    psi_xx = np.real(scipy.fftpack.ifft2((2 * np.pi * 1j * kx)**2 * psi_hat))
    psi_yy = np.real(scipy.fftpack.ifft2((2 * np.pi * 1j * ky)**2 * psi_hat))

    Q = psi_xy * psi_xy - psi_xx * psi_yy
    return Q
