from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from fastapi_utils.tasks import repeat_every

import asyncio, json, subprocess, sys, os, time, shutil, uvicorn
from lite_fastapi_local import QR_CHK_dep as CHKF

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.common.function import find_camera_index, save_cctv
from lite_fastapi_local.settings import Logger, mqtt
from lite_fastapi_local.router import setupRouter, motorRouter
from lite_fastapi_local.model.motorModel import motor
from lite_fastapi_local.model.ledModel import led


app = FastAPI()
app.include_router(setupRouter.router)
app.include_router(motorRouter.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    # mqtt.client.subscribe("tg/C8F09E12C7D8/event") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

# @mqtt.subscribe("tg/+/qr_code")
# async def message_to_topic(client, topic, payload, qos, properties):
#     data = json.loads(payload.decode())
#     qr_code = data["qr_code"]
#     result = "true"
#     motor.send_qr_result(qr_code=qr_code, result=result)
#     if result == "true":
#         led.turn_on_led()

@mqtt.subscribe("tg/+/state")
async def message_to_topic(client, topic, payload, qos, properties):
    data = json.loads(payload.decode())
    if "door" in data and data["door"] == "holding":
        common.set_operating_status("opened")
    
    if "sol2" in data and data["sol2"] == "off":
        led.turn_off_led()
        common.set_operating_status("done")

@mqtt.subscribe("tg/+/event")
async def message_to_topic(client, topic, payload, qos, properties):
    data = json.loads(payload.decode())
    common.set_count_max(data["qr_valid_count_max"])
    common.set_current_count(data["qr_valid_count"])
    mac = common.get_MACHINE_MAC()
    if mac:
        return
    common.set_MACHINE_MAC(data["MAC"])
    print("get mac address!")

    
@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "THE GREET"

@app.get("/QR_READ", response_class=PlainTextResponse)
def QR_READ():
    #print(os.getcwd())
    scan_in = subprocess.run(args=[sys.executable,'lite_fastapi_local/QR_READ_dep.py'], capture_output=True, text=True)
    # Working_Dir CHK : cwd / , cwd= 'D:\\python\DEP_SEC'
    scan_out = scan_in.stdout
    print('LINE:'+scan_out[:len(scan_out)-1])
    return scan_out[:len(scan_out)-1]

@app.get("/QR_CHK/{scan_in}")   #int 자료형 차후 Modeling
def QR_CHK(scan_in):
    print(scan_in)

    result = json.loads(CHKF.QR_CHK(scan_in=scan_in))
    return result

@app.get("/QR_END", response_class=PlainTextResponse)   #QR_READ 종료
def QR_END():
    print(os.getcwd())
    subprocess.run(args=[sys.executable,'lite_fastapi_local/QR_END_dep.py'], capture_output=True, text=True)        
    return 'QR_END'

@app.get("/update")
def update_server():
    subprocess.call([r"update.bat"])

@app.on_event("startup")
def startup_event():
    camera_inner_index = find_camera_index("HD Pro Webcam C920")
    common.set_camera_inner_index(camera_inner_index)
    
    camera_cctv_index = find_camera_index("USB Live camera")
    common.set_camera_cctv_index(camera_cctv_index)
        
        

@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 2)
def delete_old_log_file():
    # print("repeat!!")
    path = "Save_file"
    current_time = time.time()
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                # print(entry.name)
                directory = os.path.join(path, entry.name)
                if os.stat(directory).st_mtime < current_time - 3 * 86400:
                    shutil.rmtree(directory)

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)