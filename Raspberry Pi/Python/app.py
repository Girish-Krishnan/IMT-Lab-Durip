from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def run_sensor_schedule_command(command):
    """Run sensor_schedule.py with the specified command."""
    result = subprocess.run(['python', 'sensor_schedule.py'] + command, capture_output=True, text=True)
    return result.stdout

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("static/index.html", "r").read(), status_code=200)

@app.post("/execute")
async def execute_command(command: str = Form(...), args: str = Form(...)):
    args_list = args.split(',') if args else []
    result = run_sensor_schedule_command([command] + args_list)
    return result

@app.get("/view_schedules")
async def view_schedules():
    result = run_sensor_schedule_command(['view'])
    raise NotImplementedError
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)