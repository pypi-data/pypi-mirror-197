import asyncio, threading
from datetime import datetime

from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.common.function import capture_image, save_cctv, create_directory

from lite_fastapi_local.model.motorModel import motor
from lite_fastapi_local.model.ledModel import led
from lite_fastapi_local.model.setupModel import setup
from lite_fastapi_local.model.sprayModel import spray
from lite_fastapi_local.model.boxDoorModel import box_door

from lite_fastapi_local.schema.qrSchema import QrCode

router = APIRouter(
    prefix="/motor",
    tags=["motors"],
    responses={404: {"description": "Not found"}}
)

@router.post("/door")
async def move_door(qr_code: QrCode, background_tasks: BackgroundTasks):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    current_count = common.get_current_count()
    count_max = common.get_count_max()
    # if count_max == current_count:
    #     content = {
    #         "code_number": 23,
    #         "code_name": "unacceptable",
    #     }
    #     return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=content)
    common.set_current_count(current_count + 1)
    setup.change_count_set(current_count + 1)
    datetime_string = datetime.now().strftime("%d-%m-%Y")
    common.set_file_path(datetime_string)
    create_directory(f"Save_file/{datetime_string}/product")
    create_directory(f"Save_file/{datetime_string}/box")
    create_directory(f"Save_file/{datetime_string}/cctv")
    operating_status = common.get_operating_status()
    if operating_status == "wait":
        common.set_operating_status("in_progress")
        capture_image_thread = threading.Thread(target=capture_image)
        save_image_thread = threading.Thread(target=save_cctv)
        capture_image_thread.start()
        save_image_thread.start()
        
        # asyncio.create_task(capture_image())
        # asyncio.create_task(save_cctv())
        # background_tasks.add_task(
        #     capture_image
        # )
        # background_tasks.add_task(
        #     save_cctv
        # )
    motor.open_door_force()
    content = {
        "code_number": 11,
        "code_name": "accepted",
        "qr_code": qr_code.qr_code
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post("/boxdoor/{power}")
def move_boxdoor(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        box_door.open_box_door()
    elif power == 'off':
        box_door.close_box_door()
    content = {
        "code_number": 11,
        "code_name": "accepted"
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post("/led/{power}")
def turn_led(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        led.turn_on_led()
    elif power == 'off':
        led.turn_off_led()
    content = {
        "code_number": 11,
        "code_name": "accepted",
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post("/spray/{power}")
def turn_spray(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        spray.turn_on_spray()
    elif power == 'off':
        spray.turn_off_spray()
    content = {
        "code_number": 11,
        "code_name": "accepted",
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)
    