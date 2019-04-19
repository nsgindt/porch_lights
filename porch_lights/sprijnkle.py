from flask import Flask, render_template
import datetime, opc, time, random, math
from threading import Thread, Event
import light_config as config 

#***********************************************************************
# initialize the important stuff
#***********************************************************************
#initialize flask
app = Flask(__name__)

#set up pattern thread
thread = Thread()
kill_pattern = Event()

#setup Fadecandy
client = opc.Client('localhost:7890')

#***********************************************************************
# Call and build all default settings
#***********************************************************************
num_pixels = config.num_pixels
num_rows = config.num_rows
num_cols = config.num_cols
x_spacing = config.x_spacing
y_spacing = config.y_spacing 
fps = config.fps
sys_name = config.sys_name

#calculated configs
frame_delay = 1/fps
num_pixels = num_rows * num_cols

#set default settings
settings = {
	'power' : False,
	'color' : 'Rainbow',
	'pattern': 'none',
	'pattern_running': False,
	'color_one': 'White',
	'color_two': 'White',
	'color_three': 'White',
	'hide_color_one': True,
	'hide_color_two': True,
	"hide_color_three": True,
}

#used as the off position
def solidBlack():
	string = [(0,0,0)]*540
	client.put_pixels(string)
	client.put_pixels(string)

#used as acknowledge of on
def solidPink():
    string = [(255,0,255)]*540
    client.put_pixels(string)
    client.put_pixels(string)

#***********************************************************************
# these arrays & dictionaries are called througout the program
#***********************************************************************
rainbow_array = [0 for i in range(0,512)]
[rainbow_array.append(i-512) for i in range(512,768)]
[rainbow_array.append(255) for i in range(768,1280)]
[rainbow_array.append(1535-i) for i in range(1280,1536)]

mapping_array = [[int(getLightNumber(x,y)) for y in range(num_rows)] for x in range(num_cols)]
distance_array = [[getDistance(x,y) for y in range(num_rows)] for x in range(num_cols)]
offset_array = [[int(getOffset(y)) for y in distance_array[x]] for x in range(len(distance_array))]

color_list = {
	'White':(255,255,255),
	'Red':(255,0,0),
	'Orange':(255,180,0),
	'Yellow':(255,255,0),
	'Green':(0,255,0),
	'Teal':(0,255,255),
	'Blue':(0,0,255),
	'Pink':(255,0,255)
}

#***********************************************************************
# this is the primary thread used to run the pattern
#***********************************************************************

class PatternThread(Thread):
	def __init__(self, pattern, color):
		self.pattern = pattern
		self.color = color
		self.delay = 1
		super(PatternThread,self).__init__()

	def runPattern(self,color,pattern):
		color_count = 0
		shadow_count = 0
		color_reset = get_color_reset(color)
		shadow_reset = get_shadow_reset(pattern)
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
			time.sleep(3*frame_delay)	
			shadow_count = shadow_count+1
			color_count = color_count+1

			# check if we can reset counters to prevent huge overflow
			if shadow_count >= shadow_reset:
				shadow_count = 0
			if color_count >= color_reset:
				color_count = 0

	def run(self):
		self.runPattern(self.color,self.pattern)

#***********************************************************************
# these functions are called by the thread to run the pattern properly
#***********************************************************************
def get_shadow(pattern, increment):
	if pattern == 'Mirror-Wave':
		return dual_wave(increment, offset='async')
	elif pattern == 'Sync-Wave':
		return dual_wave(increment, offset='sync')
	elif pattern == 'Criss-Cross':
		return cross_shadow(increment)
	elif pattern == 'Random-Roll':
		return random_shadow(increment)
	elif pattern == 'Wave-Cave':
		return wave_cave(increment)
	elif pattern == 'None':
		return no_shadow(increment)

def get_color(color, x, y, increment):
	if color == 'Rainbow':
		return getRainbowColor(x,y,increment)
	if color == 'Solid-Fade':
		return getSolidFade(increment)
	if color == 'One-Color':
		return one_color(x,y)
	if color == 'Two-Color':
		return two_color(x,y)
	if color == 'Three-Color':
		return three_color(x,y)

def get_color_reset(color):
	if color == 'Rainbow':
		return 1536
	if color == 'Solid-Fade':
		return 1536
	if color == 'One-Color':
		return 1536
	if color == 'Two-Color':
		return 1536
	if color == 'Three-Color':
		return 1536	

def get_shadow_reset(pattern):
	if pattern == 'Mirror-Wave':
		return 20
	elif pattern == 'Sync-Wave':
		return 20
	elif pattern == 'Criss-Cross':
		return 12
	elif pattern == 'Random-Roll':
		return 27
	elif pattern == 'Wave-Cave':
		return 240
	elif pattern == 'None':
		return 100

#***********************************************************************
# these are builder functions used to build ranbow color and the mapping
#***********************************************************************

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

#***********************************************************************
# these functions drive the shadow layer
#***********************************************************************

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

def random_shadow(increment):
	setarray = [6,22,12,1,19,7,23,12,3,20,7,17,1,13,23,4,15,2,16,22]
	#set all 1s in a 2d vector of num_rows x num_cols
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	for x in range(num_cols):
		for i in range(5):
			shadow[x][((setarray[x]+i+increment)%27)]=0
	return(shadow)

def wave_cave(increment):
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	for x in range(num_cols):
		z = int(round((11-(5.5*((math.sin(math.pi*(2*x+increment)/20))+(math.sin(math.pi*(2*x+increment)/24))))),0))
		for i in range(5):
			shadow[x][z+i]=0
	return shadow

#***********************************************************************
# these functions drive the color layer
#***********************************************************************

def getRainbowColor(x,y,increment):
	rVal=(offset_array[x][y] + increment) % 1536 
	gVal=(offset_array[x][y] + increment + 512) % 1536 
	bVal=(offset_array[x][y] + increment + 1024) % 1536
	return [rainbow_array[rVal],rainbow_array[gVal],rainbow_array[bVal]]

def getSolidFade(x,y,increment):
	rVal=(3*increment) % 1536 
	gVal=(3*increment + 512) % 1536 
	bVal=(3*increment + 1024) % 1536
	return [rainbow_array[rVal],rainbow_array[gVal],rainbow_array[bVal]]	

def one_color(x,y):
	return get_color_rgb(settings['color_one'])

def two_color(x,y):
	if x <= 9:
		return get_color_rgb(settings['color_one'])
	else:
		return get_color_rgb(settings['color_two'])

def three_color(x,y):
	if x <= 6:
		return get_color_rgb(settings['color_one'])
	elif x > 6 and x <= 12:
		return get_color_rgb(settings['color_two'])	
	else:
		return get_color_rgb(settings['color_three'])	

def get_color_rgb(color):
	return [color_list[color][0],color_list[color][1],color_list[color][2]]

#***********************************************************************
# This controls all of the flask routing
#***********************************************************************

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

@app.route("/start/Rainbow/<pattern>")
def start_rainbow(pattern):
	global thread
	global kill_pattern
	settings['color']='Rainbow'
	settings['pattern']=pattern
	settings['pattern_running']=True
	settings['hide_color_one']=True
	settings['hide_color_two']=True
	settings['hide_color_three']=True
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,settings['color'])
		thread.start()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/Solid-Fade/<pattern>")
def start_solid_fade(pattern):
	global thread
	global kill_pattern
	settings['color']='Solid-Fade'
	settings['pattern']=pattern
	settings['pattern_running']=True
	settings['hide_color_one']=True
	settings['hide_color_two']=True
	settings['hide_color_three']=True
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,settings['color'])
		thread.start()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/One-Color/<color1>/<pattern>")
def start_one_color(color1,pattern):
	global thread
	global kill_pattern
	settings['color']='One-Color'
	settings['color1']=color1
	settings['pattern']=pattern
	settings['pattern_running']=True
	settings['hide_color_one']=False
	settings['hide_color_two']=True
	settings['hide_color_three']=True
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,settings['color'])
		thread.start()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/Two-Color/<color1>/<color2>/<pattern>")
def start_two_color(color1,color2,pattern):
	global thread
	global kill_pattern
	settings['color']='Two-Color'
	settings['color_one']=color1
	settings['color_two']=color2
	settings['pattern']=pattern
	settings['pattern_running']=True
	settings['hide_color_one']=False
	settings['hide_color_two']=False
	settings['hide_color_three']=True
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,settings['color'])
		thread.start()

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/Three-Color/<color1>/<color2>/<color3>/<pattern>")
def start_three_color(color1,color2,color3,pattern):
	global thread
	global kill_pattern
	settings['color']='Three-Color'
	settings['color_one']=color1
	settings['color_two']=color2
	settings['color_three']=color3
	settings['pattern']=pattern
	settings['pattern_running']=True
	settings['hide_color_one']=False
	settings['hide_color_two']=False
	settings['hide_color_three']=False
	if not thread.isAlive():
		kill_pattern.clear()
		thread = PatternThread(pattern,settings['color'])
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

#***********************************************************************
# start flask server
#***********************************************************************

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)