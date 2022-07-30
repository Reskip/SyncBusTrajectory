from geopy.geocoders import Nominatim
import subprocess
import os
import zipfile


def coordinates_from_address(address):
    try:
        location = Nominatim(user_agent='changer').geocode(address)
        print("Location entered: " + location.address)
        return str(location.latitude) + ' ' + str(location.longitude)
    except:
        print('Cannot find address.')
        time.sleep(5)
        return None


def mount_image():
    cmd = 'ideviceinfo'
    version = [i for i in subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode(
        ).split('\n') if i.startswith('ProductVersion')][0].split(' ')[1][:4]
    print(version)
    cmd = 'ideviceimagemounter ' + os.getcwd() + '/' + version + \
        '/DeveloperDiskImage.dmg ' + os.getcwd() + '/' + version + \
        '/DeveloperDiskImage.dmg.signature'
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print('Developer Disk Image mounted!')
        return True
    except Exception as e:
        if 'Device is locked' in e.output.decode() or 'Could not start' in e.output.decode():
            print('Please unlock your device and try again.')
        print(e)
        return False


def set_location(coordinates):
    try:
        cmd = 'idevicesetlocation -- ' + coordinates
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print('Device location set to ' + coordinates + '.')
    except Exception as e:
        if 'Device is locked' in e.output.decode():
            print('Please unlock your device and try again.')
            time.sleep(5)
        elif 'No device found' in e.output.decode():
            print('Please connect your device.')
            time.sleep(5)
        elif 'Make sure a developer disk image is mounted!' in e.output.decode():
            print('error')