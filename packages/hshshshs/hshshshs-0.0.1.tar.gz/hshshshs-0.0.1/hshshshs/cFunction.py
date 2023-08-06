def minMaxAvg(testlist):
    """
    최소 최댓값을 뺀 평균
    parameter : testlist = 리스트 
    return : 리스트내 값에서 최소 최대값을 뺀 평균을 반환한다
    """
    minValue = min(testlist)
    maxValue = max(testlist)

    print('최소값 : {} ,최대값 :  {}'.format(minValue,maxValue))

    testlist.remove(minValue)
    testlist.remove(maxValue)

    if len(testlist) !=0 :
        average  = sum(testlist) / len(testlist)
    else: 
        pass
    
    return average