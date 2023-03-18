import tkinter as tk
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec


# Configure audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 2048 # 1024 

# Custom colors
bg_color = "#1c3a3a"
button_color = "#2b6e6e"
text_color = "#9ed9d9"
plot_bg_color = "#1c3a3a"
line_color = "#2b6e6e"


# Create a matplotlib figure to display the audio waveform and spectrogram
fig = plt.figure()
gs = GridSpec(2, 1, figure=fig)

ax = fig.add_subplot(gs[0, 0])
x = np.arange(0, 2 * FRAMES_PER_BUFFER, 2) # 1024 samples at 16 bits/sample
line, = ax.plot(x, np.random.rand(FRAMES_PER_BUFFER), color=line_color)
ax.set_ylim([-2**15, 2**15 - 1])
ax.set_facecolor(plot_bg_color)

ax2 = fig.add_subplot(gs[1, 0])
Pxx, freqs, bins, im = ax2.specgram(np.random.rand(1024), NFFT=1024, Fs=RATE, noverlap=900, cmap='viridis')
im.set_cmap('viridis')
ax2.set_ylim([0, RATE // 2])
ax2.set_xlim([0, 2])
ax2.set_facecolor(plot_bg_color)

# Set the background color of the spectrogram
im.set_clim(vmin=0)
im.set_clim(vmax=1)

# Customize plot appearance
for a in [ax, ax2]:
    a.patch.set_facecolor(plot_bg_color)
    a.spines['bottom'].set_color(text_color)
    a.spines['top'].set_color(text_color)
    a.spines['right'].set_color(text_color)
    a.spines['left'].set_color(text_color)
    a.tick_params(axis='x', colors=text_color)
    a.tick_params(axis='y', colors=text_color)
    a.xaxis.label.set_color(text_color)
    a.yaxis.label.set_color(text_color)


# Create the main window
root = tk.Tk()
root.title("Real-time Audio Waveform")
root.configure(bg=bg_color)


# Start recording button callback
def start_recording():
    stream.start_stream()

# Stop recording button callback
def stop_recording():
    stream.stop_stream()

# Create start and stop buttons
start_button = tk.Button(root, text="Start Recording", command=start_recording, bg=button_color, fg=text_color)
start_button.pack()
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, bg=button_color, fg=text_color)
stop_button.pack()


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Callback function to process audio data
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    line.set_ydata(audio_data)
    
    Pxx, freqs, bins, _ = ax2.specgram(audio_data, NFFT=1024, Fs=RATE, noverlap=900, cmap='viridis', visible=False)
    # im.set_array(Pxx[:-1, :].ravel())
    #im.set_array(Pxx[:-1, :-1])

    canvas.draw()
    return (in_data, pyaudio.paContinue)

# Initialize audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=FRAMES_PER_BUFFER, stream_callback=callback)

# Start the main loop
root.mainloop()

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
