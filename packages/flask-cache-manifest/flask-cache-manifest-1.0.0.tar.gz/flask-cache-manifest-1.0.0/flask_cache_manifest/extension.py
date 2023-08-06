import logging
import json
import os

from flask import request, url_for

EXT_NAME = "Flask-Cache-Manifest"


class FlaskCacheManifest(object):
    def __init__(self, app=None):
        """
        Constructor function for FlaskCacheManifest. It will call
        :func:`FlaskCacheManifest.init_app` automatically if the
        app parameter is provided.

        :param app: A Flask application.
        :type app: flask.Flask
        """

        self.app = app
        self.manifests = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the extension and loads the various
        :code:`cache_manifest.json` files. It adds :func:`hashed_url_for`
        to the template globals for use in Jinja templates.

        :param app: A Flask application.
        :type app: flask.Flask
        """
        self.app = app

        app.config.setdefault('CACHE_MANIFEST_REPLACE_URL_FOR', False)

        self.load_manifest("static", app)
        for endpoint, blueprint in app.blueprints.items():
            self.load_manifest(f"{endpoint}.static", blueprint)

        app.add_template_global(self.hashed_url_for, name='hashed_url_for')
        if app.config['CACHE_MANIFEST_REPLACE_URL_FOR']:
            app.add_template_global(self.hashed_url_for, name='url_for')

    def load_manifest(self, endpoint, scaffold):
        """
        Called automatically during :any:`init_app` but can be called manually
        to load blueprints after the initialization.

        :param endpoint: The endpoint the blueprint is registered as.
        :type endpoint: str
        :param scaffold: A Flask application or a registered blueprint.
        :type scaffold: flask.Blueprint
        """

        if not scaffold.has_static_folder:
            return

        manifest_path = os.path.join(scaffold._static_folder,
                                     "cache_manifest.json")

        try:
            with scaffold.open_resource(manifest_path, "r") as f:
                self.manifests[endpoint] = json.load(f)
        except json.JSONDecodeError:
            logging.warning(
                f"{EXT_NAME} | Couldn't decode file: {manifest_path}")
        except PermissionError:
            logging.warning(
                f"{EXT_NAME} | Couldn't access file: {manifest_path}")
        except (FileNotFoundError, Exception):
            pass

    def hashed_url_for(self, endpoint, **values):
        """
        Generate a URL to the given endpoint with the given values by
        Extending the functionality of Flask's :func:`url_for()<flask.url_for>`.
        Arguments will be forwarded to url_for, with the only
        :code:`values['filename']` being mutated to the appropriate hashed
        filename.

        :param endpoint: The endpoint of the URL (name of the function).
        :type endpoint: str
        :param values: The variable arguments of the URL rule.
        :type _values: any

        :param _external: If set to ``True``, an absolute URL is generated.
                          Server address can be changed via ``SERVER_NAME``
                          configuration variable which falls back to the `Host`
                          header, then to the IP and port of the request.
        :type _external: bool, optional
        :param _scheme: A string specifying the desired URL scheme.
                        The `_external` parameter must be set to ``True`` or a
                        :exc:`ValueError` is raised. The default behavior uses
                        the same scheme as the current request, or
                        ``PREFERRED_URL_SCHEME`` from the
                        :ref:`app configuration <flask.config>` if no request context
                        is available. As of Werkzeug 0.10, this also can be set
                        to an empty string to build protocol-relative URLs.
        :type _scheme: str, optional
        :param _anchor: If provided this is added as anchor to the URL.
        :type _anchor: str, optional
        :param _method: If provided this explicitly specifies an HTTP method.
        :type _method: str, optional

        :rtype: str
        """

        if request is not None:
            blueprint_name = request.blueprint
            if endpoint[:1] == ".":
                if blueprint_name is not None:
                    endpoint = f"{blueprint_name}{endpoint}"
                else:
                    endpoint = endpoint[1:]

        manifest = self.manifests.get(endpoint, {})
        filename = values.get("filename", None)
        values['filename'] = manifest.get(filename, filename)

        return url_for(endpoint, **values)
