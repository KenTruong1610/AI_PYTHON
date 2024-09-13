import time
from threading import Thread, Lock
import sys

lock = Lock()

def animate_text(text, delay=0.1):
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print() 

def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

def sing_song():
    lyrics = [
        ("Người yêu ơi, yêu mình em được không?", 0.1),
        ("Từ giờ và sau này xua lạnh nơi đây mùa đông", 0.1),
        ("Là ngày ta sum vầy, con tim hao gầy", 0.1),
        ("Tình yêu đông đầy, hãy để em chứng minh cho anh thấy", 0.1),
        ("Người yêu ơi, yêu thì có gì sai? Đâu có sai đâu", 0.1),
        ("Không là em thì ai?",0.1),
        ("Để em đưa anh về, là tình yêu mãi mê",0.1),
        ("Mặc kệ người ta cười chê bởi vì tình yêu là thế",0.1),
        ("Làm người yêu em nhé, baby!!!",0.1)

    ]
    delays = [0.8, 1.3, 1.7, 2.1,2.5,3.0,3.3,3.7,4.1

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
