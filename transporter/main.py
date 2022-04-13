import collections
import itertools
import math
import time
import copy
import time
import numpy as np
import random

# 트랜스 포터 작업 개수,
# 염색체 세대 수, 트랜스 포터 작업 개수
from global_var import *
from Data_create.call_data import object_data
from Data_create.create_trans import transporter_data
from Object.graph import Graph
from Object.Transporter import Trans_manager  # , child_Trans_manager
from Task.Task import Task_schedule, task_classification
from Simulation import perform_graph
from Simulation.transporter_view import transporter_schedule_view
from Generation.Population import Population
from Generation.Gen import GA
from Heuristic.Heuristic_condition import H1, H2, H3
from TSP import *

np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # inf = infinity

######################## 변수 로드 #########################
# 데이터 불러오기
stock_data, inter_data, road_data = object_data()

# 그래프 생성
graph = Graph(stock_data, inter_data, road_data)

# 트랜스포터 목록 들고 오기
trans_manager = Trans_manager()
transporter_data(transporter_num, trans_manager, graph)

##########################################################

time_perform = []
trans_perform, dis_perform, c = [], [], 0
prev = time.time()

base_s = None
task_work_time = None
task_empty_time = None
origin_task_list = None

for w_index, work_num in enumerate(task_num):
    ######################## 데이터 생성 함수 #########################
    # 작업목록 스케줄 생성 및 작업 관계 생성
    task_manager = Task_schedule(graph, work_num)
    ################################################################

    # 작업 시간, 작업 간 이동 시간, 공차 시간
    task_work_time, task_empty_time, empty_speed = task_classification(task_manager.task_list,
                                                                       trans_manager.transporter_list,
                                                                       graph=graph)

    ######################## 휴리스틱 알고리즘 #########################
    # 휴리스틱 1번
    # 트랜스포터의 대수 최소화
    # 작업량이 적은 트랜스포터 (a)에 있는 작업을 작업량이 많은 트랜스포터 (b)에 할당
    # 그 후, 트랜스포터 (b)는 새로운 작업의 공차거리를 최소화할 수 있는 순서에 작업 배치
    h1 = H1(task_work_time, task_empty_time, task_manager.task_list, graph=graph)

    # 초기 세대 생성
    pop = Population(task_work_time, task_empty_time, trans_manager, task_manager, initialise=True)
    ga_base = GA(task_manager, task_work_time, task_empty_time, h1=h1)
    ga_random = GA(task_manager, task_work_time, task_empty_time)

    # 최적해 탐색                           #100
    for g_index, generation in enumerate(n_generations):
        pop_base = copy.deepcopy(pop)
        pop_random = copy.deepcopy(pop)

        random_f, random_s = 0, None
        base_f, base_s = 0, None
        for i in range(generation):
            ########### 휴리스틱 알고리즘 돌아가는 부분 ###########

            pop_random = ga_random.evolvePopulation(pop_random, trans_manager, random_flag=True)
            pop_base = ga_base.evolvePopulation(pop_base, trans_manager, base_flag=True)
            ##################################################
            print("{}/{}/{}".format(w_index, g_index, i / generation))
            ################## 평가함수 ####################

            base_pop = pop_base.getfittest()
            temp_f = base_pop.getfitness(work_time=task_work_time, empty_time=task_empty_time)
            if base_f < temp_f:
                base_s = copy.deepcopy(base_pop)
                base_f = temp_f

            random_pop = pop_random.getfittest()
            temp_f = random_pop.getfitness(work_time=task_work_time, empty_time=task_empty_time)
            if random_f < temp_f:
                random_s = copy.deepcopy(random_pop)
                random_f = temp_f

        # 트랜스포터 대수, 작업 시간, 공차 시간, 총 소요 시간, 총 이동 거리, 작업 list, 트랜스포터 번호
        base_trans_cnt, base_working_time, base_empty_time, base_total_time, base_total_dist, base_origin_task_list, base_origin_trans_num = base_s.gettrans_num_time(task_work_time, task_empty_time)
        random_trans_cnt, random_working_time, random_empty_time, random_total_time, random_empty_dist, random_origin_task_list, random_origin_trans_num = random_s.gettrans_num_time(task_work_time, task_empty_time)

        print('작업 개수:', *task_num)
        print('\t\t 트랜스포터 대수 \t 이동거리 \t tsp 적용')

        origin_dist = 0
        tsp_dist = 0
        for i in base_origin_task_list:
            ret = tsp(graph, i)
            t1, t2, _ = ret
            origin_dist += t1
            tsp_dist += t2

        print('base\t\t', base_trans_cnt, '\t\t\t', origin_dist, '\t\t', tsp_dist)

        origin_dist = 0
        tsp_dist = 0
        for i in random_origin_task_list:
            if len(i) == 1:
                origin_dist += graph.distance_node(0, init_position, i[0][0])
                origin_dist += graph.distance_node(0, i[0][0], i[0][1])
                origin_dist += graph.distance_node(0, i[0][1], init_position)
                tsp_dist += graph.distance_node(0, init_position, i[0][0])
                tsp_dist += graph.distance_node(0, i[0][0], i[0][1])
                tsp_dist += graph.distance_node(0, i[0][1], init_position)
                continue
            ret = tsp(graph, i)
            t1, t2, _ = ret
            origin_dist += t1
            tsp_dist += t2

        print('random\t\t', random_trans_cnt, '\t\t', origin_dist, '\t', tsp_dist)