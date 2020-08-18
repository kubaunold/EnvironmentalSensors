from databaseMS import Measurement, db
from datetime import datetime

db.create_all()
# print(Measurement.query.all()
# print(Measurement.query.filter(Measurement.timestamp.startswith(str(2020))).first())

result = []
""""In fact it's more like [2010,2020)"""
for i in range(2015, 2025):
    print(i)
    currentYearResponse = Measurement.query.filter(Measurement.timestamp.startswith(str(i))).first()
    # print(currentYearResponse)
    # print("-"*10)
    if currentYearResponse != None:
        result+=[i]

print(f"Years occuring in db: {result}")

a = Measurement.query.order_by(Measurement.timestamp.asc()).first().timestamp.year
print(f"First/last measurement: {a}")
# print(a.timestamp.year)