from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session
import schemas
import models
from database import SessionLocal,Base,engine

app=FastAPI()
# Creating database
Base.metadata.create_all(engine)


def get_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
def get_item(id:int,session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.post('/')
def create_new_item(item:schemas.Item,session: Session = Depends(get_session)):
    item=models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.put("/{id}")
def update_data(id:int,item:schemas.Item,session: Session = Depends(get_session)):
    item_object=session.query(models.Item).get(id)
    item_object.task=item.task
    session.commit()
    return item_object


@app.delete("/{id}")
def delete_data(id:int,session: Session = Depends(get_session)):
    item=session.query(models.Item).get(id)
    session.delete(item)
    session.commit()
    return "The item was deleted!"
