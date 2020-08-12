# Weather Forecast Proxy API
Simple Flask REST API that works as a proxy between my [React Weather Dashboard](https://github.com/martapanc/React-Weather-Dashboard) and the OpenWeatherMap API, to avoid overloading the latter with requests.

### Initialization
```
heroku login
heroku apps:cerate weather-forecast-proxy-api
heroku git:remote -a weather-forecast-proxy-api
gaa
gcmsg "Initial commit"
gp heroku master
```
To scale dyno:
```
heroku ps:scale web=1
```


### Documentation
- [Deploying a Flask API to Heroku](https://stackabuse.com/deploying-a-flask-application-to-heroku/)
