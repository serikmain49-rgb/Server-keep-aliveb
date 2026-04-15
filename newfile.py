import asyncio
import websockets
import os

# Список всех подключенных пользователей
clients = set()

async def handle_client(websocket):
    # Добавляем нового клиента в список
    clients.add(websocket)
    print("Новое подключение!")
    try:
        async for message in websocket:
            # Рассылаем сообщение всем, кроме отправителя
            # Создаем список задач для рассылки
            if clients:
                await asyncio.wait([client.send(message) for client in clients if client != websocket])
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Удаляем клиента при отключении
        clients.remove(websocket)
        print("Клиент отключился")

async def main():
    # На Render порт выдается через переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    
    # Запускаем сервер на 0.0.0.0, чтобы он был доступен извне
    async with websockets.serve(handle_client, "0.0.0.0", port):
        print(f"Сервер запущен на порту {port}...")
        await asyncio.Future()  # Это заставляет сервер работать вечно

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен")
