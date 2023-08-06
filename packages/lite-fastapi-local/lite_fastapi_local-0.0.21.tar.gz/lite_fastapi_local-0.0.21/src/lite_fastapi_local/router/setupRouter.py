from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from lite_fastapi_local.common.variable import common

from lite_fastapi_local.model.setupModel import setup
from lite_fastapi_local.schema.setupSchema import Volume, MotorMovement, CountMax, CountSet, DoorOpenPower, DoorHoldingPower

router = APIRouter(
    prefix="/setup",
    tags=["setups"],
    responses={404: {"description": "Not found"}}
)

@router.post('/volume')
def change_volume(volume: Volume):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_volume(**volume.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post('/motor_movement')
def change_motor_movement(motor_mevement: MotorMovement):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_motor_movement(**motor_mevement.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post('/count_max')
def change_count_max(count_max: CountMax):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_count_max(**count_max.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post('/count_set')
def change_count_set(count_set: CountSet):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_count_set(**count_set.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post('/door_holding_pwm')
def change_door_holding_pwm(door_holding_pwm: DoorHoldingPower):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_door_holding_pwm(**door_holding_pwm.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.post('/door_open_pwm')
def change_door_open_pwm(door_open_pwm: DoorOpenPower):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_door_open_pwm(**door_open_pwm.dict())
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)
