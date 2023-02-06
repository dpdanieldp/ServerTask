import os

from aiohttp import web

UPLOAD_DIR = "uploaded_files"


async def handle_upload(request):
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == "file"
    filename = os.path.join(UPLOAD_DIR, field.filename)
    size = 0
    with open(filename, "wb") as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text=f'File "{field.filename}" was uploaded, size: {size}')


async def handle_download(request):
    file_path = os.path.join(UPLOAD_DIR, request.match_info["file_path"])
    try:
        with open(file_path, "rb") as f:
            return web.Response(body=f.read(), content_type="application/octet-stream")
    except FileNotFoundError:
        return web.HTTPNotFound(text=f'File "{file_path}" not found')


async def init_app():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app = web.Application()
    app.add_routes(
        [
            web.post("/upload", handle_upload),
            web.get("/download/{file_path}", handle_download),
        ]
    )
    return app


def main():
    app = init_app()
    web.run_app(app, host="localhost", port=8080)


if __name__ == "__main__":
    main()
