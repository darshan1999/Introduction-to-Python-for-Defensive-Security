#To enrich scan results, you can query public IP intelligence APIs.
#This is useful for determining whether an exposed IP belongs to a cloud provider, CDN, or suspicious entity.
#Using ipinfo.io API:

import requests

ip = "8.8.8.8"
response = requests.get(f"https://ipinfo.io/{ip}/json")

if response.status_code == 200:
    data = response.json()
    print("IP Info:")
    print(f" - City: {data.get('city')}")
    print(f" - Org: {data.get('org')}")
    print(f" - ASN: {data.get('asn', {}).get('asn', 'N/A')}")
