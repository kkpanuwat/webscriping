import os

import googleapiclient.discovery
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag
from pythainlp.corpus import thai_stopwords

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
    print(stopwords)
    for i in comments:
        i = i.replace(" ","")
        i = i.replace("\n","")
        tokens = word_tokenize((i))
        tokens = [i for i in tokens if i not in stopwords]
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
