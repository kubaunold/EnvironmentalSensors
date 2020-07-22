from databaseMS import db
from databaseMS import Measurement
db.create_all()
Measurement.query.all()
exit()