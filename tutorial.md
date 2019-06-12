# Tutorial
This tutorial will provide a simple example of setting up an annotation system on CMU-Crowd. Our example is going to be a food dataset that gets data about
how many calories users consume for lunch.

## Prerequisites
Follow the setup instructions in the README.


## Job Creation
Sign up as an admin through your website.

Then, navigate to the 'Create Job' page through the navigation bar at the top. 

Fill in the required fields. For the HTML template, this is the file I am going to upload:

```HTML
{% extends "base.html" %}

{% block content %}
<form method="post">
{% csrf_token %}
{% if first_annotation %}
  <p>  What is your Height? </p>
  <input type="text" name="full_name">
 {% endif %} 
<button type="submit" class="btn btn-success"> Submit </button>
</form>
{% endblock %}
```

## Extending the worker model
For our dataset, it makes sense to store information about the worker's height, weight and gender. We can extend the Worker model in models.py, and then
either ask them for their height, weight and gender when they signup, or when they complete their first annotation. 

For this tutorial, I will store this data when they complete their first annotation to give an example of conditionals in Django's templating language.
