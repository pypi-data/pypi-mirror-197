def roundFunction(inValue):

    """
소수점 둘째짜리에서 내림
parameter: inValue
return: 소수점 둘째짜리에서 내림하여 수 반환
    """
    # step 1 : inValue 값에 roundPoint 만큼 자리 이동
    roundPoint = 10**2
    # step 2 : 정수로 변환하고 자리수 원래대로!!
    roundValue = int(inValue * roundPoint) / roundPoint
    
    return roundValue