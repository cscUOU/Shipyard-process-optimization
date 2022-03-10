from generator import generator
from evaluate import evaluate
import pandas as pd
import random
import numpy as np
import copy
import matplotlib.pyplot as plt
from scipy import stats
from util import order

pd.set_option('display.max_rows', 500)

SEED = 3
random.seed(SEED)
np.random.seed(SEED)
# numpy 옵션
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

params = [30, 30, 3, 7, 0, 100, 100]
flag = [True, True, True, True]

new_map, new_df = generator(params, flag)

# 스케줄 복사
df_copy = copy.deepcopy(new_df)

# 맵 복사
new_map_copy = copy.deepcopy(new_map)

x_axis, y_axis = order.order(df_copy)


#plot
x_axis_list_str = list(map(str, x_axis))
x_index_list = [i for i,j in enumerate(x_axis)]
# print(x_index_list)
# plt.plot(x_axis_list_str, y_axis, 'ok')
# helper = np.arange(len(x_axis_list_str))
# # helper1 = np.arange(len(y_axis_list_str))
# plt.xticks(ticks=helper, labels=x_axis_list_str)
# # plt.yticks(ticks=helper1, labels=y_axis_list_str)
# plt.xlabel('in order')
# plt.ylabel('out order')
# plt.title('order scatter')
# plt.show()
# plt.close()
# print(x_axis)
# print(y_axis)

# plt.scatter(x_index_list, y_axis)
# plt.show()

print(stats.pearsonr(x_index_list, y_axis))
