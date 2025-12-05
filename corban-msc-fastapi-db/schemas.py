from pydantic import BaseModel

# Schema for creating/updating an Item (request body)
class ItemBase(BaseModel):
    name: str
    description: str | None = None

# Schema used for creating an Item (includes all fields from Base)
class ItemCreate(ItemBase):
    pass

# Schema for reading an Item (response body) - includes the 'id'
class Item(ItemBase):
    id: int

    class Config:
        # Pydantic's configuration for working with SQLAlchemy objects
        from_attributes = True