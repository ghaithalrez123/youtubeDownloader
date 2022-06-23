from re import A
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os


def find_res(res, wanted_res):
  for r in res:
    if int(r[:-1]) >= wanted_res:
      return res.index(r)
  return len(res) - 1


def convert(length):
  return {"seconds": length % 60, "minutes": int(length / 60) % 60, 'hours': int(length / (60 * 60))}


def print_video_properties(video):
  print("the video title is : ", video.title)
  time = convert(video.length)
  print(time['hours'], "h :", time['minutes'], "m :", time['seconds'], "s")


def finish():
  print("download finish ")


def chose_path():
  path = input("Enter path to save : ")
  if path == 'desktop' or path == 'Desktop':
    path = os.path.normpath(os.path.expanduser("~/Desktop/downloads"))

  if not os.path.exists(path):
    os.makedirs(path)
  return path


while True:
  choice = input(
    "Enter a to download video \nEnter b to download playlist \nEnter c to know playlist length\nEnter q to exit "
    "the program :")
  if choice == 'a':
    link = input("Please enter video URL : ")
    try:
      video = YouTube(link, on_progress_callback=on_progress)
      print_video_properties(video)
    except:
      print('connection error')
      continue

    print('loading ... ')
    streams = video.streams.filter(file_extension='mp4', progressive=True)
    print('Available resolutions are :')
    i = 1
    for stream in streams:
      print(i, ') ', stream.resolution)
      i += 1
    res = input('Select index of resolution you want :')
    path = chose_path()
    streams[int(res) - 1].download(path)
    finish()

  elif choice == 'b':
    playlist_link = input("enter playlist URL : ")
    playlist = Playlist(playlist_link)
    start = 0
    end = len(playlist.video_urls)
    choose = input("Do you want to download specific range (yes/no) : ")
    if choose == 'yes':
      start = int(input('select start : ')) - 1
      end = int(input('select end : '))
    res = input('Enter the resolution you want :')
    path = chose_path()
    i = 1 + start
    prefix = ''
    with_prefix = input('Do you want to add prefix with the number of video in playlist (yes/no): ')
    for video in playlist.videos[start:end]:
      video.register_on_progress_callback(on_progress)
      print_video_properties(video)
      streams = video.streams.filter(file_extension='mp4', progressive=True)
      resolutions = []
      for stream in streams:
        resolutions.append(stream.resolution)
      if with_prefix == 'yes':
        prefix = str(i) + "-"
      streams[find_res(resolutions, int(res))].download(output_path=path, filename_prefix=prefix)
      i += 1
      print('---------------------------------')

    finish()

  elif choice == 'c':
    length = 0
    link = input("Enter playlist URL : ")
    playlist = Playlist(link)
    choose = input("Do you want to calculate specific range (yes/no) : ")
    start = 0
    end = len(playlist.video_urls)
    if choose == 'yes':
      start = int(input('select start : ')) - 1
      end = int(input('select end : '))
    for video in playlist.videos[start:end]:
      print(video.title)
      length += video.length
    time = convert(length)
    print("The duration is ", time['hours'], "h :", time['minutes'], "m :", time['seconds'], "s")
  elif choice == 'q':
    exit()
