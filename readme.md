# mls_scores

This python module allows to retrieve the score for any team from [the MLS website](http://www.mlssoccer.com/scores/)

## How to use it

### getScores()

About this function: `getScores(team,date)`. The `team` argument is the team city (2 or three letters in all caps). The `date` argument is optional. The website display most game in the current month, hence the availability to specify the game date. If no date passed, the function will use the current day as the date.

The function returns a dictionnary. The content will vary whether or not the team is playing that day. The key `status` will always be return and indicate if the team is playing that date or if an error occured. Other keys include the `gameStatus` (mostly the game time or FINAL if the game is over), and a key per team with the score as the value.

#### Example:

	>>> import mls_scores
	>>> mls_scores.getScores('DAL')
	{'status': 'playing', 'DAL': '1', 'gameStatus': 'FINAL', 'MTL': '2'}


### getMarker()

About this function: `getMarker(username)`. This function will parse the tweets from a given user and return the latest one containing the mention of 'goal' or 'but'. The idea is to use that tweet to find who scored.