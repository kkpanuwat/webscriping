import os

import googleapiclient.discovery
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag
from pythainlp.corpus import thai_stopwords
import re

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDGLbBnxzKiMUJInY2cDbp_bEDGE0DXgHg")

def get_comments(video_id,keyword):
    request = youtube.commentThreads().list(
        part="id,snippet",
        videoId=video_id,
        textFormat="plainText",
    )

    comments = []
    while request is not None:
        response = request.execute()
        for item in response["items"]:
            # print(response["items"])
            comment = item["snippet"]["topLevelComment"]
            comments.append(comment["snippet"]["textDisplay"])
        request = youtube.commentThreads().list_next(request, response)
    file = open("{}_{}.txt".format(keyword,video_id),"w+",encoding="utf-8")
    data = str()
    stopwords = thai_stopwords()
    for i in comments:
        i = i.replace(" ","")
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        txtClean = emoji_pattern.sub(r'', i)
        txtClean = txtClean.replace("\n","")
        tokens = word_tokenize((txtClean))
        tokens = [txtClean for txtClean in tokens if txtClean not in stopwords]
        result = pos_tag(tokens)
        print(result)
        data+=i+"\n"
    file.write(data)
    file.close()

def search_videos(query):
    request = youtube.search().list(
        part="id,snippet",
        type='video',
        q=query,
        maxResults=1,
    )
    response = request.execute()

    for item in response["items"]:
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(url)
        get_comments(video_id,query)
        
    
if __name__ == "__main__":
    search_videos(input("Please Enter Your keyword : "))
