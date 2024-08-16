import numpy as np

#데이터 최적화 함수
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



