# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:13:02 2024

@author: python2
"""

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False


st.set_page_config(page_title="Dashboard",page_icon="📊",layout="wide")
st.header("六都信用卡消費分類 |  依照年收所得區分 ")

#data = pd.read_csv('各年收入族群持卡人於六都消費樣態.csv')
data = pd.read_csv('six_city_income.csv')

data.columns = data.columns.str.strip()
data['年月'] = pd.to_datetime(data['年月'], format='%Y%m', errors='coerce')


area_codes = {
    "63000000": "臺北市",
    "64000000": "高雄市",
    "65000000": "新北市",
    "66000000": "臺中市",
    "67000000": "臺南市",
    "68000000": "桃園市",
    "全台": "全台"
}


data['地區'] = data['地區'].astype(str).replace(area_codes)


st.sidebar.header("篩選條件")


min_date, max_date = st.sidebar.date_input("選擇日期範圍", value=[data['年月'].min(), data['年月'].max()])
data = data[(data['年月'] >= pd.to_datetime(min_date)) & (data['年月'] <= pd.to_datetime(max_date))]


income_options = ['全部'] + list(data['年收入'].unique())
income = st.sidebar.selectbox("選擇年收入", income_options)


selected_area = st.sidebar.selectbox("選擇地區", list(area_codes.values()))


industry_options = ['全部'] + list(data['信用卡產業別'].unique())
selected_industry = st.sidebar.selectbox("選擇信用卡產業別", industry_options)


if selected_area == "全台":
    if income == '全部' and selected_industry == '全部':
        aggregated = data.groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    elif income == '全部':
        aggregated = data[data['信用卡產業別'] == selected_industry].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    elif selected_industry == '全部':
        aggregated = data[data['年收入'] == income].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    else:
        aggregated = data[(data['年收入'] == income) & (data['信用卡產業別'] == selected_industry)].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
else:
    if income == '全部' and selected_industry == '全部':
        aggregated = data[data['地區'] == selected_area].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    elif income == '全部':
        aggregated = data[(data['地區'] == selected_area) & (data['信用卡產業別'] == selected_industry)].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    elif selected_industry == '全部':
        aggregated = data[(data['地區'] == selected_area) & (data['年收入'] == income)].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()
    else:
        aggregated = data[(data['年收入'] == income) & (data['地區'] == selected_area) & (data['信用卡產業別'] == selected_industry)].groupby(['年月']).agg({
            '信用卡交易筆數': 'sum',
            '信用卡交易金額[新臺幣]': 'sum'
        }).reset_index()


aggregated['交易筆數年增率'] = aggregated['信用卡交易筆數'].pct_change(12) * 100  
aggregated['交易金額年增率'] = aggregated['信用卡交易金額[新臺幣]'].pct_change(12) * 100
aggregated['交易筆數月增率'] = aggregated['信用卡交易筆數'].pct_change() * 100  
aggregated['交易金額月增率'] = aggregated['信用卡交易金額[新臺幣]'].pct_change() * 100



latest_data = aggregated.iloc[-1] if not aggregated.empty else None


with st.expander("查看詳細數據"):
     st.write(f"### 信用卡產業別 - {income} - {selected_area}")
     st.dataframe(aggregated)

def style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938", border_width="2px", value_font_size="16px"):
    st.markdown(f"""
    <style>
    .metric-card {{
        background-color: {background_color};
        border-left: {border_width} solid {border_left_color};
        border: {border_width} solid {border_color};
        box-shadow: {box_shadow};
        padding: 10px;
        margin: 10px;
    }}
    .metric-card .metric-value {{
        font-size: {value_font_size};  /* Font size for metric value */
    }}
    </style>
    """, unsafe_allow_html=True)


style_metric_cards(value_font_size="14px")  


with st.container():
    total1, total2, total3, total4, total5 = st.columns(5, gap='small')

    
    with total1:
        #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.info('信用卡交易筆數', icon="💳")
        st.metric(label="總筆數", value=f"{latest_data['信用卡交易筆數']:.0f}" if latest_data is not None else "0")
        st.markdown('</div>', unsafe_allow_html=True)

    with total2:
        #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.info('交易金額[新臺幣]', icon="💵")
        st.metric(label="總金額", value=f"{latest_data['信用卡交易金額[新臺幣]']:.0f}" if latest_data is not None else "0")
        st.markdown('</div>', unsafe_allow_html=True)

    with total3:
        #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.info('筆數年增率', icon="📈")
        st.metric(label="年增率", value=f"{latest_data['交易筆數年增率']:.2f}%" if latest_data is not None else "N/A")
        st.markdown('</div>', unsafe_allow_html=True)

    with total4:
        #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.info('金額年增率', icon="📊")
        st.metric(label="年增率", value=f"{latest_data['交易金額年增率']:.2f}%" if latest_data is not None else "N/A")
        st.markdown('</div>', unsafe_allow_html=True)

    with total5:
        #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.info('筆數月增率', icon="📅")
        st.metric(label="月增率", value=f"{latest_data['交易筆數月增率']:.2f}%" if latest_data is not None else "N/A")
        st.markdown('</div>', unsafe_allow_html=True)


fig = go.Figure()


fig.add_trace(go.Scatter(
    x=aggregated['年月'], 
    y=aggregated['信用卡交易金額[新臺幣]'], 
    name='信用卡交易金額[新臺幣]', 
    yaxis='y2', 
    mode='lines+markers',
    line=dict(color='green'),
    hovertemplate='%{y}'
))


fig.add_trace(go.Bar(
    x=aggregated['年月'], 
    y=aggregated['信用卡交易筆數'], 
    name='信用卡交易筆數', 
    yaxis='y1', 
    marker=dict(color='blue', opacity=0.5),
    hovertemplate='%{y}'
))


fig.update_layout(
    title='六都信用卡金額與筆數累計表',
    xaxis=dict(title='年月', tickformat='%Y-%m'),
    yaxis=dict(
        title='信用卡交易筆數',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='信用卡交易金額[新臺幣]',
        titlefont=dict(color='green'),
        tickfont=dict(color='green'),
        overlaying='y',
        side='right'
    ),
    legend=dict(
        x=0.5,
        y=-0.1,
        xanchor='center',
        orientation='h'
    ),
    template='plotly_white',
    height=700,  
    width=1200    
)


st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Scatter(
        x=aggregated['年月'], 
        y=aggregated['交易筆數年增率'], 
        name='交易筆數年增率 (%)', 
        mode='lines+markers',
        line=dict(color='purple'),
        hovertemplate='%{y:.2f}%'
    ))
    fig_yoy.add_trace(go.Scatter(
        x=aggregated['年月'], 
        y=aggregated['交易金額年增率'], 
        name='交易金額年增率 (%)', 
        mode='lines+markers',
        line=dict(color='orange'),
        hovertemplate='%{y:.2f}%'
    ))
    fig_yoy.update_layout(
        title='年增率',
        xaxis=dict(title='年月', tickformat='%Y-%m'),
        yaxis=dict(title='增率 (%)'),
        legend=dict(
            x=0.2, 
            y=-0.3, 
            xanchor='center', 
            orientation='h'
        ),
        template='plotly_white',
        height=400,   
        width=500    
    )
    st.plotly_chart(fig_yoy)


with col2:
    fig_mom = go.Figure()
    fig_mom.add_trace(go.Scatter(
        x=aggregated['年月'], 
        y=aggregated['交易筆數月增率'], 
        name='交易筆數月增率 (%)', 
        mode='lines+markers',
        line=dict(color='blue'),
        hovertemplate='%{y:.2f}%'
    ))
    fig_mom.add_trace(go.Scatter(
        x=aggregated['年月'], 
        y=aggregated['交易金額月增率'], 
        name='交易金額月增率 (%)', 
        mode='lines+markers',
        line=dict(color='green'),
        hovertemplate='%{y:.2f}%'
    ))
    fig_mom.update_layout(
        title='月增率',
        xaxis=dict(title='年月', tickformat='%Y-%m'),
        yaxis=dict(title='增率 (%)'),
        legend=dict(
            x=0.2, 
            y=-0.4, 
            xanchor='center', 
            orientation='h'
        ),
        template='plotly_white',
        height=400, 
        width=500    
    )
    st.plotly_chart(fig_mom)
