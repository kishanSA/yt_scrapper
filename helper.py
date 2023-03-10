youtube_url = 'https://www.youtube.com'
            
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def get_video_publish_date(pubTime):
    """ 
    This function convert the absolute time into relative time.
    It will show the actual date of video uploaded.
    """
    from datetime import datetime as dt
    from datetime import timedelta as td
    
    today = dt.now()
    num, val, _ = str(pubTime).split()
    num = int(num)
    if val.startswith('hour'):
        publish_dt = today - td(hours=num)
    elif val.startswith('day'):
        publish_dt = today - td(days=num)
    elif val.startswith('week'):
        publish_dt = today - td(weeks=num) 
    elif val.startswith('month'):
        publish_dt = today - td(days=num*30) 
    elif val.startswith('year'):
        publish_dt = today - td(days=num*365) 

    return publish_dt.strftime("%d %b %Y")

