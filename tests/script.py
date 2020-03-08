import json


def get_json_content(path_to_file: str) -> dict:
    """takes one positional argument: path to a json file.
    Returns content of a JSON file available by the path, if the file is valid"""
    try:
        with open(path_to_file, encoding='utf-8') as file:
            content = json.load(file)
    except json.JSONDecodeError:
        raise Exception('Invalid JSON file')
    return content


def parser(obj, key: str):
    """takes two positional arguments: an array (obj) with a json file content, and the key to be found in it.
    Returns a chunk of the array belonging to the key given"""
    results = []
    if isinstance(obj, dict):
        if key in obj.keys():
            results.append(obj[key])
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                results += parser(v, key)
    if isinstance(obj, list):
        if key in obj:
            results.append(key)
        for i in obj:
            if isinstance(i, (dict, list)):
                results += parser(i, key)
    return results


def get_audio(path2json: str) -> str:
    """takes one positional argument: path to the json file as a string.
    Returns info about the audio stream in the file"""
    json_content = get_json_content(path2json)
    audio_in_array = parser(json_content, 'Audio')
    if len(audio_in_array) == 0:
        return 'No audio in the TS found'
    else:
        return 'Audio un the TS file: {}'.format(audio_in_array)


def get_logos(path2json: str) -> str:
    """takes one positional argument: path to the json file as a string.
    Returns info about logos in video block of the file, of their number and location on the screen"""
    results = []
    json_content = get_json_content(path2json)
    video_in_json = parser(json_content, "Video")
    logos_in_array = parser(video_in_json, "Logos")
    if len(logos_in_array) > 0:
        x_coordinates = parser(logos_in_array, 'X')
        y_coordinates = parser(logos_in_array, 'Y')
        logos_coordinates = zip(x_coordinates, y_coordinates)
        logos_number = len(x_coordinates)
        results.append('{} logos in the video were found:'.format(logos_number))
        for n, i in enumerate(logos_coordinates):
            results.append(
                '{} logo with coordinates: {}. Location on screen: {}'.format(n+1, i, 'RIGHT' if i[0] > 860 else 'LEFT')
            )
    else:
        results.append('No logos in the video found')
    return "\n".join(results)


def get_pid():
    pass


if __name__ == '__main__':
    path = '../src/ts_info.json'
    print(get_audio(path))
    print(get_logos(path))



