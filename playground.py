import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import argparse
import os
from scipy.fft import fft, fftfreq
from scipy.signal import cheby1, sosfiltfilt
from scipy import signal

def record_audio(output_file, duration=5, sample_rate=44100, channels=1):
    """
    Record audio from microphone and save to a file.
    
    Parameters:
    - output_file: Path to save the recorded audio
    - duration: Recording duration in seconds
    - sample_rate: Sample rate in Hz
    - channels: Number of audio channels (1 for mono, 2 for stereo)
    """
    print(f"Recording {duration} seconds of audio...")
    
    # Record audio
    recording = sd.rec(int(duration * sample_rate), 
                      samplerate=sample_rate, 
                      channels=channels,
                      dtype='float32')
    
    # Wait until recording is finished
    sd.wait()
    
    print("Recording finished")
    
    # Save as WAV file
    sf.write(output_file, recording, sample_rate)
    print(f"Audio saved to {output_file}")
    
    return recording

def load_audio_to_array(file_path):
    """
    Load an audio file and return the signal as a NumPy array.
    
    Parameters:
    - file_path: Path to the audio file
    
    Returns:
    - audio_array: NumPy array containing the audio signal
    - sample_rate: Sample rate of the audio
    """
    audio_array, sample_rate = sf.read(file_path)
    return audio_array, sample_rate

def process_existing_file(file_path):
    """Process an existing audio file."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return
    
    print(f"Loading audio from {file_path}")
    audio_array, sample_rate = load_audio_to_array(file_path)
    
    print(f"Audio loaded successfully:")
    print(f"- Sample rate: {sample_rate} Hz")
    print(f"- Shape of array: {audio_array.shape}")
    print(f"- Data type: {audio_array.dtype}")
    print(f"- Duration: {len(audio_array)/sample_rate:.2f} seconds")
    
    # Display a small sample of the array
    print("\nFirst 10 samples of the audio array:")
    print(audio_array[:10])
    
    return audio_array, sample_rate

def apply_hamming_window(arr):
    return arr * np.hamming(len(arr))

def create_filterbank(data, sampling_rate, band_edges, filter_order = 8):
    filtered_data = []

    for low, high in band_edges:
        sos = cheby1(
            filter_order,
            1,
            [low, high],
            btype='bandpass',
            fs=sampling_rate,
            output='sos')
        filtered = sosfiltfilt(sos, data)
        filtered_data.append(filtered)
    return np.array(filtered_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record audio or process existing audio file.")
    parser.add_argument("--input", "-i", help="Path to existing audio file to process")
    parser.add_argument("--output", "-o", default="recorded_audio.wav", help="Output file path for recording")
    parser.add_argument("--duration", "-d", type=int, default=5, help="Recording duration in seconds")
    parser.add_argument("--sample-rate", "-r", type=int, default=44100, help="Sample rate in Hz")
    parser.add_argument("--channels", "-c", type=int, default=1, help="Number of audio channels")
    
    args = parser.parse_args()

    audio_array = []
    sample_rate = 0
    
    if args.input:
        # Process existing file
        audio_array, sample_rate = process_existing_file(args.input)
    else:
        # Record new audio
        audio_array = record_audio(args.output, args.duration, args.sample_rate, args.channels)
        # Process the recorded audio
        audio_array, sample_rate = process_existing_file(args.output)


    
    # Trimming the audio array to a specific length for demonstration
    audio_array = audio_array[55995:4096+55995]

    # Playing around wiht more processing
    hamm_audio_arr = apply_hamming_window(audio_array)

    #taking FFT of signal
    fft_result = fft(audio_array)
    freq = np.fft.fftfreq(len(audio_array), 1/sample_rate)

    positive_indices = freq >= 0
    pos_freq = freq[positive_indices]
    pos_fft = fft_result[positive_indices]

    fft_magnitude = np.abs(pos_fft)
    ps = fft_magnitude ** 2

    # Convert to dB for better visualization
    fft_magnitude_db = 20 * np.log10(fft_magnitude + 1e-10)  # Adding small value to avoid log(0)
    ps_db = 10 * np.log10(ps + 1e-10)

    # Create subplots: 2 rows, 2 columns
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # First plot - Time domain original
    axs[0,0].plot(np.arange(len(audio_array))/sample_rate, audio_array)
    axs[0,0].set_title("Original Audio Signal")
    axs[0,0].set_xlabel("Time (s)")
    axs[0,0].set_ylabel("Amplitude")
    axs[0,0].grid(True)

    # Second plot - Time domain windowed
    axs[0,1].plot(np.arange(len(hamm_audio_arr))/sample_rate, hamm_audio_arr)
    axs[0,1].set_title("Hamming Windowed Audio Signal")
    axs[0,1].set_xlabel("Time (s)")
    axs[0,1].set_ylabel("Amplitude")
    axs[0,1].grid(True)

    # Third plot - Power Spectrum
    axs[1,0].plot(pos_freq, ps_db)
    axs[1,0].set_title("Power Spectral Density")
    axs[1,0].set_xlabel("Frequency (Hz)")
    axs[1,0].set_ylabel("Power (dB)")
    axs[1,0].set_xlim(0, sample_rate/2)  # Only show up to Nyquist frequency
    axs[1,0].grid(True)

    plt.tight_layout()
    plt.show()


    bands = [
    (100, 250),
    (250, 500),
    (500, 1000),
    (1000, 2000),
    (2000, 4000),
    (4000, 8000)]


    filtered_data_list = create_filterbank(hamm_audio_arr, sample_rate, bands)

    
    # Plot the original signal and each subband
    fig, axs = plt.subplots(len(filtered_data_list) + 1, 1, figsize=(10, 12))

    # Plot the original signal
    axs[0].plot(np.arange(len(hamm_audio_arr)) / sample_rate, hamm_audio_arr)
    axs[0].set_title("Original Hamming Windowed Audio Signal")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid(True)

    # Plot each subband
    for i, filtered_data in enumerate(filtered_data_list):
        axs[i + 1].plot(np.arange(len(filtered_data)) / sample_rate, filtered_data)
        axs[i + 1].set_title(f"{bands[i][0]}Hz - {bands[i][1]}Hz")
        axs[i + 1].set_xlabel("Time (s)")
        axs[i + 1].set_ylabel("Amplitude")
        axs[i + 1].grid(True)

    plt.tight_layout()
    plt.show()



    # Plot the original signal and spectrograms for each subband
    fig, axs = plt.subplots(len(filtered_data_list) + 1, 1, figsize=(10, 16))

    # Plot spectrogram of the original signal
    f, t, Sxx = signal.spectrogram(hamm_audio_arr, fs=sample_rate, nperseg=256, noverlap=128)
    axs[0].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
    axs[0].set_title("Original Hamming Windowed Audio Signal - Spectrogram")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Frequency (Hz)")
    axs[0].set_ylim(0, sample_rate/2)  # Limit to Nyquist frequency

    # Plot spectrogram for each subband
    for i, filtered_data in enumerate(filtered_data_list):
        f, t, Sxx = signal.spectrogram(filtered_data, fs=sample_rate, nperseg=256, noverlap=128)
        im = axs[i + 1].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
        axs[i + 1].set_title(f"{bands[i][0]}Hz - {bands[i][1]}Hz - Spectrogram")
        axs[i + 1].set_xlabel("Time (s)")
        axs[i + 1].set_ylabel("Frequency (Hz)")
        axs[i + 1].set_ylim(bands[i][0], bands[i][1])  # Limit y-axis to the band range
        
        # Add colorbar to each plot
        plt.colorbar(im, ax=axs[i+1], label='Power/frequency (dB/Hz)')

    plt.tight_layout()
    plt.show()


    #try to reconstruct signal after splitting up into bands
    reconstructed_signal = np.sum(filtered_data_list, axis=0)

    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(len(hamm_audio_arr))/sample_rate, hamm_audio_arr, label='Original')
    plt.plot(np.arange(len(reconstructed_signal))/sample_rate, reconstructed_signal, label='Reconstructed', alpha=0.7)
    plt.legend()
    plt.title('Comparison of Original and Reconstructed Signal')
    plt.show()
    


