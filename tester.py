from time import sleep
from requests import get
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

for x in range(30):
    req = get(url="http://localhost:5000/weight")
    print(req.status_code)
    pp.pprint(req.text)
    sleep(1)
