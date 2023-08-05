import plotly.graph_objects as go
from plotly.subplots import make_subplots

#DATA_URL = 'https://kuleuven-mda.s3.eu-central-1.amazonaws.com/water_points.csv'

TEXTS = {
    'title': '**Wonders: Community Activities**',
    'body': "Liberia and Sierra Leone are two West African countries that face significant challenges \
            in accessing clean water. Both countries have low access rates to safe drinking water, \
            particularly in rural areas, and limited infrastructure for water supply and sanitation \
            services. This has resulted in high rates of waterborne diseases and health problems, \
            particularly among vulnerable populations."
}

def get_the_line_plot(water_points, id_=82198):
    ### Extract the information from the id_ above and store it in a dictionary
    info = water_points[water_points.id == id_].to_dict(orient='records')[0]

    # Initialize the figure, but this time, make use of the make_subplots function of the plotly.subplots interface
    # Specify the following parameters:
    # - Number of rows: 2
    # - Number of columns: 2
    # - Column widths: 0.7, 0.3
    # - Explore the specs parameter and provide it with the correct values such that it allows both scattergeo and xy plots.

    fig = make_subplots(rows=2, cols=1, 
                        specs=[[{'type': 'scatter'}],
                               [{'type': 'scattergeo'}]],
                    subplot_titles=("", ""))

    # Add the general plot that highlights the locations of water access points using the Scattergeo object
    # the marker color is equal to  "#db9862" and the opacity was set to 0.5
    # give the geo attribute the value 'geo'
    # put the figure on row 1 column 1
    fig.add_trace(
        go.Scattergeo(
            lon = water_points['lon'],
            lat = water_points['lat'],
            hoverinfo= 'none',
            marker=dict(color="#db9862", opacity=0.5),
            geo='geo'
        ),
        row=1, col=1
    )


    # Add the second map that shows the location of the two contries.
    # Explore the examples in the plotly documentation to achieve this
    # set the geo attribute equal to 'geo2' and put the map in the second row, first column
    fig.add_trace(go.Choropleth(
            locationmode = 'country names',
            locations = water_points['country'],
            text = water_points['country'],
            hoverinfo= 'none',
            z = [1]*len(water_points),
            colorscale = [[0,'#58524e'],[1,'#58524e']],
            autocolorscale = False,
            showscale = False,
            geo = 'geo2',
        ),
        row=2, col=1
    )

    # Create the highlighted point:
    # tip: for size, opacity in zip([10, 25, 50, 100], [1, 0.5, 0.25, 0.05]):
    #.        fig.add_trace(...)
    # color of the marker is #a6523c
    for size, opacity in zip([10, 25, 50, 100], [1, 0.5, 0.25, 0.05]):
        fig.add_trace(go.Scattergeo(
                lon = [info['lon']],
                lat = [info['lat']],
                name = 'Highlighted point',
                hoverinfo= 'none',
                marker = dict(
                    size = size,
                    color = '#a6523c',
                    opacity = opacity
                )
            ),
            row=1, col=1
        )

    # Update the layout (difficult step)
    # - Make sure the legend is hidden
    # - Make the geo and geo2 layouts based on the examples provided in the example gallery
    #     GEO 1:
    #       - country color: #e7d3bb, landcolor: #fbf7f1, bgcolor: rgba(255, 255, 255, 0.0)
    #       - Other specs should be inferred from picture shown during lecture
    #     GEO 2:
    #       - landcolor: #f9f4eb
    #       - Other specs should be inferred from picture shown during lecture
    # - use the simple_white template
    # - Set the font equal to Times New Roman
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        geo = go.layout.Geo(
            scope = 'africa',
            countrycolor = "#e7d3bb",
            landcolor='#fbf7f1',
            showframe = False,
            showcountries = True,
            lonaxis_range= [-15, -6],
            lataxis_range= [2, 10],
            domain = dict(x = [ 0, 1 ], y = [ 0, 1]),
            bgcolor = 'rgba(255, 255, 255, 0.0)',
        ),
        geo2 = go.layout.Geo(
            scope = 'africa',
            showframe = False,
            landcolor = "#f9f4eb",
            showcountries = False,
            domain = dict(x = [ 0, 0.4 ], y = [ 0, 0.7]),
            bgcolor = 'rgba(255, 255, 255, 0.0)',
        ),
        template='simple_white',
        font=dict(
            family="Times New Roman"
        )
    )

    return fig


def get_bar_chart(water_points, id_=82198):
    fig = go.Figure()
    info = water_points[water_points.id == id_].to_dict(orient='records')[0]
    for source in water_points.source.value_counts().sort_values(ascending=True).index:
        number = water_points.source.value_counts()[source]
        if source == info['source']:
            color = '#a6523c'
        else:
            color = '#b29e8f'
        fig.add_trace(
            go.Bar(
                x=[number], 
                y=[source],
                text=[number],
                orientation='h',
                marker=dict(color=color),
                hoverinfo='none'
            )
        )
    fig.update_layout(
        showlegend=False,
        template='simple_white',
        font=dict(
            family="Times New Roman"
        )
    )
    fig.update_xaxes(title_text="Number of Access Points", title_font=dict(size=10))
    return fig

def get_point_info(water_points, id_=82198):
    return water_points[water_points.id == id_].to_dict(orient='records')[0]