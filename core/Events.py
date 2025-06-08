from fastapi import FastAPI


def start_up(app: FastAPI):
    async def app_start():
        print("启动完毕！！")

    return app_start


def stopping(app: FastAPI):

    async def app_stop():
        print("程序停止！！")

    return app_stop
