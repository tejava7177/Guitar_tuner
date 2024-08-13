import numpy as np
import pyaudio
import time

# 오디오 입력 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # 데이터를 얼마나 자주 읽을 것인지 (버퍼 크기)


def analyze_frequency(data, rate):
    # 푸리에 변환 수행
    fft_data = np.fft.fft(data)
    freq = np.fft.fftfreq(len(fft_data))

    # 주파수 추출
    idx = np.argmax(np.abs(fft_data))
    freq_in_hz = abs(freq[idx] * rate)
    return freq_in_hz


def listen_for_guitar():
    # 오디오 스트림 열기
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("줄을 튕기세요...")
    input("준비되었으면 엔터를 누르세요.")  # 사용자가 줄을 튕길 준비가 되면 엔터를 누르게 함

    print("듣고 있습니다...")

    start_time = time.time()
    while time.time() - start_time < 10:  # 10초 동안 오디오 데이터를 수집
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        frequency = analyze_frequency(data, RATE)
        print(f"Detected Frequency: {frequency:.2f} Hz")

    print("10초가 경과했습니다. 분석을 종료합니다.")

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    listen_for_guitar()

