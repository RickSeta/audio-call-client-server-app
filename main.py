import pyaudio

#def record():
# Default is Rate = 44100 Hz and Format = 24 bits
FORMAT=pyaudio.paInt24
RATE=44100
CHANNELS=1
CHUNK=1024
RECORD_SECONDS=5

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("* Recording Started")

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)

print("* Recording Finished")

stream.stop_stream()
stream.close()
p.terminate()