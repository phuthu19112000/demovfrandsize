import base64
import requests
import time

start_request = time.time()
result =  requests.get(url="http://192.168.50.69:5849/4990/trousers/5013/long_sleeve_top/4985")
print("Time is spend to get request: ", start_request-time.time())

start_request = time.time()
image = base64.b64decode(result.content)
print("Time is spend to decode image: ", start_request-time.time())


filename = 'image.png'
with open(filename, 'wb') as f:
    f.write(image)