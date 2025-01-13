import json, ast
import pygame  
import requests, json
from io import BytesIO 
import tempfile 
import time
import datetime  
import io 
import dateutil.parser  
import locale 
import os
from dotenv import load_dotenv  
import subprocess  

#load_dotenv("xiaoxin.env")  
quitReg=False
pause=False
playing=False

def getTools():
    return [fun_playmusic_desc,fun_stopplay_desc,fun_pauseplay_desc,fun_unpauseplay_desc]

def getPlayerStatus():
    global playing,pause
    if playing:
        return "playing"
    if pause:
        return "pause"
    
    
def isPlaying():
    """
    check if playing
    
    return：
        Yes if playing, No if not playing
    """
    return playing
    
def playmusic(song_name):
    """
    play music
    
    params：
        song_name：the name of music
        
    return：
        status
    """
    global playing, pause 
    print("playmusic")
    #return f"为您找到歌曲：{song_name} 已开始播放。如果有其他任务请告知我，我先退下了。"
    url='http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s= %s&type=1&offset=0&total=true&limit=10' % song_name
    res=requests.get(url)
    music_json=json.loads(res.text)
    #print(music_json)
    count=music_json["result"]["songCount"]
    
    if(count>0):
        musicName = downloadAndPlay(music_json,0)
        if musicName:
            print("找到歌曲：'"+musicName+"' 开始播放。请欣赏。")
            return f"为您找到歌曲：{musicName} 已开始播放。请欣赏。" #"找到歌曲：'"+musicName+"' 开始播放。请欣赏。"
        else:
            playing=False
            pause = False
            print("没有找到音乐")
            return "没有找到音乐"
    
    return "没有找到音乐"

def downloadAndPlay(music_json,index):
    global playing, pause 
    count=music_json["result"]["songCount"]
    if index>=count:
        return False
    songid=music_json["result"]["songs"][index]["id"]
    songName=music_json["result"]["songs"][index]["name"]
    url='http://music.163.com/song/media/outer/url?id=%s.mp3' % songid
    response = requests.get(url)  
    audio_data = BytesIO(response.content)  

    temp_file_name = "temp_audio.mp3"  # 临时文件名  
    with open(temp_file_name, 'wb') as temp_file:  
        temp_file.write(audio_data.getbuffer())  
    print(temp_file_name)

    # 初始化pygame  
    pygame.init()  
    try:
        # 播放音乐  
        pygame.mixer.music.load(temp_file_name)  
        pygame.mixer.music.play()
        playing=True
        pause = False
        print(songName)
        return songName
    except Exception as e:  
        print("failed play try next one")
        playing=False
        pause = False
        index+=1
        return downloadAndPlay(music_json,index)
        
    
fun_playmusic_desc = {
    "type": "function",
    'function':{
        'name': 'playmusic',
        'description': '播放歌曲',
        'parameters': {
            'type': 'object',
            'properties': {
                'song_name': {
                    'type': 'string',
                    'description': '歌名'
                },
            },
            'required': ['song_name']
        }
    }
}
def stopplay():
    """
    停止播放音乐
    
    返回：
        播放状态
    """
    global playing, pause 
    pygame.mixer.music.stop()  
    playing=False
    pause = False
    return "音乐已停止。"
    
fun_stopplay_desc = {
    "type": "function",
    'function':{
        'name': 'stopplay',
        'description': '停止播放',
        'parameters': {
            'type': 'object',
            'properties': {

            },
            'required': []
        }
    }
}
def pauseplay():
    """
    暂停音乐播放
    
    返回：
        播放状态 : 已暂停
    """
    global playing, pause
    pygame.mixer.music.pause()

    playing=False
    pause = True
    return "播放已暂停。"

fun_pauseplay_desc = {
    "type": "function",
    'function':{
        'name': 'pauseplay',
        'description': '暂停播放',
        'parameters': {
            'type': 'object',
            'properties': {

            },
            'required': []
        }
    }
}

def unpauseplay():
    """
    恢复音乐播放
    
    返回：
        播放状态 : 已经继续播放
    """
    global playing, pause
    pygame.mixer.music.unpause()
    playing=True
    pause = False
    return "恢复播放"

fun_unpauseplay_desc = {
    "type": "function",
    'function':{
        'name': 'unpauseplay',
        'description': '恢复播放',
        'parameters': {
            'type': 'object',
            'properties': {

            },
            'required': []
        }
    }
}
def isPause():
    return pause

def isPlaying():
    return playing
