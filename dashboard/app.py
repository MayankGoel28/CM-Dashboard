import streamlit as st
import numpy as np
import pandas as pd
import traceback
from dashboard.total_terms import governors_days
from dashboard.timeline_visualization import count_by_parameter, state_terms, timeline_name, timeline_state, names_list, states_list

st.sidebar.write("Parameters")
start_year, end_year = st.sidebar.slider(
    "Select applicable years for timeline visualizations", 1930, 2021, value=(1930, 2021))
show_df = st.sidebar.checkbox("Show dataframes")
all_states = st.sidebar.checkbox("Show all States")

st.title("CM Dataset Visualizations")
with st.beta_expander("Average Days"):
    st.plotly_chart(governors_days())

if all_states:
    state_options = states_list
else:
    state_options = st.sidebar.multiselect(
        "Filter for States", states_list, None)


with st.beta_expander("Timeline Visualized by State"):
    try:
        (fig, df, repeats) = timeline_state(
            start_year, end_year, state_options)
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(df)
            if len(repeats):
                st.write(
                    'Chief Ministers who have represented more than one state')
                st.dataframe(repeats)
    except Exception as e:
        "*Select one or more states to begin.*"
    if len(state_options) == 1:
        "State Based Terms"
        st.plotly_chart(state_terms(state_options[0]))
    else:
        "*Select only one State to get term visualization*"

with st.beta_expander("Count by Turncoat"):
    try:
        data_df, fig = count_by_parameter(state_options, "Turncoat")
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(data_df)
    except Exception as e:
        if not state_options:
            "*Select one or more states to begin.*"
        else:
            "*Data is not available*"

with st.beta_expander("Count by Incumbent"):
    try:
        data_df, fig = count_by_parameter(state_options, "Incumbent")
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(data_df)
    except Exception as e:
        if not state_options:
            "*Select one or more states to begin.*"
        else:
            "*Data is not available*"

with st.beta_expander("Count by Recontest"):
    try:
        data_df, fig = count_by_parameter(state_options, "Recontest")
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(data_df)
    except Exception as e:
        if not state_options:
            "*Select one or more states to begin.*"
        else:
            "*Data is not available*"

with st.beta_expander("Count by Terms as MLA"):
    try:
        data_df, fig = count_by_parameter(state_options, "No_Terms_as_MLA")
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(data_df)
    except Exception as e:
        if not state_options:
            "*Select one or more states to begin.*"
        else:
            "*Data is not available*"

with st.beta_expander("Count by Terms as CM"):
    try:
        data_df, fig = count_by_parameter(state_options, "No_Terms_as_CM")
        st.plotly_chart(fig)
        if show_df:
            st.dataframe(data_df)
    except Exception as e:
        if not state_options:
            "*Select one or more states to begin.*"
        else:
            "*Data is not available*"


name_options = st.sidebar.multiselect("Filter for Names", names_list, None)
with st.beta_expander("Timeline Visualized by Chief Ministers"):
    try:
        fig, df = timeline_name(start_year, end_year, name_options)
        st.plotly_chart(fig)
        if show_df:
            if len(df) > 1:
                st.dataframe(df)
    except Exception as e:
        "*Select one or more Chief Ministers to begin.*"
