import math

num_columns = 20
num_rows = 27
increment = 0



def symetric_wave(i):
	wave_array = [[1 for y in range(num_rows)] for x in range(num_columns)]	
	for x in range(num_columns):
		top_num = int(round((4*(math.sin(math.pi * i / 10 )) + 4),0))
		for y in range(top_num):
			wave_array[x][y] = 0
		for y in range(top_num):
			wave_array[x][26-y] = 0
		i = i + 1
	return(wave_array)

def sync_wave(i):
	wave_array = [[1 for y in range(num_rows)] for x in range(num_columns)]	
	for x in range(num_columns):
		top_num = int(round((4*(math.sin(math.pi * i / 10 )) + 4),0))
		bot_num = int(round((4*(math.sin((math.pi * i / 10) + math.pi )) + 4),0))
		for y in range(top_num):
			wave_array[x][y] = 0
		for y in range(bot_num):
			wave_array[x][26-y] = 0
		i = i + 1
	return(wave_array)	

def async_wave(i,top_len,bot_len):
	wave_array = [[1 for y in range(num_rows)] for x in range(num_columns)]	
	for x in range(num_columns):
		top_num = int(round((4*(math.sin(math.pi * i * (2/top_len))) + 4),0))
		bot_num = int(round((4*(math.sin(math.pi * i * (2/bot_len))) + 4),0))
		for y in range(top_num):
			wave_array[x][y] = 0
		for y in range(bot_num):
			wave_array[x][26-y] = 0
		i = i + 1
	return(wave_array)		

def dual_wave(i, top_len=20, bot_len=20, offset='sync'):
	if offset=='sync':
		delta = math.pi
	else:
		delta = 0

	wave_array = [[1 for y in range(num_rows)] for x in range(num_columns)]	
	for x in range(num_columns):
		top_num = int(round((4*(math.sin(math.pi * i * (2/top_len))) + 4),0))
		bot_num = int(round((4*(math.sin(math.pi * i * (2/bot_len)+delta)) + 4),0))
		for y in range(top_num):
			wave_array[x][y] = 0
		for y in range(bot_num):
			wave_array[x][26-y] = 0
		i = i + 1
	return(wave_array)

def testy(i,**x):
	print(i)
	if 'first' in x:
		print(x['first'])

print(dual_wave(0,offset = 'async'))
