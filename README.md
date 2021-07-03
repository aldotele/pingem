# URL Ping

This is a system to monitor availability of APIs with the option
of checking whether the API response matches a specific pattern or not. This is done
by providing an optional *regex* as a parameter of the request.
The system will always provide two information:
- **status code**
- **response time**

The system will eventually tell if the response content matches
a specific pattern in case a ***regular
expression*** is provided in the request.


## how to launch
Here are a few commands you will need in order to make
the project work properly on your local machine, after 
you have cloned the repository.\

From command line on project main directory, do these:
- type `pip install -r requirements.txt` (to install dependencies)
- type `python manage.py migrate` (to populate database)
- type `python manage.py runserver` (to launch the server)
- go to http://127.0.0.1:8000/ to try it out

## Project Structure
The core feature is inside the *ping* app, which includes
a *ping_pack* package with a *ping_data* module where the business
logic of the project is written:\
a `Ping` object gets created each time a new request is done.\
Its attributes will store the follwing data:
- the actual response object. In case of unsuccessful connection (for example
when a misspelled URL gets passed), a `ConnectionError` is raised.
- the status code
- the response time
- the response content (useful to find patterns inside it, eventually)

#### Database Entities
a single `Url` is present. It has six tables where to store
the main data, and is linked to the `UrlForm` which includes
two fields: a `url` field and a `regexp` field (optional) 

#### Templates
Two HTML templates are used:\
*index.html* is the homepage where the user
will fill the form and send the request.\
*result.html* gets triggered after the request is sent, providing
the resulting data.

#### Tests
*Unit testing* is used. Tests are available at *ping/tests.py*








