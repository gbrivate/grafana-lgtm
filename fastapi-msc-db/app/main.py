from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine, get_db

import logging


# Configure root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Utility CRUD Functions (Optional, but good practice) ---

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- FastAPI Endpoints ---

## ➕ Create an Item
@app.post("/items/", response_model=schemas.Item)
def create_an_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Creates a new item in the database."""
    logger.info("Created a new item in the database")
    return create_item(db=db, item=item)

## 📖 Read All Items
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieves a list of all items."""
    logger.info("Retrieves a list of all items")
    items = get_items(db, skip=skip, limit=limit)
    return items

## 🔍 Read a Single Item
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieves a single item by its ID."""
    logger.info("Retrieves a single item by its ID %s", item_id)
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning("Item not found %s", item_id)
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

## 🔄 Update an Item
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Updates an existing item by its ID."""
    logger.warning("Updates an existing item by its ID %s", item_id)
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields
    db_item.name = item.name
    db_item.description = item.description

    db.commit()
    db.refresh(db_item)
    return db_item

## 🗑️ Delete an Item
@app.delete("/items/{item_id}", status_code=204) # HTTP 204 No Content for successful deletion
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Deletes an item by its ID."""
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return