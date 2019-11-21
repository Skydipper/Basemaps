# Basemaps

Basemap microservice that serves pre-calculated and dynamic tiles.

## To Run with Docker

You will need Control Tower running.

```bash
./basemaps.sh develop
```

## Example of use

You can use this servce to access `/<year>/<z>/<x>/<y>` slippy map tiles. Here is an example of downloading
a single tile from 2016.

```
import requests
url = "http://localhost:4502/api/v1/basemaps/landsat/2016/14/8473/7643"
r = requests.get(url)

print(r.status_code)
with open('./image_test.jpg', 'wb') as handler:
    handler.write(r.content)
```

This would be consumed by a web-map client as an x/y/z type endpoint via `https://api.skydipper.com/v1/basemaps/landsat/<year>/<x>/<y>/<z>`

