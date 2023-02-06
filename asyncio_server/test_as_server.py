import os

import aiohttp
from aiohttp.test_utils import AioHTTPTestCase

from as_server import init_app

UPLOAD_DIR = "uploaded_files"


class FileServerTestCase(AioHTTPTestCase):
    async def get_application(self):
        return await init_app()

    async def test_upload_file(self):
        file_content = b"Test file content"
        file_name = "test_file.txt"
        form = aiohttp.FormData()
        form.add_field("file", file_content, filename=file_name)
        async with self.client.post("/upload", data=form) as resp:
            self.assertEqual(resp.status, 200)
            uploaded_file_path = os.path.join(UPLOAD_DIR, file_name)
            self.assertTrue(os.path.exists(uploaded_file_path))
            with open(uploaded_file_path, "rb") as f:
                self.assertEqual(f.read(), file_content)
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

    async def test_download_file(self):
        file_content = b"Test file content"
        file_name = "test_file.txt"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content)

        async with self.client.get(f"/download/{file_name}") as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(await resp.read(), file_content)
        if os.path.exists(file_path):
            os.remove(file_path)

    async def test_download_file_not_found(self):
        async with self.client.get("/download/not_existing_file.txt") as resp:
            self.assertEqual(resp.status, 404)
            self.assertIn(
                b'File "uploaded_files/not_existing_file.txt" not found',
                await resp.read(),
            )
