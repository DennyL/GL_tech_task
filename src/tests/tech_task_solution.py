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


def single_key_parser(obj, key):
    """takes two positional arguments: an array (obj) with a json file content, and the key to be found in it.
    Returns a chunk of the array belonging to the key given"""
    results = []
    if isinstance(obj, dict):
        if key in obj.keys():
            results.append(obj[key])
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                results += single_key_parser(v, key)
    if isinstance(obj, list):
        if key in obj:
            results.append(key)
        for i in obj:
            if isinstance(i, (dict, list)):
                results += single_key_parser(i, key)
    return results


def two_keys_parser(obj, *args):
    """takes two positional arguments: an array (obj) with a json file content, and two keys as args.
    Returns a chunk of the array where both the keys are present"""
    k1, k2 = args
    results = []
    if isinstance(obj, dict):
        if k1 in obj.keys() and k2 in obj.keys():
            results.append(obj)
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                results += two_keys_parser(v, *args)
    if isinstance(obj, list):
        if k1 in obj and k2 in obj:
            results.append(obj)
        for i in obj:
            if isinstance(i, (dict, list)):
                results += two_keys_parser(i, *args)
    return results


def get_audio(path2json: str) -> str:
    """takes one positional argument: path to the json file as a string.
    Returns info about the audio stream in the file"""
    json_content = get_json_content(path2json)
    audio_in_array = single_key_parser(json_content, 'Audio')
    if len(audio_in_array) == 0:
        return 'No audio in the TS found'
    else:
        return 'Audio in the TS file: {}'.format(audio_in_array)


def get_logos(path2json: str) -> str:
    """takes one positional argument: path to the json file as a string.
    Returns info about logos in video block of the file, of their number and location on the screen"""
    results = []
    json_content = get_json_content(path2json)
    video_in_json = single_key_parser(json_content, 'Video')
    logos_in_array = single_key_parser(video_in_json, 'Logos')
    if len(logos_in_array) > 0:
        x_coordinates = single_key_parser(logos_in_array, 'X')
        y_coordinates = single_key_parser(logos_in_array, 'Y')
        logos_coordinates = zip(x_coordinates, y_coordinates)
        logos_number = len(x_coordinates)
        results.append('{} logos found in the video:'.format(logos_number))
        for num, coordinates in enumerate(logos_coordinates):
            results.append('{} logo with coordinates: {}. Location on screen: {}'.format(
                num + 1, coordinates, 'RIGHT' if coordinates[0] > 860 else 'LEFT'))
    else:
        results.append('No logos in the video found')
    return '\n'.join(results)


def get_video_pid_hex(path2json):
    """takes one positional argument: path to the json file as a string.
    Returns a hex value of video PID in the file"""
    json_content = get_json_content(path2json)
    video = single_key_parser(json_content, 'Video')
    video_media_id = single_key_parser(video, 'MediaID')[0]
    media_id_pid_list = two_keys_parser(json_content, 'MediaID', 'PID')
    if len(media_id_pid_list) > 0:
        for chunk in media_id_pid_list:
            for k, v in chunk.items():
                if video_media_id == chunk[k]:
                    return 'Video PID in hex: {}'.format(hex(chunk['PID']))
    return 'Video PID not found'


if __name__ == '__main__':
    path = '../json_files/ts_info.json'
    print(get_audio(path))
    print(get_logos(path))
    print(get_video_pid_hex(path))
