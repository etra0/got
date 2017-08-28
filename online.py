#!/anaconda/bin/python3
import pygal
import pandas as pd
import numpy as np

# the time is stored as minutes:seconds, ignoring if they make more than
# one hour.
def time_to_float(value):
    if value != "0":
        minute, second = list(map(int, value.split(":")))
        second = second/60
        return minute + second
    else:
        return 0

def plot_by_time(df):
    final_data = []
    colors = ['#F26419', '#F6AE2D', '#2F4858', '#33658A', '#55DDE0', '#55FFE0']
    line_chart = pygal.HorizontalStackedBar(height=2000, width=1000)
    line_chart.title = "Screentime by character"
    line_chart.x_title = "Minutes"

    for i, season in enumerate(df.columns[1:len(df.columns)-1]):
        season_title = season.replace("_", " ").title()
        line_chart.add(season_title, df[season])

    line_chart.x_labels = df['actor']
    line_chart.render_to_file('./out.svg')
        

df = pd.read_csv("all_seasons.csv", sep=";")
df['total'] = 0
for col in df.columns[1:len(df.columns) - 1]:
    df[col] = df[col].map(time_to_float)
    df['total'] += df[col]

df = df.sort_values(by="total")

plot_by_time(df)
#plot_by_time_by_season(df)
#by_house(df)
#by_season(df)

#plt.show()
