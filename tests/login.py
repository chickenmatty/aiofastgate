import src.aiofastgate as aiofastgate
import asyncio

async def main():
    fastgate = aiofastgate.FastGateApi("http://192.168.1.1")
    res = await fastgate.login("", "")
    print(res)
    dev = await fastgate.get_devices()
    print(dev)
    await fastgate.close()

if __name__ == "__main__":
    asyncio.run(main())
