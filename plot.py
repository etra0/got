#!/anaconda/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Open Sans']

plt.style.use("ggplot")

SEASONS = list(map(lambda x: "season_%d" % x, range(1, 8)))

# the time is stored as minutes:seconds, ignoring if they make more than
# one hour.
def time_to_float(value):
    if value != "0":
        minute, second = list(map(int, value.split(":")))
        second = second/60
        return minute + second
    else:
        return 0

def plot_all_characters(df):
    """
    Creates a plot saved in out called 'all_actors', will
    contain top 100 character's screentimes.
    """
    fig = plt.figure(figsize=(10,20))
    ax = fig.add_subplot(1, 1, 1)
    
#    df.plot.barh(ax=ax, x='actor', y=df.columns[2:len(df.columns)-1], \
#                    stacked=True, width=.6)

    colors = [
            '#01a186',
            '#e24a33',
            '#348abd',
            '#ff930f',
            '#988ed5',
            '#fbc15e',
            '#8eba42'
            ]


    # for stacked bar, we need to use the before plot.
    for n, season in enumerate(SEASONS):

        for i, row in df.iterrows():
            left = row[SEASONS[0:n]].sum()

            death = row['death']
            if death != 'None' and int(death[1:3]) == n + 1:
                _color = 'black'
            else:
                _color = colors[n]

            label = None
            if i==1:
                label = season.replace("_", " ").title()

            current_plot = ax.barh(bottom=i, width=row[season],
                    color=_color,
                    label=label, left=left)

            if _color == 'black' and current_plot[0].get_width() > 20:
                ax.text(current_plot[0].get_x() + current_plot[0].get_width()/2,
                        current_plot[0].get_y(),
                        row['death'][:3],
                        va='bottom',
                        ha='center',
                        color='white')

    # for legend purpose
    ax.barh(0, 0, color='black', label='Death')

    ax.axvline(df.median()['total'], color='black', linestyle="dashed", label="Median")

    # ticks stuff
    ax.set_ylim(-0.8, len(df))
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df.loc[:, 'actor'])
    ax.set_xticks(range(0, 390, 60))
    ax.set_ylabel("")
    ax.set_xlabel("Time in minutes")

    ax.set_title("Screen time of GOT characters")
    fig.tight_layout(rect=[0, 0, 0.80, 1])
    ax.legend()
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig.text(.02, .005, "Source: http://imdb.com/list/ls076752033/")
    ax.text(1.05, 0.88,
            "* The black bar means that\nhe/she died in a season.\nDepends on the bar width\nif the season is specified.",
            transform=ax.transAxes, ha='left', va='top')
    fig.savefig("out/all_characters.png", dpi=300, format="png")

def by_house(df):
    # in most cases, last name is the house.
    df['house'] = df['actor'].map(lambda x: x.split(" ")[-1])

    # fix for snow :(
    df.loc[df['actor'] == "Jon Snow", 'house'] = 'Stark'

    # delete people without last name
    df = df.loc[df['actor'].map(lambda x: len(x.split(" "))) > 1]

    grouped = df.groupby(by='house').sum()

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    grouped = grouped.reset_index().sort_values(by='total')

    colors = [
            '#01a186',
            '#e24a33',
            '#348abd',
            '#ff930f',
            '#988ed5',
            '#fbc15e',
            '#8eba42'
            ]
    grouped.iloc[-10:].plot.barh(ax=ax, x='house', y=SEASONS, \
                    stacked=True, width=.6, color=colors)

    ax.legend(list(map(lambda x: x.replace("_", " ").title(), SEASONS)))
    ax.set_title("Screen time by house")
    ax.set_xlabel("Minutes")
    ax.set_ylabel("House")

    fig.tight_layout(rect=[0, 0.15, 1, 1])
    ax.text(-0.2, -0.25,
        "* Jon Snow was considered Stark because he played for them most of the time.\n" \
        + "* Tommen, Joffrey and Myrcella were considered as Baratheon\n\n" \
        + "Source: http://imdb.com/list/ls076752033/",
        transform=ax.transAxes, ha='left', va='top', alpha=0.4, fontsize=8)
    fig.savefig("out/by_house.png", dpi=300, format="png")

def top_by_season(df):
    """
    Creates an image that will contain 7 plots of top 10 characters
    by season
    """
    fig = plt.figure(figsize=(16,12))
    
    index = 1
    cmap = plt.get_cmap('Set1')
    colors = [cmap(i) for i in np.linspace(0, 1, len(SEASONS))]

    for season in SEASONS:
        # we need to sort depending of the season.
        temp = df.sort_values(by=season)

        if index == 7:
            ax = fig.add_subplot(3, 3, 8)
        else:
            ax = fig.add_subplot(3, 3, index)

        ax.set_title(season.replace("_", " ").title())

        # We just make one figure, so we plot the top 10 actors by season
        temp.iloc[-10:].plot.barh(ax=ax, x='actor', y=season, \
                    stacked=True, width=.6, legend=False, \
                    color = colors[index - 1])
        index += 1
        ax.set_ylabel("")
        ax.set_xlabel("Time in minutes")
    
    fig.suptitle("Top 10 screentimes by season", fontsize=24, weight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("out/top_by_season.png", dpi=300, format="png")

def top_house_by_season(df):
    """
    Top houses by seasons
    """
    # in most cases, last name is the house.
    df['house'] = df['actor'].map(lambda x: x.split(" ")[-1])

    fig = plt.figure(figsize=(16,12))
    fig.suptitle("Screentime of houses by season", fontsize=24, weight='bold')

    # fix for snow :(
    df.loc[df['actor'] == "Jon Snow", 'house'] = 'Stark'

    # delete people without last name
    df = df.loc[df['actor'].map(lambda x: len(x.split(" "))) > 1]
    grouped = df.groupby(by='house').sum()
    grouped = grouped.reset_index()

    cmap = plt.get_cmap('Set1')

    colors = [cmap(i) for i in np.linspace(0, 1, len(SEASONS))]
    index = 1
    for i, season in enumerate(SEASONS):

        if index == 7:
            ax = fig.add_subplot(3, 3, 8)
        else:
            ax = fig.add_subplot(3, 3, index)

        temp = grouped.sort_values(by=season).iloc[-10:]
        temp.plot.barh(ax=ax, x='house', y=season, legend=False, color=colors[index - 1])

        ax.set_ylabel("House")
        ax.set_xlabel("Minutes")
        ax.set_title(season.replace("_", " ").title())
        index += 1


    fig.text(.02, .005,
        "* Jon Snow was considered Stark because he played for them most of the time.\n" \
        + "* Tommen, Joffrey and Myrcella were considered as Baratheon\n\n" \
        + "Source: http://imdb.com/list/ls076752033/",
        ha='left', va='bottom', alpha=0.4, fontsize=8)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("out/top_house_by_season.png", dpi=300, format="png")


if __name__ == '__main__':
    df = pd.read_csv("all_seasons.csv")
    df['total'] = 0
    for col in df.columns[2:len(df.columns) - 1]:
        df[col] = df[col].map(time_to_float)
        df['total'] += df[col]

    df = df.sort_values(by="total", ascending=True)
    df.index = range(len(df))

    plot_all_characters(df)
    by_house(df)
    top_house_by_season(df)
    top_by_season(df)

