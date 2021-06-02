import numpy as np
import streamlit as st
import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import plotly.express as px

from streamlit.file_util import streamlit_read

url = "https://api.yelp.com/v3/businesses/search"

api_key = 'XwBQbDLTSHgR4k4LhzRoMAg4Br1VKMJ-dgqbpU-iqne0HTu65cleEj-9KjH1RnSAowqkSeEpoqPJISpxjVJDprj6XsaXQSC7Br8Me0re9tyvG_mLCjyM-stvUs63YHYx'

def get_data(input1, input2):
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {'term': str(input1), 'location': str(input2)}
    resp = requests.get(url, headers=headers, params=params, verify=False)
    return json.loads(resp.text)

def main():

    with st.form(key = "searchform"):
        
        nav1, nav2, nav3 = st.beta_columns([3,2,1])

        with nav1:
            search_term = st.text_input("Search Input")
        with nav2:
            search_term2 = st.text_input("Search Input2")
        with nav3:
            st.text("Search")
            search = st.form_submit_button(label="Search")
    st.success("Searching for {} in {}".format(search_term, search_term2))  

    #Results 
    if search:
        result = get_data(search_term, search_term2)
        df = json_normalize(result["businesses"], sep="_", record_path = "categories", meta=["name", 'alias',
                                                                                    "rating", ["coordinates", "latitude"],
                                                                                    ["coordinates", 'longitude']],
                    meta_prefix="biz_")

        st.write(df)

        df['biz_rating'] = df['biz_rating'].astype(float)
        fig = px.bar(df, x='alias', y='biz_rating')
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()