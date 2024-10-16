'''
A real-time tuner in python

Tuan Vu
'''
import numpy as np
import pyaudio
import scipy.fftpack

# Initialize constants for pyaudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize constants to reference in algorithms
A4 = 440
C4 = A4 * 2 ** (-9 / 12)
ALL_NOTES = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']

# Algorithm that will find the nearest note to a given frequency
def nearest_note(examined_pitch):
    i = int(np.round(12 * np.log2(examined_pitch/A4)))
    close_note = ALL_NOTES[i % 12] + f'{4 + (i + 9) // 12}'
    close_pitch = A4 * 2 ** (i / 12)
    return close_note, close_pitch

# Algorithm that uses nearest_note() function to find the amount of cents away the given frequency is from the nearest note
def distance_from_nearest_note_in_cents(examined_pitch):
    close_tuple = nearest_note(examined_pitch)
    cents = 1200 * np.log2(examined_pitch / close_tuple[1])
    return np.round(cents)

# Algorithm to find the peak frequency of an audio recording given the samples and the sample rate
def find_freq(samples, rate):
    # Apply Fourier's Transform
    spectrum = scipy.fftpack.fft(samples)
    freqs = scipy.fftpack.fftfreq(len(spectrum))
    
    # Find the peak in the spectrum
    peak_idx = np.argmax(np.abs(spectrum))
    peak_freq = abs(freqs[peak_idx] * rate)
    
    return peak_freq

def main():
    # Initialize pyaudio object
    p = pyaudio.PyAudio()
    
    # Opens audio stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    # Notifies the user that the tuner is active
    print("Play or sing a note...")
    try:
        while True:
            # Read audio data
            audio_data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            
            # Find the peak frequency from the data
            frequency = find_freq(audio_data, RATE)
            
            try:
                # Find closest note
                note, closest_freq = nearest_note(frequency)
            except OverflowError as e:
                continue
            
            # Calculate the amount of cents away the note is
            distance_from_note = distance_from_nearest_note_in_cents(frequency)
            
            # Print result
            print(f"Nearest note: {note}\nCents: {distance_from_note}")
        
    except KeyboardInterrupt:
        # Stops the tuner when there's a keyboard interrupt
        print("\nTuner stopped.")
    finally:
        # Stop and close stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
if __name__ == "__main__":
    main()
