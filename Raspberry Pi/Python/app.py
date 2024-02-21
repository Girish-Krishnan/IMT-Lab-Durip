from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import os
import json
import uvicorn

app = FastAPI()

# Serve static files like CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

def run_sensor_schedule_command(command):
    """Run sensor_schedule.py with the specified command."""
    result = subprocess.run(['python', 'sensor_schedule.py'] + command, capture_output=True, text=True)
    return result.stdout

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("index.html", "r").read(), status_code=200)

@app.post("/execute")
async def execute_command(command: str = Form(...), args: str = Form(...)):
    args_list = args.split(',') if args else []
    try:
        result = run_sensor_schedule_command([command] + args_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/view_schedules")
async def view_schedules():
    try:
        result = run_sensor_schedule_command(['view'])
        print(result)
        # Assuming the result is in a JSON-compatible format
        schedules = json.loads(result)
        return JSONResponse(content=schedules)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")