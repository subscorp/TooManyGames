from howlongtobeatpy import HowLongToBeat
import requests


def get_how_long_to_beat(input_name):
    results = HowLongToBeat(0).search(input_name)
    if results:
        max_similarity_game = results[0]
        name = max_similarity_game.game_name
        similarity = max_similarity_game.similarity          
        gameplay_main = convert_time_to_beat(max_similarity_game.gameplay_main)
        gameplay_main_extra = convert_time_to_beat(max_similarity_game.gameplay_main_extra)
        gameplay_completionist = convert_time_to_beat(max_similarity_game.gameplay_completionist)
        game_image_url = max_similarity_game.game_image_url
    return name, similarity, gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url


def get_title_details(title_name):
    r = requests.get(f'http://api.opencritic.com/api/game/search?criteria={title_name}')
    r_json = r.json()
    print(len(r_json))
    print(f"Status code: {r.status_code}")
    print()

    print("Content:")
    print()

    closest_match = r_json[0]
    name = closest_match["name"]
    game_id = closest_match["id"]
    print(f'id: {game_id}')
    print()

    r = requests.get(f'http://api.opencritic.com/api/game/{game_id}')
    r_json = r.json()
    name = r_json["name"]
    developer = r_json["Companies"][1]["name"]
    platforms = r_json["Platforms"]
    genres = r_json["Genres"]
    firstReleaseDate = r_json["firstReleaseDate"].split("T")[0]
    score = round(r_json["topCriticScore"])
    description = r_json["description"]
    reviewSummary = r_json["reviewSummary"]
    #logoScreenshot_fullRes = r_json["logoScreenshot"]["fullRes"]
    #logoScreenshot_thumbnail = r_json["logoScreenshot"]["thumbnail"]
    screenshots_fullRes = r_json["screenshots"][0]["fullRes"]
    screenshots_thumbnail = r_json["screenshots"][0]["thumbnail"]
    trailer_title = r_json["trailers"][0]["title"]
    trailer_url = r_json["trailers"][0]["externalUrl"]

    print(f"Name: {name}")
    print()
    print(f"Developer: {developer}")
    print()
    print("Platforms: ")
    for platform in platforms:
        print(platform["name"])
    print()
    print("Genres:")
    for genre in genres:
        print(genre["name"])
    print()
    print(f"Release Date: {firstReleaseDate}")
    print()
    print(f"score: {score}")
    print()
    print(f"description: {description}")
    print()
    if 'summary' in reviewSummary:
        print(f"reviewSummary: {reviewSummary['summary']}")
    print()
    #print(f"logoScreenshot_fullRes: {logoScreenshot_fullRes}")
    #print(f"logoScreenshot_thumbnail: {logoScreenshot_thumbnail}")
    print(f"screenshots fullRes: {screenshots_fullRes}")
    print()
    print(f"screenshots thumbnail: {screenshots_thumbnail}")
    print()
    print(f"trailer title: {trailer_title}")
    print()
    print(f"trailer url: {trailer_url}")
    print()

    _, _, gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url = get_how_long_to_beat(name)
    print("How Long To Beat:")
    print(f'Gameplay Main: {gameplay_main}')
    print(f'Gameplay Main and Extra: {gameplay_main_extra}')
    print(f'Gameplay Completionist: {gameplay_completionist}')
    print(f"game cover image url: {game_image_url}")


def search_by_filters(opencritic_range, how_long_to_beat_range):
    found_it = False
    opencritic_min, opencritic_max = opencritic_range
    how_long_to_beat_min, how_long_to_beat_max = how_long_to_beat_range
    print(f'opencritic_min: {opencritic_min}')
    print(f'opencritic_max: {opencritic_max}')
    print(f'how_long_to_beat_min: {how_long_to_beat_min}')
    print(f'how_long_to_beat_max: {how_long_to_beat_max}')
    print()

    r_json = requests.get('http://api.opencritic.com/api/game?sort=score&time=last90').json()
    print("Top rated recently released games:")
    for i, game_details in enumerate(r_json, 1):
        name = game_details["name"]
        score = round(game_details["topCriticScore"])
        print(f"#{i}")
        print(f'Name: {name}')
        print(f'Score: {score}')
        if score >= opencritic_min and score <= opencritic_max:
            _, _, gameplay_main, _, _, _ = get_how_long_to_beat(name)
            print(f"Gameplay Main: {gameplay_main}")
            if gameplay_main >= how_long_to_beat_min and gameplay_main <= how_long_to_beat_max:
                print("This is the best match!\n")
                found_it = True
                chosen = name
                break
        print()


    if found_it:
        print(f"The chosen game is: {chosen}")
        print(f"Score: {score}")
        print(f"Time to beat: {gameplay_main} Hours")
        get_title_details(chosen)
    else:
        print("no game was found")
        #print(f'Score: {(game_details["topCriticScore"])}')
        print()



def convert_time_to_beat(time):
    if time != -1:
        if time[-1] == "½":
            time = int(time[:-1]) + 0.5
        else:
            time = int(time)
        return time



input_name = "The Last of us part"
opencritic_range = (85, 100)
how_long_to_beat_range = (7, 14)
print("Searching by filters:")
search_by_filters(opencritic_range, how_long_to_beat_range)

print()
print()

#get_title_details("The Last of Us Remastered")
#get_title_details("The Last of Us Remastered")