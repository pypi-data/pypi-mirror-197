def listSort(sortList) :
    """
    리스트에 숫자를 넣으면 자동으로 오름차순으로 만드는 함수
    """

    # sortList = [1,8,3,1,8,3,9,15,0]

    print("기존값 : ",sortList)

    step1 = sortList.sort()

    step2 = print("결과값 : ",sortList)
    return;