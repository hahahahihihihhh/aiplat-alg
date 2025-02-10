import asyncio
import websockets

async def log_generator(websocket, path):
    # 连接成功时
    print(f"New connection from {websocket.remote_address}")

    try:
        # 接收客户端训练开始命令
        async for message in websocket:
            print(f"Received message from client: {message}")
            if (message == "Start"):
                # 回复客户端确认消息
                print("----------")
                log_msg = "Trainning start"
                await websocket.send(log_msg)
                for _progress in range(0, 100 + 20, 20):
                    log_msg = f"Training progress: {_progress}%"
                    print(log_msg)  # 在服务器端打印日志
                    # 发送日志到 WebSocket 客户端 (Java 后端)
                    await websocket.send(log_msg)
                    await asyncio.sleep(2)
    except asyncio.CancelledError:
        print(f"Connection from {websocket.remote_address} closed.")


async def main():
    # 监听端口 5000 上的 WebSocket 服务
    async with websockets.serve(log_generator, "localhost", 5000):
        print("WebSocket server started at ws://localhost:5000")
        await asyncio.Future()  # 服务器持续运行直到手动停止


# 启动 WebSocket 服务器
asyncio.run(main())
