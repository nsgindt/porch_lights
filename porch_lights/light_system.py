import math, opc, time, random
import light_config as config 

#setup Fadecandy
client = opc.Client('localhost:7890')

#set configs
num_pixels = config.num_pixels
num_rows = config.num_rows
num_cols = config.num_cols
x_spacing = config.x_spacing
y_spacing = config.y_spacing 
fps = config.fps


frame_delay = 1/fps

rainbow_array = [0 for i in range(0,512)]
[rainbow_array.append(i-512) for i in range(512,768)]
[rainbow_array.append(255) for i in range(768,1280)]
[rainbow_array.append(1535-i) for i in range(1280,1536)]

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
	return [rainbow_array[rVal],rainbow_array[gVal],rainbow_array[bVal]]

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

mapping_array = [[int(getLightNumber(x,y)) for y in range(num_rows)] for x in range(num_cols)]
distance_array = [[getDistance(x,y) for y in range(num_rows)] for x in range(num_cols)]
offset_array = [[int(getOffset(y)) for y in distance_array[x]] for x in range(len(distance_array))]



increment = 0
color_delay = 2
color_lap = 0
drip_delay = 999 #set to 999 to initialize design
shadow_lap = 0

#set initial string object
string = [(0,0,0) for i in range(num_pixels)]
while True:
	wave_array = dual_wave(drip_lap, offset='async')
	for x in range(num_cols):
		for y in range(num_rows):
			rVal = getRainbowColor(x,y,increment)[0] * wave_array[x][y]
			bVal = getRainbowColor(x,y,increment)[1] * wave_array[x][y]
			gVal = getRainbowColor(x,y,increment)[2] * wave_array[x][y]
			string[mapping_array[x][y]] = (rVal, bVal, gVal)
	client.put_pixels(string)
	client.put_pixels(string)
	drip_lap = drip_lap+1
	time.sleep(.1)

