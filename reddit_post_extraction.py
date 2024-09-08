import json
import pandas as pd
import requests
import time

timeframe = 'year'  # hour, day, week, month, year, all
listing = 'top'  # controversial, best, hot, new, random, rising, top
subreddits = [  # Top SFW 1000 subreddits
    'funny', 'AskReddit', 'gaming', 'worldnews', 'todayilearned', 'aww', 'Music', 'memes', 'movies', 'science',
    'Showerthoughts', 'pics', 'Jokes', 'news', 'videos', 'space', 'askscience', 'DIY', 'books', 'nottheonion',
    'mildlyinteresting', 'EarthPorn', 'food', 'explainlikeimfive', 'GetMotivated', 'LifeProTips', 'gadgets', 'IAmA',
    'Art', 'gifs', 'sports', 'dataisbeautiful', 'Futurology', 'Documentaries', 'UpliftingNews', 'photoshopbattles',
    'personalfinance', 'tifu', 'OldSchoolCool', 'WritingPrompts', 'history', 'nosleep', 'philosophy', 'listentothis',
    'television', 'wholesomememes', 'technology', 'Damnthatsinteresting', 'InternetIsBeautiful', 'wallstreetbets',
    'creepy', 'NatureIsFuckingLit', 'relationship_advice', 'lifehacks', 'nba', 'pcmasterrace', 'interestingasfuck',
    'Fitness', 'dadjokes', 'ContagiousLaughter', 'travel', 'HistoryMemes', 'oddlysatisfying', 'anime', 'Unexpected',
    'MadeMeSmile', 'Bitcoin', 'NintendoSwitch', 'MakeupAddiction', 'oddlyspecific', 'horror', 'JapanTravel',
    'sciencememes', 'bodybuilding', 'Health', 'Astronomy', 'writing', 'DigitalPainting', 'zelda', 'MinecraftMemes',
    'MachineLearning', 'ChildrenFallingOver', 'fantasyfootball', 'atheism', 'somethingimade', 'Meditation', 'mac',
    'humor', 'Android', 'Marvel', 'apexlegends', 'canada', 'antiwork', 'youtubehaiku', 'Filmmakers', 'meirl',
    'whatisthisthing', 'Physics', 'wow', 'likeus', 'hacking', 'harrypotter', 'legaladvice', 'investing', 'crafts',
    'FanTheories', 'vandwellers', 'baseball', 'Boxing', 'CampingandHiking', 'yoga', 'AsianBeauty', 'CollegeBasketball',
    'dogs', 'EDM', 'astrophotography', 'UFOs', 'Fishing', 'oddlyterrifying', 'electronicmusic', 'techsupport',
    'GamePhysics', 'GetStudying', 'Coronavirus', 'Watches', 'comics', 'SweatyPalms', 'lotrmemes', 'webdev',
    '3Dprinting', 'xxfitness', 'OUTFITS', 'tipofmytongue', 'Naruto', 'mlb', 'Twitch', 'PUBATTLEGROUNDS',
    'RelationshipMemes', 'dogecoin', 'BeautyGuruChatter', 'AnimalCrossing', 'popheads', 'Guitar', 'india',
    'natureismetal', 'BuyItForLife', 'analog', 'CasualConversation', 'javascript', 'college', 'budgetfood',
    'CasualUK', 'houseplants', 'ArtPorn', 'FreeEBOOKS', '3amjokes', 'VALORANT', 'NFT', 'Metal', 'BaldursGate3',
    'hockey', 'TrueOffMyChest', 'ArtisanVideos', 'languagelearning', 'thewalkingdead', 'nhl', 'ethtrader', 'Graffiti',
    'youtube', 'StardewValley', 'nintendo', 'financialindependence', 'PixelArt', 'AITAH', 'digitalnomad',
    'WhatsWrongWithYourDog', 'learntodraw', 'terriblefacebookmemes', 'graphic_design', 'ATBGE', 'spotify',
    'povertyfinance', 'PoliticalDiscussion', 'beginnerfitness', 'StupidFood', 'reallifedoodles', '100yearsago',
    'Philippines', 'sidehustle', 'DesignPorn', 'Justrolledintotheshop', 'AskHistorians', 'AbandonedPorn',
    'ShingekiNoKyojin', 'hiking', 'malelivingspace', 'Mommit', 'literature', 'minimalism', 'StrangerThings',
    'urbanexploration', 'australia', 'datascience', 'introvert', 'audiophile', 'ufc', 'Poetry', 'grilling', 'IWantOut',
    'forbiddensnacks', 'Coffee', 'rap', 'perfectlycutscreams', 'ofcoursethatsathing', 'BokuNoHeroAcademia',
    'classicalmusic', 'confusing_perspective', 'AskEngineers', 'mealtimevideos', 'ArchitecturePorn', 'finance', 'Amd',
    'hmmm', 'LongDistance', 'roblox', 'BestofRedditorUpdates', 'disney', 'elonmusk', 'OnePunchMan', '30PlusSkinCare',
    'hearthstone', 'softwaregore', 'homeowners', 'ADHD', 'vinyl', 'AnimeART', 'MangaCollectors', 'powerwashingporn',
    'selfimprovement', 'savedyouaclick', 'reddeadredemption', 'AnimalsBeingGeniuses', 'wallpaper', 'TheLastAirbender',
    'cookingforbeginners', 'realestateinvesting', 'AskAcademia', 'dbz', 'cscareerquestions', 'nvidia', 'ExposurePorn',
    'Satisfyingasfuck', 'lego', 'flexibility', 'Cinemagraphs', 'smallbusiness', 'JuJutsuKaisen', 'halo', 'OpenAI',
    'cyberpunkgame', 'algotrading', 'AbsoluteUnits', 'TattooDesigns', 'Makeup', 'RoomPorn', 'RealEstate',
    'Skincare_Addiction', 'aviation', 'sewing', 'vegan', 'carporn', 'getdisciplined', 'startups', 'photocritique',
    'netflix', 'HouseOfTheDragon', 'architecture', 'Screenwriting', 'AskUK', 'hbo', 'learnart', 'CryptoMarkets',
    'Fallout', 'gamedev', 'PoliticalHumor', 'jobs', 'LatinoPeopleTwitter', 'womensstreetwear', 'RocketLeague',
    'HunterXHunter', 'iamverysmart', 'thalassophobia', 'tennis', 'Journaling', 'worldbuilding', 'specializedtools',
    'PerfectTiming', 'Cricket', 'snowboarding', 'CharacterAI', 'environment', 'MachinePorn', 'fragrance',
    'theydidthemath', 'rpg', 'DotA2', 'MovieSuggestions', 'childfree', 'StartledCats', 'virtualreality', 'Basketball',
    'DisneyPlus', 'HumansAreMetal', 'thatHappened', 'crossfit', 'skiing', 'Bossfight', 'Weird', 'PersonalFinanceCanada',
    'KerbalSpaceProgram', 'astrology', 'cringepics', 'climbing', 'AskEurope', 'olympics', 'NationalPark', 'SpecArt', 'AskHR', 
    'TheWayWeWere', 'truegaming', 'tumblr', 'Helldivers', 'UKPersonalFinance', 'Zoomies', 'AnimeSketch', 'funnyvideos', 
    'Pizza', 'acne', 'animation', 'ShouldIbuythisgame', 'HobbyDrama', 'ifyoulikeblank', 'Terraria', 'BollyBlindsNGossip', 
    'Mindfulness', 'Sims4', 'CreditCards', 'Simulated', 'privacy', 'wholesomeanimemes', 'socialmedia', 'LofiHipHop', 
    'TwoSentenceHorror', 'linux', 'IWantToLearn', 'MechanicAdvice', 'crochet', 'Paranormal', 'BrandNewSentence', 'NASCAR', 
    'singapore', 'Colorization', 'Europetravel', 'simpleliving', 'nostalgia', 'UrbanHell', 'Nike', 'marketing', 
    'BotanicalPorn', 'CryptoTechnology', 'beermoney', 'chess', 'gifsthatkeepongiving', 'Catswithjobs', 'DidntKnowIWantedThat', 
    'AskEconomics', 'PraiseTheCameraMan', 'mashups', 'babyelephantgifs', 'chemicalreactiongifs', 'curlyhair', 'indiasocial', 
    'EngineeringPorn', 'golf', 'ImTheMainCharacter', 'japan', 'MechanicalKeyboards', 'awesome', 'IllegallySmolCats', 
    'thisismylifenow', 'smashbros', 'Python', 'playstation', 'FrugalFemaleFashion', 'whatsthisplant', 'thenetherlands', 
    'FinancialCareers', 'SipsTea', 'midjourney', 'HydroHomies', 'FellowKids', 'freefolk', 'TheSimpsons', 'london', 
    'Hololive', 'PhotoshopRequest', 'blender', 'headphones', 'help', 'BeforeNAfterAdoption', 'ANormalDayInRussia', 
    'agedlikemilk', 'MostBeautiful', 'WhyWereTheyFilming', 'ramen', 'Hulu', 'tippytaps', 'holdmyredbull', 'booksuggestions', 
    'Disneyland', 'DecidingToBeBetter', 'TheDepthsBelow', 'AMA', 'options', 'Bundesliga', 'vagabond', 'electronics', 
    'minipainting', 'whatcouldgoright', 'discordapp', 'witcher', 'resumes', 'whatsthisbug', 'Glitch_in_the_Matrix', 
    'AmazonPrimeVideo', 'mildlysatisfying', 'VintageFashion', 'indiameme', 'RetroFuturism', 'DCcomics', 'bicycling', 
    'homegym', 'dndmemes', 'birdswitharms', 'Brawlstars', 'Aquariums', 'beards', 'Dogtraining', 'EASportsFC', 'boxoffice', 
    'evilbuildings', 'lgbt', 'Conservative', 'MUAontheCheap', 'Superstonk', 'BitcoinBeginners', 'woooosh', 'gravityfalls', 
    'NotMyJob', 'ffxiv', 'ApplyingToCollege', 'UnusualVideos', 'brooklynninenine', 'wheredidthesodago', 'wholesomegifs', 
    'airpods', 'ZeroWaste', 'GooglePixel', 'rnb', 'AnimeFunny', 'ThingsCutInHalfPorn', 'btc', 'im14andthisisdeep', 
    'AccidentalRenaissance', 'Moviesinthemaking', 'Teachers', 'Minecraftbuilds', 'wiiu', 'tooktoomuch', 'bollywood', 
    'futbol', '3DS', 'JustGuysBeingDudes', 'confidentlyincorrect', 'PokemonGoFriends', 'Breadit', 'VietNam', 
    'PokemonScarletViolet', 'LeopardsAteMyFace', 'CatsWithDogs', 'GPT3', 'weddingplanning', 'Turkey', 'blessedimages', 
    'weirddalle', 'ClashRoyale', '3Dmodeling', 'ThatLookedExpensive', 'landscaping', 'wholesome', 'italy', 'CityPorn', 
    'Animesuggest', 'bleach', 'EconomicHistory', 'IndoorGarden', 'economy', 'hometheater', '2007scape', 'AskCulinary', 
    'Autos', 'AskAnAmerican', 'HomeDecorating', 'futurama', 'FunnyandSad', 'WeWantPlates', 'korea', 'crappyoffbrands', 
    'everymanshouldknow', 'Funnymemes', 'ask', 'microsoft', 'dogpictures', 'RobinHood', 'burgers', 'puns', 'manhwa', 
    'Breath_of_the_Wild', 'SkincareAddicts', 'ihadastroke', 'warriors', 'Twitter', 'Handwriting', 'westworld', 
    'Spiderman', 'EscapefromTarkov', 'lakers', 'notinteresting', 'nbadiscussion', 'corgi', 'blunderyears', 
    'youngpeopleyoutube', 'parrots', 'photoshop', 'beauty', 'lotr', 'cycling', 'mechanical_gifs', 'ireland', 
    'TalesFromTheFrontDesk', 'hiphop101', 'Pareidolia', 'Eminem', 'notliketheothergirls', 'Cruise', 'antimeme', 
    'megalophobia', 'xboxinsiders', 'nflmemes', 'TrueCrimePodcasts', 'GrandPrixRacing', 'Warhammer40k', 'CabinPorn', 
    'asoiaf', 'PanPorn', 'SquaredCircle', 'buildapcsales', 'AskPhysics', 'jacksepticeye',
    'Instagram', 'tattoo', 'HaircareScience', 'singing', 'intermittentfasting', 'oilpainting', 'gamernews', 'sysadmin', 'NoMansSkyTheGame', 
    'bonehurtingjuice', 'mexicanfood', 'hiphopvinyl', 'malaysia', 'cybersecurity', 'GameDeals', 'destiny2', 'poland', 'formuladank', 
    'betterCallSaul', 'RedditLaqueristas', 'ImaginaryArchitecture', 'TheSilphRoad', 'KDRAMA', 'NewToReddit', 'PourPainting', 
    'netflixwitcher', 'ScottishPeopleTwitter', 'Starfield', 'rupaulsdragrace', 'nyc', 'InteriorDesign', 'dogswithjobs', 'Watercolor', 
    'DadReflexes', 'catpics', 'PandR', 'worldcup', 'artificial', 'surrealmemes', 'Romania', 'fantasywriters', 'LegalAdviceUK', 
    'web_design', 'aliens', 'football', 'GodofWarRagnarok', 'MLS', 'freebies', 'piano', 'intel', 'PenmanshipPorn', 
    'MarvelStudiosSpoilers', 'GreatBritishMemes', 'casualiama', 'britishproblems', 'Prematurecelebration', 'ontario', 'Metalcore', 
    'FinancialPlanning', 'tea', 'startrek', 'AnimeMusicVideos', 'eupersonalfinance', 'Cyberpunk', 'IndiaSpeaks', 'BadDesigns', 
    'tf2', 'creepypasta', 'IndianFood', 'CrossStitch', 'germany', 'Kanye', 'AppleWatch', 'FullmetalAlchemist', 'SpyxFamily', 
    'Illustration', 'bestoflegaladvice', 'Embroidery', 'findfashion', 'Scams', 'IndiaCricket', 'AskScienceFiction', 
    'GameTheorists', 'Accounting', 'billieeilish', 'pasta', 'metalworking', 'AwesomeCarMods', 'Cheap_Meals', 'melbourne', 
    'developersIndia', 'CleaningTips', 'femalelivingspace', 'learnpython', 'HonkaiStarRail', 'spain', 'nursing', 'Jazz', 
    'doctorwho', 'gatekeeping', 'MakeNewFriendsHere', 'AutoDetailing', 'VaporwaveAesthetics', 'PuppySmiles', 'Patriots', 
    'Anticonsumption', 'Wallstreetbetsnew', 'malegrooming', 'KoreanFood', 'cosplayprops', 'rapbattles', 'lostredditors', 
    'whitepeoplegifs', 'technews', 'shortscarystories', 'fantasybball', 'bjj', 'delhi', 'easyrecipes', 'NailArt', 
    'manganews', 'UkraineWarVideoReport', 'CampingGear', 'OldPhotosInRealLife', 'eu_nvr', 'Ghosts', 'EngineeringStudents', 
    'community', 'onejob', 'imsorryjon', 'dankchristianmemes', 'pathofexile', 'streetwearstartup', 'sweden', 'smarthome', 
    'EatCheapAndVegan', 'engrish', 'CrazyIdeas', 'piercing', 'toronto', 'Tools', 'goldenretrievers', 'dndnext', 'magicTCG', 
    'Cartalk', 'geography', 'AskOuija', 'HollowKnight', 'LiminalSpace', 'seriouseats', 'Rabbits', 'vegetarian', 
    'badeconomics', 'BackYardChickens', 'DataHoarder', 'ImaginaryLandscapes', 'talesfromtechsupport', 'onebag', 'tearsofthekingdom', 
    'xbox', 'botecodoreddit', 'lawncare', 'Cawwsplay', 'pitbulls', 'redneckengineering', 'NFL_Draft', 'apolloapp', 
    'smoking', 'BlackPink', 'holdmycatnip', 'edmproduction', 'plotholes', 'googlehome', 'centuryhomes', 'NotHowGirlsWork', 
    'amv', 'playboicarti', 'Cheese', 'WitchesVsPatriarchy', 'TwoHotTakes', 'WhatsWrongWithYourCat', 'IndianStockMarket', 
    'AskElectronics', 'Marriage', 'BritishTV', 'PeterExplainsTheJoke', 'subnautica', 'yugioh', 'GradSchool', 'AskOldPeople', 
    'ConvenientCop', 'ClimbingPorn', 'AnimalsOnReddit', 'Costco', 'chinesefood', 'holdmyjuicebox', 'WhyWomenLiveLonger', 
    'Warframe', 'medicalschool', 'plantclinic', 'FindTheSniper', 'KitchenConfidential', 'hmm', 'DesignMyRoom', 'Awww', 
    'canadatravel', 'assassinscreed', 'SCP', 'happy', 'offbeat', 'sustainability', 'FantasyPL', 'InfrastructurePorn', 
    'championsleague', 'SteamDeck', 'WildernessBackpacking', 'excel', 'batman', 'LawSchool', 'calvinandhobbes', 'WorkReform', 
    'nope', 'Catloaf', 'PetiteFashionAdvice', 'pelotoncycle', 'beyondthebump', 'VisitingHawaii', 'dontdeadopeninside', 
    'recruitinghell', 'foraging', 'steak', 'MonsterHunter', 'selfie', 'redditgetsdrawn', 'awwwtf', 'LearnUselessTalents', 
    'PunPatrol', 'outside', 'Markiplier', 'ThailandTourism', 'ArtificialInteligence', 'comedyhomicide', 'cardano', 
    'snakes', 'homelab', 'Buddhism', 'premed', 'ClashOfClans', 'mumbai', 'toolporn'
]

def get_reddit(subreddit, listing, timeframe, after=None):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit=100&t={timeframe}'
        if after:
            base_url += f'&after={after}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
        
        # Capture the rate limit headers
        rate_limit_used = request.headers.get('X-Ratelimit-Used')
        rate_limit_remaining = request.headers.get('X-Ratelimit-Remaining')
        rate_limit_reset = request.headers.get('X-Ratelimit-Reset')

        # Convert the rate limit values to float, then to int if necessary
        rate_limit_used = float(rate_limit_used) if rate_limit_used else None
        rate_limit_remaining = float(rate_limit_remaining) if rate_limit_remaining else None
        rate_limit_reset = float(rate_limit_reset) if rate_limit_reset else None

        # Print the rate limit information
        print(f"Rate Limit Used: {rate_limit_used}")
        print(f"Rate Limit Remaining: {rate_limit_remaining}")
        print(f"Rate Limit Resets In: {rate_limit_reset} seconds")

        # Check rate limit remaining and apply the kill switch
        if rate_limit_remaining == 1 and rate_limit_reset:
            sleep_time = int(rate_limit_reset) + 1
            print(f"Rate limit almost exhausted. Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
        
    except Exception as e:
        print(f'An Error Occurred: {e}')
    
    return request.json()

def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score, and Number of Comments.
    '''
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['id']] = {
            'subreddit': post['data']['subreddit_name_prefixed'],
            'title': post['data']['title'],
            'upvotes': post['data']['ups'],
            'downvotes': post['data']['downs'],
            'score': post['data']['score'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'comments': post['data']['num_comments'],
            'views': post['data']['view_count'],
            'created_date': post['data']['created'],
            'url': post['data']['url']
        }
    temp_df = pd.DataFrame.from_dict(myDict, orient='index')
    return temp_df

if __name__ == '__main__':
    df = pd.DataFrame()  # Initialize an empty DataFrame to store the results
    for subreddit in subreddits:
        after = None
        for batch in range(10):  # Fetch 10 batches (100 posts per batch); 1000 posts per subreddit limit
            print(f"Fetching batch {batch+1} for {subreddit}")
            r = get_reddit(subreddit, listing, timeframe, after)
            temp_df = get_results(r)
            df = pd.concat([df, temp_df], ignore_index=True)
            
            # Update 'after' with the last post ID from the current batch
            after = r['data'].get('after', None)
            
            if after is None:
                break  # Stop if no more posts to fetch
    
    # Save the DataFrame to a CSV file
    df.to_csv('reddit_top_posts.csv', index=False)
    print("DataFrame saved as 'reddit_top_posts.csv'.")
