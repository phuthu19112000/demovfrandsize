from logging import debug
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app",host="192.168.2.22",port=9000,reload=True,\
        debug=True,workers=8)