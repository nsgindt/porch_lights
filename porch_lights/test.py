import datetime, time, random, math
from threading import Thread, Event
import light_config as config 

#set configs from file
num_pixels = config.num_pixels
num_rows = config.num_rows
num_cols = config.num_cols
x_spacing = config.x_spacing
y_spacing = config.y_spacing 
fps = config.fps

#calculated configs
frame_delay = 1/fps

#settings being updated by user options
settings = {
	'power' : False,
	'color' : 'Rainbow',
	'pattern': 'none',
	'pattern_running': False,
	'color_one': 'Red',
	'color_two': 'White',
	'color_three': 'Blue',
	'hide_color_one': True,
	'hide_color_two': True,
	"hide_color_three": True,
}

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
setarray = [6,22,12,1,19,7,23,12,3,20,7,17,1,13,23,4,15,2,16,22]

#set all 1s in a 2d vector of num_rows x num_cols
# pos_diag = [[1 for y in range(num_rows)] for x in range(num_cols)]
# neg_diag = [[1 for y in range(num_rows)] for x in range(num_cols)]
# shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
# for x in range(num_cols):
# 	for i in range(5):
# 		shadow[x][((setarray[x]+i+increment)%27)]=0

#print(shadow)

# for x in range(num_cols):
# 	shadow[x].insert(0,shadow[x][26])
# newshadow = [i[:-1] for i in shadow]
# print(newshadow)
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

def wave_cave(increment):
	shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
	for x in range(num_cols):
		z = int(round((11-(5.5*((math.sin(math.pi*(2*x+increment)/20))+(math.sin(math.pi*(2*x+increment)/24))))),0))
		for i in range(5):
			shadow[x][z+i]=0
	return shadow

print(wave_cave(0))

# while True:
# 	wave_array = dual_wave(drip_lap, offset='async')
# 	for x in range(num_cols):
# 		for y in range(num_rows):
# 			rVal = getRainbowColor(x,y,increment)[0] * wave_array[x][y]
# 			bVal = getRainbowColor(x,y,increment)[1] * wave_array[x][y]
# 			gVal = getRainbowColor(x,y,increment)[2] * wave_array[x][y]
# 			string[mapping_array[x][y]] = (rVal, bVal, gVal)
# 	client.put_pixels(string)
# 	client.put_pixels(string)
# 	drip_lap = drip_lap+1
# 	time.sleep(.1)