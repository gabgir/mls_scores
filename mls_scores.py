import urllib2
import datetime

# today = str(datetime.date.today())
# today = '2015-05-23'
# team = 'MTL'

def getScores(team,date=str(datetime.date.today())):
	## enter two or three letters team name as argument, game date as optional argument (format 'yyyy-mm-dd')
	## returns a dictionnary. Struture will change if team is playing on date or not.
	## if playing, first key is 'status' = 'playing'
	## then 'first club name' = 'score'
	## then 'second club name' = 'score'
	## if not playing, only key is 'status'='not playing'


	try:
		## parse html from mls website
		url = 'http://www.mlssoccer.com/scores'
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		page = response.read()
	
		data = urllib2.unquote(str(page))
	
		## isolate the html code about the wanted match
		
		# this function iterate to find all the occurence of the date
		# it hence finds all the html game blocks for that day.
		def find_all(a_str, sub):
			start = 0
			while True:
				start = a_str.find(sub, start)
				if start == -1: return
				yield start
				start += len(sub) # use start += 1 to find overlapping matches

		gamesAtDate = find_all(data,"'"+date)


		# find if team plays at that date
		startIdx = -1
		for game in gamesAtDate:
			stopIdx = data.find(']',game)

			if data[game:stopIdx].find(team) != -1:
				startIdx = game
				
	
		# check if team is playing at date and isolate the info.
		if startIdx != -1:
			aBeginIdx = data.find('<a',startIdx)+2
			aEndIdx = data.find('</a>',aBeginIdx)
		
			scoreSection = data[aBeginIdx:aEndIdx]
		
			## First club
			firstClubBeginIdx = scoreSection.find('"club"')+7
			firstClubEndIdx = scoreSection.find('</',firstClubBeginIdx)
			firstClubName = scoreSection[firstClubBeginIdx:firstClubEndIdx]
			firstClubScoreBeginIdx = scoreSection.find('score')+7
			firstClubScoreEndIdx = scoreSection.find('</',firstClubScoreBeginIdx)
			firstClubScore = scoreSection[firstClubScoreBeginIdx:firstClubScoreEndIdx]
		
			# print firstClubName
			# print firstClubScore.strip() # strip to remove whitespaces
		
			## Second Club
			SecondClubBeginIdx = scoreSection.find('"club"',firstClubEndIdx)+7
			SecondClubEndIdx = scoreSection.find('</',SecondClubBeginIdx)
			SecondClubName = scoreSection[SecondClubBeginIdx:SecondClubEndIdx]
			SecondClubScoreBeginIdx = scoreSection.find('score',SecondClubBeginIdx)+7
			SecondClubScoreEndIdx = scoreSection.find('</',SecondClubScoreBeginIdx)
			SecondClubScore = scoreSection[SecondClubScoreBeginIdx:SecondClubScoreEndIdx]
		
			# print SecondClubName
			# print SecondClubScore.strip() # strip to remove whitespaces

			## retrieve time status
			gameStatusBeginIdx = scoreSection.find('class="time"')+13
			gameStatusEndIdx = scoreSection.find('</',gameStatusBeginIdx)
			gameStatus = scoreSection[gameStatusBeginIdx:gameStatusEndIdx]
			# print gameStatus

	
			## create answer dict
			answer = dict([('status','playing'),(firstClubName,firstClubScore.strip()),(SecondClubName,SecondClubScore.strip()),('gameStatus',gameStatus.strip())])
		
		# if team is not playing
		else:
			answer = dict([('status','not playing')])
	
		return answer
	
	except:
		answer = dict([('status','could not retrieve info.')])
		return answer