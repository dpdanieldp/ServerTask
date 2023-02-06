import os
from concurrent.futures import ThreadPoolExecutor

from aiohttp import web

UPLOAD_DIR = "uploaded_files"


async def handle_upload(request):
    file = await request.post()["file"]
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        while True:
            chunk = await file.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    return web.HTTPCreated(text=f"File {file.filename} was uploaded.")


async def handle_download(request):
    file_name = request.match_info["file_name"]
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        raise web.HTTPNotFound(text=f"File {file_name} not found.")
    return web.FileResponse(
        file_path,
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(
        [
            web.post("/upload", handle_upload),
            web.get("/download/{file_name}", handle_download),
        ]
    )
    app["executor"] = ThreadPoolExecutor()
    return app


def main():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app = create_app()
    web.run_app(app, host="localhost", port=8080)


if __name__ == "__main__":
    main()
