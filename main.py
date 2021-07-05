from logging import debug
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app",host="192.168.50.66",port=3000,reload=True,\
        debug=True)