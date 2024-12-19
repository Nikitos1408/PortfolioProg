from datetime import datetime, timedelta
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

JWT_SECRET = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {
    "user1": dict(username="user1", password="password1", spending=5000.0),
    "user2": dict(username="user2", password="password2", spending=15000.0),
}

bonus_levels = [
    dict(level="Silver", min_spending=0, cashback=0.01),
    dict(level="Gold", min_spending=10000, cashback=0.02),
    dict(level="Platinum", min_spending=20000, cashback=0.03),
]

class User(BaseModel):
    username: str
    password: str
    spending: float

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    return jwt.encode({**data, "exp": expire}, JWT_SECRET, algorithm=ALGORITHM)

@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token({"sub": user["username"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or not (user := users_db.get(username)):
           raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})


@app.get("/bonus", response_model=dict)
async def read_bonus_data(current_user: User = Depends(get_current_user)):
    spending = current_user.spending
    sorted_levels = sorted(bonus_levels, key=lambda x: x["min_spending"])
    current_level = next((l for l in reversed(sorted_levels) if spending >= l["min_spending"]), None)
    next_level = next((l for l in sorted_levels if spending < l["min_spending"]), "No higher level")
    return {"current_level": current_level, "next_level": next_level}