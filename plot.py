#!/anaconda/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use("ggplot")

SEASONS = list(map(lambda x: "Season %d" % x, range(1, 8)))

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
    fig = plt.figure(figsize=(8,20))
    ax = fig.add_subplot(111)
    
    df.plot.barh(ax=ax, x='actor', y=df.columns[2:len(df.columns)-1], \
                    stacked=True, width=.6)

    ax.axvline(df.median()['total'], color='black', linestyle="dashed")
    
    ax.set_title("Screen time of GOT characters")
    ax.set_ylabel("")
    ax.set_xlabel("Time in minutes")
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.legend()
    ax.legend(["Median"] + SEASONS)
    fig.text(.02, .005, "Source: http://imdb.com/list/ls076752033/")
    fig.savefig("out/all_actors.png", dpi=300, format="png")


def plot_by_time_by_season(df):
    fig = plt.figure(figsize=(16,12))
    
    index = 1
    cmap = plt.get_cmap('Set1')
    colors = [cmap(i) for i in np.linspace(0, 1, 6)]

    for season in df.columns[2:len(df.columns)-1]:
        # we need to sort depending of the season.
        temp = df.sort_values(by=season)

        ax = fig.add_subplot(2, 3, index)
        ax.set_title(season.replace("_", " ").title())

        # We just make one figure, so we plot the top 10 actors by season
        temp.iloc[-10:].plot.barh(ax=ax, x='actor', y=season, \
                    stacked=True, width=.6, legend=False, \
                    color = colors[index - 1])
        index += 1
        ax.set_ylabel("")
        ax.set_xlabel("Time in minutes")
    
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    fig.text(.02, .005, "Source: http://imdb.com/list/ls076752033/")
    fig.savefig("out/char_by_season.png", dpi=300, format="png")

def by_house(df):
    # in most cases, last name is the house.
    df['house'] = df['actor'].map(lambda x: x.split(" ")[-1])

    # fix for snow :(
    df.loc[df['actor'] == "Jon Snow", 'house'] = 'Stark'

    # delete people without last name
    df = df.loc[df['actor'].map(lambda x: len(x.split(" "))) > 1]

    grouped = df.groupby(by='house').sum()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    grouped = grouped.reset_index().sort_values(by='total')

    grouped.iloc[-10:].plot.barh(ax=ax, x='house', y=df.columns[2:len(df.columns)-2], \
                    stacked=True, width=.6)

    ax.legend(SEASONS)
    ax.set_title("Screen time by house")
    ax.set_xlabel("Minutes")

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    fig.savefig("out/by_house.png", dpi=300, format="png")

def by_season(df):
    # in most cases, last name is the house.
    df['house'] = df['actor'].map(lambda x: x.split(" ")[-1])

    fig = plt.figure(figsize=(19, 10))

    # fix for snow :(
    df.loc[df['actor'] == "Jon Snow", 'house'] = 'Stark'

    # delete people without last name
    df = df.loc[df['actor'].map(lambda x: len(x.split(" "))) > 1]
    grouped = df.groupby(by='house').sum()
    grouped = grouped.reset_index()

    cmap = plt.get_cmap('Set1')

    colors = [cmap(i) for i in np.linspace(0, 1, 6)]
    row = 0
    for i, season in enumerate(list(map(lambda x: "season_%d" % x, range(1, 7)))):
        if i > 0 and i % 3 == 0:
            row += 1

        i = i % 3
        index = row * 3 + i + 1
        ax = fig.add_subplot(2, 3, index)
        temp = grouped.sort_values(by=season).iloc[-10:]
        temp.plot.barh(ax=ax, x='house', y=season, legend=False, color=colors[index - 1])

        ax.set_ylabel("House")
        ax.set_xlabel("Minutes")
        ax.set_title(season.replace("_", " ").title())

        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    fig.text(.02, .005, "Source: http://imdb.com/list/ls076752033/")
    fig.savefig("out/by_season.png", dpi=300, format="png")


df = pd.read_csv("all_seasons.csv")
df['total'] = 0
for col in df.columns[2:len(df.columns) - 1]:
    df[col] = df[col].map(time_to_float)
    df['total'] += df[col]

df = df.sort_values(by="total")
for season in df.columns[2:len(df.columns)-1]:
    print(df[season].sum() / 60)

# Just uncomment the plot you want
plot_by_time(df)
#plot_by_time_by_season(df)
#by_house(df)
#by_season(df)

#plt.show()
