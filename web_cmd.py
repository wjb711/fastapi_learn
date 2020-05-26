import secrets

import subprocess

from starlette.requests import Request

from fastapi import Depends, FastAPI, HTTPException, status

from fastapi.security import HTTPBasic, HTTPBasicCredentials

import os

from jinja2 import Template

from starlette.templating import Jinja2Templates

from starlette.responses import HTMLResponse



from starlette.responses import RedirectResponse



dir.html='''

<html>

<body>

<h1>web版shell命令行</h1>

<ul>

{% for user in list0 %}

<br><a href="/items/console?cmd={{q}}{{ user }}">{{ user }}</a></br>

{% endfor %}

</ul>



<dir>

<ul>

<form action="/items/console">

其它，请输入shell命令:<br>

<input type="text" name="cmd" size="80">

<br>

<br><br>

<input type="submit" value="Submit">

</form>



<p>如果您点击提交，命令将在服务器被执行。</p>



{% for user in id %}

<br><a>{{ user }}</a></br>

{% endfor %}

</ul>

</body>

</html>


'''



templates = Jinja2Templates(directory="templates")

app = FastAPI()



security = HTTPBasic()





def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):

correct_username = secrets.compare_digest(credentials.username, "root")

correct_password = secrets.compare_digest(credentials.password, "rootpasswd")

if not (correct_username and correct_password):

raise HTTPException(

status_code=status.HTTP_401_UNAUTHORIZED,

detail="Incorrect email or password",

headers={"WWW-Authenticate": "Basic"},

)

return credentials.username





@app.get("/")

def read_current_user(username: str = Depends(get_current_username)):

#return {"username": username}

return RedirectResponse(url='/items/console?cmd=')



@app.get("/hello")

def read_hello():

return "china"



@app.get("/items/{item_id}")

def read_item(request:Request, item_id: str, cmd: str = None):

list0=[]

for item in os.listdir('./'):

if item.endswith('.sh'):

list0.append(item)

list0.sort()

print('cmd is:',cmd)

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

stdout, stderr = p.communicate()

print('stderr:',stderr.decode())

if "command not found" in stderr.decode():

cmd='sh '+cmd

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

stdout, stderr = p.communicate()

id0=stdout.decode()

print(id0,type(id0))

id1=id0.split('\n')

print(id1)

#return {"item_id": item_id, "q": q, "r":stdout}

#return id1

return templates.TemplateResponse("dir.html", {"request": request, "id": id1, "list0":list0})





@app.get("/cmd")

def read_item():

return RedirectResponse(url='/items/console?cmd=')



@app.get("/dir")

def read_dir():

list0=[]

for item in os.listdir('./'):

if item.endswith('.sh'):

list0.append(item)

return list0

