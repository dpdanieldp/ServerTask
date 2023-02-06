import io
import os

from fastapi.testclient import TestClient

from fastapi_server import app

client = TestClient(app)


def test_upload_file():
    file = io.BytesIO(b"Test Content")
    response = client.post(
        "http://localhost:8080/upload", files={"file": ("test.txt", file)}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded"}
    assert os.path.isfile("uploaded_files/test.txt")
    if os.path.exists("uploaded_files/test.txt"):
        os.remove("uploaded_files/test.txt")


def test_download_file():
    file_name = "test_download.txt"
    file_content = "This is a test file to download."
    with open("uploaded_files/" + file_name, "w") as file:
        file.write(file_content)

    response = client.get(f"/download/{file_name}")
    assert response.status_code == 200
    assert response.content == file_content.encode()
    assert (
        response.headers["Content-Disposition"] == f'attachment; filename="{file_name}"'
    )

    os.remove("uploaded_files/" + file_name)


def test_download_file_not_found():
    response = client.get("/download/not_found.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}
