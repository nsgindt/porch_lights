from flask import Flask, render_template
import datetime, opc, time, random, math
from threading import Thread, Event
import light_config as config 

sys_name = config.sys_name

#import opc
app = Flask(__name__)

settings = {
	'power' : False,
	'color' : 'none',
	'pattern': 'none',
	'pattern_running': False
}

#set up pattern thread
thread = Thread()
kill_pattern = Event()

#setup Fadecandy
client = opc.Client('localhost:7890')

#set configs
num_pixels = config.num_pixels
num_rows = config.num_rows
num_cols = config.num_cols
x_spacing = config.x_spacing
y_spacing = config.y_spacing 
fps = config.fps

#calculated configs
frame_delay = 1/fps
num_pixels = num_rows * num_cols

rainbow_array = [0 for i in range(0,512)]
[rainbow_array.append(i-512) for i in range(512,768)]
[rainbow_array.append(255) for i in range(768,1280)]
[rainbow_array.append(1535-i) for i in range(1280,1536)]

class PatternThread(Thread):
	def __init__(self, pattern, color):
		self.pattern = pattern
		self.color = color
		self.delay = 1
		super(PatternThread,self).__init__()

	# def rainbowWave(self):
	# 	increment = 0
	# 	color_delay = 2
	# 	color_lap = 0
	# 	drip_lap = 0
	# 	string = [(0,0,0) for i in range(num_pixels)]
	# 	while not kill_pattern.isSet():
	# 		wave_array = dual_wave(drip_lap, offset='async')
	# 		for x in range(num_cols):
	# 			for y in range(num_rows):
	# 				rVal = getRainbowColor(x,y,increment)[0] * wave_array[x][y]
	# 				bVal = getRainbowColor(x,y,increment)[1] * wave_array[x][y]
	# 				gVal = getRainbowColor(x,y,increment)[2] * wave_array[x][y]
	# 				string[mapping_array[x][y]] = (rVal, bVal, gVal)
	# 		client.put_pixels(string)
	# 		client.put_pixels(string)
	# 		drip_lap = drip_lap+1
	# 		time.sleep(.1)

	# def wiggleFade(self):
	# 	print('starting wiggleFade')
	# 	wiggleArray = [0 for i in range(numLEDs)]
	# 	string = [black] * numLEDs
	# 	increment = 0
	# 	for i in range(numLEDs):
	# 		wiggleArray[i] = random.randint(-17, 17)        
	# 	while not kill_pattern.isSet():
	# 		for i in range(numLEDs):
	# 			rVal=(wiggleArray[i]+increment) % 105 
	# 			gVal=(wiggleArray[i]+increment+35) % 105 
	# 			bVal=(wiggleArray[i]+increment+70) % 105 
	# 			string[i] = (rFade[rVal],rFade[gVal],rFade[bVal])
	# 		client.put_pixels(string)
	# 		time.sleep(.25)
	# 		increment = increment + 1

	def runPattern(self,color,pattern):
		increment = 0
		color_count = 0
		shadow_count = 0
		string = [(0,0,0) for i in range(num_pixels)]
		while not kill_pattern.isSet():
			#get which shadow overlay to be used - returned as full array
			shadow_array = get_shadow(pattern,shadow_count)
			for x in range(num_cols):
				for y in range(num_rows):
					rVal = get_color(color,x,y,color_count)[0] * shadow_array[x][y]
					bVal = get_color(color,x,y,color_count)[1] * shadow_array[x][y]
					gVal = get_color(color,x,y,color_count)[2] * shadow_array[x][y]
					string[mapping_array[x][y]] = (rVal, bVal, gVal)
			client.put_pixels(string)
			client.put_pixels(string)
			time.sleep(frame_delay)	
			shadow_count = shadow_count+1
			color_count = color_count+1

			# check if we can reset counters to prevent huge overflow
			# if shadow_count >= shadow_reset:
			# 	shadow_count = 0
			# if color_count >= color_reset:
			# 	color_count = 0

	def run(self):
		self.runPattern(self.color,self.pattern)

def solidBlack():
	string = [(0,0,0)]*540
	client.put_pixels(string)
	client.put_pixels(string)

def solidPink():
    string = [(255,0,255)]*540
    client.put_pixels(string)
    client.put_pixels(string)

def get_shadow(pattern, increment):
	if pattern == 'Mirror-Wave':
		return dual_wave(increment, offset='async')
	elif pattern == 'Sync-Wave':
		return dual_wave(increment, offset='sync')
	elif pattern == 'Criss-Cross':
		return cross_shadow(increment)
	elif pattern == 'Random-Roll':
		return random_shadow(increment)
	elif pattern == 'None':
		return no_shadow(increment)

def get_color(color, x, y, increment):
	if color == 'Rainbow':
		return getRainbowColor(x,y,increment)



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
		return round(( (len(rainbow_array)-1) / getDistance((num_cols-1),(num_rows-1)) * distance),0)

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

def random_shadow(increment):
	setarray = [6,22,12,1,19,7,23,12,3,20,7,17,1,13,23,4,15,2,16,22]
	#set all 1s in a 2d vector of num_rows x num_cols
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	for x in range(num_cols):
		for i in range(5):
			shadow[x][((setarray[x]+i+increment)%27)]=0
	return(shadow)

def cross_shadow(increment):
	pattern = [0,0,0,1,1,1,1,1,1,1,1,1]
	pos_diag = [[1 for y in range(num_rows)] for x in range(num_cols)]
	neg_diag = [[1 for y in range(num_rows)] for x in range(num_cols)]
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	
	#create posative diagonal - this one moves
	for x in range(num_cols):
		for y in range(num_rows):
			pos_diag[x][y]=pattern[(3*x + y + increment)%12]

	#create negative diagonal
	for x in range(num_cols):
		for y in range(num_rows):
			neg_diag[x][y]=pattern[(3*x + y)%12]
	neg_diag.reverse()

	#combine diagonals
	for x in range(num_cols):
		for y in range(num_rows):
			shadow[x][y]=pos_diag[x][y]*neg_diag[x][y]
	#always return full vector for shadow layer
	return(shadow)

def no_shadow(increment):
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	return(shadow)

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



@app.route("/")
def main():

	templateData = {
	'sys_name': sys_name,
	'settings': settings
	}
	return render_template('main.html', **templateData)

@app.route("/power/<action>")
def power(action):
	if action == "on":
		# update the dictionary 
		settings['power']=True
		solidPink()

	if action == "off":
		# update the dictionary 
		settings['power']=False
		solidBlack()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/<color>/<pattern>")
def start(color,pattern):
	global thread
	global kill_pattern
	settings['color']=color
	settings['pattern']=pattern
	
	settings['pattern_running']=True
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,color)
		thread.start()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/stop")
def stop():
	global thread
	global kill_pattern
	settings['pattern_running']=False
	kill_pattern.set()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

	

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)