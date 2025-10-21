### YOUR IMPORTS HERE ###
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def query_climate(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    # filter by year_begin and year_end
    df = df[df['Year'].between(year_begin, year_end)]
    
    # filter by country
    df = df.loc[df['Country'] == country]
    
    # remove unecessary columns, i now realize there is a better way to do this haha
    for i in range(1, 13):
        if i != month:
            df = df.drop("VALUE"+str(i), axis='columns')
    df = df.drop("ID", axis='columns')
    
    # rename VALUEi to Temp
    df = df.rename(columns = {"VALUE"+str(month): "Temp"})
    
    # add month column
    df['Month'] = month
    
    # rearrange column order
    df = df.reindex(columns = ['NAME', 'LATITUDE', 'LONGITUDE', 'Country', 'Year', 'Month', 'Temp'])
    return df

def get_mean_temp(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    
    # format dataframe same way I have in previous function
    df = query_climate(df, country, year_begin, year_end, month)

    # group each by each station name and calculate the mean
    mean_temps = df.groupby(['NAME', 'LATITUDE', 'LONGITUDE'])['Temp'].agg('mean').round(2)
    # merge the mean temps back into the main dataframe
    df = df.merge(mean_temps, on=['NAME', 'LATITUDE', 'LONGITUDE'])    

    # rename the columns
    df = df.rename(columns={'Temp_x': 'Temp', 'Temp_y': 'Mean_Temp'})
    return df

def temperature_plot(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> go.Figure:

    stations = get_mean_temp(df, country, year_begin, year_end, month)

    fig = px.scatter_mapbox(stations,
                        title=f"Average temperature at each station during {year_begin} to {year_end} in Month {month}",
                        lat="LATITUDE", 
                        lon="LONGITUDE",
                        color="Mean_Temp",
                        hover_name="NAME",
                        hover_data="Mean_Temp",
                        mapbox_style="open-street-map",
                        height=300,
                        width=700,
                        zoom=4)
    fig.update_layout(margin={"r": 0,"t": 40,"l": 0,"b": 0})
    
    return fig








