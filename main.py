from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import create_todo , get_todo , update_todo , delete_todo
from models import Base
from database import SessionLocal, engine
Base.metadata.create_all(bind=engine)

from schemas import CreateTodo
app = FastAPI()


# Dependency 
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@app.post("/todo", response_model=CreateTodo)
def create_todo(todo:CreateTodo,db:Session=Depends(get_db)):
    db_todo = create_todo(db,todo=todo)
    return db_todo

@app.get("/todoget", response_model=list[CreateTodo])
def read_Todo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    Todo = get_todo(db, skip=skip, limit=limit)
    return Todo



# Update a TODO item
@app.put("/todos/{todo_id}", response_model=CreateTodo)
def update_todo(todo_id: int, todo_update: CreateTodo, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id=todo_id, todo_update=todo_update)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="TODO item not found")
    return db_todo

# Delete a TODO item
@app.delete("/todos/{todo_id}", response_model=CreateTodo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="TODO item not found")
    return db_todo


