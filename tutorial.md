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
  <p>  What is your height? </p>
  <input type="text" name="height">
    <p>  What is your weight? </p>
  <input type="text" name="weight">
      <p>  What is your gender? </p>
  <input type="text" name="gender">
 {% endif %} 
  <p> What did you eat for lunch? </p>
    <input type="text" name="food">
    <p> How many calories did this have? </p>
    <input type="text" name="calories">
<button type="submit" class="btn btn-success"> Submit </button>
</form>
{% endblock %}
```

### Batch Creation
Now that we have our job created, we have to launch a batch so workers can begin annotating.  Go to the 'Create Batch' tab on the navigation bar.


## Extending the worker model
For our dataset, it makes sense to store information about the worker's height, weight and gender. We can extend the Worker model in models.py, and then
either ask them for their height, weight and gender when they signup, or when they complete their first annotation. 

For this tutorial, I will store this data when they complete their first annotation to give an example of conditionals in Django's templating language.
