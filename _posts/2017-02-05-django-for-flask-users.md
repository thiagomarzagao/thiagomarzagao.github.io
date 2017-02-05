---
comments: true
layout: post
title: Django for Flask users
---

I'm using Django for a serious project for the first time. I had played with Django a couple of times before, but I'm a long-time Flask fanboy and I invariably gave up in frustration ("why would anyone ever need separate files for settings, urls, and views?!"). Well, turns out Django is pretty cool if you want to put a bunch of apps under the same umbrella. Now, the official [tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/) is a bit too verbose if you're impatient. And if you're used to Flask's minimalism, you *will* get impatient with Django at times. So, here a few potentially useful pointers (largely for my own future consultation).

To get started, just `pip install` Django, run `django-admin startproject mysite`, then run `python manage.py startapp myapp`. (Replace `mysite` and `myapp` by whatever names you want.) This should create the essential files and directories you'll need.

**making urls work**

In Flask you create your views and map your urls all at once:

{% highlight python %}
@app.route('/')
def index():
    return 'Hello World!'
{% endhighlight %}

This is about as simple as it gets (unless you want to get [really minimalist](http://cherrypy.org/)).

In Django you can't do that. You have to define your views in one place and map your urls elsewhere. The usual way to do it is to define your views in your (aptly named) `myapp/views.py` file, like this:

{% highlight python %}
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello World!')
{% endhighlight %}

Unlike in Flask you can't just do `return 'Hello World!'` - the returned object cannot be a string, so we need to import `HttpResponse`. Also unlike in Flask, we must feed the request to the function - there is no global `request` object in Django, so we need to pass it around explicitly (more about this in a moment).

Now on to mapping urls. This requires changing two different files. The first is your `mysite/urls.py` file, wherein you'll put this:

{% highlight python %}
from django.conf.urls import url

urlpatterns = [url(r'^myapp/', include('myapp.urls'))]
{% endhighlight %}

This piece of code tells `mysite` (the big project inside which your various apps will live) to defer to `myapp` (one of your various apps) whenever someone hits `http://blablabla/myapp/`. (That `r'^myapp/` thing is a [regular expression](https://docs.python.org/3/library/re.html) that matches any url that contains `myapp/`.)

So, `mysite/urls.py` is a big dispatcher: it'll check the url and send the request to the appropriate app. Here we only have one app (`myapp`), but if you're using Django you'll likely have several apps, in which case the `urlpatterns` list will contain several `url()` objects.

Now, `myapp` must be prepared to receive the baton. For that to happen your `myapp/urls.py` file (*not* your `mysite/urls.py` file!) must look like this:

{% highlight python %}
from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.index, name = 'index')]
{% endhighlight %}

Here we have another regex: `r'^$`. This will capture any requests that end in `myapp/`. (If the request got this far then it must contain `myapp/`, so you don't need to repeat it in the regex here.) We're telling `myapp` that any such requests should be handled by the view function named `index` - which you defined before, in your `myapp/views.py` file (see above).

So, `myapp/urls.py` is a secondary dispatcher: it'll check the url and send the request to the appropriate view. Here we only have one view (the app's index page), but in real life you'll have several views, in which case the `urlpatterns` list will contain several `url()` objects.

That's it. If you run `python manage.py runserver` and then open `http://127.0.0.1:8000/` in your browser you should be greeted by the `Hello World!` message.

If you really want to you *can* have a single-file Django project: check [this](https://www.safaribooksonline.com/library/view/lightweight-django/9781491946275/ch01.html). But if your project is so small that you can have a single file then maybe you'd be better off using Flask or CherryPy or some other minimalist web framework.

**request and session**

Accessing request and session data in Flask is a no brainer. There is a global `request` object and a global `session` object and, well, you just do whatever you want to do with them.

{% highlight python %}
from flask import request
from flask import session

@app.route('/')
def hello():
    if request.method == 'POST':
        user_input = request.form['user_input']
        session['foo'] = 'bar'
    elif request.method == 'GET':
        session['foo'] = 'macarena'
    return session['foo']
{% endhighlight %}

In Django, as I mentioned before, there is no global `request` object - you need to explicitly pass `request` around to work with it. There is no global `session` object either. Instead, `session` is an attribute of `request`. This is how the above snippet translates into Django:

{% highlight python %}
from django.http import HttpResponse

def hello(request):
    if request.method == 'POST':
        user_input = request.POST['user_input']
        request.session['foo'] = 'bar'
    elif request.method == 'GET':
        request.session['foo'] = 'macarena'
    return HttpResponse(request.session['foo'])
{% endhighlight %}

So, `session` becomes `request.session` and `request.form` becomes `request.POST`.

**templates**

You must tell Django where to look for templates. Open `mysite/settings.py`, locate the `TEMPLATES` list and edit `DIRS`.

{% highlight python %}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/path/to/my/templates/folder/',
                 '/path/to/my/other/templates/folder/'],
        'APP_DIRS': True,
        'OPTIONS': {
            # ...
        },
    },
]
{% endhighlight %}

There are a few syntax differences between Jinja2 (Flask's default templating language) and Django's templating language (DTL). For instance, to access the first element of `mylist` it's {% raw %}`{% mylist[0] %}`{% endraw %} in Jinja2 but {% raw %}`{% mylist.0 %}`{% endraw %} in DTL. But most of the syntax is identical. Template inheritance works the same way, with {% raw %}`{% extends 'parent.html' %}`{% endraw %} and {% raw %}`{% block blockname %}{% endblock $}`{% endraw %}. Same with loops, if/elses, and variables: {% raw %}`{% for bla in blablabla %}{% endfor %}`{% endraw %}, {% raw %}`{% if something %}{% elif somethingelse %}{% else %}{% endif %}`{% endraw %}, {% raw %}`{{ some_variable }}`{% endraw %}. If you're porting something from Flask to Django there is a chance your templates will work just as they are.

You need to change your views though. In Flask you render a template and pass variables to it like this:

{% highlight python %}
from flask import render_template

@app.route('/')
def hello():
    return render_template('mytemplate.html', 
                           some_var = 'foo', 
                           other_var = 'bar')
{% endhighlight %}

In Django you do it like this:

{% highlight python %}
from django.shortcuts import render

def hello(request):
    return render(request,
                  'mytemplate.html', 
                  {'some_var' = 'foo', 
                   'other_var' = 'bar'})
{% endhighlight %}

So, in Django you must pass the `request` object to render the template. And your template variables must be passed as a dict.

**connections**

In both Flask and Django you can use something like `pyodbc` or `pymssql` to connect to your databases. But you can put a layer of abstraction on top of that. In Flask there is Flask-SQLAlchemy. Here's their quickstart [snippet](http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application):

{% highlight python %}
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
{% endhighlight %}

In Django the connection and the models go into separate scripts. You set up the connection by adding an entry to the `DATABASES` dict in your `mysite/settings.py` file:

{% highlight python %}
DATABASES = {

    # ... your other db connections ...

    'my_database_name': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'my_database_name',
        'USER': 'my_username',
        'PASSWORD': 'my_password',
        'HOST': 'my.host.address',
        'PORT': 'my_port'}
    }
{% endhighlight %}

Then, in your `myapp/models.py`, you define your models.

{% highlight python %}
from django.db import models

class User(models.Model):
    id = models.IntegerField()
    username = models.CharField(max_length = 80)
    email = models.CharField(max_length = 120)
{% endhighlight %}

You don't have to use any models though. If you prefer to run raw SQL queries you can do it like this:

{% highlight python %}
from django.db import connections

cursor = connections['my_database_name'].cursor()
cursor.execute('SELECT * FROM sometable')
results = cursor.fetchall()
{% endhighlight %}

Just as you would do with pyodbc (except that here you don't need to `.commit()` after every database modification).

**afterwards**

I'm just trying to get you past the initial rage over all the boilerplate code Django requires. :-) This is all just about *syntax* - I'm merely "translating" Flask to Django. If you're serious about Django you should invest some time in learning Django's *semantics*. Their official [tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/) is a good place to start. Have fun!