import cgi
import http.server
import mimetypes
import os
import re
import socketserver
import urllib

import jinja2


class MiniMVC(http.server.BaseHTTPRequestHandler):
    """
    MiniMVC is a simple web framework that allows users to quickly develop and deploy web
    applications. It uses the Jinja2 templating engine for rendering templates and provides a set of convenient
    methods for handling HTTP requests and responses.

    MiniMVC includes a routing system that allows users to map URLs to Python functions, and it supports both
    GET and POST requests. It also provides a method for serving static files, and includes a basic file upload feature.

    To use MiniMVC, create a new class that inherits from MiniMVC, define your routes using the route decorator,
    and implement the corresponding Python functions. Then, create an instance of MiniMVCRun and call its run method,
    passing in your app class as an argument.

    For more information on how to use MiniMVC, please refer to the documentation and examples on GitHub.
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    routes = []

    @classmethod
    def route(cls, pattern):
        '''
        A decorator for registering a URL pattern and callback function to handle requests for that pattern.
        '''
        def wrapper(callback):
            cls.routes.append((pattern, callback))
            return callback

        return wrapper

    def url_for_static(self, filename, port=None):
        '''
        Generates a URL for serving a static file from the 'static' directory, given the filename and optional port number.
        :param filename: the name of the file to generate the URL for.
        :param port: an optional port number to include in the URL. Default is None.
        :return: a URL string.
        '''
        current_dir = os.getcwd()
        path = os.path.join(current_dir, 'static', filename)
        return f'http://localhost:{port}/static/{path}'

    def handle_error(self, status, message, template_name='upload.html', context=None):
        """
        Handles errors by sending the specified status and message as a response
        and rendering the specified template with the given context.

        Args:
            status (int): The HTTP status code to send in the response.
            message (str): The message to send in the response.
            template_name (str): The name of the template to render.
            context (dict): A dictionary containing any variables to be used in the template.

        Returns:
            None
        """
        self.send_error(status, message)
        if context is None:
            context = {}
        context['status'] = status
        context['message'] = message
        self.render_template(template_name, context)

    def do_GET(self):
        '''
        This method handles GET requests sent to the server. If the path starts with '/static/', it serves a static
        file using the serve_static_file() method. If the path matches a pattern in self.routes, it calls the
        corresponding callback function. If none of the patterns match, it sends a 404 error response.
        '''
        if self.path.startswith('/static/'):
            path = self.path[1:]
            self.serve_static_file(path)
            return

        for pattern, callback in self.routes:
            match = re.match(pattern, self.path)
            if match:
                callback(self, match)
                return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        '''
        This method handles POST requests sent to the server. It first checks if the request contains multipart form
        data. If it does, it saves the uploaded file and sends a success response. If it doesn't, it reads the
        request body and searches for a callback function in self.routes with the matching path and function name. If
        it finds a match, it calls the function with the request body as a parameter. If no match is found,
        it sends a 404 error response.
        '''
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']

        if 'multipart/form-data' in content_type:
            fields = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': content_type,
            })

            if 'file' in fields:
                file_item = fields['file']
                filename = os.path.join('uploads', file_item.filename)
                with open(filename, 'wb') as f:
                    f.write(file_item.file.read())
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Successfully uploaded file')

                return
        else:
            body = self.rfile.read(content_length).decode('utf-8')

            for pattern, callback in self.routes:
                if self.path == pattern and callback.__name__ == 'handle_post':
                    callback(self, body)
                    return

        self.send_response(404)
        self.end_headers()

    @classmethod
    def post(cls, path):
        """
        Class method that acts as a decorator for registering a POST request handler with a given path.

        Args:
            path (str): The path to associate the handler with.

        Returns: function: The decorator function that registers the given callback function as a POST request
        handler for the given path.
        """
        def wrapper(callback):
            """
            Wrapper function that registers the given callback function as a POST request handler for the path given
            to the outer function.

            Args:
                callback (function): The function that handles the POST request.

            Returns:
                function: The given callback function.
            """
            cls.routes.append((path, callback))
            return callback

        return wrapper

    @staticmethod
    def handle_post(handler, body):
        """
        Static method that handles POST requests by sending a plain text response with the given request body.

        Args:
            handler (MiniMVC): The instance of the MiniMVC server handling the request.
            body (str): The body of the POST request.

        Returns:
            None
        """
        handler.send_response(200)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        handler.wfile.write(body.encode('utf-8'))

    def serve_static_file(self, path):
        """
        Serves a static file to the client with the given path.

        Args:
            path (str): The path of the file to serve.

        Returns:
            None
        """
        try:
            current_dir = os.getcwd()
            file_path = os.path.join(current_dir, 'static', path)

            if not os.path.isfile(file_path):
                raise IOError

            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type == 'text/css':
                self.send_header('Cache-Control', 'max-age=86400')
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(os.path.getsize(file_path)))
            self.end_headers()

            with open(file_path, 'rb') as f:
                chunk_size = 8192
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except IOError:
            self.send_error(404, 'File not found')

    def validate_input(self, data, fields):
        """
        Validates the input data for a request, checking that all required fields are present.

        Args:
            data (dict): The input data for the request.
            fields (list): The list of required fields.

        Returns:
            bool: True if all required fields are present, False otherwise.
        """
        missing_fields = []
        for field in fields:
            if field not in data:
                missing_fields.append(field)
        if missing_fields:
            self.send_error(400, f'Missing fields: {", ".join(missing_fields)}')
            return False
        return True

    def render_template(self, template_name, context=None, css_url=None):
        """
        Renders a Jinja2 template with the given context and sends the resulting HTML to the client.

        Args:
            template_name (str): The name of the template file.
            context (dict, optional): The context to render the template with. Defaults to None.
            css_url (str, optional): The URL of a CSS stylesheet to include in the template. Defaults to None.

        Returns:
            None
        """
        template = self.env.get_template(template_name)
        if context is None:
            context = {}
        context['css_url'] = css_url
        html = template.render(context)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


class MiniMVCRun:

    def __init__(self, port=8080):
        self.PORT = port

    def run(self, app_class):
        with socketserver.TCPServer(("", self.PORT), app_class) as httpd:
            print(f"Running on port {self.PORT}\nEnter here: http://localhost:{self.PORT}/")

            httpd.serve_forever()
