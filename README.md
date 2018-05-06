# Data Source:
The data I trained on is from https://www.lendingclub.com/info/download-data.action, and the recomendation listing data from the lending club api. I used python request library to retrive new listings.

# APP:
The product I created can be viewed here:
http://p2p-invest.herokuapp.com/index

There are two part in the project, first the new listing recommender, I request new listing from the lending club API and make prediction

Secondly, user input current and my app predict the charge off risk left in the time span. 

# Model:
This is high precision logistic regression model because, from an investor's perspective missing out on a good loan cost much less comparing to having a charge off event.

I pickled the model for each grade and plug it in to my web page.

The framework used for the webapp is flask, and the app is deployed in heroku, detailed instruction below.

# flask web sorce code:
More of the how the app works can be viewed here: https://github.com/ella199161/flask-framework

I used a docker enviroment to unsure the program works.


# Flask on Heroku

This project is intended to help you tie together some important concepts and
technologies from the 12-day course, including Git, Flask, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The repository contains a basic template for a Flask configuration that will
work on Heroku.

A [finished example](https://lemurian.herokuapp.com) that demonstrates some basic functionality.

## Step 1: Setup and deploy
- Git clone the existing template repository.
- `Procfile`, `requirements.txt`, `conda-requirements.txt`, and `runtime.txt`
  contain some default settings.
- There is some boilerplate HTML in `templates/`
- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.
- (Suggested) Use the [conda buildpack](https://github.com/kennethreitz/conda-buildpack).
  If you choose not to, put all requirements into `requirements.txt`

  `heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git`

  The advantages of conda include easier virtual environment management and fast package installation from binaries (as compared to the compilation that pip-installed packages sometimes require).
  One disadvantage is that binaries take up a lot of memory, and the slug pushed to Heroku is limited to 300 MB. Another note is that the conda buildpack is being deprecated in favor of a Docker solution (see [docker branch](https://github.com/thedataincubator/flask-framework/tree/docker) of this repo for an example).
- Deploy to Heroku: `git push heroku master`
- You should be able to see your site at `https://<app_name>.herokuapp.com`
- A useful reference is the Heroku [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python-o).

## Step 2: Get data from API and put it in pandas
- Use the `requests` library to grab some data from a public API. This will
  often be in JSON format, in which case `simplejson` will be useful.
- Build in some interactivity by having the user submit a form which determines which data is requested.
- Create a `pandas` dataframe with the data.

## Step 3: Use Bokeh to plot pandas data
- Create a Bokeh plot from the dataframe.
- Consult the Bokeh [documentation](http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html)
  and [examples](https://github.com/bokeh/bokeh/tree/master/examples/embed).
- Make the plot visible on your website through embedded HTML or other methods - this is where Flask comes in to manage the interactivity and display the desired content.
- Some good references for Flask: [This article](https://realpython.com/blog/python/python-web-applications-with-flask-part-i/), especially the links in "Starting off", and [this tutorial](https://github.com/bev-a-tron/MyFlaskTutorial).
