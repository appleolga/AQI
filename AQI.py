import requests
import json
import pandas
import re
import html
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Text, Grid
from bokeh.palettes import Oranges6

# downloading aqi levels reference table
url = 'https://aqicn.org/city/ukraine/kyiv/mykhaila-hrushevskoho-street--30/'
ref_table = pandas.read_html(url)[18]
ref_table = ref_table.iloc[:, 0:2]
ref_table = ref_table.to_html('table.html')


# Reading file with station IDs list and creating DataFrame with necessary columns

data = pandas.read_excel('C:\\Users\\Пользователь\\PycharmProjects\\AQI\\station_ids.xlsx', index_col='ID')
data['Station name'] = ''
data['aqi'] = ''
data['color'] = ''

# obtaining data from API
for id in data.index:
    station_data = json.loads(requests.get(
        'https://api.waqi.info/feed/@' + str(id) + '').text)['data']
    data.loc[id, 'aqi'] = station_data['aqi']
    data.loc[id, 'Station name'] = re.match(r'(.*)(?:, K.*)', station_data['city']['name']).group(1)
    if int(station_data['aqi']) <= 50:
        data.loc[id, 'color'] = 'green'
    elif int(station_data['aqi']) <= 100:
        data.loc[id, 'color'] = 'yellow'
    elif int(station_data['aqi']) <= 150:
        data.loc[id, 'color'] = 'orange'
    else:
        data.loc[id, 'color'] = 'red'


output_file("AQI_Dorogozhychi.html")
station_plot = data['Station name']
aqi_plot = data['aqi']
color = data['color']
source = ColumnDataSource(data=dict(station=station_plot, aqi=aqi_plot, color=color, text=aqi_plot))

# Creating plot object
p = figure(x_range=station_plot, y_range=(0, 300), plot_height=400, toolbar_location=None, title="Air Quality Indices for Dorogozhychi")
p.vbar(x='station', top='aqi', width=0.7, source=source, line_color='white', fill_color='color')

glyph_text = Text(x='station', y='aqi', text='text')
glyph_text.text_align = 'center'
glyph_text.text_font_size = '30pt'

# grid_layout = Grid(band_fill_alpha=1, band_fill_color='red')


p.grid.grid_line_color = 'gray'
p.grid.grid_line_alpha = 0.1
p.grid.band_fill_color = 'blue'
p.grid.band_fill_alpha = 0.2
p.xgrid.visible = False
p.outline_line_color = None
p.yaxis.visible = True
p.title.align = 'center'
p.title.text_font_size = '20pt'
p.add_glyph(source, glyph_text)
p.sizing_mode = 'stretch_both'

show(p)


