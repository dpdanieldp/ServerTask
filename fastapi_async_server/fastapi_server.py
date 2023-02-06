import os

from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

UPLOAD_DIR = "uploaded_files"

description = """
### This is example async FastAPI HTTP API 🚀
It can perform files upload/download
"""
app = FastAPI(
    title="Async server to upload/download files",
    description=description,
    version="0.0.1",
)


@app.get("/", tags=["Welcome"])
def welcome(request: Request):
    return {
        "service_info": app.openapi().get("info", ""),
        "documentation_swagger": str(request.url) + "docs",
        "documentation_redoc": str(request.url) + "redoc",
    }


@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = "uploaded_files/" + file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded"}


@app.get("/download/{file_name}")
async def download_file(file_name: str, response: FileResponse):
    file_path = "uploaded_files/" + file_name
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    headers = {"Content-Disposition": f'attachment; filename="{file_name}"'}
    return FileResponse(file_path, headers=headers)


def main():
    import uvicorn

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    uvicorn.run(app, host="localhost", port=8080)  # , reload=True


if __name__ == "__main__":
    main()
