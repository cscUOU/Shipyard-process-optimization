from matplotlib import pyplot as plt
import numpy as np


def order(df):
    # print(df)
    # print(df[df.type == 1])  # 입고인 블럭만
    # print(df[df.duplicated(['block_number']) == True])  # 당일 입고 되었다가 출고되는 블럭
    # exist_block = df[df.position_x != 0]
    # print(exist_block)
    # y = list(range(len(exist_block)))
    # x_axis = exist_block.append(df[df.type == 1]).reset_index()  # x 축
    # print(df)
    x_axis = df[df.type == 1].reset_index(drop=True)
    y_axis = df[df.type == 2].reset_index(drop=True)  # y 축
    #
    # print(x_axis)
    # print(y_axis)

    x_axis_list = x_axis['block_number'].tolist()
    # print("x_axis_list ", x_axis_list)
    # print(y)
    y_axis_list = []

    temp_list = []
    dup_list = []
    dup_del_list = []
    dup_set = set()

    # 중복 요소 찾기
    for i,j in enumerate(x_axis_list):
        if j in temp_list:
            dup_set.add(j)
        else:
            temp_list.append(j)
    # 중복 요소의 각 인덱스 찾기
    for i in dup_set:
        indexes = [a for a, b in enumerate(x_axis_list) if i == b]
        dup_list.append(indexes)
    # 맨 뒤 값 제외한 인덱스 만
    dup_del_list = [j for i in dup_list for j in i[:-1]]
    # print(dup_list)
    # print(dup_del_list)
    # 중복 제거
    for index in sorted(dup_del_list, reverse=True):
        del x_axis_list[index]

    x_len = len(x_axis_list)
    for i in range(x_len):
        y = y_axis.loc[x_axis_list[i] == y_axis.block_number, 'block_number'].index.tolist()
        if not y:
            y_axis_list.append(x_len)
        else:
            y_axis_list.extend(y)
        # y_axis.loc[x_axis_list[i] == y_axis.block_number, 'block_number'].index.value
    # print("x_axis_list", x_axis_list)
    # print("y_axis_list ", y_axis_list)
    # x_axis_list_str = list(map(str, x_axis_list))
    # y_axis_list_str = list(map(str, y_axis_list))
    # ######################################
    # plt.plot(x_axis_list_str, y_axis_list, 'ok')
    # helper = np.arange(len(x_axis_list_str))
    # # helper1 = np.arange(len(y_axis_list_str))
    # plt.xticks(ticks=helper, labels=x_axis_list_str)
    # # plt.yticks(ticks=helper1, labels=y_axis_list_str)
    # plt.xlabel('in order')
    # plt.ylabel('out order')
    # plt.title('order scatter')
    # plt.show()
    # plt.close()

    return x_axis_list, y_axis_list
