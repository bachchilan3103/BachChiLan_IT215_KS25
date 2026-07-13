from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("")
def get():
    return{
        "message": "API dang chay",
        "status": "succes"
    }

@app.get("/patients")
def get_list():
    return{
        "message": "Tra ve danh sach thanh cong",
        "status": "success",
        "data": "patient_db"
    }
        
@app.get("/patients/{patients_id}")
def get_patients():
    return{
        "message": "Lay benh nhan thanh cong",
        "status": "success",
        "data": "patient_db"
    }

@app.post("/patients")
def add_patients():
    return{
        "message": "Them benh nhan thanh cong",
        "status": "success",
        "data": "patient_db"
    }

@app.put("/patients/{patients_id}")
def add_patients():
    return{
        "message": "Cap nhat benh nhan thanh cong",
        "status": "success",
        "data": "patient_db"
    }

@app.delete("/patients/{patients_id}")
def delete_patients():
    return{
        "message": "Xoa benh nhan thanh cong",
        "status": "success",
        "data": "patient_db"
    }

