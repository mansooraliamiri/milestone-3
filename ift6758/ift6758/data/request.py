import requests

#import utils
from utils import utils




class RequestNHL():
    nb_games = {30: 1230, 31:1271, 32:1353}
    #base_url = "https://statsapi.web.nhl.com/api/v1/"

    base_url = "https://api-web.nhle.com/v1/"
    # get_game: https://statsapi.web.nhl.com/api/v1/  game/  {$season} -> https://api-web.nhle.com/v1/skater-stats-leaders/20222023/3
    # get_game: https://api-web.nhle.com/v1/player/8478402/game-log/20232024/2
    #teams_url = base_url + 'teams'
    #https://api-web.nhle.com/v1/club-schedule-season/TOR/20232024
    teams_url = 'https://api.nhle.com/stats/rest/en/team/summary?cayenneExp='

    '''
    @classmethod
    def get_game(self, season: int, id = int, regular = True) -> object:
        """
        Get a game data

        Args:
            season (int): The first year of the season to retrieve, i.e. for the 2016-17
                season you'd put in 2016
            if (int): The id of the game to retrive
        """
        #theme: https://statsapi.web.nhl.com/api/v1/game/20222023/02/game_id/feed/live
        season = str(season)
        game_id = f"{id:04d}"
        url = self.base_url + 'game/' + season
        # if regular game we add to the url 02 and if it is playoff we add 03
        url += '02' if regular else '03'
        url += game_id
        url += '/feed/live'
        return requests.get(url).json()
    '''
    @classmethod
    def get_game(self, season: int, id = int, regular = True) -> object:
        """
        Get a game data

        Args:
            season (int): The first year of the season to retrieve, i.e. for the 2016-17
                season you'd put in 2016
            if (int): The id of the game to retrive
        """
        #https://api-web.nhle.com/v1/player/8478402/game-log/20232024/2
        season = str(season)
        game_id = f"{id:04d}"
        #https://api-web.nhle.com/v1/gamecenter/{GAME_ID}/play-by-play
        #player/8478402/game-log/20232024/2
        url = self.base_url + 'gamecenter/'
        url += game_id
        url += "/play-by-play"
        #url += season
        # if regular game we add to the url 02 and if it is playoff we add 03
        #url += '/2' if regular else '/3'
        #print('game link ======== ', url)
        try:
            
            data = requests.get(url).json()
            #response.raise_for_status()  # Raises an HTTPError if the response status code is not in the 2xx range
            # Process the response content here
            #print(response.text)
            return data
        except requests.exceptions.HTTPError as http_error:
            print(f" :: HTTP error occurred: {http_error}\n")
            return None
        except requests.exceptions.ConnectionError as connection_error:
            print(f" :: Connection error occurred: {connection_error}\n")
            return None
        except requests.exceptions.Timeout as timeout_error:
            print(f" :: Request timeout occurred: {timeout_error}\n")
            return None
        except requests.exceptions.TooManyRedirects as redirects_error:
            print(f" :: Too many redirects occurred: {redirects_error}\n")
            return None
        except requests.exceptions.RequestException as request_exception:
            print(f" :: Error occurred during the request: {request_exception}\n")
            return None
        #return requests.get(url).json()

    '''    
    @classmethod
    def nb_regular_games(self, season: int) -> int:
        """
        Get the number of regulars games for the specified season

        Args:
            season (int): The first year of the season to retrieve, i.e. for the 2016-17
                season you'd put in 2016
        """
        # season_fullname = season + str(int(season)+1)
        season_fullname = utils.season_full_name(season)
        teams = requests.get(self.teams_url, params={"season": season_fullname})
        teams = teams.json()
        return self.nb_games[len(teams["teams"])]
    '''

    @classmethod
    def nb_regular_games(self, season: int) -> int:
        """
        Get the number of regulars games for the specified season

        Args:
            season (int): The first year of the season to retrieve, i.e. for the 2016-17
                season you'd put in 2016
        """
        # season_fullname = season + str(int(season)+1)
        season_fullname = utils.season_full_name(season)
        #print('season_fullname: ',season_fullname)
        data = None
        try:
            url= 'https://api.nhle.com/stats/rest/en/game'
            data = requests.get(url)
            #response.raise_for_status()  # Raises an HTTPError if the response status code is not in the 2xx range
            # Process the response content here
            #print(response.text)
        except requests.exceptions.HTTPError as http_error:
            print(f" :: HTTP error occurred: {http_error}\n")
            return None
        except requests.exceptions.ConnectionError as connection_error:
            print(f" :: Connection error occurred: {connection_error}\n")
            return None
        except requests.exceptions.Timeout as timeout_error:
            print(f" :: Request timeout occurred: {timeout_error}\n")
            return None
        except requests.exceptions.TooManyRedirects as redirects_error:
            print(f" :: Too many redirects occurred: {redirects_error}\n")
            return None
        except requests.exceptions.RequestException as request_exception:
            print(f" :: Error occurred during the request: {request_exception}\n")
            return None
        
        
        #data = requests.get('https://api.nhle.com/stats/rest/en/game')
        #response = requests.get('https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=', params={"seasonId": season_fullname,"gameTypeId":3})
        #response = requests.get('https://api.nhle.com/stats/rest/en/team/summary?')
        #response = requests.get('https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId={$season}%20and%20gameTypeId=3')
        #print('games: ',games.json())
        games = data.json()
        filtered_data = [game for game in games["data"] if game["season"] == int(season_fullname)]
        filtered_data = [game for game in games["data"] if game["season"] == int(season_fullname)]
        #filtered_games = [game for game in games["data"] if game["season"] == season_fullname]
        #filtered_games = list(filter(filter_games, games["data"],season_fullname))
        #print('filtered_games: ',filtered_data)
        id_list = [item['id'] for item in filtered_data]
        #print('id_list: ',id_list)
        #teams = response.json()
        #print(len(teams["data"]))
        return  id_list#self.nb_games[len(teams["teams"])]
    