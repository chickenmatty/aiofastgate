import aiohttp
import urllib.parse
from datetime import datetime

from dataclasses import dataclass

from .exceptions import InvalidCredentials, LoginFailed

@dataclass
class FastGateDevice:
    mac: str
    ip: str
    network: str
    icon: str
    name: str
    boost: bool
    boost_remaining: str
    family: bool
    stop: bool
    stop_remaining: str
    type_of_connection: str
    

class FastGateApi:
    def __init__(self, base_url) -> None:
        self._cookie_jar = aiohttp.CookieJar(unsafe=True)
        self.session = aiohttp.ClientSession(cookie_jar=self._cookie_jar)
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
        }

    def _get_timestamp(self):
        dt = datetime.now()
        ts = datetime.timestamp(dt) 
        return int(ts)

    async def login(self, username: str, password: str):
        params = {
            "_": self._get_timestamp(),
            "cmd": 3,
            "nvget": "login_confirm",
            "password": password,
            "username": username
        }
        response = await self.session.get(self.base_url+"/status.cgi?"+urllib.parse.urlencode(params), headers=self.headers)

        if response.status != 200:
            raise LoginFailed("Login failed")
        data = await response.json(content_type="text/plain")
        if not data.get("login_confirm", False):
            raise LoginFailed("Login failed")
        if not (data["login_confirm"]["check_user"] == "1" and data["login_confirm"]["check_pwd"] == "1"):
            raise InvalidCredentials(data["login_confirm"]["check_user"], data["login_confirm"]["check_pwd"])

    async def get_devices(self):
        params = {
            "_": self._get_timestamp(),
            "nvget": "connected_device_list",
        }
        response = await self.session.get(self.base_url+"/status.cgi?"+urllib.parse.urlencode(params), headers=self.headers)
        if response.status != 200:
            raise LoginFailed("Failed to get devices")
        
        data = await response.json(content_type="text/plain")
        data = data["connected_device_list"]
        devices : list[FastGateDevice] = []

        for device in range(data["total_num"]):
            devices.append(FastGateDevice(
                data.get(f"dev_{device}_mac", ""),
                data.get(f"dev_{device}_ip", ""),
                data.get(f"dev_{device}_network", ""),
                data.get(f"dev_{device}_icon", ""),
                data.get(f"dev_{device}_name", ""),
                data.get(f"dev_{device}_boost", "") == "1",
                data.get(f"dev_{device}_boost_remaining", ""),
                data.get(f"dev_{device}_family", "") == "1",
                data.get(f"dev_{device}_stop", "") == "1",
                data.get(f"dev_{device}_stop_remaining", ""),
                data.get(f"dev_{device}_type_of_connection", "")
            ))
        return devices
    
    async def logout(self):
        self._cookie_jar.clear()

    async def close(self):
        await self.session.close()
