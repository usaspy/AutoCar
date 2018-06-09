import pyaudio
import wave

chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 16000
record_seconds = 2

wave_output_file = "d://向左转.wav"

p = pyaudio.PyAudio()

stream = p.open(format=format,
                channels = channels,
                rate = rate,
                input = True,
                frames_per_buffer = chunk)
print("recording...")
frames = []

for i in range(0,int(rate/chunk*record_seconds)):
    data = stream.read(chunk)
    frames.append(data)

print("record finished..")
print(frames)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(wave_output_file,'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
wf.close()