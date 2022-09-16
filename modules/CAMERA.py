import os
import datetime

class CAMERA:
    def __init__(self, output_dir_name):
        self.output_dir_name = output_dir_name
        try:
            os.mkdir(self.output_dir_name)
        except:
            pass

    def take_photo(self):
        output_photo_dir = self.output_dir_name + "/" + str(datetime.date.today())
        try:
            os.mkdir(output_photo_dir)
        except:
            pass

        ct = datetime.datetime.now()
        command = "libcamera-still --width 640 --height 640 -o " + output_photo_dir + "/" + str(ct.hour) + ":" + str(ct.minute)  + ":" + str(ct.second) + ".jpg"
        os.system(command)
