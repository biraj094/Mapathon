import dash
import dash_core_components as dcc 
import dash_html_components as html   
import pandas as pd  
import numpy as np
from dash.dependencies import Input,Output
import plotly.graph_objs as go

app=dash.Dash()


#reading data
df80=pd.read_json('/Users/apple/Desktop/Biraj/Mapathon/data/Glacier_1980.json')
df10=pd.read_json('/Users/apple/Desktop/Biraj/Mapathon/data/Glacier_2010.json')

data=['df80','df10']
#features list
features80= df80['features'].values.tolist()
features10= df10['features'].values.tolist()

yaxis_parameter=['Area_SqKm','Thickness']

#basin list 
basin=[]
for f in features10:
    basin.append(f['properties']['Basin'])
finalbasin=pd.Index(set(basin))



app.layout= html.Div([

                #Header
                html.Div(
                     [html.H2('Visualizing Himalayan Glaciers of Nepal-Phase I ')]
                 ),

                #Year Dropdown 
                html.Div(dcc.Dropdown(
                                id='year',
                                options=[{'label':i, 'value':i}for i in data ],
                                value='df80'
                                        ),style={'width':'48%','display':'block'} ),

                #Basin Dropdown
                 html.Div(dcc.Dropdown(
                                id='basin',
                                options=[{'label':i , 'value':i}for i in finalbasin ],
                                value='Koshi'
                                        ),style={'width':'48%','display':'block'}  ),
                #Print the subbasin name 
                html.Div(id='subbasin_area'),

                #X-axis Dropdown
                html.Div(dcc.Dropdown(
                                id='xaxis',
                                options=[{'label':'GLIMS_ID','value':'GLIMS_ID'}],
                                value='GLIMS_ID'
                                        ),style={'width':'48%','display':'block'} ),

                #Y-axis Dropdown
                html.Div(dcc.Dropdown(
                                id='yaxis',
                                options=[{'label':i,'value':i}for i in yaxis_parameter ],
                                value='Area_SqKm'
                                        ),style={'width':'48%','display':'block'} ),

                html.Div(dcc.Graph(id='mygraph'))
                
])


#function to update the subbasin name 
@app.callback(Output("subbasin_area","children"),
              [Input('basin','value')] )
def update_subbasin(basin):
    subbasin=[]
    for f in features10:
        if f['properties']['Basin']==basin:
            subbasin.append(f['properties']['Sub_Basin'])
    
    finalsubbasin=set(subbasin)
    return "The subbasin of {} is {}".format(basin,finalsubbasin)




#function to print the plot
@app.callback(Output('mygraph','figure'),
            [ Input('year','value'),
                Input('basin','value'),
                Input('xaxis','value'),
                Input('yaxis','value'),
                ])
def update_graph(year,basin,xaxis_name,yaxis_name):
    x=[]
    y=[]
    if year=='df80':
        for f in features80:
            if f['properties']['Basin']==basin:
                x.append(f['properties'][xaxis_name])
                y.append(f['properties'][yaxis_name])
    elif year=='df10':
        for f in features10:
            if f['properties']['Basin']==basin:
                x.append(f['properties'][xaxis_name])
                y.append(f['properties'][yaxis_name])

    data=[go.Scatter(x=x,
                    y=y,
                    text='Hi',
                    mode='markers')]   #CLUE:add another dataset here for both visualization
    
    return {'data':data ,
            'layout': go.Layout(title="My graph",
                                xaxis={'title':xaxis_name},
                                yaxis={'title':yaxis_name},
                                hovermode='closest' )}



    
#function to get area of the same glimid from both dataset 





if __name__=='__main__':
    app.run_server(debug=True,host='127.0.0.1',port='5167')