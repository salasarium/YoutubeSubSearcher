from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup


def sub_search(vid, query):
    try:
        raw_sub = YouTubeTranscriptApi.get_transcript(vid, languages=['ru'])
    except:
        raw_sub = [{'text': ''}]

    sublink_array = []
    for i in range(len(raw_sub)):
        if query in raw_sub[i]['text']:
            sub = raw_sub[i]['text']
            print("Найдено: ", sub)
            start = round(raw_sub[i]['start']) - 3
            link = 'https://www.youtube.com/watch?v=' + vid + '&t=' + str(start) + 's'
            print("Таймлинк: ", link)
            sublink=[sub,link]
            sublink_array.append(sublink)

    # pprint(sublink_array)
    return sublink_array


def get_videoid(playlist_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

    r = requests.get(url=playlist_url, headers=headers)
    src = r.text
    with open("../../index.html", "w") as file:
        file.write(src)

    soup = BeautifulSoup(src, "lxml")

    # channel_title = soup.title
    # print(channel_title.text)

    scripts = soup.find_all("script")
    string = str(scripts[-6])
    string = string[59:-10]
    data = json.loads(string)

    data = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']["sectionListRenderer"]['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

    video_ids = []
    for item in data:
        if 'playlistVideoRenderer' in item:
            video_id = str(item['playlistVideoRenderer']['videoId'])
            video_ids.append(video_id)
    print('Количество видео: ', len(video_ids))
    print("Получены ID video: ", video_ids)
    return(video_ids)


def Youtube_Sub_Searcher(url, q):
    video_ids = get_videoid(url)
    result = {}
    for video_id in video_ids:
        result.update(sub_search(video_id, q))
    return result

if __name__ == '__main__':
    test_url = "https://www.youtube.com/playlist?list=UUCKcF--89LBIP6Q5eaWXwJw"  # change this
    test_q = 'семья' # change this 

    xxx = Youtube_Sub_Searcher(test_url, test_q)
    print(len(xxx))
    pprint(xxx)

