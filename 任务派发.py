from fastapi import FastAPI
import time
import os
app = FastAPI()
no_action="当前无任务"
delta=no_action

@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.get("/action/{item_id}")
async def read_action(item_id: str, q: str = None, w: str = None):
    global delta
    
    print('q:',q)
    if q:
        #return {"item_id": item_id, "q": q, "w": w}
        delta=q
        os.popen(q)
        return q
    else:
        d0=delta
        delta=no_action
        return d0
        
    
