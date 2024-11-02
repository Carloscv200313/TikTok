import json
import asyncio
import time
import schedule
from datetime import datetime, timedelta
from tiktokapipy.async_api import AsyncTikTokAPI

async def fetch_video_data(video_url):
    async with AsyncTikTokAPI() as api:
        video = await api.video(video_url)
        data = {
            "TIEMPO": datetime.now().isoformat(),
            "TITULO": video.desc,
            "VISTAS": video.stats.play_count,
            "LIKES": video.stats.digg_count,
            "COMPARTIDOS": video.stats.share_count
        }
        
        try:
            with open('video_data.json', 'r') as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        history.append(data)
        
        with open('video_data.json', 'w') as file:
            json.dump(history, file, indent=4)
        
        print(f"Datos guardados: {data}")


def schedule_task():
    video_url = "https://www.tiktok.com/@ofertas_rapidas/video/7421237085232729349"
    asyncio.run(fetch_video_data(video_url))

schedule.every(1).minutes.do(schedule_task)
start_time = datetime.now()
end_time = start_time + timedelta(hours=1)

while datetime.now() < end_time:
    schedule.run_pending() 
    time.sleep(1)  

print("Finalizó el período de 1 hora.")
