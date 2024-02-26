# Figure out

Welcome to the figure-out wiki!

# Setting up the environment (use Visual Code)
## Requirements:
1. Visual Code 
2. Python 3.9+


## Bash:
`cd figure-out`  
`code .`    
### Without docker:
`source env/bin/activate` 
> Make sure that you are **always** working in the virtual environment.
Check for the `(env) ->` sign in bash/zsh before the current directory information.
For example: `(env) -> figure-out git:(main) $` 

__Run a virtual server__
`python web/manage.py runserver` - 8080 port default  
### With docker:
Launch the docker
`cd docker` - you have to be in docker/ dir     
`docker compose up -d`.     
## Finally
**Access it at** [localhost:8080](localhost:8080)   
**Use for templates** [Bootstrap4](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
(Pending an update for Bootstrap5+)
**It's better to test it without docker though** - try to set everything on your computer correctly and just use venv.    
There should not be any complications with Mac/Linux users. (Windows users might try using [WSL](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjoj6fYqJeEAxUwPxAIHV2mDq8QFnoECBEQAQ&url=https%3A%2F%2Flearn.microsoft.com%2Fru-ru%2Fwindows%2Fwsl%2Finstall&usg=AOvVaw1j6UvzJrUuBGYGvM9HhDRq&opi=89978449))
# Navigation
* `env/` - python [venv](https://docs.python.org/3/library/venv.html) folder (contains all the info about current python set up for this project)  
* `docker/` - contains YAML file (Docker compose) and `requirements.txt` - file that contains all the packages versions of current python set up.
> You can update this file using the bash command `pip freeze > docker/requirements.txt`    
* `web/` - contains Django PWA app project  
  
# Django project info
## Brief file descriptions
`web/web` contains general Django files   
&copy; [Django tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
1. `__init__.py` - An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read [more about packages](https://docs.python.org/3/tutorial/modules.html#tut-packages) in the official Python docs.
2. `settings.py` - Settings/configuration for this Django project. [Django settings](https://docs.djangoproject.com/en/5.0/topics/settings/) will tell you all about how settings work.
3. `urls.py` - The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in [URL dispatcher](https://docs.djangoproject.com/en/5.0/topics/http/urls/).
4. `asgi.py` - An entry-point for ASGI-compatible web servers to serve your project. See [How to deploy with ASGI](https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/) for more details.
5. `wsgi.py` - An entry-point for WSGI-compatible web servers to serve your project. See [How to deploy with WSGI](https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/) for more details.

## Informative explanation
1. **web/urls.py**    
`urlpatterns = [...]` describes all available addresses.   
For instance, [](localhost:8080/admin/) will request `admin.site.urls` and opens an administrator page.  
`path(address, view)` takes two parameters: view can be added from an external package: `path('sign-in/', auth_views.LoginView.as_view(template_name="sign_in.html"))` or from the `core/views.py`: `path('', views.home)`.    

`django.contrib.auth` was imported for the auth templates views.

2. **Dockerfile**
The basic Dockerfile that sets up an environment for the app frontend view testing (Django).
> Will be upgraded.   
3. 
Hello world