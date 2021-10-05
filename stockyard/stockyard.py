import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import pandas as pd
from stockyard.method import inout_2quad, inout_random, inout_depth, \
    inout_4quad
from stockyard.util import schedule, weight, plot, map_create
import argparse
from tqdm import tqdm


pd.set_option('display.max_rows', 500)

SEED = 3
random.seed(SEED)
np.random.seed(SEED)
# numpy 옵션
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def random(df, new_map, flag, index, total_list):
    curr = 0
    insert_cnt = 0
    area = 0
    out_cnt = 0

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_random.insert(task, new_map, flag, insert_cnt, area, df)
        if task.type == 2:
            out_cnt, df = inout_random.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df):
            break

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)


def depth(df, new_map, flag, weight_map, index, total_list):
    curr = 0
    insert_cnt = 0
    area = 0
    out_cnt = 0

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_depth.insert(task, new_map, weight_map, insert_cnt, area, df, flag)
        if task.type == 2:
            out_cnt, df = inout_depth.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df):
            break

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)


def quad2(df, new_map, flag, weight_map, index, total_list):
    curr = 0
    insert_cnt = 0
    area = 0
    out_cnt = 0

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_2quad.insert(task, new_map, weight_map, insert_cnt, area, df, flag)
        if task.type == 2:
            out_cnt, df = inout_2quad.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df) - 1:
            break

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)


def quad4(df, new_map, flag, weight_map, index, total_list):
    curr = 0
    insert_cnt = 0
    area = 0
    out_cnt = 0

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_4quad.insert(task, new_map, weight_map, insert_cnt, area, df, flag,
                                                    curr, branch=0)
        if task.type == 2:
            out_cnt, df = inout_4quad.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df) - 1:
            break

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)


def user(df, new_map, flag, index, total_list):
    '''


    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    '''


def stockyard1(ax, param, epoch, flag, methods):
    # epoch, flag, methods = opt.epoch, opt.flag, opt.method
    param_block = param

    total_insert_cnt = [[] for _ in range(len(methods))]
    total_area = [[] for _ in range(len(methods))]
    total_out_cnt = [[] for _ in range(len(methods))]

    total_list = [total_insert_cnt, total_area, total_out_cnt]

    for _ in tqdm(range(epoch)):

        n_block = param_block[4]  # 기적치블록 개수
        block_number = 0  # 출고 순서 -> 나중에 스케줄에서 들고 와야함

        # 각 블록 정보 들어있는 리스트
        stockyard_list = []

        # 적치장 생성
        new_map = map_create.Map(param_block[0], param_block[1])

        # weight 맵 생성
        weight_map = weight.create_weight(new_map.x_size, new_map.y_size, flag)
        # weight_map = weight.color(weight_map)

        # 블록 생성
        for k in range(n_block):
            stockyard_list.append(map_create.Block(new_map, weight_map, param_block[2], param_block[3],
                                                   block_number=k))
            block_number += 1

        # 기존 블록 개수 넘겨서 새 입고 블록 생성
        insert_block = schedule.exist_block(len(stockyard_list), param_block[2], param_block[3], param_block[5])
        total_insert_num = len(insert_block) + len(stockyard_list)

        # 스케쥴 생성해서 받아오기
        df = schedule.out_block(stockyard_list, insert_block, total_insert_num, param_block[6])
        df = df.fillna(value=0)

        # 스케줄 복사
        df_copy = [copy.deepcopy(df) for _ in range(len(methods))]

        # 맵 복사
        new_map_copy = [copy.deepcopy(new_map) for _ in range(len(methods))]

        # 함수 실행
        for index, method in enumerate(methods):
            if method == 'random':
                random(df_copy[index], new_map_copy[index], flag, index, total_list)
            if method == 'depth':
                depth(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'quad2':
                quad2(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'quad4':
                quad4(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'user':
                user(index, total_list)

    # 결과 출력
    for index, method in enumerate(methods):
        print(method)
        print("total_insert_avg =", np.mean(total_list[0][index]))
        print("total_area_avg =", np.mean(total_list[1][index]))
        print("total_out_avg = ", np.mean(total_list[2][index]))

    # plot
    label = [method for method in methods]
    x_list = total_list[2]  # total_out_cnt
    y_list = total_list[1]  # total_area
    plot.scatter(ax, x_list, y_list, label)


def stockyard(ax, param):
    epoch, flag, methods = opt.epoch, opt.flag, opt.method
    param_block = param

    total_insert_cnt = [[] for _ in range(len(methods))]
    total_area = [[] for _ in range(len(methods))]
    total_out_cnt = [[] for _ in range(len(methods))]

    total_list = [total_insert_cnt, total_area, total_out_cnt]

    for _ in tqdm(range(epoch)):

        n_block = param_block[4]  # 기적치블록 개수
        block_number = 0  # 출고 순서 -> 나중에 스케줄에서 들고 와야함

        # 각 블록 정보 들어있는 리스트
        stockyard_list = []

        # 적치장 생성
        new_map = map_create.Map(param_block[0], param_block[1])

        # weight 맵 생성
        weight_map = weight.create_weight(new_map.x_size, new_map.y_size, flag)
        # weight_map = weight.color(weight_map)

        # 블록 생성
        for k in range(n_block):
            stockyard_list.append(map_create.Block(new_map, weight_map, param_block[2], param_block[3],
                                                   block_number=k))
            block_number += 1

        # 기존 블록 개수 넘겨서 새 입고 블록 생성
        insert_block = schedule.exist_block(len(stockyard_list), param_block[2], param_block[3], param_block[5])
        total_insert_num = len(insert_block) + len(stockyard_list)

        # 스케쥴 생성해서 받아오기
        df = schedule.out_block(stockyard_list, insert_block, total_insert_num, param_block[6])
        df = df.fillna(value=0)

        # 스케줄 복사
        df_copy = [copy.deepcopy(df) for _ in range(len(methods))]

        # 맵 복사
        new_map_copy = [copy.deepcopy(new_map) for _ in range(len(methods))]

        # 함수 실행
        for index, method in enumerate(methods):
            if method == 'random':
                random(df_copy[index], new_map_copy[index], flag, index, total_list)
            if method == 'depth':
                depth(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'quad2':
                quad2(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'quad4':
                quad4(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list)
            if method == 'user':
                user(index, total_list)

    # 결과 출력
    for index, method in enumerate(methods):
        print(method)
        print("total_insert_avg =", np.mean(total_list[0][index]))
        print("total_area_avg =", np.mean(total_list[1][index]))
        print("total_out_avg = ", np.mean(total_list[2][index]))

    # plot
    label = [method for method in methods]
    x_list = total_list[2]  # total_out_cnt
    y_list = total_list[1]  # total_area
    plot.scatter(ax, x_list, y_list, label)


def sota(epoch=None, params=None, flag=None, methods=None):
    if epoch is None:
            epoch = 10

    if params is None:
        params = [[20, 20, 3, 7, 0, 100, 100]]

    if methods is None:
        methods = ['random']

    if flag is None:
        flag = [True, True, True, True]

    parameters = {'axes.labelsize': 7,
                  'axes.titlesize': 7,
                  'xtick.labelsize': 7,
                  'ytick.labelsize': 7,
                  'legend.fontsize': 7}
    plt.rcParams.update(parameters)

    fig = plt.figure(1)

    print("start")
    for i, param in enumerate(params):
        print('블록 파라미터{}'.format(param))
        ax = fig.add_subplot(1, len(params), i + 1)
        stockyard1(ax, param, epoch, flag, methods)

    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='stockyard test')
    parser.add_argument('--epoch', default=10, type=int)
    parser.add_argument('--params', default=[20, 20, 3, 7, 0, 100, 100], nargs='+', type=int, help='20 20 3 7 0 100 100')
    parser.add_argument('--flag', default=[True, True, True, True], nargs='+', type=bool, help='True True True True')
    parser.add_argument('--method', default=['random'], nargs='+', help='random, depth, quad2, quad4')
    opt = parser.parse_args()

    '''
    맵 텍스트 파일 업로드
    '''

    # 여러 파라미터 확인 하고 싶을 때
    # 적치장 가로 세로 , 블록 사이즈 범위, 기 적치 블록, 입고 블록 수, 출구 블록 수
    '''params = [[20, 30, 3, 4, 0, 30, 30],
              [20, 30, 3, 4, 15, 30, 30],
              [20, 30, 3, 7, 0, 30, 30],
              [20, 30, 3, 7, 0, 100, 100],
              [20, 40, 3, 7, 0, 100, 100],
              [40, 50, 3, 7, 0, 100, 100]]'''

    # 출입구 지정 위쪽, 왼쪽, 오른쪽, 아래쪽
    # flag = [True, True, True, True]

    parameters = {'axes.labelsize': 7,
                  'axes.titlesize': 7,
                  'xtick.labelsize': 7,
                  'ytick.labelsize': 7,
                  'legend.fontsize': 7}
    plt.rcParams.update(parameters)

    fig = plt.figure(1)
    params = [opt.params]

    print(opt)
    print("start")
    for i, param in enumerate(params):
        print('블록 파라미터{}'.format(param))
        ax = fig.add_subplot(1, len(params), i+1)
        stockyard(ax, param)

    plt.show()