import random  
import light_config as config 

#set configs
num_pixels = config.num_pixels
num_rows = config.num_rows
num_cols = config.num_cols
x_spacing = config.x_spacing
y_spacing = config.y_spacing 
fps = config.fps


frame_delay = 1/fps



setarray = [6,22,12,1,19,7,23,12,3,20,7,17,1,13,23,4,15,2,16,22]

#set all 1s in a 2d vector of num_rows x num_cols
shadow = [[1 for y in range(num_rows)] for x in range(num_cols)]
increment = 2
for x in range(num_cols):
	for i in range(5):
		shadow[x][((setarray[x]+i+increment)%27)]=0

print(shadow)

# for x in range(num_cols):
# 	shadow[x].insert(0,shadow[x][26])
# newshadow = [i[:-1] for i in shadow]
# print(newshadow)




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