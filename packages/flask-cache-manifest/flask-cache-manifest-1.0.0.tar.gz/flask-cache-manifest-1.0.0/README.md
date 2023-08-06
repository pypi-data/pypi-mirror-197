[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/maxdup/flask-cache-manifest/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/flask-cache-manifest.svg)](https://pypi.python.org/pypi/flask-cache-manifest/)
[![PyPI version fury.io](https://badge.fury.io/py/flask-cache-manifest.svg)](https://pypi.python.org/pypi/flask-cache-manifest/)
[![Coverage](https://github.com/maxdup/flask-cache-manifest/blob/master/docs/source/coverage.svg "coverage")]()

# Flask-Cache-Manifest

Flask-cache-manifest is a [Flask](https://flask.palletsprojects.com/en/2.2.x/) extension to help you serve your md5 hashed assets. Having file hashes in filenames is a popular feature of modern asset bundlers. It's a good strategy for browser cache busting. However, Flask does not provide an easy way to reference those complicated and ever-changing filenames. Flask-cache-manifest lets you reference those assets by leveraging `cache_manifest.json` files.


Full Documentation: https://maxdup.github.io/flask-cache-manifest/

Turns:
```Jinja
<link type="text/css" rel="stylesheet"
      href="{{ hashed_url_for('static', filename='css/app.css') }}">
```

into:

```html
<link type="text/css" rel="stylesheet"
      href="/static/css/app-d41d8cd98f00b204e9800998ecf8427e.css">
```


## Installation

```
pip install flask-cache-manifest
```


## Initializing

The extension needs to be loaded alongside your Flask application.

Here's how it's done:

```python

from flask import Flask, Blueprint
from flask_cache_manifest import FlaskCacheManifest

flaskCacheManifest = FlaskCacheManifest()

app = Flask('my-app',
            static_folder='dist/static',
            static_url_path='/static')

bp = Blueprint('my-blueprint',
               __name__,
               static_folder='blueprints/static',
               static_url_path='/bp/static')

app.register_blueprint(bp)

flaskCacheManifest.init_app(app)

app.run()
```

**_NOTE:_**
    Ideally, `flaskCacheManifest.init_app` needs to be called after you've registered your blueprints.
    Static folders registered after `init_app` will not be loaded.


## Usage

Flask-cache-manifest adds the `hashed_url_for` function for use in your templates.
It is analogous to Flask's url_for. Given the above example and its blueprints,
here's how you would be able to reference your static files in your Jinja templates.

```html
<!-- from the app's static folder -->
<link type="text/css" rel="stylesheet"
      href="{{ hashed_url_for('static', filename='css/app.css') }}">

<!-- from the blueprint's static folder -->
<link type="text/css" rel="stylesheet"
      href="{{ hashed_url_for('my-blueprint.static', filename='css/app.css') }}">

<!-- from the static folder relative to what is currently being rendered -->
<link type="text/css" rel="stylesheet"
      href="{{ hashed_url_for('.static', filename='css/app.css') }}">