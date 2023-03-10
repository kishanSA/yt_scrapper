from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests as req
import re
import logging
import helper as h
import os

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/ytVids" , methods = ['POST' , 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:           
            channel_name = request.form['content'].replace(" ","")
            vid_count = int(request.form['v_count'])

            video_channel_url = f"{h.youtube_url}/@{channel_name}/videos"
            response = req.get(video_channel_url, headers=h.header, cookies={'CONSENT':'YES+1'})
            
            filename = channel_name + ".csv"
            fw = open(filename, "w", encoding="utf-8")
            cols = "No, Video URL, Thumbnail, Video Title, Views, Publish Date \n"
            fw.write(cols)
            
            if response.ok:
                data = response.text

                videourls = re.findall('"videoRenderer":{"videoId":".*?"', data)
                thumbs = re.findall('"thumbnail":{"thumbnails":\[{"url":".*?"', data)
                titles = re.findall('"title":{"runs":\[{"text":".*?"', data)
                published = re.findall('"publishedTimeText":{"simpleText":".*?"', data)
                views = re.findall('"shortViewCountText":{"accessibility":{"accessibilityData":{"label":".*?"', data)
             
                videos_list = list()
                for n in range(vid_count):
                    videoId = h.youtube_url+'/watch?v='+ videourls[n].split(":")[-1].replace('"','')
                    thumb = thumbs[n].split('"')[-2].split('?')[0]
                    title = titles[n].split('"')[-2]
                    view = views[n].split('"')[-2]
                    publish = h.get_video_publish_date(published[n].split('"')[-2])
                    
                    fw.write(f"{(n+1)}, {videoId}, {thumb}, {title}, {view}, {publish} \n")
                    detail = {"No": (n+1), "Video URL": videoId, "Thumbnail": thumb, "Video Title": title, 
                              "Views": view, "Publish Date": publish}

                    videos_list.append(detail)

                logging.info("Final Search Result: {}".format(videos_list))
                return render_template('result.html', videos=videos_list, channel=channel_name)
            else:
                os.remove(filename)
                return "Please check the channel name. Something is wrong."
        except Exception as e:
            logging.info(e)
            if not fw.closed:
                fw.close()
            return 'something is wrong' 
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000)
