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
	rtn = math.floor(i/num_rows) * x_spacing
	return (rtn)

def getY(i):
	if math.floor(i/num_rows)%2 == 0:
		rtn = (i%num_rows) * y_spacing
	else:
		rtn = ((num_rows -1)-(i%num_rows))*y_spacing
	return (rtn)

def getDistance(i):
	rtn = round(math.sqrt(getX(i)**2 + getY(i)**2),2)
	return (rtn)

def getOffset(i,max_distance):
	if i == 0:
		return 0
	else:
		return round((1535/max_distance * i),0)

distance_array = [getDistance(i) for i in range(0,num_pixels)]
offset_array = [int(getOffset(i,max(distance_array))) for i in distance_array]

display_array = [()]
increment = 0
string = [(0,0,0) for i in range(num_pixels)]	
wiggle_array = [random.randint(-225, 225) for i in range(num_pixels)]
while True:
	for i in range(num_pixels): 
		rVal=(wiggle_array[i] + increment) % 1536 
		gVal=(wiggle_array[i] + increment + 512) % 1536 
		bVal=(wiggle_array[i] + increment + 1024) % 1536
		string[i] = (color_array[rVal],color_array[gVal],color_array[bVal])
	client.put_pixels(string)
	time.sleep(.25)
	increment = increment + 10