import streamlit as st
from vega_datasets import data
import pandas as pd
import base64
import asyncio
from datetime import datetime

st.set_page_config(page_title="Orienteering Starter",layout="wide", initial_sidebar_state="collapsed")
pd.options.display.width = 100


@st.cache(allow_output_mutation=True)
def load_data():
   data = pd.read_csv('Startlist_sample.csv', encoding='cp932')
   return data

@st.cache(allow_output_mutation=True)
def get_table_download_link(df):

    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False, encoding='shift_jis')
    b64 = base64.b64encode(csv.encode(encoding='shift_jis')).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

@st.cache(allow_output_mutation=True)
def get_paragraph(string:str, size: str, color:str):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    href = f'<p style="font-size: {size}; color: {color};">{string}</p>'
    return href

async def refresh_table(disp, data: pd.DataFrame):
    while True:
        # 現在時刻以後のリスト抽出
        mask = (data['スタート時刻'] >= datetime.now())
        data = data.loc[mask]
        disp.dataframe(data, height=500)
        r = await asyncio.sleep(1)

async def refresh_time(disp):
    while True:
        datestr = datetime.now().strftime("%H:%M:%S")
        disp.markdown(get_paragraph(datestr, "80px", 'red'), unsafe_allow_html=True)
        r = await asyncio.sleep(1)

data = load_data()
data['スタート時刻'] = data['スタート時刻'].astype('datetime64')

# サイドバー表示
lanes = st.sidebar.multiselect("表示レーン", data['レーン'].unique())
data = data[data['レーン'].isin(lanes)]

# 現在時刻表示
disp_current_time = st.empty()
disp_table = st.empty()
st.markdown(get_table_download_link(data), unsafe_allow_html=True)

# col1, col2 = st.beta_columns(2)

async def tasks():
    await asyncio.gather(
        refresh_time(disp_current_time),
        refresh_table(disp_table, data)
    )

asyncio.run(tasks())
