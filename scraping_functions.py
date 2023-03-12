import json
import asyncio
import traceback
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ---SubFunctions---

# --page renderers--
# "RenderingFunction":"default-renderer"
async def render_default(URL):
    session = AsyncHTMLSession()
    res = await session.get(URL)
    return res

# "RenderingFunction":"renderer-001"
async def render_001(URL):
    session = AsyncHTMLSession()
    res = await session.get(URL)
    await res.html.arender(scrolldown=1000, sleep=0.01)
    return res
# --page renderers end--


# --soup source shaper--
# soup to soup, find method
def s2s_find(soup,style):
    if style["IdentifyMethod"]=="None":
        res = soup
    elif style["IdentifyMethod"]=="Class":
        res = soup.find(class_=style["Class"])
    elif style["IdentifyMethod"]=="Tag":
        res = soup.find(style["Tag"])
    elif style["IdentifyMethod"] in style:
        res = soup.find(style["Tag"], {style["IdentifyMethod"]:style[style["IdentifyMethod"]]})
    else:
        raise NameError("Unexpected IdentifyMethod Value")
    return res

# soup to soup array, find_all method
def s2sArray_find_all(soup,style):
    if style["IdentifyMethod"]=="Class":
        res = soup.find_all(class_=style["Class"])
    elif style["IdentifyMethod"]=="Tag":
        res = soup.find_all(style["Tag"])
    elif style["IdentifyMethod"]=="Id":
        res = soup.find_all(style["Id"])
    elif style["IdentifyMethod"] in style:
        res = soup.find_all(style["Tag"], {style["IdentifyMethod"]:style[style["IdentifyMethod"]]})
    else:
        raise NameError("Unexpected IdentifyMethod Value")
    return res
    
# --soup source shaper end--


# --str data shaper--
def title_shaper_001(param,i):
    if i+1>=100:
        param=param[5:]
    elif i+1>=10:
        param=param[4:]
    elif i+1>=4:
        param=param[3:]
    else:
        pass
    return param

def rank_shaper_001(param,j):
    res = j+1
    return res

def int_shaper_001(param,j):
    res=param.replace(",","")
    return res
# --str data shaper end--


# Function Selection Map
function_map={
    "default-renderer":render_default,
    "renderer-001":render_001,
    
    "title-shaper-001":title_shaper_001,
    "rank-shaper-001":rank_shaper_001,
    "int-shaper-001":int_shaper_001
}

# ---SubFunctions end---


# Select renderer and Get HTML
async def getHTML(format):
    renderer=function_map[format["Renderer"]]
    URL=format["URL"]
    res = await renderer(URL)
    if res is None:
        raise ValueError("RendererError occurred")
    return res

# Shaping HTML data
def shaping(page_data,format):
    # BeautifulSoup
    soup=BeautifulSoup(page_data.html.html,"lxml")
    if soup is None:
        raise ValueError("Soup is None")
    
    # Extract main containts
    soup_main=s2s_find(soup,format["Main"])
    if soup_main is None:
        raise ValueError("Main containts is None. Please check IdentifyMethod and Class value in Format-Main.")
    
    # Extract containts per anime title
    soup_animes=s2sArray_find_all(soup_main,format["Animes"])
    if soup_animes is None:
        raise ValueError("Animes containts is None. Please check IdentifyMethod and Class value in Format-Animes.")
    
    # Create dataframe
    columns=["date"]
    for feature in format["Features"]:
        columns.append(feature["FeatureName"])
    df = pd.DataFrame(columns=columns)
    
    # Imput data into dataframe
    today = datetime.utcnow().date()
    for i,soup_anime in enumerate(soup_animes):
        # Inisialize add_list
        add_list=[[today]]
    
        # Shaping data
        for feature in format["Features"]:
            
            soup_param=s2s_find(soup_anime,feature)
            if soup_param is None:
                print(feature["FeatureName"]," containts is None. Please check IdentifyMethod and Class value in Format-Feature.")
                if feature["FeatureType"]=="Integer":
                    add_list[0].append(0)
                else:
                    add_list[0].append("")
                continue
            
            # Extract text
            param = soup_param.text
            # Shaping if extra processes are needed
            if feature["ShapingFunction"]!="default":
                param=function_map[feature["ShapingFunction"]](param,i)
            if param is None:
                raise ValueError(feature["FeatureName"]," containts is None. Please check IdentifyMethod, Class, ShapingFunction value in Format-Feature.")
                
            add_list[0].append(param)

        # Merge add_list to dataframe
        df_add = pd.DataFrame(data=add_list,columns=columns)
        df = pd.concat([df, df_add], ignore_index=True, axis=0)
    
    return df
