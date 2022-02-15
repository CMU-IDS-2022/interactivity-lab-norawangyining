from enum import unique
from re import U

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache
def load_data():
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    df = pd.read_csv("/Users/xmnora/Desktop/interactivity-lab-norawangyining/pulse39.csv")
    return df
   # pass

@st.cache
def get_slice_membership(df, genders, races, educations, age_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.
    
    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df['gender'].isin(genders)
    # ... complete this function for the other demographic variables
    return labels

def make_long_reason_dataframe(df, reason_prefix):
    """
    ======== You don't need to edit this =========
    
    Utility function that converts a dataframe containing multiple columns to
    a long-style dataframe that can be plotted using Altair. For example, say
    the input is something like:
    
         | why_no_vaccine_Reason 1 | why_no_vaccine_Reason 2 | ...
    -----+-------------------------+-------------------------+------
    1    | 0                       | 1                       | 
    2    | 1                       | 1                       |
    
    This function, if called with the reason_prefix 'why_no_vaccine_', will
    return a long dataframe:
    
         | id | reason      | agree
    -----+----+-------------+---------
    1    | 1  | Reason 2    | 1
    2    | 2  | Reason 1    | 1
    3    | 2  | Reason 2    | 1
    
    For every person (in the returned id column), there may be one or more
    rows for each reason listed. The agree column will always contain 1s, so you
    can easily sum that column for visualization.
    """
    reasons = df[[c for c in df.columns if c.startswith(reason_prefix)]].copy()
    reasons['id'] = reasons.index
    reasons = pd.wide_to_long(reasons, reason_prefix, i='id', j='reason', suffix='.+')
    reasons = reasons[~pd.isna(reasons[reason_prefix])].reset_index().rename({reason_prefix: 'agree'}, axis=1)
    return reasons


# MAIN CODE


st.title("Household Pulse Explorable")
with st.spinner(text="Loading data..."):
    df = load_data()
st.text("Visualize the overall dataset and some distributions here...")
st.write(df[:10])

#visualize the distributions of race and education levels in the data.
chart = alt.Chart(df).mark_bar().encode(
    alt.Y("race"),
    alt.X("count()"),
    alt.Color("education"),
    tooltip = ['count()']
).interactive()

st.altair_chart(chart, use_container_width=True)
#st.write(chart)

st.header("Custom slicing")
st.text("Implement your interactive slicing tool here...")
genders = st.multiselect("Choose the gender you are intrested in: ", df['gender'].unique())
races = st.multiselect("Races: ", df['race'].unique())
educations = st.multiselect("Educations: ", df['education'].unique())
print(df['age'].unique())
age_range = st.slider(
    'select age range:',
    int(np.amin(df['age'].unique())), int(np.amax(df['age'].unique())),
    (int(np.amin(df['age'].unique())), int(np.amax(df['age'].unique())))
)

get_slice_membership(df, genders, races, educations, age_range)



st.header("Person sampling")
st.text("Implement a button to sample and describe a random person here...")
