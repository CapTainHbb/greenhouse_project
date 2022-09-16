import glob
import os

class COMVIS:
    def __init__(self, output_photo_dir_name):
        self.output_photo_dir_name = output_photo_dir_name
        self.grow_stage = 1
    def get_plant_grow_stage(self):
        latest_photo_dir = get_latest_photo()
        cmd = "python3 /home/captainhb/yolov5/detect.py python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source "
        cmd += latest_photo_dir
        os.system(cmd)

        with open("/home/captainhb/yolov5/runs/detect/latest_photo.csv", "r") as file:
            self.grow_stage = file.read(1) # read first charachter with determines grow stage

        return grow_stage

    def get_latest_photo(self):
        """
        this function returns latest photo taken by camera module in
        output_photo_dir_name directory
        """
        newest_directory = max(glob.glob(os.path.join(self.output_photo_dir_name, '*/')), key=os.path.getmtime)
        list_of_files = glob.glob(newest_directory + "/*")
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    