from PIL import Image
import os
import threading


def compress(file, size_limit=2.0, rate=0.95):
    size = os.path.getsize(file)/1024/1024
    while size > size_limit:
        img = Image.open(file)
        x, y = img.size
        img.resize([int(x*rate), int(y*rate)], Image.LANCZOS).save(file)
        size = os.path.getsize(file)/1024/1024
        # print('\r', file, size, end='')
    print(file, size, 'MB')


dir = './images'

threads = []
for file in os.listdir(dir):
    threads.append(threading.Thread(target=compress, args=(os.path.join(dir, file), )))

for t in threads:
    t.start()
for t in threads:
    t.join()
