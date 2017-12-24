import asyncio
import coinwraps


async def main():
    await coinwraps.init()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())