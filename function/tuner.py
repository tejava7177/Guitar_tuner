
# # 튜닝 상태 판단 함수
# def check_tuning(freq, standard_freq):
#     tolerance = 5  # 허용 오차
#     if freq > standard_freq + tolerance:
#         return "너무 높습니다."
#     elif freq < standard_freq - tolerance:
#         return "너무 낮습니다."
#     else:
#         return "정확합니다."


def check_tuning(user_input):
    """
    사용자 입력에 따라 튜닝 상태를 판단합니다.

    Args:
        user_input: 사용자 입력 (정수)

    Returns:
        튜닝 상태 문자열
    """

    standard_freqs = {
        1: 82,
        2: 110,
        3: 147,
        # ... (4, 5, 6에 대한 기준값 추가)
    }
    tolerance = 5

    if user_input not in standard_freqs:
        return "잘못된 입력입니다."

    standard_freq = standard_freqs[user_input]
    freq = float(input("주파수를 입력하세요: "))  # 사용자에게 주파수 입력 받기

    if freq > standard_freq + tolerance:
        return "너무 높습니다."
    elif freq < standard_freq - tolerance:
        return "너무 낮습니다."
    else:
        return "정확합니다."