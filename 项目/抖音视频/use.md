# 获取抖音网页版所有个人作品数据

## <1> 运行 video-id.py
 输入主页链接和 **cookie**
![img.png](img/img.png)

运行结果
![img_1.png](img/img_1.png)  
会在当前目录下生成一个 **video-id.txt** 文件

## <2> 运行 crawl.py
会在当前目录下生成 VIDEO 文件夹，其中保存着所有视频的 JSON 数据

![img_2.png](img/img_2.png)

如果视频为图片视频，则：
![img_3.png](img/img_3.png)
其中 **video_music** 为视频的背景音乐， **video_images** 为 **URL**

其它则为：
![img_4.png](img/img_4.png)
其中 **video_url** 为视频的 **URL**，已默认为 **1080p**

其中可自定义获取的视频数据，修改视频 **id** 列表即可

***
# 本代码仅作为学习与科研用处，切勿用于违法行为
***

