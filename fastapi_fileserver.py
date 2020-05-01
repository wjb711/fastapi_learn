#fastapi像apache一样，列出文件夹内容列表，也可以下载文件
from fastapi import FastAPI
from starlette.requests import Request
import os
#from fastapi.templating import Jinja2Templates
#from fastapi import templating
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

location='c:/Games'

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
