from fastapi import FastAPI
from starlette.requests import Request
import os
#from fastapi.templating import Jinja2Templates
#from fastapi import templating
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
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
    x=json.dumps(data,indent=4)
    with open("demo2.json", 'w', encoding="utf-8") as f:
        f.write(x)


#运行本程序方法
#python3 -m uvicorn main1:app  "--host" "0.0.0.0" --port 80 --reload &

location='c:/Games'
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
    
if __name__=="__main__":
    print('hello')
    #os.system('python3 -m uvicorn a3:app  "--host" "0.0.0.0" --port 80 --reload')
