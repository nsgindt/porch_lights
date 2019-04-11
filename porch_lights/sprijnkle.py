from flask import Flask, render_template
import datetime, time, random
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

	if action == "off":
		# update the dictionary 
		settings['power']=False

	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/start/<color>/<pattern>")
def start(color,pattern):
	settings['color']=color
	settings['pattern']=pattern
	settings['pattern_running']=True
	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/stop")
def stop():
	settings['pattern_running']=False
	templateData = {
	'sys_name': sys_name,
	'settings' : settings
	}
	return render_template('main.html', **templateData)

	

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)