from scipy.signal import firwin
import numpy as np

sample_rate = 48000
num_taps = 127

bands = [
    (100, 250),
    (250, 500),
    (500, 1000),
    (1000, 2000),
    (2000, 4000),
    (4000, 8000),
]

for band in bands:
    low, high = band
    coeffs = firwin(
        numtaps=num_taps,
        cutoff=[low, high],
        fs=sample_rate,
        pass_zero=False,  # bandpass
        window='hamming'
    )
    print(','.join([f"{c:.8f}" for c in coeffs]))
