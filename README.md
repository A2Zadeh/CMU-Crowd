# CMU-Crowd
CMU-Crowd is a Human Intelligence Task (HIT) platform that is fully customisable for specialized tasks. Built on Django and Bootstrap, it streamlines the process of building large datasets and setting up an in-house annotation system.
It may be used as a complete solution by simply providing HTML templates for jobs and using example templates that come with it, or serve as a starting point for dealing with different levels of worker authentication,
tracking worker statistics and launching tasks easily.

## Functionality





## Setup

###Requirements: 
python 3.x, tested with 3.6 and 3.7

1. (recommended) Activate a virtual enviroment 
```console
python3 -m venv <$your_venv_name>
source <your_venv_name>/bin/activate
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

## Deployment to Production


## Usage

### Valid HTML Templates
- needs method="post"
- mention csrf token that django needs
- ensure that form has submit button 


### Passing context data to templates

### Launching Jobs


## TODO:
