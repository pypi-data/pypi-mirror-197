import numpy as np

def spectral_skewness(x: np.ndarray):
    """
    Calculate the spectral skewness of a audio signal.
    """
    # Calculate the power spectrum
    x = x.astype(float)
    spectrum = np.abs(np.fft.fft(x))**2
    # Sum across all frequency bins
    mean = np.mean(spectrum)
    std = np.std(spectrum)
    skew = np.mean(np.power(spectrum - mean, 3)) / (std ** 3)
    return skew

def spectral_kurtosis(x: np.ndarray):
    """
    Calculate the spectral skewness of a audio signal.
    """
    x = x.astype(float)
    # Calculate the power spectrum
    spectrum = np.abs(np.fft.fft(x))**2
    # Sum across all frequency bins
    mean = np.mean(spectrum)
    std = np.std(spectrum)
    kurtosis = np.mean(np.power(spectrum - mean, 4)) / (std ** 4)
    return kurtosis

def loudness(x: np.ndarray) -> float:
    """Caclulate the loudness of a audio signal.

    Args:
        x (np.ndarray): Input signal.

    Returns:
        float: Loudness
    """
    rms = np.sqrt(np.mean(x**2))
    loudness = 20 * np.log10(rms) # to db
    return  loudness
