######################################################
# 폴더 별 필요 수량을 위한 FUNCTION
######################################################

######################################################
# get_list_v2()를 쓰기 위한 조건
# 1. folder_list=list()형태로 file path의 모든 모음일 것.
# 2. count_list는 무조건 list()형태로서 하나 이상의 값을 가질 것
#    - 애초에 root 경로, 즉 전체 파일 중 수량을 가져오는 것이나 마찬가지이기 때문
# 3. path_count는 경로를 뜻하는 '/'의 개수.
#    - 예를 들어, object1/object1-1/object1-1-1/file1 이라는 경로가 있을 때
#      object1-1을 기준으로 꺼내고 싶다면 path_count = 2를 입력하고
#      object1-1-1을 기준으로 한다면 path_count = 3을 변수에 저장하면 됨.


######################################################
# Example_path
######################################################

# object1/object1-1/object1-1-1/file1-1, file1-2, file1-3
# object1/object1-1/object1-1-2/file2-1, file2-2, file2-3
# object1/object1-1/object1-1-3/file3-1, file3-2, file3-3

######################################################


import random
import os


def get_random(folder_list, cnt):
    tmp_list = folder_list
    random.shuffle(tmp_list)

    return tmp_list[:cnt]


def path_dice(folder_list, count_list, path_count):
    """
    위와 같은 경로가 있을 때
    "최하위 폴더에서 1개씩 가져온다."라는 조건이라면
    get_list_v2(file_path_list, [1], 3)


    "object1-1에 존재하는 파일 중 랜덤으로 1개를 가져온다."라는 조건이라면
    get_list_v2(file_path_list, [1], 2)


    "object1-1-1 >> 2개
    object1-1-2 >> 3개
    object1-1-3 >> 1개
    순으로 가져온다.
    "
    라는 조건이라면

    get_list_v2(file_path_list, [2, 3, 1], 3)
    """

    file_path_list = list()
    result_list = list()
    path_list = list()
    cnt = 0

    for temp in folder_list:
        temp_path = os.path.split(temp)[0]
        temp_str = ''
        result_str = ''
        for t in temp_path:
            temp_str += t

            if temp_str.count('/') == path_count - 1:
                result_str = temp_str + '/'

        if result_str not in file_path_list:
            file_path_list.append(result_str)

    for temp_2 in file_path_list:
        path_list = []
        for i in folder_list:
            if temp_2 in i:
                path_list.append(i)
        if len(count_list) > 1:
            path_list = get_random(path_list, count_list[cnt])
        else:
            path_list = get_random(path_list, count_list[0])

        cnt += 1
        for j in path_list:
            result_list.append(j)

    return result_list
