# URL Ping

This is a system to monitor availability of APIs with the option
of checking whether the API response matches a specific pattern or not. 
This is done by providing an optional *regex* as a parameter of the request.
The system will always provide two information:
- **status code**
- **response time**

The system will eventually tell whether the response content matches
a specific pattern or not when a ***regular
expression*** is provided as part of the request.


## how to launch
Here are a few commands you will need to type in order to
test the system on your local machine.

After you have cloned the repository, go to the project root
and type these commands from the command line:
- `pip install -r requirements.txt` (to install dependencies)
- `python manage.py migrate` (to populate database)
- `python manage.py runserver` (to launch the server)\
Go to http://localhost:8000/ or http://127.0.0.1:8000/ and try it out!

## Project Structure
The core feature of the system is inside the *ping* app, which includes
a *ping_pack* package with a *ping_data* module where the business
logic of the project is written:\
a `Ping` object gets created each time a new request is sent when
submitting the homepage form.\
The following data will be stored inside the instance's attributes:
- the actual response object. Note that in case of unsuccessful connection
(e.g. a misspelled url, a not existing url or an existing but very slow url),
a `ConnectionError` is raised.
- the status code
- the response time
- the response content (eventually useful to find matching patterns)

#### Database Entities
SQLite3 database is used.\
a `Url` is present, with six tables where to store
the main "ping" data: the url, the status code, the response time,
the provided regexp (if any), a boolean regexp match and matching details (if any).\
The *Model* is linked to the `UrlForm`, which includes
two fields: a `url` field and a `regexp` field (optional).

#### Templates
Two HTML templates are used:\
*index.html* is the homepage where the user
will fill the form and send the request.\
*result.html* gets triggered after the request is sent, finally displaying
the ping data.

#### Styling
The bulk of the styling comes from this [Bootstrap template](https://startbootstrap.com/theme/landing-page) \
Additional styling are added inside the templates as well as
within Forms `Widget.attrs`.\
Static files are loaded from the *staticfiles* directory.

#### Tests
*Unit testing* is used. Tests are available at *ping/tests.py*\
From the project root directory, type `python manage.py test` to launch them.








