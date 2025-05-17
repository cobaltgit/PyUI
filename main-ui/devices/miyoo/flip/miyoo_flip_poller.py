
import time
from devices.device import Device
from devices.utils.process_runner import ProcessRunner


class MiyooFlipPoller:
    def __init__(self):
        self.headphone_status = None
        
    def check_audio(self):
        try:
            new_headphone_status = Device.are_headphones_plugged_in()
            if(new_headphone_status != self.headphone_status):
                self.headphone_status = new_headphone_status
                if(self.headphone_status):
                    ProcessRunner.run(["amixer","sset","Playback Path","HP"])
                else:
                    ProcessRunner.run(["amixer","sset","Playback Path","SPK"])
        except:
            pass

    def continuously_monitor(self):
        while(True):
            self.check_audio()
            time.sleep(1)  # Sleep for 1 second
