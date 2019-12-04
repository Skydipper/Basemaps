# Basemaps

Basemap microservice that serves pre-calculated and dynamic tiles.

## To Run with Docker

You will need Control Tower running.

```bash
./basemaps.sh develop
```

## Example of use

### Satellite Basemaps

You can use this servce to access our pre-built satellite basemaps, as slippy map tiles. Here is an example of downloading
a single tile from 2016 from the Landsat collection we have processed `landsat/<year>/<z>/<x>/<y>`.

```python
import requests
url = "http://localhost:4502/api/v1/basemaps/landsat/2016/14/8473/7643"
r = requests.get(url)

print(r.status_code)
with open('./image_test.jpg', 'wb') as handler:
    handler.write(r.content)
```

This would be consumed by a web-map client as an x/y/z type endpoint via `https://api.skydipper.com/v1/basemaps/landsat/<year>/<x>/<y>/<z>`

### Layer Basemaps

Any public asset in Earth Engine can be accessed as a web map tile layer. The asset needs to have a Dataset and Layer
associated with it in the Skydipper API. You can set the styles for the layer using the open standard SLD method.
Accessing the layer is straighforward `basemaps/layer/<layer_id>/<z>/<x>/<y>`.

```python
import requests
url = "http://localhost:4502/v1/basemaps/layer/e7070d5f-3d38-46b1-86eb-e98782da55dd/14/8473/7643"
r = requests.get(url)

print(r.status_code)
with open('./image_test.jpg', 'wb') as handler:
    handler.write(r.content)
```

