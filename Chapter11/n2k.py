#! /usr/bin/env python3
"""n2k: number to Korean words conversion module: contains function
   num2korean. Can also be run as a script
usage as a script: n2k num1 num2 num3 ...
           (Convert a number to its Korean word description)
           num1, num2, num3, ...: whole integer from 0 and 9,999,999,999,999,999 (commas are
           optional)
example: n2k 10,003,103 10,003,104
           for 10,003,103, 10,003,104 say: 천만삼천백삼, 천만삼천백사
"""
import sys, argparse
import n2k # n2k 모듈을 임포트 (main이 아닌 경우)

n2k.num2korean("12345")  # 만이천삼백사십오

# 기본 숫자 딕셔너리
_digit_dict = {
    "0": "",
    "1": "일",
    "2": "이",
    "3": "삼",
    "4": "사",
    "5": "오",
    "6": "육",
    "7": "칠",
    "8": "팔",
    "9": "구",
}

# 자리수 단위 (한글은 4자리씩 끊음)
_magnitude_list = [
    (0, ""),
    (4, "만"),
    (8, "억"),
    (12, "조"),
    (16, ""),
]


def num2korean(num_string):
    """num2korean(num_string): convert number to Korean words"""
    if num_string == "0":
        return "영"
    
    num_string = num_string.replace(",", "")
    num_length = len(num_string)
    max_digits = _magnitude_list[-1][0]
    
    if num_length > max_digits:
        return f"죄송합니다. {max_digits}자리 이상의 숫자는 처리할 수 없습니다"
    
    # 4자리씩 처리하기 위해 앞에 0을 추가
    num_string = "0" * (4 - num_length % 4 if num_length % 4 != 0 else 0) + num_string
    word_string = ""
    
    for mag, name in _magnitude_list:
        if mag >= len(num_string):
            return word_string.strip()
        else:
            # 4자리씩 끊어서 처리
            start_pos = len(num_string) - mag - 4
            if start_pos < 0:
                break
            
            four_digits = num_string[start_pos:start_pos + 4]
            thousands, hundreds, tens, ones = four_digits[0], four_digits[1], four_digits[2], four_digits[3]
            
            if not (thousands == hundreds == tens == ones == "0"):
                word_string = _handle1to9999(thousands, hundreds, tens, ones) + name + word_string
    
    return word_string.strip()


def _handle1to9999(thousands, hundreds, tens, ones):
    """1부터 9999까지의 숫자를 한글로 변환"""
    result = ""
    
    # 천의 자리
    if thousands != "0":
        if thousands == "1":
            result += "천"
        else:
            result += _digit_dict[thousands] + "천"
    
    # 백의 자리
    if hundreds != "0":
        if hundreds == "1":
            result += "백"
        else:
            result += _digit_dict[hundreds] + "백"
    
    # 십의 자리
    if tens != "0":
        if tens == "1":
            result += "십"
        else:
            result += _digit_dict[tens] + "십"
    
    # 일의 자리
    if ones != "0":
        result += _digit_dict[ones]
    
    return result


def test():
    """표준 입력에서 숫자들을 읽어서 변환"""
    values = sys.stdin.read().split()
    for val in values:
        print(f"{val} = {num2korean(val)}")


def main():
    parser = argparse.ArgumentParser(
        description="숫자를 한글로 변환합니다",
        usage=__doc__
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="test",
        action="store_true",
        default=False,
        help="테스트 모드: 표준 입력에서 읽기",
    )
    args = parser.parse_args()
    
    if args.test:
        test()
    else:
        if not args.num:
            parser.error("숫자를 입력해주세요")
        
        for num in args.num:
            try:
                result = num2korean(num)
            except (KeyError, IndexError) as e:
                parser.error("숫자가 아닌 문자가 포함되어 있습니다")
            else:
                print(f"{num}은(는): {result}")


if __name__ == "__main__":
    main()
else:
    print("n2k 모듈로 로드되었습니다")