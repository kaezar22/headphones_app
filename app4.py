# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 08:36:06 2023

@author: ASUS
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib as mpl
import streamlit as st
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")
df = pd.read_csv('C:/Users/ASUS/Documents/Python Scripts/Headphones/headphones_clean.csv')
#image = Image.open('D:/Beats store/CZR_logo.png')

col8, col9 = st.columns(2)
#with col8:
    
    st.title('HEADPHONES WORLD')
#with col9:
 #   st.image(image, caption=None, width = 140 )
st.header('Hearing the latest trends on headphones available to buy on-line.\n ')
st.caption('Automatically updated every 3 days')

col1, col2 = st.columns(2)
'''
______________________________________
'''
st.header('               Analysis by Market Segment')

col3, col4 = st.columns(2)
col6, col7 = st.columns(2)
###################################
with col1:
    st.subheader('Items available per brand')
    country_brand = df.groupby(['Brand','country'])[['Title']].count() #subgrouping the table
    cb=country_brand.reset_index()
    fig,ax=plt.subplots(1,1,figsize=(10, 5))
    
    
    color_map={'Austria': '#05445E', 'China': '#189AB4', 'Germany': '#75E6DA', 'Japan':'#D4F1F4','Korea': '#ECF87F', 'Swiss': '#A3EBB1', 'UK': '#2E8BC0', 'USA':'#18A558'}
    
    cb["colors"]=cb["country"].map(color_map)
    for g in ["Austria","China","Germany",'Japan',"Korea","Swiss","UK","USA"]:
        xs=cb.Brand[cb["country"]==g]
        ys=cb["Title"][cb["country"]==g]
        color=cb["colors"][cb["country"]==g]
        ## or, perhaps easier in this specific case: 
        #  color=color_map[g]
    
        ax.bar(xs,ys,color=color,label=g)
    
        #plt.title(label = ' Number of Items by Brand', fontsize = 30,
         #     color = "gray",
          #    loc="left",
           #   fontstyle='italic')
    ax.legend()
    ax.set_xticks(cb.Brand)
    ax.set_xticklabels(cb["Brand"],rotation = 90)
    
    st.write(fig)



#########################################################


with col2:
    st.subheader('Availability of Items per country and segment')
    df = pd.read_csv('C:/Users/ASUS/Documents/Python Scripts/Headphones/headphones_clean.csv')
    c_seg = df.groupby(['country','segment'])[['Title']].count()
    c_seg = c_seg.reset_index()
    
    domain = ["professional", "high-end", "Mobil accessories","Other"]
    range_ = ["#05445E", "#189AB4","#75E6DA","#D4F1F4"]
     
    bar_chart = alt.Chart(c_seg).mark_bar().encode(
            x="sum(Title):Q",
            y="country:O",
            color=alt.Color("segment", scale=alt.Scale(domain=domain, 
                                                       range=range_)),
            
        )
    st.altair_chart(bar_chart, use_container_width=True)

##############################################

with st.sidebar:
    st.subheader('Select the segment')
    MarketSeg = st.selectbox(' ', ('professional',
                         'high-end','Mobil accessories','Other'))
 
    sg = MarketSeg

    s2 = df[df['segment']== sg]



##################################################

with col3:
    st.subheader('Sales per brand')
    sold = s2.groupby(['Brand','design'])[['Num_reviews']].sum()
    sold = sold.reset_index()
    
    domain = ["Headphones", "in-ear"]
    range_ = ["#05445E", "#189AB4"]
    bar_chart = alt.Chart(sold).mark_bar().encode(
            x="sum(Num_reviews):Q",
            y="Brand:O",
            color=alt.Color("design", scale=alt.Scale(domain=domain, range=range_))
        )
    st.altair_chart(bar_chart, use_container_width=True)

###################################################

# Average price by brand, vertical bar chart
with col4:
    st.subheader('Average price')
    av_price = s2.groupby(['Brand'])[['Price']].mean()
    av_price['avprice'] = av_price['Price'].astype(int)
    
    av_price.sort_values('avprice', ascending = False, inplace = True)
    df4 = av_price.drop('Price', axis = 1)
    df4 = df4.reset_index()
    
    bar_chart = alt.Chart(df4).mark_bar().encode(
            y='avprice:Q',
            x=alt.X("Brand:N", sort="-y")
            )
            
    st.altair_chart(bar_chart, use_container_width=True)

#########################################################
#scatter plot

st.subheader('Sales, Brand and Price Bubble plot')
range_ = ["#05445E", "#189AB4","#75E6DA","#D4F1F4","#ECF87F","#A3EBB1","#2E8BC0","#18A558"]
price = s2[['Title','Price','Brand','Num_reviews']]
   
sctr = alt.Chart(price).mark_circle(size=60).encode(
    y='Price',
    x='Title',
    color=alt.Color("Brand", scale=alt.Scale(range=range_)),
    size = 'Num_reviews',
    tooltip=['Title', 'Brand', 'Price', 'Num_reviews']
    )
    
st.altair_chart(sctr, use_container_width=True)

####################
# Calculating percentage and ploting Pie charts for type of connection
with col6:
    st.subheader('Connection Type')
    conn = s2.groupby(['conn'])[['Title']].count()
    conn['percent'] = (conn['Title'] / 
                        conn['Title'].sum()) * 100
    conn.percent = conn.percent.round(2)  #adjust the decimal point
    conn = conn.reset_index()
    
    conn1 = alt.Chart(conn).encode(
        theta=alt.Theta("percent:Q", stack=True), color=alt.Color("conn:N", scale=alt.Scale(range=range_))
    )
    
    pie = conn1.mark_arc(outerRadius=100)
    text = conn1.mark_text(radius=80, size=10).encode(text="conn:N")
    pie + text

###########################################
with col7:
    st.subheader('Gamer')
    range_2 = ["#75E6DA","#A3EBB1"]
    gam = s2.groupby(['Use'])[['Title']].count()
    gam['percent'] = (gam['Title'] / 
                        gam['Title'].sum()) * 100
    gam.percent = gam.percent.round(2)  #adjust the decimal point
    gam = gam.reset_index()
    
    gam1 = alt.Chart(gam).encode(
        theta=alt.Theta("percent:Q", stack=True), color=alt.Color("Use:N", scale=alt.Scale(range=range_2))
    )
    
    pie1 = gam1.mark_arc(outerRadius=100)
    text1 = gam1.mark_text(radius=80, size=10).encode(text="Use:N")
    pie1 + text1

##############################################
with st.sidebar:
    '''
    
    
    
    
    
    ________________________________
    
    '''
    st.subheader('Compare two brands')
    br1 = st.selectbox('Choose the first brand',('BOSE','BEYERDYNAMIC','PIONEER',
                                                 'BEATS','MARSHALL','AUDIO-TECHNICA',
                                                 'AFTERSHOKZ','SENNHEISER','SONY',
                                                 'SOUNDCORE','LOGITECH','SKULLCANDY',
                                                 'HUAWEI','JBL','SAMSUNG','AKG',
                                                 'HONOR','BEHRINGER','HAYLOU',
                                                 'XIAOMI','LENOVO','MAXELL','MOTOROLA',
                                                 'APPLE','HYPERX','SOUNDPEATS','ASTRO',
                                                 'ONIKUMA','CORSAIR','XTRIKE','RAZER',
                                                 'KOTION','GENIUS','OTHER', 'OPPO'
                                                 ))

    br2 = st.selectbox('Choose the second brand',('BOSE','BEYERDYNAMIC','PIONEER',
                                                  'BEATS','MARSHALL','AUDIO-TECHNICA',
                                                  'AFTERSHOKZ','SENNHEISER','SONY',
                                                  'SOUNDCORE','LOGITECH','SKULLCANDY',
                                                  'HUAWEI','JBL','SAMSUNG','AKG',
                                                  'HONOR','BEHRINGER','HAYLOU',
                                                  'XIAOMI','LENOVO','MAXELL','MOTOROLA',
                                                  'APPLE','HYPERX','SOUNDPEATS','ASTRO',
                                                  'ONIKUMA','CORSAIR','XTRIKE','RAZER',
                                                  'KOTION','GENIUS','OTHER', 'OPPO'
                                                  ))
'''
__________________________
'''
st.header('Brand Price Analyzer')   
options = [br1, br2] 
compbr = df.loc[df['Brand'].isin(options)] 
compbr = compbr[['Title','Brand','Price']]
        
pr1=compbr['Brand'].unique()
df5=pd.concat([compbr.set_index(['Title']).groupby('Brand')['Price'].get_group(key) for key in pr1],axis=1)
df5.columns=pr1
df5.reset_index(inplace=True)
df5[br1].fillna(0, inplace = True)
df5[br2].fillna(0, inplace = True)
df5 = df5[options]
    
chart = alt.Chart(compbr).mark_boxplot(extent='min-max').encode(
        x='Brand:O',
        y='Price:Q',
        color=alt.Color("Brand", scale=alt.Scale(range=range_))
        )
    
tab1, tab2 = st.tabs(["Comparing brands", "BOXPLOT"])
    
with tab1:
     st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
     st.altair_chart(chart, theme=None, use_container_width=True)
