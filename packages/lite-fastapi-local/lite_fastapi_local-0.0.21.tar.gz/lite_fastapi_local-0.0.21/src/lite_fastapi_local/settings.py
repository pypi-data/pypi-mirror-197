from fastapi_mqtt import FastMQTT, MQTTConfig
import logging, os, boto3



    
# mqtt 세팅
mqtt_config = MQTTConfig()

mqtt = FastMQTT(
    config=mqtt_config
)


# logger 세팅
class Logger:
    """
    커스텀 로거 클래스
    """
    def __init__(self, className, filePath=None):
        
        # 로거 이름
        self.className = className

        # 로그 파일 생성 경로
        if filePath is None:
            self.filePath = "./log/"
        else:
            self.filePath = filePath

        # 로그 파일 생성 경로 부재 시 생성
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

        
    def initLogger(self, filename):
        """
        로거 인스턴스 반환
        """
        # 로거 인스턴스 생성
        __logger = logging.getLogger(self.className)

        # 포매터 설정
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s]|%(filename)s:%(lineno)s] >> %(message)s"
        )
        #=====================================================
        # 핸들러 설정
        #=====================================================
        # 스트림 핸들러 정의
        streamHandler = logging.StreamHandler()
        
        # 파일 핸들러 정의
        fileHandler = logging.FileHandler(f'{self.filePath}{filename}.log')
        #=====================================================
        # 핸들러에 포매터 지정
        #=====================================================
        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # 로거 인스턴스에 핸들러 삽입
        __logger.addHandler(streamHandler)
        __logger.addHandler(fileHandler)

        # 로그 레벨 정의
        __logger.setLevel(logging.DEBUG)

        return __logger
    

# s3 이미지 저장
def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="AKIAYHFAYHVMQTJSSL43",
            aws_secret_access_key="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",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3
    
s3 = s3_connection()