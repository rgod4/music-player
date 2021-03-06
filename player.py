from tkinter import*
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

def sliderf(x):
    song = song_list.get(ACTIVE)
    song = f'C:/Users/SHEETAL YADAV/Downloads/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider.get()))
#song duration
def playtime():
    if stopped:
        return
    current=pygame.mixer.music.get_pos()/1000#convert to second
    converted = time.strftime('%M:%S', time.gmtime(current))  # convert to minute second format
    csong=song_list.curselection()  #get current song
    song =song_list.get(csong)  #get song name
    song = f'C:/Users/SHEETAL YADAV/Downloads/{song}'#change name
    # get song length
    songmut=MP3(song)
    global songl
    songl=songmut.info.length#
    csongl=time.strftime('%M:%S', time.gmtime(songl))
    current+=1
    if int(slider.get()) == int(songl):
        status_bar.config(text=f'Time elapsed:{csongl}')
    elif pauseinfo:
        pass
    elif int(slider.get())==int(current):
        #slider hasn't been moved
        slidepos = int(songl)
        slider.config(to=slidepos, value=current)
    else:
        #slider has been moved
        slidepos = int(songl)
        slider.config(to=slidepos, value=int(slider.get()))
        converted = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        status_bar.config(text=f'Time elapsed:{converted} of {csongl}')  # output to status bar
        ntime=int(slider.get()) +1
        slider.config(value=ntime)
    #update slider to position
    status_bar.after(1000,playtime)#update time

#add song
def addsong():
    song = filedialog.askopenfilename(title="choose a song", filetypes=(("mp3 files","*.mp3"),))
    song = song.replace("C:/Users/SHEETAL YADAV/Downloads/", "")
    song_list.insert(END, song)
#add multiple songs
def addmore():
    songs=filedialog.askopenfilenames(title="choose a song", filetypes=(("mp3 files","*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/SHEETAL YADAV/Downloads/", "")
        song_list.insert(END, song)
#play song
def playsong():
    global stopped
    stopped=False
    song = song_list.get(ACTIVE)
    song=f'C:/Users/SHEETAL YADAV/Downloads/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=1)
    #call playtime to get song duration
    playtime()
#stop songs
global stopped
stopped=False
def stop():
    #reset slider and status bar
    status_bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    global stopped
    stopped=True
global pauseinfo
pauseinfo = False
#pause button func.
def pause(p):
    global pauseinfo
    pauseinfo=p
    if pauseinfo:
        pygame.mixer.music.unpause()
        pauseinfo = False
    else:
        pygame.mixer.music.pause()
        pauseinfo = True

#forward func
def forward():
    status_bar.config(text='')
    slider.config(value=0)
    nextsong = song_list.curselection()
    song=song_list.get(nextsong)
    last=song_list.get(END)
    if song==last:
        nextsong=0
        song=song_list.get(nextsong)
    else:
        nextsong=nextsong[0]+1
        song=song_list.get(nextsong)
    song = f'C:/Users/SHEETAL YADAV/Downloads/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=1)

    song_list.selection_clear(0,END)
    song_list.activate(nextsong)
    song_list.selection_set(nextsong,last=None)

#backward function
def backward():
    status_bar.config(text='')
    slider.config(value=0)
    prevsong= song_list.curselection()
    prevsong= prevsong[0]-1
    song=song_list.get(prevsong)
    song= f'C:/Users/SHEETAL YADAV/Downloads/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=1)

    song_list.selection_clear(0, END)
    song_list.activate(prevsong)
    song_list.selection_set(prevsong, last=None)

def deletesong():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()

def deleteallsongs():
        stop()
        song=song_list.delete(0,END)


root = Tk()
root.geometry("500x400")
root.wm_iconbitmap("images.ico")
root.title("MUSIC PLAYER")
root.configure(background="black")

#initialize pygame mixer
pygame.mixer.init()
rt = Frame(root)
name=Label(rt,text="PlayList",font="lucida 20 bold",fg='silver',bg='black')
name.pack()
rt.pack()

#making a playlist
song_list =Listbox(root, fg="yellow", bg="grey", width=50)
song_list.pack()

#making button frame
frame=Frame(root)
frame.pack(pady=14)

#music buttons
previmg = PhotoImage(file="prev.png")
nextimg = PhotoImage(file="next.png")
playimg = PhotoImage(file="play.png")
pauseimg = PhotoImage(file="pause.png")
stopimg = PhotoImage(file="stop.png")
#backward button
prev_btn=Button(frame, image=previmg, bg="silver",command=backward)
prev_btn.grid(row=0, column=1)
#forward button
next_btn=Button(frame, image=nextimg, bg="silver",command=forward)
next_btn.grid(row=0, column=2)
#play button
play_btn=Button(frame, image=playimg, bg="silver", command=playsong)
play_btn.grid(row=0, column=3)
#pause button
pause_btn=Button(frame, image=pauseimg, bg="silver",command=lambda: pause(pauseinfo))
pause_btn.grid(row=0, column=4)
#stop button
stop_btn=Button(frame, image=stopimg, bg="silver", command= stop)
stop_btn.grid(row=0, column=5)

#creating menu
mymenu= Menu(root)
submenu1=Menu(mymenu)
submenu1.add_command(label="Add One", command=addsong)
submenu1.add_command(label="Add Multiple", command=addmore)
submenu2=Menu(mymenu)
submenu2.add_command(label="Delete One", command=deletesong)
submenu2.add_command(label="Delete All", command=deleteallsongs)
mymenu.add_cascade(label="Add", menu=submenu1)
mymenu.add_cascade(label="Delete", menu=submenu2)
root.configure(menu=mymenu)
#status bar
status_bar=Label(root,text="Song Duration",bd=1,relief=GROOVE)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
#slider
slider=ttk.Scale(root,from_=0,to_=100,orient=HORIZONTAL,value=0,command=sliderf,length=360)
slider.pack(ipady=5)

root.mainloop()
