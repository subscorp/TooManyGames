from howlongtobeatpy import HowLongToBeat
import requests
from flask import Flask, render_template, request


def get_how_long_to_beat(input_name):
    results = HowLongToBeat(0).search(input_name)
    if results:
        max_similarity_game = results[0]
        gameplay_main = convert_time_to_beat(max_similarity_game.gameplay_main)
        gameplay_main_extra = convert_time_to_beat(max_similarity_game.gameplay_main_extra)
        gameplay_completionist = convert_time_to_beat(max_similarity_game.gameplay_completionist)
        game_image_url = max_similarity_game.game_image_url
    else:
        gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url =  -1, -1, -1, None
    return gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url


def get_title_details(title_name):
    r = requests.get(f'http://api.opencritic.com/api/game/search?criteria={title_name}')
    r_json = r.json()
    closest_match = r_json[0]
    name = closest_match["name"]
    game_id = closest_match["id"]
    r = requests.get(f'http://api.opencritic.com/api/game/{game_id}')
    r_json = r.json()
    name = r_json["name"]
    if len(r_json["Companies"]) > 1:
        developer = r_json["Companies"][1]["name"]
    else:
        developer = r_json["Companies"][0]["name"]
    platforms = r_json["Platforms"]
    genres = r_json["Genres"]
    firstReleaseDate = r_json["firstReleaseDate"].split("T")[0]
    score = round(r_json["topCriticScore"])
    description = r_json["description"]
    trailer_title = r_json["trailers"][0]["title"]
    trailer_url = r_json["trailers"][0]["externalUrl"]
    trailer_url = "https://www.youtube.com/embed/" + trailer_url.split('?v=')[1]
    gameplay_main, gameplay_main_extra, gameplay_completionist, game_image_url = get_how_long_to_beat(name)

    details = {"Name": name, "Developer": developer, "Release": firstReleaseDate,
    "Score": score, "Description": description, "TrailerTitle": trailer_title, "TrailerUrl": trailer_url,
    "MainTime": gameplay_main, "ExtraTime": gameplay_main_extra, "ComplitionTime": gameplay_completionist, "CoverImage": game_image_url}

    if not game_image_url:
        details["CoverImage"] = r_json["screenshots"][0]["fullRes"]
    details["Platforms"] = []
    for platform in platforms:
        details["Platforms"].append(platform["name"])
    details["Genres"] = []
    for genre in genres:
        details["Genres"].append(genre["name"])
    return details


def search_by_filters(opencritic_range, how_long_to_beat_range):
    found_it = False
    opencritic_min, opencritic_max = opencritic_range
    how_long_to_beat_min, how_long_to_beat_max = how_long_to_beat_range

    r_json = requests.get('http://api.opencritic.com/api/game?sort=score&time=last90').json()
    print("Top rated recently released games:")
    for i, game_details in enumerate(r_json, 1):
        name = game_details["name"]
        score = round(game_details["topCriticScore"])
        print(f"#{i}")
        print(f'Name: {name}')
        print(f'Score: {score}')
        if score >= opencritic_min and score <= opencritic_max:
            gameplay_main, _, _, _ = get_how_long_to_beat(name)
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


def handle_bad_inputs(min_val, max_val):
    if min_val <= 0:
        min_val = 1
    if min_val > 100:
        min_val = 100
    if max_val <= 0:
        max_val = 1
    if max_val > 100:
        max_val = 100
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    
    return min_val, max_val


"""
Credit for the following function:
source: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
author profile: https://stackoverflow.com/users/355230/martineau
"""
def is_number(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


app = Flask(__name__)
@app.route('/', methods=["GET"])
def first_page():
    return render_template('index.html')


@app.route('/index2', methods=["GET"])
def about_page():
    return render_template('index2.html')


@app.route('/index3', methods=['POST'])
def result_page():
    # get from first form
    chosen_game = request.form.get("chosen_game")
    if chosen_game == "":
        # default name
        chosen_game = "Pokemon Sword and Shield" 
    print(f"chosen game is: {chosen_game}")
    button_pressed = request.form["submit_btn"]

    # get from second form
    if button_pressed != "by name":
        min_openCritic = request.form.get("min_openCritic")
        max_openCritic = request.form.get("max_openCritic")
        min_howLongToBeat = request.form.get("min_howLongToBeat")
        max_howLongToBeat = request.form.get("max_howLongToBeat")
    
        if is_number(min_openCritic) and is_number(max_openCritic) and is_number(min_howLongToBeat) and is_number(max_howLongToBeat):
            min_openCritic, max_openCritic, min_howLongToBeat, max_howLongToBeat = int(min_openCritic), int(max_openCritic), int(min_howLongToBeat), int(max_howLongToBeat)

            min_openCritic, max_openCritic = handle_bad_inputs(min_openCritic, max_openCritic)
            min_howLongToBeat, max_howLongToBeat = handle_bad_inputs(min_howLongToBeat, max_howLongToBeat)
            opencritic_range = (min_openCritic, max_openCritic)
            how_long_to_beat_range = (min_howLongToBeat, max_howLongToBeat)
        else:
            # default vals
            opencritic_range = (75, 85)
            how_long_to_beat_range = (7, 14)
        print(f"opencritic_range: {opencritic_range}")
        print(f"how_long_to_beat_range: {how_long_to_beat_range}")
        chosen_game = search_by_filters(opencritic_range, how_long_to_beat_range)
        print(f"chosen game is: {chosen_game}")
    details = get_title_details(chosen_game)
    return render_template('index3.html', details=details)


if __name__ == '__main__':
    app.run()