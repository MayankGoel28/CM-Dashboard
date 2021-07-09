# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import json

import plotly.graph_objects as go

import plotly.express as px

pd.options.plotting.backend = "plotly"

source = "./TCPD-CMID_1962_2021.csv"

df = pd.read_csv(source)
df = df.replace(np.nan, "", regex=True)

# print(df)


states = []
for index, row in df.iterrows():
    states.append(row["State_Name"])

states = list(np.unique(np.array(states)))

# print(states, len(states))


data = []


def date_get(s):
    x = s.split('-')
    if len(x[0]) != 2:
        x[0] = "0"+x[0][0]
    if len(x[1]) != 2:
        x[1] = "0"+x[1][0]
    return x[2] + '-' + x[1] + '-' + x[0]


states_list = []
for index, row in df.iterrows():
    states_list.append(row["State_Name"])
names_dict = {}
for index, row in df.iterrows():
    names_dict[row['pid_CM']] = row["Name"]
names_list = []
for id in names_dict:
    names_list.append(f'{names_dict[id]} ({id})')
states_list = list(set(states_list))

repeat_governors = {}


def timeline_state(start_year, end_year, states=[]):
    if not states:
        return None
    data = []
    for state in states:
        for index, row in df.iterrows():
            if row["State_Name"] == state:
                # print(type(row["Start_Date"]))
                start_date = date_get(row["Start_Date"])
                if row["End_Date"] != "Current":
                    end_date = date_get(row["End_Date"])
                else:
                    end_date = "2021-01-13"
                if int(end_date[:4]) >= start_year and int(start_date[:4]) <= end_year:
                    if row["Name"] not in repeat_governors:
                        repeat_governors[row["Name"]] = [row["State_Name"]]
                    else:
                        repeat_governors[row["Name"]].append(row["State_Name"])
                    data.append(
                        {
                            "Name": f'{row["Name"]} ({row["State_Name"]})',
                            "Start": start_date,
                            "Finish": end_date,
                            "State": row["State_Name"],
                        }
                    )
    repeats = []
    for name in repeat_governors:
        cur_list = list(set(repeat_governors[name]))
        if len(cur_list) > 1:
            repeats.append({"name": name, "States": ', '.join(cur_list)})
    repeats = pd.DataFrame(repeats)
    data_df = pd.DataFrame(data)
    fig = px.timeline(data_df, x_start="Start",
                      x_end="Finish", y="Name", color="State")
    for index, row in data_df.iterrows():
        row["Name"] = row["Name"].split("(")[0]
    return (fig, data_df, repeats)


def count_by_parameter(states=[], parameter=""):
    if not states:
        return None
    data_df = []
    for state in states:
        for index, row in df.iterrows():
            if row["State_Name"] == state and row[parameter] != "":
                data_df.append(row)
    fig = px.histogram(data_df, x=parameter)
    return (data_df, fig)

# fig = px.timeline(data_df, x_start='Start', x_end='Finish', y='State', color='State')
# fig.show()


def timeline_name(start_year, end_year, names=[]):
    if not names:
        return None
    data = []
    for name_id in names:
        for index, row in df.iterrows():
            name = name_id.split(' (')
            name = name[0]
            if row["Name"] == name:
                # print(type(row["Start_Date"]))
                start_date = date_get(row["Start_Date"])
                if row["End_Date"] != "Current":
                    end_date = date_get(row["End_Date"])
                else:
                    end_date = "2021-01-13"
                if int(end_date[:4]) >= start_year and int(start_date[:4]) <= end_year:
                    data.append(
                        {
                            "Name": row["Name"],
                            "Start": start_date,
                            "Finish": end_date,
                            "State": row["State_Name"],
                        }
                    )
    data_df = pd.DataFrame(data)
    fig = px.timeline(data_df, x_start="Start",
                      x_end="Finish", y="State", color="Name")
    return (fig, data_df)


def gender_data():
    keys = df.groupby(
        ["State_Name"])["Gender"].value_counts(normalize=True).keys().tolist()
    values = df.groupby(
        ["State_Name"])["Gender"].value_counts(normalize=True).tolist()
    ratio = {"State": [], "Ratio": []}
    for ptr in range(len(keys)):
        if keys[ptr][1] == "M":
            ratio["State"].append(keys[ptr][0])
            ratio["Ratio"].append(1 - values[ptr])

    states = json.load(open("./Governors Data/states_india.geojson", "r"))
    states["features"][1]["properties"]
    state = {}
    anomalies = {
        "Arunanchal Pradesh": "Arunachal Pradesh",
        "Andaman & Nicobar Island": "Andaman & Nicobar Islands",
        "Dadara & Nagar Havelli": "Dadra & Nagar Haveli",
        "NCT of Delhi": "Delhi",
    }
    list_states = []
    for f in states["features"]:
        f["pid_CM"] = f["properties"]["state_code"]
        s = f["properties"]["st_nm"]
        if s in anomalies:
            s = anomalies[s]
        list_states.append(s)
        state[s] = f["pid_CM"]
    ratio = pd.DataFrame(ratio)
    ratio.drop(index=ratio[ratio["State"] == "Ladakh"].index, inplace=True)
    ratio.drop(
        index=ratio[ratio["State"] ==
                    "Dadra & Nagar Haveli & Daman & Diu"].index,
        inplace=True,
    )
    # state['Dadra & Nagar Haveli & Daman & Diu']=state['Dadra & Nagar Haveli']
    # state['Ladakh']=state['Jammu & Kashmir']
    # print(state['Lad'])
    ratio["pid_CM"] = ratio["State"].apply(lambda x: state[x])
    flag = False
    # print(ratio.iloc[0]['State'])
    # This is to check if all the states match or not
    for i in range(len(ratio.index)):
        if ratio.iloc[i]["State"] in list_states:
            continue
        else:
            flag = True
    # print(flag)
    fig = px.bar(ratio, x='State', y='Ratio', labels={
        "Ratio": "Percentage of Females"
    })
    # print(ratio)
    return fig


def state_terms(state=""):
    try:
        unique_id = []
        for index, row in df.iterrows():
            if row["State_Name"] == state:
                unique_id.append(row["pid_CM"])
        unique_id = list(set(unique_id))
        # print(unique_id)
        names = []
        total_dur = []

        for i in unique_id:
            name = ""
            total = 0
            for index, row in df.iterrows():
                if row["State_Name"] == state and row["pid_CM"] == i:
                    total += row["Days_in_Office"]
                    name = row["Name"]
            names.append(name), total_dur.append(total)
        #print(names, total_dur)
        fig = go.Figure(
            data=[go.Pie(labels=names, values=total_dur)])
        return fig
    except Exception as e:
        return None
