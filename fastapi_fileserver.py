#fastapi做的文件服务器
#python3 -m uvicorn fastapi0:app --host '0.0.0.0' --reload
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

#读取配置文件
def read_config():
    default_config='''
    [first]
        name="yusheng_liang"
        age=20
        sex = "man"

    [second]
        name="june"
        age=25
        sex = "weman"
    '''
    import configparser

    config = configparser.ConfigParser()

    #---------------------------查找文件内容,基于字典的形式

    print(config.sections())        #  []

    config.read('example.ini')

    print(config.get('first','age'))        #   ['bitbucket.org', 'topsecret.server.com']


#日志的处理方法
def log():
    import logging
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
     
    logger.addHandler(handler)
    logger.addHandler(console)
     
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")
    

#读取json
def readjson():
    demo_json='''
    {
        "name": "Cactus",
        "age": 20
    }
    '''
    with open("demo2.json", encoding="utf-8") as f:
        data = json.load(f)

    print(data['age'])
    

#写json
def writejson():
    demo_json='''
    {
        "name": "Cactus",
        "age": 20
    }
    '''
    
    with open("demo2.json", encoding="utf-8") as f:
        data = json.load(f)

    print(data['age'])
    data['age']=20
    dict_var = {
        "name": "Cactus",
        "age":19
    }
    x=json.dumps(data,indent=4,ensure_ascii=False)
    with open("demo2.json", 'w', encoding="utf-8") as f:
        f.write(x)


#运行本程序方法
#python3 -m uvicorn main1:app  "--host" "0.0.0.0" --port 80 --reload &

location='static'
dir_html='''
<html>
<body>
<dir>
<ul>
{% for user in id %}
<br>{{ user }}</br>
<a href="/files/1?q={{q}}/{{ user }}">{{ user }}</a>
{% endfor %}
</ul>
{{ id1 }}
</body>
</html>
'''
app = FastAPI()
app.mount('/static', StaticFiles(directory=location), name='static') 
templates = Jinja2Templates(directory="templates")

@app.get("/dir")
def read_root():
    #return {"Hello": "World"}
    return RedirectResponse(url='/files/1?q=')


@app.get("/files/{item_id}")
def read_files(request:Request, item_id: str, q: str = None):
    
    #return {"item_id": item_id, "q": q}
    data=['hello','china']
    print('q before:')
    q0=location+'/'+q
    print('q0 after:',q0)
    if os.path.isdir(q0):
        list0=os.listdir(q0)
        print('*****************folder************************'+q0)
    #return x
        return templates.TemplateResponse("dir.html", {"request": request, "id": list0, "id1":"xxxx", "q":q})
    else:
        print('&&&&&&&&&&&file&&&&&&&&&&&&&&&&&&&&&&'+q0)
        q=q.replace(' ','%20')
        print('q again:::::::',q)
        return RedirectResponse(url='/static'+q)

@app.post("/uploadfiles/")
async def create_upload_files(
    files: List[UploadFile] = File(...)
):
    #return {"filenames": [file.filename for file in files]}
    #contents = await files[0].read().decode('utf8')
    contents = files[0].file.read()
    name0=files[0].filename
    with open('static/upload/'+name0,'wb') as f:
        f.write(contents)
    #return files[0].filename, files[0].content_type
        content = """
<body>
<a href="/static/upload/{}" title="转到CSS5主页">上传完成，下载链接请右键复制</a>
</body>
 """.format(name0)
    return HTMLResponse(content=content)

@app.get("/upload")
async def upload():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
 """
    return HTMLResponse(content=content)
    
