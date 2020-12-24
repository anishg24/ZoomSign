import requests
import sys
from datetime import datetime

classes = ["AP Chemistry", "AP Economics", "AP Computer Science A", "Personal Finance", "AP Physics C", "ERWC", "Differential Equations"]

data = {
	"message": classes[int(sys.argv[1]) - 1],
	"timestamp": str(datetime.now()),
	"planned_length": str(2)
}

r = requests.post("http://192.168.1.126:5000/updates", json=data)
r.close()
