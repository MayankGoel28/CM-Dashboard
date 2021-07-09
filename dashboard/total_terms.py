# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
import bisect
from random import choices

pd.options.plotting.backend = "plotly"

source = "./TCPD-CMID_1962_2021.csv"
new_source = "./TCPD-CMID_1962_2021.csv"
# source = "./Chief Minister's Data/CM_Final.csv"
# new_source = "./Chief Minister's Data/CM_Final.csv"


df = pd.read_csv(source)
df = df.replace(np.nan, "", regex=True)


# print(df)


def correct_duration():
    global df
    for index, row in df.iterrows():
        s = row["Start_Date"].split("/")

        if row["End_Date"] == "Current":
            today = date.today()
            e = today.strftime("%d/%m/%Y")
            e = e.split("/")
        else:
            e = row["End_Date"].split("/")

        s = [int(i) for i in s]
        e = [int(i) for i in e]
        start = datetime(s[2], s[1], s[0])
        end = datetime(e[2], e[1], e[0])

        duration = (end - start).days

        df.at[index, "Days_in_Office"] = duration


# correct_duration()
# print(df)
# df.to_csv(new_source, index=False)


unique_ids = list(df["pid_CM"])

unique_ids = list(set(unique_ids))


total_duration = []
names = []
state_comp = []

for i in unique_ids:
    total = 0
    name = ""
    of_state = []
    for index, row in df.iterrows():
        if row["pid_CM"] == i:
            total += row["Days_in_Office"]
            name = row["Name"]
            of_state.append(row["State_Name"])
    total_duration.append(total)
    names.append(name)
    state_comp.append(list(np.unique(np.array(of_state))))

# print("total duration", total_duration)

# id_and_dur = {unique_ids[i]: total_duration[i] for i in range(len(unique_ids))}
# print(id_and_dur)

for i in range(len(names)):
    names[i] += " ("
    for j in range(len(state_comp[i])):
        st = state_comp[i][j]
        if j != len(state_comp[i]) - 1:
            names[i] += st + ", "
        else:
            names[i] += st + ")"

# print(names)


def total_duration_gov():
    fig = go.Figure(
        data=go.Scatter(
            x=unique_ids,
            y=total_duration,
            text=names,
            hovertemplate="<b>ID</b>: %{x}<br>"
            + "<b>Total Duration</b>: %{y} days<br>"
            + "<b>Name</b>: %{text}<extra></extra>",
        )
    )
    return fig


# fig = go.Figure(data = go.Scatter(x = names, y = total_duration))
# fig.show()


bar_range_labels = [
    "<=100",
    "101-400",
    "401-800",
    "801-1200",
    "1201-1600",
    "1601-2000",
    "2001-4000",
    "4000-8000",
    "8000-16000"
]
range_labels = [100, 400, 800, 1200, 1600, 2000, 4000, 8000, 16000]

# bar_ranges = [i for i in range(range_labels)], bar_count = []

bar_count_gov = [0 * i for i in range_labels]
bar_count_names = ["" for i in range_labels]

for index, row in df.iterrows():
    bisected_position = bisect.bisect_left(range_labels, row['Days_in_Office'])
    bar_count_names[bisected_position] += f"\n{row['Name']}"

for val in range(len(range_labels)):
    for i in total_duration:
        if i <= range_labels[val]:
            bar_count_gov[val] += 1

# print("yo", bar_count_gov)
for i in range(len(bar_count_gov) - 1, 0, -1):
    if i > 0:
        bar_count_gov[i] -= bar_count_gov[i - 1]

# add = 0
# for i in bar_count_gov:
#    add += i

# print(bar_count_gov)

# print(bar_range_labels, bar_count_gov)

# With List of names on hover
# fig = go.Figure(
#     data=go.Bar(
#         x=bar_range_labels,
#         y=bar_count_gov,
#         hovertemplate="<b>Range in days</b>: %{x}<br>"
#         + "<b>Corresponding no. of Governors</b>: %{y} days<br><extra></extra>" + "<b> List of names:\n %{text}",
#         text=bar_count_names,
#     )
# )

fig = go.Figure(
    data=go.Bar(
        x=bar_range_labels,
        y=bar_count_gov,
        hovertemplate="<b>Range in days</b>: %{x}<br>"
        + "<b>Corresponding no. of Chief Ministers</b>: %{y} <br><extra></extra>",
    )
)


def governors_days():
    # print(bar_count_gov)
    return fig
