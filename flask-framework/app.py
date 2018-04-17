# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
#from boto.s3.connection import S3Connection
import requests
import pandas as pd
import datetime
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from math import pi
from bokeh.models import DatetimeTickFormatter

# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def main():
	return redirect(url_for('index'))

@app.route('/index')
def index():
	return render_template('index.html') 

@app.route('/model')
def model():
	return render_template('model.html') 


#@login_required
@app.route('/stock')
def stock():
	stockticker = request.args.get('ticker')
	stockclose = request.args.get('close')
	stockopen = request.args.get('open')
	stockAclose = request.args.get('Aclose')
	stockAopen = request.args.get('Aopen')
	#print('he is', stockticker, stockclose, stockopen ,stockAclose,stockAopen,'here')
	script = 0
	div = 0
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()




	return render_template('stock.html')
@app.route('/project')
def projectp():
	return render_template('project.html') 


@app.route('/about')
def about():
    return render_template('about.html')  # render a template



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)






