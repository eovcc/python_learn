import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())
            

def makmd():
    pass



if __name__ == "__main__":
    asyncio.run(main())