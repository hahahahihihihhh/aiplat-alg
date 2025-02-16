import asyncio
import json
import threading
import websockets

# 模拟训练任务
def train_model(taskMsg, msg_callback, loop):
    reply = {'userId': taskMsg.get('userId', None), 'taskId': taskMsg.get('taskId', None), 'msg': "开始训练"}
    msg_callback(reply, loop)   # 训练开始
    asyncio.run(asyncio.sleep(2))
    for progress in range(20, 100 + 20 , 20):
        reply['msg'] = f"Training progress: {progress}%"
        msg_callback(reply, loop)
        asyncio.run(asyncio.sleep(2))  # 模拟训练过程
    reply['msg'] = "训练完成"
    msg_callback(reply, loop)  # 训练结束

async def handle_client(websocket):
    print(f"New connection from {websocket.remote_address}")
    async for message in websocket:
        print(f"Received message from client: {message}")
        try:
            taskMsg = json.loads(message)
            if (taskMsg.get("msg") == "开始训练"):
                # 定义进度回调函数
                def msg_callback(reply, loop):
                    print("Send message to client: ", reply)
                    asyncio.run_coroutine_threadsafe(
                        websocket.send(str(reply)),
                        loop
                    )
                # 启动新线程处理训练任务
                train_thread = threading.Thread(
                    target=train_model,
                    args=(taskMsg, msg_callback, asyncio.get_event_loop())
                )
                train_thread.start()
        except json.JSONDecodeError:
            await websocket.send("Invalid JSON format")
        except Exception as e:
            await websocket.send(f"Error: {str(e)}")

# 启动 WebSocket 服务器
start_server = websockets.serve(handle_client, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()