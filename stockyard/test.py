import stockyard
#inital value
epoch = 100
flag = [True,True,True,True]

# 여러 파라미터 확인
params = [[20, 30, 3, 7, 0, 200, 200]]
# 여러 메소드 확인
methods = ['quad2']
stockyard.sota(epoch=epoch, params=params, flag=flag, methods=methods)