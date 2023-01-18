from __future__ import print_function
import myo


class Listener(myo.DeviceListener):

    def on_connected(self, event):
        print("Hello, '{}'! Double tap to exit.".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)
        event.device.request_battery_level()
        event.device.stream_emg(True)

    def on_battery_level(self, event):
        print("Your battery level is:", event.battery_level)
        

    def on_pose(self, event):
        if event.pose == myo.Pose.double_tap:
            return False
    
    def on_unpaired(self, event):
        return False  # Stop the hub

    def on_emg(self, event):
        print(event.emg)


if __name__ == '__main__':
    myo.init(sdk_path='D:\\4_KULIAH_S2\Semester 4\myo-project\myo-sdk-win-0.9.0')
    hub = myo.Hub()
    listener = Listener()
    while hub.run(listener.on_event, 500):
        pass
    print('Bye, bye!')
