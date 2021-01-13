# Tuya Bulb Control #

Tuya Bulb Control - API wrapper for you smart bulbs <a href="https://www.tuya.com" target="_blanck">**developed by Tuya**</a>

[![PyPi Versions](https://img.shields.io/pypi/v/tuya-bulb-control.svg)](https://pypi.org/project/tuya-bulb-control/)
[![Python versions](https://img.shields.io/pypi/pyversions/tuya_bulb_control.svg)](https://pypi.org/project/tuya-bulb-control/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)

---
## Installation
Install or upgrade tuya-bulb-control:
```
$ pip install tuya-bulb-control --upgrade
```
Or install source:
```
$ git clone https://github.com/Octoober/tuya-bulb-control.git
$ cd tuya-bulb-control
$ python setup.py install
```

Demo:
```Python
from tuya_bulb_control import Bulb

CLIENT_ID = ''
SECRET_KEY = ''
DEVICE_ID = ''
REGION_KEY = 'eu'


bulb = Bulb(client_id=CLIENT_ID, secret_key=SECRET_KEY, region_key=REGION_KEY, device_id=DEVICE_ID)

# Turn on the bulb
bulb.switch(status=True)

# Turn on colour mode
bulb.work_mode(mode='colour')

# Choosing color, saturation and brightness(value)
bulb.color(hue_color=260, saturation=50, value=50)
```

## Getting access to API
#### Step 1: CLIENT_ID and SECRET_KEY
- Register or Login on <a href="https://auth.tuya.com" target="_blanck">Tuya</a>.
1. Create a cloud development project <a href="https://iot.tuya.com/cloud" target="_blanck">Cloud -> Project</a>.
2. After successful creation, you will receive the **Client ID** and **Secret Key**.


#### Step 2: DEVICE_ID
1. Install **Tuya Smart** app or **Smart Life** app on your mobile phone.
2. Go to <a href="https://iot.tuya.com/cloud/appinfo/cappId/device" target="_blanck">Cloud -> Link Devices</a> page.
3. Selecting a tab **Link Devices by App Account**.
4. Click **Add App Account** and scan the QR code with **Tuya Smart** app or **Smart Life** app.
5. Now you can go to devices <a href="https://iot.tuya.com/cloud/appinfo/cappId/deviceList" target="_blanck">Cloud -> Device List</a> and copy **Device ID**.
    * Notes: Try to select a your region if devices are not displayed.


#### Step 3: Request access to API calls
Go to <a href="https://iot.tuya.com/cloud/appinfo/cappId/setting" target="_blanck">Cloud -> API Group</a> and enable **Authorization management**, **Device Management** and **Device Control**.

**Done!**