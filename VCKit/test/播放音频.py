##
#　使用pyaudio播放WAVE格式的音频文件
#

import pyaudio
import wave

chunk = 1024
#貌似只有特定波特率的wav文件才能播放，不然报错：wave.Error: unknown format XX
f = wave.open("d://Audio.wav","rb")
p = pyaudio.PyAudio()

# open stream based on the wave object which has been input.
stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)

# read data (based on the chunk size)
data = f.readframes(chunk)

# play stream (looping from beginning of file to the end)
while data != b'':
    stream.write(data)
    data = f.readframes(chunk)
    print(data)

# cleanup stuff.
stream.close()
p.terminate()
print("-----end------")
