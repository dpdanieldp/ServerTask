import asyncio
from datetime import datetime

import aiohttp
import click


async def download_file(url, session):
    async with session.get(url) as response:
        data = await response.read()
        print(f"Finished downloading file, size: {len(data)}")


async def main(url, n):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(download_file(url, session)) for _ in range(n)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # change one of the servers port to 8081
    # and make sure that stress_test.txt is present in uploaded_files folder in directory of tested servers

    n = 100
    start = datetime.now()
    asyncio.run(main("http://localhost:8080/download/stress_test.txt", n))
    click.secho(f"{datetime.now() - start}", bold=True, bg="blue", fg="white")

    start = datetime.now()
    asyncio.run(main("http://localhost:8081/download/stress_test.txt", n))
    click.secho(f"{datetime.now() - start}", bold=True, bg="blue", fg="white")
