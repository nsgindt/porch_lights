import math, random

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

def getRainbowColor(light_number, increment):
	rVal=(offset_array[light_number] + increment) % 1536 
	gVal=(offset_array[light_number] + increment + 512) % 1536 
	bVal=(offset_array[light_number] + increment + 1024) % 1536
	return [color_array[rVal],color_array[gVal],color_array[bVal]]

mapping_array = [[getLightNumber(x,y) for y in range(num_rows)] for x in range(num_cols)]
distance_array = [[getDistance(x,y) for y in range(num_rows)] for x in range(num_cols)]
offset_array = [[int(getOffset(y)) for y in distance_array[x]] for x in range(len(distance_array))]

# map_test = [0 for i in range(num_pixels)]
# for x in range(num_cols):
# 	for y in range(num_rows):
# 		map_test[mapping_array[x][y]] = distance_two_array[x][y]

increment = 0
color_delay = 12
color_lap = 0
drip_delay = 999 #set to 999 to initialize design
drip_lap = 0
string = [(0,0,0) for i in range(num_pixels)]

while True:
if drip_lap%drip_delay == 0:
	if drip_delay == 999: #initialize drip array
		drip_array = [[1 for i in range(num_rows)] for j in range(num_cols)]
	drip_delay = random.randint(10, 75)
	drip_lap = 0
	drip_array = dripShift(drip_array)
	drip_array = startDrip(drip_array)
else:
	drip_array = dripShift(drip_array)

if color_lap%color_delay == 0:
	color_lap = 0
	increment = increment + 1

#combine arrays
for x in range(num_cols):
	for y in range(num_rows):
		string[getLightNumber(x,y)] = (getRainbowColor(getLightNumber(x,y),increment)[0]*drip_array[x][y], getRainbowColor(getLightNumber(x,y),increment)[1]*drip_array[x][y], getRainbowColor(getLightNumber(x,y),increment)[2]*drip_array[x][y] )



print(offset_array)
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

