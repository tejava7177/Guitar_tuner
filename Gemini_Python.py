import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

import logging              #로그작성
import traceback            #오류 출력

#로깅 설정
logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# 오디오 스트림 파라미터 (CHUNK 값 증가)
FORMAT = pyaudio.paInt16  # 오디오 포맷 (16비트 PCM)
CHANNELS = 1              # 채널 수 변경 (모노)
RATE = 44100              # 샘플 레이트 (44.1kHz)
CHUNK = 2048              # 버퍼 크기 (2048 프레임) 증가

# 표준 주파수 (예: E, B, G, D, A, E 현)
standard_freqs = [330, 247, 196, 147, 110, 82.41]  # Hz

# 데이터 최적화 함수
def process_data(data):
    # 벡터화 연산 예시
    filtered_data = np.convolve(data, np.ones(5) / 5, mode='valid')  # 이동 평균 필터링
    return filtered_data

# 주파수 피크 찾기 함수
def find_peak_frequency(fft_data, freqs):
    idx = np.argmax(np.abs(fft_data))
    if idx < len(freqs):
        return freqs[idx]
    else:
        return None  # 또는 적절한 값 반환

# 튜닝 상태 판단 함수
def check_tuning(freq, standard_freq):
    tolerance = 5  # 허용 오차
    if freq > standard_freq + tolerance:
        return "너무 높습니다."
    elif freq < standard_freq - tolerance:
        return "너무 낮습니다."
    else:
        return "정확합니다."

# matplotlib 백엔드 설정
#plt.ion()

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

try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=dev_index,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    freqs = np.fft.fftfreq(CHUNK, 1.0 / RATE)  # freqs를 외부에서 계산
    for i in range(0, int(RATE / CHUNK * 20)):       #2초 동안 동작
        data = stream.read(CHUNK)
        data_int16 = np.frombuffer(data, dtype=np.int16)

        # 데이터 처리
        processed_data = process_data(data_int16)

        # FFT 수행 및 주파수 피크 찾기
        fft_data = np.fft.fft(data_int16)
        peak_freq = find_peak_frequency(fft_data, freqs)

        print(f"freq : {peak_freq}")

        #
        # # 튜닝 상태 확인 및 출력
        # for i, std_freq in enumerate(standard_freqs):
        #     tuning_result = check_tuning(peak_freq, std_freq)
        #     print(f"현 {i+1}: {tuning_result}")



# 오류처리
except OSError as e:
    logging.error(f"오류 발생: {e}")
    logging.exception(traceback.format_exc())


# 스트림 종료
stream.stop_stream()
stream.close()
p.terminate()

# 캡처된 데이터를 파일로 저장 (옵션)
frames = []  # frames 리스트 초기화
wf = wave.open("output_stereo.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()