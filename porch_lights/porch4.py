import math, opc, time, random

client = opc.Client('localhost:7890')

num_pixels = 540
num_rows = 27
num_cols = 20
x_spacing = 16
y_spacing = 3.3

color_array = [0 for i in range(0,512)]
[color_array.append(i-512) for i in range(512,768)]
[color_array.append(255) for i in range(768,1280)]
[color_array.append(1535-i) for i in range(1280,1536)]

def getX(i):
	if i == 0:
		return 0
	else:
		return int(math.floor(i/num_rows))

def getY(i):
	if i == 0:
		return 0
	else:	
		if math.floor(i/num_rows)%2 == 0:
			return int((i%num_rows))
		else:
			return int((num_rows -1)-(i%num_rows))

def getLightNumber(x,y):
	if x%2 == 0:
		return(x*num_rows + y)
	else:
		return(x*num_rows + 26 - y)

def getDistance(x,y):
	return (round(math.sqrt((x * x_spacing)**2 + (y * y_spacing)**2),2))

def getOffset(distance):
	if distance == 0:
		return 0
	else:
		return round(( (len(color_array)-1) / getDistance((num_cols-1),(num_rows-1)) * distance),0)

def dripShift(array):
	for i in array:
		if i[0] < 1:
			i.insert(0,(i[0]+.2))
		else:
			i.insert(0,1)
	return([i[:-1] for i in array])

def startDrip(array):
	array[random.randint(0, (num_cols-1))][0] = 0
	return array

def getRainbowColor(x,y,increment):
	rVal=(offset_array[x][y] + increment) % 1536 
	gVal=(offset_array[x][y] + increment + 512) % 1536 
	bVal=(offset_array[x][y] + increment + 1024) % 1536
	return [color_array[rVal],color_array[gVal],color_array[bVal]]

def dual_wave(i, top_len=20, bot_len=20, offset='sync'):
	if offset=='sync':
		delta = math.pi
	else:
		delta = 0

	wave_array = [[1 for y in range(num_rows)] for x in range(num_cols)]	
	for x in range(num_cols):
		top_num = int(round((4*(math.sin(math.pi * i * (2/top_len))) + 4),0))
		bot_num = int(round((4*(math.sin(math.pi * i * (2/bot_len)+delta)) + 4),0))
		for y in range(top_num):
			wave_array[x][y] = 0
		for y in range(bot_num):
			wave_array[x][26-y] = 0
		i = i + 1
	return(wave_array)

def random_shadow(increment):
	setarray = [6,22,12,1,19,7,23,12,3,20,7,17,1,13,23,4,15,2,16,22]
	#set all 1s in a 2d vector of num_rows x num_cols
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	for x in range(num_cols):
		for i in range(5):
			shadow[x][((setarray[x]+i+increment)%27)]=0
	return(shadow)

mapping_array = [[int(getLightNumber(x,y)) for y in range(num_rows)] for x in range(num_cols)]
distance_array = [[getDistance(x,y) for y in range(num_rows)] for x in range(num_cols)]
offset_array = [[int(getOffset(y)) for y in distance_array[x]] for x in range(len(distance_array))]



increment = 0
color_delay = 2
color_lap = 0
drip_delay = 999 #set to 999 to initialize design
drip_lap = 0
string = [(0,0,0) for i in range(num_pixels)]

while True:
	shadow_array = random_shadow(drip_lap)
	for x in range(num_cols):
		for y in range(num_rows):
			rVal = getRainbowColor(x,y,increment)[0] * shadow_array[x][y]
			bVal = getRainbowColor(x,y,increment)[1] * shadow_array[x][y]
			gVal = getRainbowColor(x,y,increment)[2] * shadow_array[x][y]
			string[mapping_array[x][y]] = (rVal, bVal, gVal)
	client.put_pixels(string)
	client.put_pixels(string)
	drip_lap = drip_lap+1
	time.sleep(.1)


#print(string)
#print(map_test)
#print(getRainbowColor(300, 10)[1])



#print(getX(480))
#print(getY(480))
#print(getDistance(480))
#print(distance_array)
#print(max(distance_array))
#print(offset_array)
#print(max(offset_array))
#print(string)
#print(mapping_array)
#print(getLightNumber(16,1))

#while not kill_pattern.isSet():
# while True:
# 	for i in range(num_pixels): 
# 		rVal=(offset_array[i] + increment) % 1536 
# 		gVal=(offset_array[i] + increment + 512) % 1536 
# 		bVal=(offset_array[i] + increment + 1024) % 1536
# 		string[i] = (rgbString[rVal],rgbString[gVal],rgbString[bVal])
# 	client.put_pixels(string)
# 	time.sleep(1)
# 	increment = increment + 1
# string = [(0,0,0) for i in range(num_pixels)]	
# for i in range(num_pixels): 
# 	rVal=(offset_array[i] + increment) % 1536 
# 	gVal=(offset_array[i] + increment + 512) % 1536 
# 	bVal=(offset_array[i] + increment + 1024) % 1536
# 	string[i] = (color_array[rVal],color_array[gVal],color_array[bVal])

# map_test = [0 for i in range(num_pixels)]
# for x in range(num_cols):
# 	for y in range(num_rows):
# 		map_test[mapping_array[x][y]] = distance_two_array[x][y]

# while True:
# 	if drip_lap%drip_delay == 0:
# 		if drip_delay == 999: #initialize drip array
# 			drip_array = [[1 for i in range(num_rows)] for j in range(num_cols)]
# 		drip_delay = random.randint(10, 25)
# 		drip_lap = 0
# 		drip_array = dripShift(drip_array)
# 		drip_array = startDrip(drip_array)
# 	else:
# 		drip_array = dripShift(drip_array)

# 	if color_lap%color_delay == 0:
# 		color_lap = 0
# 		increment = increment + 10

# 	#combine arrays
# 	for x in range(num_cols):
# 		for y in range(num_rows):
# 			rVal = getRainbowColor(x,y,increment)[0] * drip_array[x][y]
# 			bVal = getRainbowColor(x,y,increment)[1] * drip_array[x][y]
# 			gVal = getRainbowColor(x,y,increment)[2] * drip_array[x][y]
# 			string[mapping_array[x][y]] = (rVal, bVal, gVal)

# 	client.put_pixels(string)
# 	time.sleep(.02)
# 	drip_lap = drip_lap + 1
# 	color_lap = color_lap + 1
