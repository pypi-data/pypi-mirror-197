from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'MiniMVC is a lightweight, open-source web framework for building small web applications in Python.'
LONG_DESCRIPTION = '''MiniMVC is a lightweight, open-source web framework for building small web applications in 
Python. It provides a simple and intuitive interface for handling HTTP requests and generating dynamic HTML content.

With MiniMVC, you can define routes for handling different URLs, process GET and POST requests, and serve static 
files such as images, CSS files, and JavaScript files. MiniMVC also includes a simple file uploader and validator for 
processing file uploads from HTML forms.

MiniMVC is designed to be easy to use and easy to extend. It is suitable for building small web applications and 
prototypes, as well as for learning the basics of web development in Python.

### Features:
* Simple and intuitive interface
* Supports GET and POST requests
* Jinja2 templating engine for generating dynamic HTML content
* Routing system for handling different URLs
* Simple file uploader and validator for processing file uploads
* Supports serving static files such as images, CSS files, and JavaScript files
* Lightweight and easy to extend

### Documentation:
https://github.com/Dcohen52/MiniMVC

### Installation:
```pip install MiniMVC```

'''

# Setting up
setup(
    name="MiniMVC",
    version=VERSION,
    author="Dekel Cohen",
    author_email="<dcohen52@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['Jinja2'],
    keywords=['python', 'web', 'framework', 'desktop', 'html', 'javascript', 'styles', 'js', 'API', 'microservices',
              'REST'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
