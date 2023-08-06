import cv2, os, time, boto3, json
import numpy as np

from datetime import datetime
from pygrabber.dshow_graph import FilterGraph
from skimage.metrics import structural_similarity as ssim 

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import s3
        
def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def find_camera_index(name: str):
    devices = FilterGraph().get_input_devices()
    
    try:
        device_index = devices.index(name)
    except ValueError:
        device_index = -1
        
    return device_index

def save_cctv():
    
    camera_cctv_index = common.get_camera_cctv_index()
    cctv_cap = cv2.VideoCapture(camera_cctv_index, cv2.CAP_DSHOW)
    cctv_cap.set(cv2.CAP_PROP_POS_FRAMES, 15)

    frame_width = int(cctv_cap.get(3))
    frame_height = int(cctv_cap.get(4))
    
    file_path = common.get_file_path()
    size = (frame_width, frame_height)
    result = cv2.VideoWriter(f'./Save_file/{file_path}/cctv/up_cctv_{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.avi', 
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            30, size)
    print("cctv start!!")
    while True:
        # 프레임 읽기
        ret, frame = cctv_cap.read()

        # 프레임이 제대로 읽혔는지 확인
        if not ret:
            print("Error: failed to capture frame")
            break
        result.write(frame)

        operating_status = common.get_operating_status()
        if operating_status =="done":
            print("cctv end!!")
            break

    # 작업 완료 후, 리소스 반환
    cctv_cap.release()
    cv2.destroyAllWindows()

def capture_image():
    RESIZE_IMG = 256  #클수록 제외되는 가장자리 면적 증가 recommend:256
    is_first  = True
    up_score = 0
    delay = 10
    is_send = False
    camera_inner_index = common.get_camera_inner_index()
    up_cap = cv2.VideoCapture(camera_inner_index, cv2.CAP_DSHOW)
    # for i in range(10):
    #     up_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    #     if up_cap.isOpened():
    #         break
    person_count = common.get_person_count()
    mac = common.get_MACHINE_MAC()
    while True:
        up_ret, up_frame = up_cap.read()
        if up_ret == False:
            break

        ### pre-process ###
        up_image = cv2.resize(up_frame, dsize=(RESIZE_IMG,RESIZE_IMG)) 

        operating_status = common.get_operating_status()
        if is_first == True:

            i = 0
            bf_up =  cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)
            closed_image = cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)
            is_first = False
            print("start!!")
        else:            
            if operating_status == "opened":
                (up_score, up_diff) = ssim(cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY), closed_image, full=True)
                if up_score > 0.95:
                    data = {
                        "mac": mac
                    }
                    trigger_lambda("lite_collection_box_did_not_open", data)
                    up_filename = f'/Save_file/up_img_did_not_open_{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.jpg'
                    cv2.imwrite(up_filename,up_frame)
                    upload_image_to_s3(mac, up_filename, "lite-image-storage-bucket")
                    
                common.set_operating_status("wait")
            (up_score, up_diff) = ssim(cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY), bf_up, full=True)
            bf_up =  cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)            
            if (up_score)<0.9:
                i +=1
            else:
                i = 0
            if i>3:
                if is_send == False:
                    #store image 
                    file_path = common.get_file_path()
                    up_filename = f'./Save_file/{file_path}/product/up_img_{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.jpg'
                    cv2.imwrite(up_filename,up_frame)

                    #s3에 이미지 저장
                    upload_image_to_s3(mac, up_filename, "lite-image-storage-bucket")
                    i = 0
                    delay = 70
                    is_send = True
                else:
                    i = 0
            if delay<0:
                is_send =False
            else:
                delay-=1
                i = 0
        operating_status = common.get_operating_status()
        if operating_status =="done":
            print("end!!")
            person_count = common.get_person_count()
            if person_count % 10 == 0:
                #store image 
                file_path = common.get_file_path()
                if person_count == 0:
                    up_filename = f'./Save_file/up_img_base.jpg'
                else:
                    up_filename = f'./Save_file/{file_path}/box/up_img_{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.jpg'
                cv2.imwrite(up_filename,up_frame)

                upload_image_to_s3(mac, up_filename, "lite-image-storage-bucket")

            common.set_person_count(person_count + 1)
            common.set_operating_status("wait")
            break
    up_cap.release()                    
    cv2.destroyAllWindows()   
    
# aws
def upload_image_to_s3(mac: str, captured_image_name: str, bucket: str):
    try:
        filename = captured_image_name.split("Save_file")[1]
        s3.upload_file(captured_image_name, bucket, f"{mac}{filename}")
        s3.upload_file(captured_image_name,"lite-image-storage-bucket",f"{mac}{filename}")
    except Exception as e:
        print(e)
        
def trigger_lambda(lambda_name: str, data: dict={}):
    lambda_client = boto3.client(
            'lambda',
            region_name='ap-northeast-2',
            aws_access_key_id='AKIAYHFAYHVMQTJSSL43',
            aws_secret_access_key='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'
        )

    lambda_client.invoke(
        FunctionName=lambda_name,
        InvocationType='Event',
        Payload=json.dumps(data)
    ) 