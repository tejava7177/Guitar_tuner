import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 44100  # 샘플 레이트를 44100으로 조정

p = pyaudio.PyAudio()

# 사용 가능한 오디오 인터페이스 나열
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# 사용자 입력을 통해 오디오 인터페이스 선택
dev_index = int(input("Choose the device index: "))

# 사용자가 선택한 오디오 인터페이스 정보 확인
dev_info = p.get_device_info_by_index(dev_index)
CHANNELS = dev_info['maxInputChannels']  # 해당 장치의 최대 입력 채널 수 사용

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=dev_index,
                frames_per_buffer=CHUNK)

print('Start recording')

frames = []

# 녹음 시간 (예: 3초)
record_seconds = 3
for i in range(0, int(RATE / CHUNK * record_seconds)):
    data = stream.read(CHUNK)
    frames.append(data)

print('Record stopped')

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
