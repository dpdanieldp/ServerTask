# import asyncio
import os
import unittest

import aiohttp

from threads_server import create_app

UPLOAD_DIR = "uploaded_files"


class TestFileServer(unittest.TestCase):
    async def setUp(self):
        self.app = create_app()
        self.client = await aiohttp.ClientSession().__aenter__()

    async def tearDown(self):
        await self.client.close()
        await self.app.shutdown()

    async def test_upload_file(self):
        file_name = "test_file.txt"
        file_content = b"this is a test file."

        async with self.client.post(
            "http://localhost:8080/upload", data={"file": (file_name, file_content)}
        ) as resp:
            self.assertEqual(resp.status, 201)
            self.assertTrue(os.path.exists(os.path.join(UPLOAD_DIR, file_name)))

    async def test_download_file(self):
        file_name = "test_file.txt"
        file_content = b"this is a test file."
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content)

        async with self.client.get(
            f"http://localhost:8080/download/{file_name}"
        ) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(await resp.read(), file_content)

    async def test_download_nonexistent_file(self):
        file_name = "nonexistent_file.txt"

        async with self.client.get(
            f"http://localhost:8080/download/{file_name}"
        ) as resp:
            self.assertEqual(resp.status, 404)
            self.assertEqual(await resp.text(), f"File {file_name} not found.")
