# CMU-Crowd
CMU-Crowd is a Human Intelligence Task (HIT) platform that is fully customisable for specialized tasks. Built with Django and Bootstrap, it streamlines the process of building large datasets and setting up an in-house annotation system.
It may be used as a complete solution by simply providing HTML templates for jobs and using example templates that come with it, or serve as a starting point for dealing with different levels of worker authentication, tracking worker statistics and launching tasks easily.

## Functionality
### Fully customisable
As CMU-Crowd is a Django webapp, you can easily edit the classes in models.py to add more fields to the worker and admin models if required. It is also easy to add new pages. For getting started with django, [this guide](https://docs.djangoproject.com/en/2.1/intro/tutorial01/) as well as their official documentation is recommended.




## Setup

### Requirements: 
python 3.x, tested with 3.6 and 3.7

1. (recommended) Activate a virtual enviroment 
```console
python3 -m venv <$your_venv_name>
source <$your_venv_name>/bin/activate
```
2. Install required modules 
```console
pip3 install -r requirements.txt
```
3. Make Django database migrations
```console
./manage.py makemigrations
./manage.py migrate
```
4. Test on localhost 
```console
./manage.py runserver
```
You should now have an instance of the webapp running on your localhost.

## Deploying to Production


## Usage

### Valid HTML Templates
Essentially, the HTML template for a job will be a POST form. Because of this, there are certain requirements in order for the template to render correctly.

Make sure you include "post" as the form method, that the form has a submit button and that you include the {% csrf_token %} tag as we use Django's inbuilt templating system. You will also want a appopriate name for each input field in your form, so that when the data is saved to the database as a JSON dictionary you can access its contents easily.

It is also highly recommend to extend 'base.html', as this is where the navigation bar and some CSS are included, but you could always write your own navigation as long as the links are valid. If you choose to extend 'base.html', note that your form must be placed within the block content. 

A very simple example of a valid HTML template that simply asks the user for their name (and extends 'base.html') is as follows:

```HTML
{% extends "base.html" %}

{% block content %}
<form method="post">
{% csrf_token %}
<p> What is your full name? </p>
<input type="text" name="full_name">
<button type="submit" class="btn btn-success"> Submit </button>
</form>
{% endblock %}
```
Further examples are also included in the example_templates folder.


### Linking static files (CSS/JS/Images)
Static files should be placed in the /static folder and loaded with the static tag. You can change where your static files are being served from in settings.py. If you are unfamiliar with serving static files in Django, refer to [this guide](https://docs.djangoproject.com/en/2.1/howto/static-files/).


### Templating and passing data in context
For a brief introduction to Django's template language, please see https://docs.djangoproject.com/en/2.2/topics/templates/#the-django-template-language.
Django uses key-value pairs called context to pass data into HTML template. It is very similar to handlebars.js or jinja2. For more information, refer [here](https://docs.djangoproject.com/en/2.2/ref/templates/api/#django.template.Context).

For example, we can define a context dictionary like so:
```python
context = {'question':'What is your full name?'}
```
and access the data as follows:
```HTML
<p> Question 1: {{question}} </p>
```


### How data is saved

### Launching Jobs
To create a job, you must 

When creating a batch
- supply list of json dictionaries for each HIT
- give the number of HITs


## License

This project is licensed under ....

## Contact

Please open an issue or contact mkchan@cs.cmu.edu for any feedback and issues.
