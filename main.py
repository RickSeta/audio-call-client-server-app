import pyaudio

#def record():
# Default is Rate = 44100 Hz and Format = 24 bits
FORMAT=pyaudio.paInt24
RATE=44100
CHANNELS=1
CHUNK=1024
RECORD_SECONDS=5
OUTPUT=True

p = pyaudio.PyAudio()
stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, output=OUTPUT, frames_per_buffer=CHUNK)
frames = []

print("* Recording Started")

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* Recording Finished")

stream.stop_stream()
stream.close()
p.terminate()