import os
from tkinter import *
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import filedialog
import threading
from ttkthemes import themed_tk as tk
from tkinter import ttk
import time

#root = Tk()
root=tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)

statusBar=ttk.Label(root,text='Welcome to music player',relief=SUNKEN,anchor=W,font='Times 15 italic')
statusBar.pack(side=BOTTOM,fill=X)

playlist=[]
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

paused = FALSE
def pause_music():
    global paused
    paused=True
    mixer.music.pause()
    statusBar['text']='Music paused'+'-'+os.path.basename(filename)


menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)

def help_player():
    tkinter.messagebox.showinfo('Tips',"You have to add music to playlist or directly play from folder.Then you can use other functionality of this apps.Otherwise this app may misbehave.")
def about_us():
    tkinter.messagebox.showinfo('Riyadh',
                                'This is a music player built by a novice python engineer named Riyadh.It is built with educational purpose.')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='Click here', command=help_player)
menubar.add_command(label='About Developer',command=about_us)
mixer.init()
root.geometry('600x550')
root.title("Stairway To Heaven")
root.wm_iconbitmap(r'@images/technology(1).xbm')
leftFrame=Frame(root)
leftFrame.pack(side=LEFT)
rightFrame=Frame(root)
rightFrame.pack()
topFrame=Frame(rightFrame)
topFrame.pack()

def add_to_playlist(filename):
    index=0
    filename=os.path.basename(filename)
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index+=1

playlistbox = Listbox(leftFrame)
playlistbox.pack(side=TOP)


addBtn=Button(leftFrame,text='+add',command=browse_file)
addBtn.pack(side=LEFT)
def remove_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
removeBtn=Button(leftFrame,text='-remove',command=remove_song)
removeBtn.pack(side=LEFT)


playPhoto = PhotoImage(file='images/multimedia.png')
photo2 = PhotoImage(file='images/play.png')
labelPhoto = Label(topFrame, image=photo2)
currentTimelabel=ttk.Label(root,text="Time passed",relief=GROOVE)
currentTimelabel.pack()




def show_details(play_song):
    file_data=os.path.splitext(play_song)
    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:2d}:{:2d}'.format(mins,secs)
    lengthlabel['text']='Total runtime-'+timeformat
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:2d}:{:2d}'.format(mins, secs)
            currentTimelabel['text']='Time spent - '+timeformat
            time.sleep(1)
            current_time+=1


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusBar['text']='Music resumed.'
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
            statusBar['text']="Music currently playing from"+'--'+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Your have to select correct music first. ')



def stop_music():
    mixer.music.stop()
    statusBar['text']="Music is stopped."


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)

def rewind_music():
    play_music()
    statusBar['text']='Music is rewinded.'
muted=FALSE
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.4)
        unmuteBtn.configure(image=unmutePhoto)
        scale.set(40)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        unmuteBtn.configure(image=mutePhoto)
        scale.set(0)
        muted=TRUE


middleFrame=Frame(rightFrame)
middleFrame.pack(pady=10,padx=10)


playBtn = ttk.Button(middleFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0,column=0,padx=5)
stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0,column=1,padx=5)
pausePhoto=PhotoImage(file='images/pause.png')
pauseBtn=ttk.Button(middleFrame,image=pausePhoto,command=pause_music)
pauseBtn.grid(row=0,column=2,padx=5)

bottomFrame=Frame(rightFrame)
bottomFrame.pack()

lengthlabel=ttk.Label(topFrame,text='length of song-> 00:00 ',font='Arial 12 bold')
lengthlabel.pack(pady=5)


rewindPhoto=PhotoImage(file='images/rewind.png')
rewindBtn=ttk.Button(bottomFrame,image=rewindPhoto,command=rewind_music)
rewindBtn.grid(row=0,column=0,padx=10)
mutePhoto=PhotoImage(file='images/silence.png')
unmutePhoto=PhotoImage(file='images/unmute.png')
unmuteBtn=ttk.Button(bottomFrame,image=unmutePhoto,command=mute_music)
unmuteBtn.grid(row=0,column=1)

scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(40)
mixer.music.set_volume(0.4)
scale.grid(row=0,column=2,pady=15,padx=10)

labelPhoto.pack()

def on_closing():
    tkinter.messagebox.showinfo('Close Apps','Are you want to close apps')
    stop_music()
    root.destroy()
root.protocol('WM_DELETE_WINDOW',on_closing)
root.mainloop()
