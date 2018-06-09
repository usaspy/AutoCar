import winsound, time, sys

#播放音频，仅windows平台
mp3 = 'd://test.wav'
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        times = 1
    else:
        times = int(sys.argv[1])
    if times == 0:
        while 1:
            winsound.PlaySound(mp3, winsound.SND_NODEFAULT)
    else:
        for i in range(times):
            winsound.PlaySound(mp3, winsound.SND_NODEFAULT)