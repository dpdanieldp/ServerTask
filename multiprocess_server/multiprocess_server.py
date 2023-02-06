import multiprocessing
import os

from aiohttp import web

UPLOAD_DIR = "uploaded_files"


def upload_process(field, filename):
    size = 0
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        while True:
            chunk = field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return size


async def handle_upload(request):
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == "file"
    filename = field.filename

    size = 0
    with multiprocessing.Pool() as pool:
        size = pool.apply_async(upload_process, args=(field, filename)).get()

    return web.Response(text=f'File "{filename}" was uploaded, size: {size}')


def download_process(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


async def handle_download(request):
    file_name = request.match_info["file_path"]
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with multiprocessing.Pool() as pool:
        data = pool.apply_async(download_process, args=(file_path,)).get()

    if data is None:
        return web.HTTPNotFound(text=f'File "{file_name}" not found')

    return web.Response(body=data, content_type="application/octet-stream")


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
