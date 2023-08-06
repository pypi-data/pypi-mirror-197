class Common():
    def __init__(self):
        self.currnet_device_data = {}
        self.MACHINE_MAC = ''
        self.is_cctv_stop = False
        self.count_max = 0
        self.current_count = 0
        self.operating_status = "wait"
        self.file_path = str()
        self.person_count = 0
        self.camera_inner_index = -1
        self.camera_cctv_index = -1

    def get_current_device_data(self):
        return self.current_device_data
    
    def set_current_device_data(self, data):
        self.current_device_data = data

    def get_MACHINE_MAC(self):
        return self.MACHINE_MAC
    
    def set_MACHINE_MAC(self, mac):
        self.MACHINE_MAC = mac

    def get_is_cctv_stop(self):
        return self.is_cctv_stop
    
    def set_is_cctv_stop(self, bool):
        self.is_cctv_stop = bool
    
    def get_count_max(self):
        return self.count_max
    
    def set_count_max(self, count_max):
        self.count_max = count_max
    
    def get_current_count(self):
        return self.current_count
    
    def set_current_count(self, current_count):
        self.current_count = current_count

    def get_operating_status(self):
        return self.operating_status
    
    def set_operating_status(self, status):
        self.operating_status = status

    def get_file_path(self):
        return self.file_path
    
    def set_file_path(self, path):
        self.file_path = path

    def get_person_count(self):
        return self.person_count

    def set_person_count(self, count):
        self.person_count = count

    def get_camera_inner_index(self):
        return self.camera_inner_index

    def set_camera_inner_index(self, index):
        self.camera_inner_index = index
        
    def get_camera_cctv_index(self):
        return self.camera_cctv_index

    def set_camera_cctv_index(self, index):
        self.camera_cctv_index = index

common = Common()