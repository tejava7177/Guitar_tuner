
# 튜닝 상태 판단 함수
def check_tuning(freq, standard_freq):
    tolerance = 5  # 허용 오차
    if freq > standard_freq + tolerance:
        return "너무 높습니다."
    elif freq < standard_freq - tolerance:
        return "너무 낮습니다."
    else:
        return "정확합니다."