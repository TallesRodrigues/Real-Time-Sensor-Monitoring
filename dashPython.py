import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import serial
import time
from collections import deque
import pymongo
from pymongo import MongoClient


#Read Data
dataDB = []
timelapse = []
max_length = 100

#Connection to MongoDB
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.iotDB
collections = db.home
	
def update_values(sensor_name):
	try:
		dataDB.clear()
		timelapse.clear()
	except:
		print ("Error ")

	print ("Running\n"+"Selected sensor(s): ",sensor_name)
	cursor = collections.find({'sensor':sensor_name}).sort('_id',-1).limit(30)
	
	for element in cursor:
		dataDB.append(element['value'])
		timelapse.append(element['_id'])

	dataDB.reverse()
	timelapse.reverse()
	return


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.Div([
		html.H2('Sensor Data',
			style={'float': 'left',
			}),
        ]),
	dcc.Dropdown(
		id = 'sensor_name',
        options=[
            {'label': 'LDR', 'value': 'ldr'},
            {'label': 'Temp', 'value': 'temp'},
        ],
        value='ldr',
        multi=True
    ),
     html.Div(children=html.Div(id='graphs'), className ='row'),
     dcc.Interval(
        id='graph-update',
        interval=10*1000),
],)

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('sensor_name', 'value'),
    dash.dependencies.Input('graph-update','n_intervals')])
def update_graph(data_names,n_intervals):
    graphs = []
    #data_names was the given name for the input from the sensor_name. This variable starts as a str and can be turned into a list<>
    update_values(data_names)
   
    if(isinstance(data_names,str)):

    	data = go.Scatter(
    		x=timelapse,
            y=dataDB,
            name='Scatter',
            mode= 'lines+markers'
            )
    	graphs.append(html.Div(dcc.Graph(
            id=data_names,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(timelapse),max(timelapse)]),
                                                        yaxis=dict(range=[min(data),max(data)]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_names))}
            ),))
    elif tisinstance(data_names,list):
    	for data_name in data_names:
    		print (data_name)
    		data = go.Scatter(
    			x=timelapse,
    			y=dataDB,
    			name='Scatter',
    			mode= 'lines+markers'
    			)
    		graphs.append(html.Div(dcc.Graph(
    			id=data_name,
    			animate=True,
    			figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(timelapse),max(timelapse)]),
    				yaxis=dict(range=[min(data),max(data)]),
    				margin={'l':50,'r':1,'t':45,'b':1},
    				title='{}'.format(data_name))}
    			),))

    return graphs
if __name__ == '__main__':
    app.run_server(debug=True)
