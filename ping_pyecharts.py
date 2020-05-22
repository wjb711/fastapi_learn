#直接从ping值出图
from fastapi import FastAPI
from starlette.requests import Request
import os
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from typing import List
from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse
import json
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Scatter
from pyecharts.charts import Line
from shutil import copyfile

from ping3 import ping

@app.get("/ping/{item_id}")
def read_ping(item_id: str, q: str = None, width: str = "800px"):
    line=Line(init_opts=opts.InitOpts(js_host='/static/',theme=ThemeType.LIGHT,width=width,animation_opts=opts.AnimationOpts(animation_duration=500)))
        #Bar()
    set0=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    
    x=list(range(len(set0)))
    #x=[1,2,3,4,5,6,7,8,9]
    line.add_xaxis(x)
    list_ip=item_id.split(',')
    for ip in list_ip:
        try:
            data=int(ping(ip, unit='ms'))
        except:
            data=5impo00
        
        if ip in dict_ip:
            pass
        else:
            dict_ip[ip]=list(set0)
        dict_ip[ip].append(data)
        dict_ip[ip].pop(0)
    #x=['1','2','3','4','5','6']
    #y=[1,2,3,4,5,6]
    #y1=[0,1,2,3,4,5]
    #c = (
        #Bar(init_opts=opts.InitOpts(js_host='./static',theme=ThemeType.LIGHT,width="2000px",animation_opts=opts.AnimationOpts(animation_duration=3000)))
    #line=Line(init_opts=opts.InitOpts(js_host='/static/',theme=ThemeType.LIGHT,width=width,animation_opts=opts.AnimationOpts(animation_duration=500)))
        #Bar()
    #line.add_xaxis(x)
    
        line.add_yaxis(ip, dict_ip[ip])
    #line.add_yaxis('hello1', y1)
        #.add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
    #line.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=12,interval=0,rotate=-45)),title_opts=opts.TitleOpts(title=item_id),toolbox_opts=opts.ToolboxOpts())
    line.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=12,interval=0,rotate=-45)),title_opts=opts.TitleOpts(title=""),toolbox_opts=opts.ToolboxOpts())
    
    #return {"Hello": "World"}
    xxx='''
<meta charset="UTF-8">
<script>
    setTimeout('location.href="/ping/{}"', 5000);
</script>

'''.format(item_id)
    y=line.render_embed()
    y=y.replace('<meta charset="UTF-8">',xxx)
    return HTMLResponse(content=y)
