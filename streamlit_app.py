# Standard imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import streamlit as st

st.title("See some stuff I created for the first time ;)")

volcano_df = pd.read_csv("volcano_ds_pop.csv")
with open('countries.geojson') as file:
    volcano_geojson = json.load(file)

    if st.sidebar.checkbox('Show dataframe'):
        st.header("dataframe")
        st.dataframe(volcano_df.head(9))

volcano_df['Country'] = volcano_df['Country'].replace({'United States': 'United States of America',
                                                           'Tanzania': 'United Republic of Tanzania',
                                                           'Martinique': 'Martinique',
                                                           'Sao Tome & Principe': 'Sao Tome and Principe',
                                                           'Guadeloupe': 'Guadeloupe',
                                                           'Wallis & Futuna': 'Wallis and Futuna'})

countries = ["All"]+sorted(pd.unique(volcano_df['Country']))
country = st.sidebar.selectbox("Choose a Country", countries)   # Here the selection of the country.
vol_names = ['All'] + sorted(pd.unique(volcano_df['Volcano Name']))
vol_name = st.sidebar.selectbox("Choose a Volcano Name", vol_names)  # and the selection of the volcano names.
st.subheader(f'Volcanoes of the World!')

if country == 'All':
    group = volcano_df
else:
    group = volcano_df[volcano_df['Country'] == country]

fig = px.scatter_mapbox(group,
                        lat='Latitude',
                        lon='Longitude',
                        color='Type',
                        hover_name='Volcano Name',
                        hover_data=['Type', 'Country', 'Region', 'Status'],
                        zoom=1.5,
                        title=f'Volcanoes of {country}',
                        color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
                    title={"font_size":20,
                         "xanchor":"center", "x":0.38,
                        "yanchor":"bottom", "y":0.95},
                    title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
                    height=900,
                    width=1100,
                    autosize=True,
                    hovermode='closest',
                    mapbox=dict(
                        style='open-street-map'
                    ),
                    legend_title_text='Volcano Type'
)
plt.close()
st.plotly_chart(fig)

fig = px.choropleth(
    volcano_df,
    geojson = volcano_geojson,
    locations="Country",
    featureidkey="properties.ADMIN",
    color="Elev",

    width=950,
    height=450,
    labels={"Individuals using the Internet (% of population)": "% of Population",
           "most_recent_year": "Year"},
    hover_name="Elev",
    title="<b>Distribution of Volcanoes in the World!</b>",
    color_continuous_scale="Viridis",

)

fig.update_traces(marker={"opacity": 0.7})

fig.update_layout(margin={"r": 20, "t": 35, "l": 0, "b": 0},
                  font_family="Rockwell",
                  hoverlabel={"bgcolor": "white",
                              "font_size": 12,
                              "font_family": "Rockwell"},
                  title={"font_size": 20,
                         "xanchor": "left", "x": 0,
                         "yanchor": "top"},
                  geo={"resolution": 50,
                       "showlakes": True, "lakecolor": "lightblue",
                       "showocean": True, "oceancolor": "aliceblue"
                       }
                  )

st.plotly_chart(fig)