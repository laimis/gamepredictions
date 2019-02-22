# NFL & NBA game outcomes

Using very basic stats for both leagues and building models that can predict the game outcomes. The models are built using XGBoost, sckikit-learn's GaussianNB, and NLP.

At the end of the day, since the inputs are pretty basic stats, the model accuracy between the various implementations does not very as much.

## Data

NBA regular season data obtained from 2014 through 2019 season.
NFL regular season data obtained from 2014 through 2019 season.

## Results

NFL 2019 ~ 68%
NBA 2019 ~ 66%

## Areas to explore

- Need to do more research what other features to use to improve
- Any way to take into account team make up (# of all stars?)
- Calibration, over season, when it says that it is confident by %, is it confident by that percentage?
- Ability to evaluate a strategy on a given data set

- current strategy
	- choose games that are above certain threshold of confidence
	- bet on those, compare outcomes, accumulate money
	- describe strategy by name
	- return strategry wins/losses?