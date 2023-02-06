# ServerTask

This is my solution to the task of creating three HTTP servers using asyncio, threading and
multiprocessing in Python.
Each of these servers is to handle download and upload requests.

As a bonus, I added an async server in `fastapi` to compare its performance with other servers.

In the `timing` folder, there is a program that allows you to compare the speed of the two servers in the operation of downloading the file stress_test.txt n times.


Install dependencies before starting the servers:
```bash
pip install -r requirements.txt
```