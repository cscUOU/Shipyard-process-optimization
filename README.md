# 조선소 공정물류 최적화

## 1. 공정 스케줄링 최적화



------------

## 2. 트랜스포터 스케줄링 최적화
조선소 내에서 트랜스포터의 대수 및 이동 최적화 알고리즘
* Approach -> Minimize the number of transporters and the tolerance movement distance by optimizing the placement of tasks in the transporter 

* Generator -> make map, transporter
  * parameters - (map informations, transporter informations)
    * map informations - [stockyard position, intersection position, road_information]
			                      * road_information - [position, distance, width]
    * transporter informations - [work speed, empty speed, weight, width]

* Evaluation -> The number of transporters, distance of the transporter.

* Example
```python

stock_data, inter_data, road_data = object_data()

# Generator Map
graph = Graph(stock_data, inter_data, road_data)

# Generator Transporter
trans_manager = Trans_manager()
transporter_data(transporter_num, trans_manager, graph)

###
modify_schdule
###

# Evaluate
temp_f = base_pop.getfitness(work_time=task_work_time, empty_time=task_empty_time)
```

* 알고리즘 종류
 * 랜덤, 대수 최소화 휴리스틱, 이동 최소화 휴리스틱, 유전알고리즘


------------

## 3. 적치장 내 블록 배치 최적화
적치장 내에서 블록 반입 • 반출 최적화 알고리즘
* Approach -> Minimize obstruction blocks by optimizing the position of insertion blocks 

* Generator -> make map, schedule
  * parameters - (map informations, entrance)
    * map informations - [horizontal length, vertical length,Number of blocks placed, Number of blocks to be insert, Number of blocks to be out]
    * entrance - [top, bottom, left, right]   

* Evaluation -> Number of impossible insert blocks, Number of obstructing blocks

* Example
```python

map_inf = [20,20,3,7,0,100,100]
entrance = [True,True,True,True]

new_map, new_df = shipyard.generator(map_inf, entrance)

###
modify_schdule
###

insert_cnt, out_cnt = shipyard.evaluate(modify_df, new_map, flag)
```

* 알고리즘 종류
 * 랜덤, 깊이, 2사분면, 4사분면


------------
