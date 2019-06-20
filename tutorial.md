# Tutorial
This tutorial will provide a simple example of setting up an annotation system on CMU-Crowd. Our example is going to be a food dataset that gets data about
how many calories users consume for lunch.

## Prerequisites
Follow the setup instructions in the README.


## Job Creation
Sign up as an admin through your website.

Then, navigate to the 'Create A Job' page through the navigation bar at the top. 

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
Note that {{meal}} is going to be a randomly generated meal choice from breakfast, lunch and dinner. This will be populated by a list of JSON dictionaries in our batch content later on, which is where any dynamically generated data (video URLs, question types) should be passed.

### Batch Creation
Now that we have our job created, we have to launch a batch so workers can begin annotating.  Go to the 'Start Batch' tab on the navigation bar. Select the job you created in the Job field. For this example, I will pass a list of 4 JSON dictionaries, each with a meal key to be passed to the HTML template's {{meal}} tag. Ensure that your number of HITs matches the amount of total annotations you would like in your batch, and the length of the JSON list in the content field.
![Screenshot](start_batch.png)



## Annotating
Our job is now ready for annotation by workers. Sign up as a worker to being annotating. You should see a page similar to the one below. 


