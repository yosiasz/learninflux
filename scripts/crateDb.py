# pip install crate
from crate import client

conn = client.connect("https://aquamarine-r2-d2.aks1.eastus2.azure.cratedb.net:4200", username="admin", password="Q9eI6Gx&fSxVE^C(p1G(_FZb", verify_ssl_cert=True)

with conn:
    cursor = conn.cursor()
    cursor.execute("select * from Berliner limit 100")
    result = cursor.fetchone()
    print(result)