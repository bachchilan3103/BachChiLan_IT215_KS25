from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {"id": 1, "room_id": 1, "class_name": "Python Basic", "student_count": 25, "date": "2026-07-01", "slot": "MORNING"}
]

class Room(BaseModel):
    code: str
    name: str
    capacity: int
    status: str

class RoomBooking(BaseModel):
    room_id: int
    class_name: str
    student_count: int
    date: str
    slot: str

@app.get("/rooms")
def list_rooms():
    return rooms

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        raise HTTPException(404, "Room not found")
    return room

@app.post("/rooms")
def create_room(room: Room):
    if any(r["code"] == room.code for r in rooms):
        raise HTTPException(400, "Room code already exists")
    new_id = max(r["id"] for r in rooms) + 1 if rooms else 1
    new_room = {"id": new_id, **room.dict()}
    rooms.append(new_room)
    return new_room

@app.put("/rooms/{room_id}")
def update_room(room_id: int, room: Room):
    for r in rooms:
        if r["id"] == room_id:
            r.update(room.dict())
            return r
    raise HTTPException(404, "Room not found")

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for r in rooms:
        if r["id"] == room_id:
            rooms.remove(r)
            return {"message": "Room deleted"}
    raise HTTPException(404, "Room not found")

@app.get("/room-bookings")
def list_bookings():
    return room_bookings

@app.post("/room-bookings")
def create_booking(booking: RoomBooking):
    room = next((r for r in rooms if r["id"] == booking.room_id), None)
    if not room:
        raise HTTPException(400, "Room not found")
    if room["status"] != "AVAILABLE":
        raise HTTPException(400, "Room not available")
    if booking.student_count <= 0 or booking.student_count > room["capacity"]:
        raise HTTPException(400, "Invalid student count")
    if booking.slot not in ["MORNING", "AFTERNOON", "EVENING"]:
        raise HTTPException(400, "Invalid slot")
    if any(b["room_id"] == booking.room_id and b["date"] == booking.date and b["slot"] == booking.slot for b in room_bookings):
        raise HTTPException(400, "Room already booked for this date and slot")

    new_id = max(b["id"] for b in room_bookings) + 1 if room_bookings else 1
    new_booking = {"id": new_id, **booking.dict()}
    room_bookings.append(new_booking)
    return new_booking
