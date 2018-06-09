from aip import AipSpeech

APP_ID="11369605"
API_KEY="ZcoySFOErYdoHEGbcZiFFPsj"
SECRET_KEY="rbTxEXBvWqTauQHUMbGYOwNn3WViBcPa"

client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()

#print(get_file_content("d://8k.wav"))

import time

ss = time.time()

f = "d://向左转.wav"
s = client.asr(get_file_content(f),'wav',16000,{'dev_pid':1536,})
e = time.time()
print(e -ss)
print(s)

