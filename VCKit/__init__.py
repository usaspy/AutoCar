#
# 声控模块
# 通过声音来控制小车行走的套件
# 需要将vcKit整个部署在有麦克风的PC端
# 打开浏览器进入控制界面，点击按钮后，口述命令（最长2秒），声音经PC麦克风传入后生成wav文件并调用百度声音识别SDK返回命令字符
# vcKit根据返回字符判断调用小车的命令接口API --http://192.168.0.9/wheel GET {"action": "forward"}
#

#声音文件
command_wav = "./video.wav"
from VCKit import command
import time
#--------百度分析音频----------
from aip import AipSpeech

APP_ID="11369605"
API_KEY="ZcoySFOErYdoHEGbcZiFFPsj"
SECRET_KEY="rbTxEXBvWqTauQHUMbGYOwNn3WViBcPa"

client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

def get_file_content():
    with open(command_wav,'rb') as fp:
        return fp.read()

def video2text():
    re = client.asr(get_file_content(),'wav',16000,{'dev_pid':1536,})
    if re.get('result') != None:
        command.sendCMD2AutoCar(re['result'])
    else:
        print("没听清楚，请再说一遍！")

#------录制音频-------
import pyaudio
import wave

# 声音录制
def startVideoRecord():
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = 2

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

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(command_wav,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == "__main__":
   stime = time.time()
   startVideoRecord()
   video2text()
   etime = time.time()
   print(etime - stime)