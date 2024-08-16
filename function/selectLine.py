# function/selectLine.py
def selectLine(text, line_number):
    """
    주어진 텍스트에서 특정 라인을 추출합니다.

    Args:
        text: 텍스트 문자열
        line_number: 추출할 라인 번호 (1부터 시작)

    Returns:
        해당 라인의 문자열
    """

    lines = text.splitlines()
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1]
    else:
        return "Invalid line number"