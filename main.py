from App.App import app
import uvicorn

from Users.user_db import create_user

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
