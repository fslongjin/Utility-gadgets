import os

import multiprocessing


base_path = './input'
out_path = './output'

if not os.path.exists(base_path):
    print('请将要转码的视频放置在{}文件夹下面！'.format(base_path))
    os.mkdir(base_path)

if not os.path.exists(out_path):
    print('请将要转码的视频放置在{}文件夹下面！'.format(out_path))
    os.makedirs(out_path)

suffix = ('mov', 'mp4', 'mpeg', 'avi', 'flv', 'mkv')

max_proc = int(input('请输入最大工作进程数量(建议为2~4) >> '))
del_flag = input("处理完成后是否删除源文件？(y/n) >> ").lower()

if del_flag == 'y':
    del_flag = True
else:
    del_flag = False


def run_func(path, rm_flag):
    name = os.path.splitext(path.split('/')[-1])[0]
    op = os.path.join(out_path, path[len(base_path):])
    op = os.path.splitext(op)[0]

    pid = os.getpid()
    print("[process {}] --- 正在编码：{}".format(pid, path))
    print("ffmpeg -i {} -c:v libx265 -x265-params crf=18:preset=placebo {}/{}.mp4".format(path, op, name))
    os.system("ffmpeg -i {} -c:v libx265 -x265-params crf=18:preset=placebo {}/{}.mp4".format(path, op, name))
    if rm_flag:
        os.remove(path)
    print('exit')


pool = multiprocessing.Pool(processes=max_proc)

for root, dirs, files in os.walk(base_path, topdown=False):
    for name in files:
        if name.lower().endswith(suffix):
            p = os.path.join(root, name)
            print(os.path.join(root, name))
            pool.apply_async(run_func, args=(p, del_flag))

pool.close()
pool.join()
print('处理完成！')


