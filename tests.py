import tattlnk.utils.database as tud
conn = tud.DBAdapter.factory()
data = conn.dql("SELECT RANDOM()", ())

for d in data:
    print(d)
