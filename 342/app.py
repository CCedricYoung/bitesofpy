from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# We'll export authentication further in a later Bite
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class Food(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: float = 0


class User(BaseModel):
    id: int
    username: str
    password: str

    def __init__(self, **data: Any):
        data["password"] = get_password_hash(data["password"])
        super().__init__(**data)


class FoodEntry(BaseModel):
    id: int
    user: User
    food: Food
    date_added: datetime = datetime.now()
    number_servings: float

    @property
    def total_calories(self):
        return self.food.kcal_per_serving * self.number_servings


app = FastAPI()
food_log: Dict[int, FoodEntry] = {}


@app.post("/")
def add_food(food_entry: FoodEntry):
    food_log[food_entry.id] = food_entry
    return food_entry


@app.get("/users/{user_id}")
def get_food_log_user(user_id: int):
    return [x for x in food_log.values() if x.user.id == user_id]


@app.put("/{entry_id}")
def update_food_entry(entry_id: int, food_entry: FoodEntry):
    if entry_id not in food_log:
        raise HTTPException(404, detail="Food entry not found")
    food_log[entry_id] = food_entry
    return food_entry


@app.delete("/{entry_id}")
def delete_food_entry(entry_id: int):
    if entry_id not in food_log:
        raise HTTPException(404, detail="Food entry not found")
    del food_log[entry_id]
    return {"ok": True}