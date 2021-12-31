def generate_worklist(n, n_process, generate_mode="random", time_weights=None):
	works_type = {}
	works = []

	if generate_mode == "random":
		minimum_time = 10
		maximum_time = 300
		reset_time_weights_prob = 0.05

		time_weights = [random.randint(minimum_time, maximum_time) for i in range(n_process)]
		type_name = time.time()
		works_type[type_name] = {"time":time_weights, "sort":[[] for np in range(N_PROCESS-1)]}
		for i in range(n):
			work = {}
			work["type"] = type_name
			work["time"] = []
			for tw in time_weights:
				tmp = np.random.normal(tw, np.log(tw))
				if tmp < 0:
					tmp = 0
				work["time"].append(tmp)
				
			if random.random() < reset_time_weights_prob:
				time_weights = [random.randint(minimum_time, maximum_time) for i in range(n_process)]
				type_name = time.time()
				works_type[type_name] = {"time":time_weights, "sort":[[] for np in range(N_PROCESS-1)]}
			works.append(work)

	return works, works_type

def get_conveyor(works):
	n_work, n_process_seq = works.shape

	conveyor = np.zeros((n_work, n_process_seq+(n_work-1)))
	conveyor_mask = np.zeros((n_work, n_process_seq+(n_work-1)))
	index = np.zeros((n_work, n_process_seq)).astype(np.int32)
	index_process_seq = np.arange(n_process_seq)
	index_work = np.arange(n_work)
	index += index_process_seq
	index += index_work.reshape(-1, 1)

	conveyor[index_work.reshape(-1,1), index] += works
	conveyor_mask[index_work.reshape(-1, 1), index] += 1
	
	return conveyor, conveyor_mask

def cal_conveyor_time(conveyor):
	return sum(np.amax(conveyor, axis=0))

def cal_works_time(works):
        return cal_conveyor_time(get_conveyor(works))
