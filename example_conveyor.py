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


