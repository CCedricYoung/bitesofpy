from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# normally would load from env
SECRET_KEY = (
    "963456d8424a9e506d82d1947774c56a2fa3cf1099315cd93e07f44dc5eea21a"  # noqa S105
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
food_log: Dict[int, FoodEntry] = {}

# We created an extra in memory user DB
users_db: Dict[str, User] = {}


def verify_password(plain_password, hashed_password):
    """Provided, all good"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Provided, all good"""
    return pwd_context.hash(password)


def get_user(username: str):
    """Provided, all good"""
    if username in users_db:
        user = users_db[username]
        return user


def authenticate_user(username: str, password: str):
    """
    TODO: complete this function, use:
    https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """


def create_access_token(data: dict, expires_delta: timedelta):
    """TODO: complete this function"""


def get_current_user(token: str = Depends(oauth2_scheme)):
    """TODO: complete this function"""


@app.post("/create_user", status_code=201)
async def create_user(user: User):
    """Ignore / don't touch this endpoint, the tests will use it"""
    users_db[user.username] = user
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """TODO: complete this endpoint"""


# TODO: use fastapi.Depends (already imported) to add authentication tot the following endpoints ...


@app.post("/", status_code=201)
async def create_food_entry(entry: FoodEntry):
    food_log[entry.id] = entry
    return entry


@app.get("/", response_model=List[FoodEntry])
async def get_foods_for_user():
    """
    This endpoint does not take a user_id anymore, make it so that the
    food entries are filtered on logged in user.
    """
    return [
        food_entry
        for food_entry in food_log.values()
        # filter by logged in user
    ]


@app.put("/{entry_id}", response_model=FoodEntry)
async def update_food_entry(entry_id: int, new_entry: FoodEntry):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")

    food_log[entry_id] = new_entry

    return new_entry


@app.delete("/{entry_id}", response_model=Dict[str, bool])
async def delete_food_entry(entry_id: int):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")

    del food_log[entry_id]

    return {"ok": True}