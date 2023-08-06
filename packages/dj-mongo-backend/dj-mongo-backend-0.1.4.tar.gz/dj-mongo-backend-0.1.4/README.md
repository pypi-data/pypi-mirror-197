# dj-mongo-backend

[![GitHub](https://img.shields.io/github/license/VicoDevTeam/dj-mongo-backend?style=for-the-badge)](../master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/dj-mongo-backend?style=for-the-badge)](https://pypi.org/project/dj-mongo-backend/)

> This project is a fork from [doableware/djongo](https://github.com/doableware/djongo)

> This documentation is a work in progress based on the base repo.

## The second connector that lets you use Django with MongoDB _without_ changing the Django ORM

Use MongoDB as a backend database for your Django project, without changing the Django ORM.
Use the Django Admin GUI to add and modify documents in MongoDB.

## Usage:

<ol>
<li> Install dj-mongo-backend:

```
pip install dj-mongo-backend
```

</li>
<li> Into settings.py file of your project, add:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your-db-name',
        'CLIENT': {
           'host': 'your-db-host',
        }
    }
}
```

</li>   
   <li> Run <code>manage.py makemigrations &ltapp_name&gt </code> followed by <code>manage.py migrate</code> (ONLY the first time to create collections in mongoDB) </li>
   <li> YOUR ARE SET! HAVE FUN! </li>
</ol>

## Requirements:

1. Python 3.6 or higher.
2. MongoDB 3.4 or higher.
3. If your models use nested queries or sub querysets like:

   ```python
   inner_qs = Blog.objects.filter(name__contains='Ch').values('name')
   entries = Entry.objects.filter(blog__name__in=inner_qs)
   ```

   MongoDB 3.6 or higher is required.

## How it works

djongo is a SQL to mongodb query compiler. It translates a SQL query string into a mongoDB query document.
As a result, all Django features, models etc. work as is.

Django contrib modules:

<pre><code>  
'django.contrib.admin',
'django.contrib.auth',    
'django.contrib.sessions',

</code></pre>

and others... fully supported.

## Features

- Use Django Admin GUI to access MongoDB.
- Embedded Model.
- Embedded Array.
- Embedded Form Fields.

Read the [full documentation](https://www.djongomapper.com/)

## Contribute

If you think djongo is useful, **please share it** with the world!

You can contribute to the source code or the documentation by creating a simple pull request!
You may want to refer to the design documentation to get
an idea on how [Django MongoDB connector](https://www.djongomapper.com/djongo/django-mongodb-connector-design-document/)
is implemented.

Add a star, show some love :)

## Questions and Discussion

- [Djongo groups](https://groups.google.com/d/forum/djongo) is where you can watch for new release announcements, suggest improvements, and discuss topics pertaining to Django and MongoDB.
- Issues, where things are not working as expected, please raise a git-hub issue ticket.
- For questions and clarifications regarding usage, please put it up on stackoverflow instead.
