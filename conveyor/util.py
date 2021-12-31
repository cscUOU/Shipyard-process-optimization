def swap(works, conveyor, n, n_):
	n_work, n_process_seq = works.shape
	_, n_seq = conveyor.shape

	conveyor[n, n:n+n_process_seq] = np.copy(works[n_])
	conveyor[n_, n_:n_+n_process_seq] = np.copy(works[n])

	works[n], works[n_] = np.copy(works[n_]), np.copy(works[n])

def roulette_wheel(x, inverse=False):
	k = 4
	n = len(x)
	d = (k-1)/(n-1)
	sort = np.argsort(x)[::-1] if inverse else np.argsort(x)
	index_sort = np.argsort(sort)

	prob = np.array([1+d*index_sort[i] for i in range(n)])
	prob = prob/sum(prob)
	
	return prob

def nan_to_zero(x):
	return np.nan_to_num(x, nan=0, posinf=0, neginf=0)

def softmax(x):
	x = np.exp(x)
	return x/sum(x)
