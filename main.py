from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import logging 
from typing import Dict 

logging.basicConfig(
    level=logging.INFO,  # Level log (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s" 
)
logger = logging.getLogger(__name__)  

app = FastAPI()


class UserInfo(BaseModel):
    name: str
    email: str
    data: str = ""
    
# Mock db
mock_db: Dict[str, UserInfo] = {}

@app.post("/user")
def update_user_data(request: UserInfo):
    # Update user data in the mock database.    
    if request.email not in mock_db:
        mock_db[request.email] = request
        return {"message": "User created successfully."}

    user = mock_db[request.email]
    logger.info(f"Updating user data for {user.data }.")
    user.data += f". {request.data}"

    return {"message": "User data updated successfully."}
    
@app.get("/user")
def get_user_data(email: str = Query):
    if email not in mock_db:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user = mock_db[email]
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)