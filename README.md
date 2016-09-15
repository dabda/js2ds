# js2ds
js2ds is a django app that creates JSON files and the associated file and directory structure based on the underlying JSON schemes.

`requirements.txt` includes:
```
Django==1.9.7
python==3.5.1
django-bootstrap3
```

## Installation

### 1. virtualenv (optional)
Use [virtualenv](http://www.virtualenv.org/). Type command

`$ virtualenv`

inside your projectname folder.

### 2. Download
Download the *django-js2ds-app* project files to your workspace:

    $ cd /path/to/your/workspace
    $ git clone git://github.com/dabda/js2ds.git projectname && cd projectname

### 3. Requirements
The *requirements.txt* file has all the tools you need.
To install them, simply type:

`$ pip install -r requirements.txt`

Add to INSTALLED_APPS in your settings.py:

    INSTALLED_APPS = [
        ...
        'bootstrap3',
        'js2ds',
    ]

Add to urlpatterns in your urls.py:

    from django.conf.urls import url, include

    urlpatterns = [
        ...
        url(r'', include('js2ds.urls')),
    ]
