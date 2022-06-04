<div align="center">
<p>
   <a align="left" href="https://cscuou.github.io/" target="_blank">
   <img width="850" src="https://github.com/cscUOU/Shipyard-process-optimization/blob/main/images/shipyard.png"></a>
</p>
</div>
<br>

# <div align="center">조선소 공정물류 최적화</div>
<br></br>


<details open>
<summary>Install</summary>

Python 3.8.3 버전 필요합니다.

```bash
$ git clone https://github.com/cscUOU/Shipyard-process-logistics-optimization.git
$ cd Shipyard-process-logistics-optimization
$ pip install -r requirements.txt
```

</details>

## <div align="center">1. 공정 스케줄링 최적화</div>
<div align="center">
<p>
   <a align="left" href="https://cscuou.github.io/" target="_blank">
   <img width="150" src="https://github.com/cscUOU/Shipyard-process-optimization/blob/main/images/shipyard1.png"></a>
</p>
</div>

<div align="center">공정 스케줄링 최적화</div>

<details>
<summary>Description</summary>

* 목적 - 컨베이어 환경에서 작업물 투입 순서 최적화를 통한 전체 작업 시간 최소화

	
* generate_worklist(n_work, n_process) : 작업물 리스트 생성
  * 매개변수
    * n_work : 작업물 개수
    * n_process : 공정 개수
  * 반환
    * works : 작업물 리스트
    * works_type : 작업물 종류
	
* unidev_search(works) : 작업물 투입 순서 최적화 - unidev 탐색
  * 매개변수
    * works : 작업물 리스트
  * 반환
    * works : 투입 순서가 최적화된 작업물 리스트
    * logs : 최적화 결과 [최적화된 작업 시간, 총 반복 횟수, 총 처리 시간, 유효 탐색 횟수, best 반복 횟수, best 처리 시간, [교체대상1 선정 처리 시간, 교체대상2 선정 처리 시간, 교체 처리 시간]]

* random_bubble_search(works) : 작업물 투입 순서 최적화 - random_bubble 탐색
  * 매개변수
    * works : 작업물 리스트
  * 반환
    * works : 투입 순서가 최적화된 작업물 리스트
    * logs : 최적화 결과 [최적화된 작업 시간, 총 반복 횟수, 총 처리 시간, 유효 탐색 횟수, best 반복 횟수, best 처리 시간, [교체대상1 선정 처리 시간, 교체대상2 선정 처리 시간, 교체 처리 시간]]
	
* cal_works_time(works) : 작업물 리스트의 전체 작업 시간
  * 매개변수
    * works : 작업물 리스트
  * 반환
    * time : 전체 작업 시간
	
<details open>
<summary>Example(example_conveyor.py)</summary>

```python
import random

import numpy as np

from conveyor.conveyor import *
from conveyor.method import *
from conveyor.util import *

RANDOM_SEED = 15
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

if __name__ == "__main__":
	n_work = 10 # 10, 50, 100, 200, 400
	n_process = 6 # 6, 10, 20

        #
        works, works_type = generate_worklist(n_work, n_process)
	random.shuffle(works)

        works, logs = unidev_search(works)

        performance = cal_works_time(works)
```

</details>
	
</details>

------------
## <div align="center">2. 트랜스포터 스케줄링 최적화</div>
<div align="center">
<p>
   <a align="left" href="https://cscuou.github.io/" target="_blank">
   <img width="150" src="https://github.com/cscUOU/Shipyard-process-optimization/blob/main/images/shipyard2.png"></a>
</p>
</div>

<div align="center">조선소 내에서 트랜스포터의 대수 및 이동 최적화 알고리즘</div>

<details>
<summary>Description</summary>

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

</details>

------------
## <div align="center">3. 적치장 내 블록 배치 최적화</div>

<div align="center">
<p>
   <a align="left" href="https://cscuou.github.io/" target="_blank">
   <img width="150" src="https://github.com/cscUOU/Shipyard-process-logistics/blob/main/images/shipyard3.png"></a>
</p>
</div>

<div align="center">적치장 내에서 블록 반입 • 반출 최적화 알고리즘</div>

<details>
<summary>Description</summary>

* 목적 - 반입 블록의 위치 최적화를 통해 간섭 블록 개수의 최소화


* 생성 - 적치장 맵, 스케줄 생성
  * 매개변수 - 맵 정보, 입구
    

* 평가 - 반입 불가 블록 개수, 간섭 블록 개수


* 알고리즘 종류
    * 랜덤, 깊이우선, 2사분면, 4사분면

<details open>
<summary>Example(main.py)</summary>

```python
from generator import generator
from evaluate import evaluate

# 맵 정보 - [적치장 가로 길이, 적치장 수직 길이, 블록 가로 크기, 블록 세로 크기, 기적치 블록 개수, 입고 블록 개수, 출고 블록 개수]
map_inf = [20,20,3,7,0,100,100]
# 출입구 - [위, 아래, 왼쪽, 오른쪽]
entrance = [True,True,True,True]

new_map, new_df = generator(map_inf, entrance)

###
modify_schdule
###

insert_cnt, out_cnt = evaluate(modify_df, new_map, flag)
```

</details>

<details open>
<summary>SOTA(sota.py)</summary>

```python
import stockyard
#inital value
#epoch = 10, params = [[20, 20, 3, 7, 0, 100, 100]], flag = [True,True,True,True], methods = ['random']

# 여러 파라미터 확인
'''params = [[20, 30, 3, 4, 0, 30, 30], [20, 30, 3, 4, 15, 30, 30],[20, 30, 3, 7, 0, 30, 30],[20, 30, 3, 7, 0, 100, 100]]'''
# 여러 메소드 확인
'''methods = ['random', 'depth', 'quad2', 'quad4'] '''
    
stockyard.sota(epoch=None, params=None, flag=None, methods=None)
```

</details>

</details>

------------

## <div align="center">Contact</div>
<div align="center"><p>If you’re interested in our lab, please contact <a href="https://cscuou.github.io/">HERE</a></p></div>
