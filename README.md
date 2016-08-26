# js2ds
js2ds is a django app that creates JSON files and the associated file and directory structure based on the underlying JSON schemes.

`requirements.txt` includes:
```
Django==1.9.7
python==3.5.1
```

django-bootstrap3 is also needed.

## Installation

### 1. virtualenv
You can use [virtualenv](http://www.virtualenv.org/). Create your own project, where `projectname` is the name of your project:

`$ mkvirtualenv --clear projectname`

### 2. Download
Download the *django-js2ds-app* project files to your workspace:

    $ cd /path/to/your/workspace
    $ git clone git://github.com/dabda/js2ds.git projectname && cd projectname

### 3. Requirements
The *requirements.txt* file has all the tools you need.
To install them, simply type:

`$ pip install -r requirements.txt`

`$ pip install django-bootstrap3`
