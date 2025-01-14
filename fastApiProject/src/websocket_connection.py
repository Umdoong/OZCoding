from typing import TypedDict

from fastapi import WebSocket


class ConnectionManager:
	def __init__(self):
		self.active_connections: dict[int, list] = {}

	async def connect(self, connection: WebSocket, room_id: int):
		await connection.accept()

		room_connections: list[WebSocket] = self.active_connections.get(room_id, [])  # chat_room_id가 없으면 빈 리스트 할당
		room_connections.append(connection)
		self.active_connections[room_id] = room_connections
		# ex) {1: [ws1], [ws2]}

	async def broadcast(self, connection: WebSocket, room_id: int, massage: str) -> None:
		for room_conn in self.active_connections[room_id]:
			if room_conn == connection:
				await room_conn.send_text(f"<Me> {massage}")
			else:
				await room_conn.send_text(f"<Friend> {massage}")

	def disconnect(self, connection: WebSocket, room_id: int) -> None:
		room_connections = self.active_connections[room_id]
		room_connections.remove(connection)