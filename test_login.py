from src import aiofastgate
import asyncio
import yarl

async def main():
    fastgate = aiofastgate.FastGateApi("192.168.1.1", "http", "", "")

    while True:
        print(fastgate._cookie_jar.filter_cookies(yarl.URL("http://192.168.1.1")))
        await fastgate.login()
        devices = await fastgate.get_devices()
        print(devices)
asyncio.run(main())
