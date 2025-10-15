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
    # get list of all names of stations
    names = df["NAME"].unique()
    # add new column
    df['Mean_Temp'] = 0.0
    # for each station, calculate the mean and set as the Mean_Temp
    for name in names:
        df.loc[df['NAME'] == name, 'Mean_Temp']= df.loc[df['NAME'] == name, 'Temp'].agg('mean')
    df['Mean_Temp'] = df['Mean_Temp'].round(2)
    
    return df

def temperature_plot(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> go.Figure:

    stations = get_mean_temp(df, country, year_begin, year_end, month)

    fig = px.scatter_map(stations,
                        title="test",
                        lat="LATITUDE", 
                        lon="LONGITUDE",
                        color="Mean_Temp",
                        hover_name="NAME",
                        hover_data="Mean_Temp",
                        map_style="open-street-map",
                        zoom=4)
    fig.update_layout(margin={"r": 0,"t": 0,"l": 0,"b": 0})
    
    return fig








