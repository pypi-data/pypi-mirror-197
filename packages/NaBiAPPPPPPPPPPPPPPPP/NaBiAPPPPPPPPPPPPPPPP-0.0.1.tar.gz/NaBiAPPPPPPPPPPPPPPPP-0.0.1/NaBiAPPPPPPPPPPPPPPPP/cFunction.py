def samsuBye(mainNum, nanumNum) :
    """
    main num / nanum num 을 소수점 2까지.
    """
    intNum = int(mainNum)/int(nanumNum)    #String to Int
    print("나눗셈 결과는 {} 입니다.".format(intNum))
    byeNum = round(intNum, 2)   #round함수 round(숫자, 반올림할자리수)
    print("소수점 둘째자리까지 반올림한 숫자는 {} 입니다.".format(byeNum))
    return byeNum;

def minMaxAvg(testlist) :
    """
    함수 : average that sum= sum - min - max
    최소최대값을뺀평균
    """
    minValue = min(testlist)
    maxValue = max(testlist)
    print("최대값{}, 최소값{}".format(minValue,maxValue))
    for _ in range(testlist.count(minValue)) :
        testlist.remove(minValue)
    for _ in range(testlist.count(maxValue)) :
        testlist.remove(maxValue)
    avr = 0;
    if len(testlist) != 0 :
        avr = sum(testlist)/len(testlist)
    else :
        pass
    return avr;