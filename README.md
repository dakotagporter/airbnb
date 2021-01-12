# AirBread'n'Butter

## Description
This web application was created with the intention of allowing a user who is interested in renting out a property as an AirBnB to enter their information and get back a predicted rent result for their property. A simple user-interface allows them to input only a few details and will immmediatly return results. In addition, a helpful search bar can help them navigate to other properties they have entered in the app. Click around and best of luck!

### API:
The API for this project contains the configuration of files needed to run the app. The machine learning models are placed in accessibility to the app. Each URL endpoint is configured for any neutral, GET or POST methods.

### Models
Prices are predicted using a 3-input neural network. The model takes the main listing image, the listing description, and the list of amenities.




### Accessibility and Installation
To install locally:

```
pipenv install -r requirements.txt
```

View online at https://airbreadnbutter.herokuapp.com/.
