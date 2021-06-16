from logging import debug
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app",host="127.0.0.1",port=9000,reload=True,\
        debug=True,workers=8)