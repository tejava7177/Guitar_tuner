import pyaudio
import wave

# 오디오 스트림 파라미터
FORMAT = pyaudio.paInt16  # 오디오 포맷 (16비트 PCM)
CHANNELS = 1              # 채널 수 변경 (모노)
RATE = 44100              # 샘플 레이트 (44.1kHz)
CHUNK = 1024              # 버퍼 크기 (1024 프레임)

# PyAudio 객체 생성
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

print("Recording...")

frames = []

# 5초간 오디오 데이터 캡처
for i in range(0, int(RATE / CHUNK * 5)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# 스트림 종료
stream.stop_stream()
stream.close()
p.terminate()

# 캡처된 데이터를 파일로 저장 (옵션)
wf = wave.open("output_stereo.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
