import tkinter as tk
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Callback function to process audio data
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    line.set_ydata(audio_data)
    canvas.draw()
    return (in_data, pyaudio.paContinue)

# Start recording button callback
def start_recording():
    stream.start_stream()

# Stop recording button callback
def stop_recording():
    stream.stop_stream()

# Custom colors
bg_color = "#1c3a3a"
button_color = "#2b6e6e"
text_color = "#9ed9d9"
plot_bg_color = "#1c3a3a"
line_color = "#2b6e6e"

# Create the main window
root = tk.Tk()
root.title("Real-time Audio Waveform")
root.configure(bg=bg_color)

# Create start and stop buttons
start_button = tk.Button(root, text="Start Recording", command=start_recording, bg=button_color, fg=text_color)
start_button.pack()
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, bg=button_color, fg=text_color)
stop_button.pack()

# Create a matplotlib figure to display the audio waveform
fig, ax = plt.subplots()
x = np.arange(0, 2 * 1024, 2)  # 1024 samples at 16 bits/sample
line, = ax.plot(x, np.random.rand(1024), color=line_color)
ax.set_ylim([-2**15, 2**15 - 1])
ax.set_facecolor(plot_bg_color)
fig.patch.set_facecolor(plot_bg_color)
ax.spines['bottom'].set_color(text_color)
ax.spines['top'].set_color(text_color)
ax.spines['right'].set_color(text_color)
ax.spines['left'].set_color(text_color)
ax.tick_params(axis='x', colors=text_color)
ax.tick_params(axis='y', colors=text_color)
ax.xaxis.label.set_color(text_color)
ax.yaxis.label.set_color(text_color)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Configure audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 1024

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
