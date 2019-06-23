from flask import Flask, render_template, request, redirect, jsonify, url_for
from datetime import datetime

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

import pandas as pd
import quandl
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
  return render_template('index.html')

@app.route('/index', methods = ['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/graph', methods = ['GET', 'POST'])
def graph():
  if request.method == 'POST':
    symbol = request.form['ticker']
  else:
    dat = "method not post"

  #get quandl data
  quandlTicker = "WIKI/%s" % symbol
  data = quandl.get(
    quandlTicker,
    start_date="2018-01-01"
  )

  data.index.name = 'Date'
  data.reset_index(inplace=True)
  
  fig=figure(x_axis_type="datetime", title="Stock Closing Price")
  fig.grid.grid_line_alpha=0.3
  fig.xaxis.axis_label = 'Date'
  fig.yaxis.axis_label = 'Price'

  fig.line(data['Date'], data['Close'], color='#A6CEE3', legend=symbol)

  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()

#  window_size = 30
#  window = np.ones(window_size)/float(window_size)
#  avg = np.convolve(data['Close'], window, 'same')

#  return(output_file("graph.html", title="Stock Closing Price"))

  script, div = components(fig)

  html = render_template(
    'graph.html',
    plot_script=script,
    plot_div=div,
    js_resources=js_resources,
    css_resources=css_resources
  )

  return encode_utf8(html) 

if __name__ == '__main__':
  app.run(port=33507)
