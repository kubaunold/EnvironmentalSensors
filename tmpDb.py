from databaseMS import Measurement, db
from datetime import datetime

db.create_all()
# print(Measurement.query.all()
print(Measurement.query.filter(Measurement.timestamp.startswith('2019')).first())

for i in range(2000, 2025):
    print(i)
    res = []
    res = Measurement.query.filter(Measurement.timestamp.startswith(i)).first()
    if(res != []):
        print("YES!")
    else:
        print("NO")