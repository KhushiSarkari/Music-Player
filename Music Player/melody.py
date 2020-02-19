import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
from ttkthemes import themed_tk as tk
from tkinter import ttk

#create window
root=tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

#create status bar
statusbar=ttk.Label(root,text="Welcome to Melody",relief=SUNKEN,anchor=W, font='Times 10 italic') #w=west
statusbar.pack(side=BOTTOM,fill=X)

#create menu bar
menubar=Menu(root)
root.config(menu=menubar)

#create submenu
subMenu=Menu(menubar,tearoff=0)

playlist=[] #contains path+filename required to music

def browse_file():
  global filename_path
  filename_path=filedialog.askopenfilename()
  statusbar['text']="Selected: "+os.path.basename(filename_path)
  add_to_playlist(filename_path)
 
 
def add_to_playlist(filename):
  filename=os.path.basename(filename)
  index=0
  playlistbox.insert(index,filename)
  playlist.insert(index,filename_path)
  index+=1
  
  
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command=browse_file)
subMenu.add_command(label="Exit",command=root.destroy)

def about_us():
  tkinter.messagebox.showinfo('About Melody',"This is a music player build using Python for partial fulfillment of the requirement for the award of the degree of Bachelor of Technology in Computer Science and Engineering, by Khushi Sarkari")

subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us",command=about_us)

#initializing mixer
mixer.init()  

#set window parameters
#root.geometry('300x300')
root.title("Melody")
root.iconbitmap(r'images/icon.ico')

#left frame for listbox
leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

#right frame 
rightframe=Frame(root)
rightframe.pack(pady=30)

#top frame inside right frame
topframe=Frame(rightframe)
topframe.pack()

#frame to group play, pause and stop buttons
middleframe=Frame(rightframe)
middleframe.pack(pady=30,padx=30)

#frame to group rewind button, mute/unmute button and scale
bottomframe=Frame(rightframe)
bottomframe.pack(pady=10)
  

#create a label for length of song
lengthLabel=ttk.Label(topframe,text='Total length- --:--')
lengthLabel.pack(pady=5)

#create a label for current time 
currentLabel=ttk.Label(topframe,text='Current Time- --:--',relief=GROOVE)
currentLabel.pack()

#create playlist that containsfilename
playlistbox=Listbox(leftframe)
playlistbox.pack()

addBtn=ttk.Button(leftframe,text="+ Add",command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
  selected_song=playlistbox.curselection()
  selected_song=int(selected_song[0])
  play_it=playlist[selected_song]
  playlistbox.delete(selected_song)
  playlist.pop(selected_song)

delBtn=ttk.Button(leftframe,text="- Delete",command=del_song)
delBtn.pack(side=LEFT)

#function definitions

def show_details(play_song):
  filedata=os.path.splitext(play_song)
  if(filedata[1])=='.mp3':
    audio=MP3(play_song)
    total_length=audio.info.length
	
  else:
    a=mixer.sound(play_song)
    total_length=a.get_length()
	
  min,sec=divmod(total_length,60)  #div- total_length/60, mod- total_length%60
  min=round(min)
  sec=round(sec)
  timeformat='{:02d}:{:02d}'.format(min,sec)
  lengthLabel['text']="Total length- "+timeformat
  t1=threading.Thread(target=start_count, args=(total_length,))
  t1.start()
  
def start_count(t):
  global paused
  #mixer.music.get_busy() returns false when music is stopped so countdown stops
  current_time=0
  while current_time<=t and mixer.music.get_busy():
    if paused :
      continue
    else:
      min,sec=divmod(current_time,60) 
      min=round(min)
      sec=round(sec)
      timeformat='{:02d}:{:02d}'.format(min,sec)
      currentLabel['text']="Current Time- "+timeformat
      time.sleep(1)
      current_time+= 1
    
def play_music():
  global paused
  if paused:
    mixer.music.unpause()
    statusbar['text']="Music resumed"
    paused=FALSE
   
  else:
    try:
      stop_music()
      time.sleep(1)
      selected_song=playlistbox.curselection()
      selected_song=int(selected_song[0])
      play_it=playlist[selected_song]
      mixer.music.load(play_it)
      mixer.music.play()
      statusbar['text']="Playing "+os.path.basename(play_it)
      show_details(play_it)
    except:
      
      tkinter.messagebox.showerror('File not found',"Melody couldn't find your file.Please check again")
    
paused=FALSE
def pause_music():
  global paused
  paused=TRUE
  mixer.music.pause()	
  statusbar['text']="Music paused.Click Play to resume"
  
def stop_music():
  mixer.music.stop()
  statusbar['text']="Music stopped"
  
def rewind_music():
  play_music()
  statusbar['text']="Music rewinded"
  
def set_vol(val):
  volume=float(val)/100   #as set_volumefunction only accepts values in range 0-1
  mixer.music.set_volume(volume)
  
muted=FALSE
def mute_music():
  global muted
  if muted:#unmute the music
    mixer.music.set_volume(0.3)
    unmuteBtn.configure(image=unmutePhoto)
    scale.set(30)
    muted=FALSE
  else: #mute music
    mixer.music.set_volume(0)
    unmuteBtn.configure(image=mutePhoto)
    scale.set(0)
    muted=TRUE
  
  
#create play button
playPhoto=PhotoImage(file="images/play.png") 
playBtn=ttk.Button(middleframe, image=playPhoto,command=play_music)
playBtn.grid(row=0,column=0,padx=8)

#create pause button
pausePhoto=PhotoImage(file="images/pause.png") 
pauseBtn=ttk.Button(middleframe, image=pausePhoto,command=pause_music)
pauseBtn.grid(row=0,column=1,padx=8)

#create stop button
stopPhoto=PhotoImage(file="images/stop.png") 
stopBtn=ttk.Button(middleframe, image=stopPhoto,command=stop_music)
stopBtn.grid(row=0,column=2,padx=8)

#create rewind button
rewindPhoto=PhotoImage(file="images/rewind.png") 
rewindBtn=ttk.Button(bottomframe, image=rewindPhoto,command=rewind_music)
rewindBtn.grid(row=0,column=0)

#create mute/unmute button
mutePhoto=PhotoImage(file="images/mute.png") 
unmutePhoto=PhotoImage(file="images/unmute.png") 
unmuteBtn=ttk.Button(bottomframe, image=unmutePhoto,command=mute_music)
unmuteBtn.grid(row=0,column=1)

#create volume scale
scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(30) #default volume
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,pady=15,padx=30)


def on_closing():
  stop_music()
  root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()

