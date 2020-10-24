from howlongtobeatpy import HowLongToBeat
import requests
from flask import Flask, render_template, request


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

    print("Game Details:")
    print()

    closest_match = r_json[0]
    name = closest_match["name"]
    game_id = closest_match["id"]
    print(f'id: {game_id}')
    print()

    details = {}
    r = requests.get(f'http://api.opencritic.com/api/game/{game_id}')
    r_json = r.json()
    name = r_json["name"]
    details["Name"] = name
    if len(r_json["Companies"]) > 1:
        developer = r_json["Companies"][1]["name"]
    else:
        developer = r_json["Companies"][0]["name"]
    details["Developer"] = developer
    platforms = r_json["Platforms"]
    details["Platforms"] = []
    for platform in platforms:
        details["Platforms"].append(platform["name"])
    genres = r_json["Genres"]
    details["Genres"] = []
    for genre in genres:
        details["Genres"].append(genre["name"])
    firstReleaseDate = r_json["firstReleaseDate"].split("T")[0]
    details["Release"] = firstReleaseDate
    score = round(r_json["topCriticScore"])
    details["Score"] = score
    description = r_json["description"]
    details["Description"] = description
    #logoScreenshot_fullRes = r_json["logoScreenshot"]["fullRes"]
    #logoScreenshot_thumbnail = r_json["logoScreenshot"]["thumbnail"]
    trailer_title = r_json["trailers"][0]["title"]
    details["TrailerTitle"] = trailer_title
    trailer_url = r_json["trailers"][0]["externalUrl"]
    trailer_url = "https://www.youtube.com/embed/" + trailer_url.split('?v=')[1]
    print(f"fixed trailer url: {trailer_url}")
    details["TrailerUrl"] = trailer_url

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
    
    print()
    #print(f"logoScreenshot_fullRes: {logoScreenshot_fullRes}")
    #print(f"logoScreenshot_thumbnail: {logoScreenshot_thumbnail}")
    print(f"trailer title: {trailer_title}")
    print()
    print(f"trailer url: {trailer_url}")
    print()

    _, _, gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url = get_how_long_to_beat(name)
    details["MainTime"] = gameplay_main
    details["ExtraTime"] = gameplay_main_extra
    details["ComplitionTime"] = gameplay_completionist
    details["CoverImage"] = game_image_url

    print("How Long To Beat:")
    print(f'Gameplay Main: {gameplay_main}')
    print(f'Gameplay Main and Extra: {gameplay_main_extra}')
    print(f'Gameplay Completionist: {gameplay_completionist}')
    print(f"game cover image url: {game_image_url}")
    
    return details


def search_by_filters(opencritic_range, how_long_to_beat_range):
    found_it = False
    opencritic_min, opencritic_max = opencritic_range
    how_long_to_beat_min, how_long_to_beat_max = how_long_to_beat_range
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
        return chosen
    else:
        return r_json[0]["name"]


def convert_time_to_beat(time):
    if time != -1:
        if time[-1] == "½":
            time = int(time[:-1]) + 0.5
        else:
            time = int(time)
        return time



input_name = "The Last of us part"
opencritic_range = (50, 85)
how_long_to_beat_range = (7, 14)
#print("Searching by filters:")
#search_by_filters(opencritic_range, how_long_to_beat_range)

print()
print()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex' # chagne later

@app.route('/')
def first_page():
    return render_template('index.html')


@app.route('/index3', methods=['GET', 'POST'])
def signup():
    #form = SignUpForm()
    #if form.is_submitted():
     #   result = request.form
        #return render_template('user.html', result=result)
    #image_file = url_for('static', filename=path)
    """
    description = "In crash 4 we start exactly where we left off in crash 3, and a new adventure awaits our heros."
    details2 = {"Name": 'Cool Game', "CoverImage": "https://howlongtobeat.com/games/80317_Crash_Bandicoot_4_Its_About_Time.jpg", "Developer": "Dev", "Platforms": ["A", "B", "C"], "Genres": ["D", "E", "F"],
     "Release": "2020-10-02", "Score":"85", "MainTime": "13", "ExtraTime": "17", "ComplitionTime": "23", "Description": description,
      "TrailerTitle":"Trailer1", "TrailerUrl": "https://www.youtube.com/embed/JfPlBm-y-U0"}
"""

    # get from first form
    chosen_game = request.form.get("chosen_game")
    if chosen_game == "":
        chosen_game = "Pokemon Sword and Shield"
    print(f"chosen game is: {chosen_game}")
    button_pressed = request.form["submit_btn"]
    print(request.form["submit_btn"])
    # get from second form
    #opencritic_range = (50, 85) 
    #how_long_to_beat_range = (7, 14)

    if button_pressed != "by name":
        min_openCritic = request.form.get("min_openCritic")
        max_openCritic = request.form.get("max_openCritic")
        min_howLongToBeat = request.form.get("min_howLongToBeat")
        max_howLongToBeat = request.form.get("max_howLongToBeat")
    
        print(f"min_openCritic: {min_openCritic}")
        print(f"max_openCritic: {max_openCritic}")
        print(f"min_howLongToBeat: {min_howLongToBeat}")
        print(f"max_howLongToBeat: {max_howLongToBeat}")
        if min_openCritic and max_openCritic and min_howLongToBeat and max_howLongToBeat:
            opencritic_range = (int(min_openCritic), int(max_openCritic))
            how_long_to_beat_range = (int(min_howLongToBeat), int(max_howLongToBeat))
        else:
            opencritic_range = (75, 85)
            how_long_to_beat_range = (7, 14)
        print(f"opencritic_range: {opencritic_range}")
        print(f"how_long_to_beat_range: {how_long_to_beat_range}")
        #print("Searching by filters:")
        chosen_game = search_by_filters(opencritic_range, how_long_to_beat_range)
    details = get_title_details(chosen_game)
    return render_template('index3.html', details=details)
    #return "hello world"

#get_title_details("The Last of Us Remastered")
#get_title_details("The Last of Us Remastered")

if __name__ == '__main__':
    app.run()