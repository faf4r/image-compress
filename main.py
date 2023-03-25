from PIL import Image
import os
import threading


def compress(file, size_limit=2.0, rate=0.95):
    size = os.path.getsize(file)/1024/1024
    if size <= size_limit:
        return
    
    # 加一步预处理，使图片大小在2左右，减少压缩次数
    r = (size_limit / size) ** 0.5
    img = Image.open(file)
    x, y = img.size
    img.resize([int(x*r), int(y*r)], Image.LANCZOS).save(file)
    size = os.path.getsize(file)/1024/1024
    # print(file, size,sep='\t')

    while size > size_limit:
        img = Image.open(file)
        x, y = img.size
        img.resize([int(x*rate), int(y*rate)], Image.LANCZOS).save(file)
        size = os.path.getsize(file)/1024/1024
        # print('\r', file, size, end='')
        # print('\t', size,sep='\t')
    # print()
    print(f'{file}\t{size}MB')


dir = './images'

# for file in os.listdir(dir):
#     compress(os.path.join(dir, file))


threads = []
for file in os.listdir(dir):
    threads.append(threading.Thread(target=compress, args=(os.path.join(dir, file), )))

for t in threads:
    t.start()
for t in threads:
    t.join()
