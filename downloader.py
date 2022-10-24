import pafy
from youtubesearchpython import VideosSearch
from concurrent.futures import ThreadPoolExecutor
import threading

lock=threading.Lock()
class Downloader():
    def __init__(self,name):
        self.name=name
        with ThreadPoolExecutor(max_workers=700) as executor:
            executor.map(self.down,self.name)

    def down(self):
        result = [video['link'] for video in VideosSearch(self.name, limit=1).result()['result']]
        final_result = result[0]
        url = pafy.new(final_result)
        media = url.getbestaudio()
        lock.acquire()
        media.download()
        lock.release()



