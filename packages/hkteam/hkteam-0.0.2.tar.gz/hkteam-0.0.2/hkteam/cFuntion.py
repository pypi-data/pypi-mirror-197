# 기능: 입력값을 받아 반올림 수행
# 입력: inValue: 숫자형 값
# 반환: outvalue: 2자리수 반올림 결과 값
def roundFunction( inValue ): 
    """
    testFunction
    """
    step1 = inValue * 100 
    step2 = int(step1 + 0.5)
    outvalue = step2 / 100
    return outvalue

# 기능: 입력값을 받아 반올림 수행
# 입력: inValue: 숫자형 값
# 반환: outvalue: 2자리수 반올림 결과 값
def roundFunction2( inValue ): 
    """
    testFunction
    """
    step1 = inValue * 1000 
    step2 = int(step1 + 0.5)
    outvalue = step2 / 1000
    return outvalue