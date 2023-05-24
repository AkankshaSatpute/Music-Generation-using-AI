import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from pprint import pprint
import pyaudio  
import wave
import time
import os
from genetic_version1 import melody1,melody2
import mysql.connector as msql
# assign directory
directory = r'C:\Users\PC Point\.spyder-py3\btech_project\out'

db = msql.connect(user='root',passwd='root123',host ='localhost',database='btech')

samplerate = 44100 #Frequecy in Hz
octave = ['C', 'c', 'D', 'd','E', 'F', 'f', 'G', 'g', 'A', 'a', 'B','F#']
rating =[]
m =0
count =0


# twinkle "CCGGAAG,FFEEDDC"
# ddlj song EEEBABGACB, EEEBABAGAGF


def get_wave(freq, duration=0.5):
    '''
    Function takes the "frequecy" and "time_duration" for a wave
    as the input and returns a "numpy array" of values at all points
    in time
    '''
   
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
   
    return wave

def get_piano_notes():
    '''
    Returns a dict object for all the piano
    note's frequencies
    '''
    base_freq = 261.63 #Frequency of Note C4
   
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0 # silent note
   
    return note_freqs
 
  # To get the piano note's frequencies

def get_song_data(music_notes):
    '''
    Function to concatenate all the waves (notes)
    '''
    note_freqs = get_piano_notes() # Function that we made earlier
    song = [get_wave(note_freqs[note]) for note in music_notes.split('-')]
    song = np.concatenate(song)
    return song

inc =0

#select composition from music where melody1= 'abc' and melody2 = 'abc'
cur = db.cursor()

#query ="insert into music (melody1,melody2) values('{}','{}')".format(melody1,melody2)

#cur.execute(query)
db.commit()
# print("Query executed")
# select *from music where melody1 = 'abcdef' and melody2 = 'abcdef' order by rating desc limit 0,5;
print("Do want to create new music or want to want to listen old music if available")
print("Press : 0:- old music ")
print("Press : 1:- new music ")
print("Press : 2:- both old and new music ")
inst = int(input("Enter your choice : "))

if inst == 0:
    
    cur.execute("select composition from music where melody1 = 'CCGGAAG' and melody2 = 'EEEBABAGAGF' order by rating desc limit 0,3")
    
    f=cur.fetchall()   
    for inp in f:
         inplist = []
         m1 = []
         # print("-----------inp---------------")
         # print(inp)
         for i in inp:
             
             for j in i:
                 # print("--------j ===="+ j)
                 if j in octave:
                     inplist.append(j)
                     inplist.append('-')
                 if j == ',' or j == '+' or j =='@':
                     inplist.append('-')
                 # print("-----inplist----------")
                 # print(inplist)
             m1 = inplist
             # print("i--------------------------------")
             # print(i)
             str1 = ""
             music_notes = str1.join(inplist)
             # print("music_notes--------------------------------")
             # print(music_notes)
             data = get_song_data(music_notes)
             
             data = data * (16300/np.max(data))
             write('twinkle-twinkle.wav', samplerate, data.astype(np.int16))
             chunk = 1024
             f = wave.open(r"twinkle-twinkle.mp3","rb") 
             p = pyaudio.PyAudio()
             stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                             channels = f.getnchannels(),  
                             rate = f.getframerate(),  
                             output = True)
             data = f.readframes(chunk)
             while data:  
                 stream.write(data)  
                 data = f.readframes(chunk) 
             stream.stop_stream()  
             stream.close()  
             time.sleep(1)
             print("It was melody",(inc+1),end=" ")
             inc = inc +1
             rate = input("Enter 1 to continue : ")
             print()
             
             rating.append(rate) 
             cur = db.cursor()
             
             query ="insert into music (melody1,melody2,composition,rating) values('{}','{}','{}','{}')".format(melody1,melody2,music_notes,rate)
             
             cur.execute(query)
             db.commit()
             # print("Query executed")
    query ="delete from music where rating is null or rating =1 or rating =0"
    cur.execute(query)
    db.commit()
    print("Thank you")
elif inst == 2:
    cur.execute("select composition from music where melody1 = 'CCGGAAG' and melody2 = 'EEEBABAGAGF' order by rating desc limit 0,3")
    
    f=cur.fetchall()   
    for inp in f:
         inplist = []
         m1 = []
         # print("-----------inp---------------")
         # print(inp)
         for i in inp:
             
             for j in i:
                 # print("--------j ===="+ j)
                 if j in octave:
                     inplist.append(j)
                     inplist.append('-')
                 if j == ',' or j == '+' or j =='@':
                     inplist.append('-')
                 # print("-----inplist----------")
                 # print(inplist)
             m1 = inplist
             # print("i--------------------------------")
             # print(i)
             str1 = ""
             music_notes = str1.join(inplist)
             # print("music_notes--------------------------------")
             # print(music_notes)
             data = get_song_data(music_notes)
             
             data = data * (16300/np.max(data))
             write('twinkle-twinkle.mp3', samplerate, data.astype(np.int16))
             chunk = 1024
             f = wave.open(r"twinkle-twinkle.mp3","rb") 
             p = pyaudio.PyAudio()
             stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                             channels = f.getnchannels(),  
                             rate = f.getframerate(),  
                             output = True)
             data = f.readframes(chunk)
             while data:  
                 stream.write(data)  
                 data = f.readframes(chunk) 
             stream.stop_stream()  
             stream.close()  
             time.sleep(1)
             print("It was melody ",(inc+1),end=" ")
             inc = inc +1
             rate = input("Enter 1 to continue: ")
             print()
             
             rating.append(rate) 
             cur = db.cursor()
             
             query ="insert into music (melody1,melody2,composition,rating) values('{}','{}','{}','{}')".format(melody1,melody2,music_notes,rate)
             
             cur.execute(query)
             db.commit()
             # print("Query executed")
    query ="delete from music where rating =1 "
    cur.execute(query)
    db.commit()
    print("-------------------------------------------")
    print("Old music is done now new music will start")
    cur = db.cursor()

    #query ="insert into music (melody1,melody2) values('{}','{}')".format(melody1,melody2)

    #cur.execute(query)
    db.commit()
    # print("Query executed")

    cur.execute("select composition from music where melody1= 'CCGGAAG' and melody2 = 'EEEBABAGAGF' and rating = 0 order by rating desc limit 0,3")

    f=cur.fetchall()
    # print(type(f))


    # for i in f:
    #     inplist = []
    #     m1 = []
    #     print(i)
       
    for inp in f:
         inplist = []
         m1 = []
         # print("-----------inp---------------")
         # print(inp)
         for i in inp:
             for j in i:
                 # print("--------j ===="+ j)
                 if j in octave:
                     inplist.append(j)
                     inplist.append('-')
                 if j == ',' or j == '+' or j =='@':
                     inplist.append('-')
                 # print("-----inplist----------")
                 # print(inplist)
             m1 = inplist
             # print("m1--------------------------------")
             # print(m1)
             str1 = ""
             music_notes = str1.join(inplist)
             # print("music_notes--------------------------------")
             # print(music_notes)
             data = get_song_data(music_notes)
             
             data = data * (16300/np.max(data))
             write('twinkle-twinkle.wav', samplerate, data.astype(np.int16))
             chunk = 1024
             f = wave.open(r"twinkle-twinkle.mp3","rb") 
             p = pyaudio.PyAudio()
             stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                             channels = f.getnchannels(),  
                             rate = f.getframerate(),  
                             output = True)
             data = f.readframes(chunk)
             while data:  
                 stream.write(data)  
                 data = f.readframes(chunk) 
             stream.stop_stream()  
             stream.close()  
             time.sleep(1)
             print("For melody",(inc+1),end=" ")
             inc = inc +1
             rate = int(input("Enter rating between 0 to 5 : "))
             print()
             if(rate<0 or rate > 5):
                 
                 if(rate < 0 ):
                     print("as u have entered -ve rating which is false so we will consider it as 0")
                     rate  =0
                 if(rate >5):
                     print("as u have entered rating greater than 5 which is false so we will consider it as 5")
                     rate = 5
                    
             rating.append(rate) 
             cur = db.cursor()
             
             query ="insert into music (melody1,melody2,composition,rating) values('{}','{}','{}','{}')".format(melody1,melody2,music_notes,rate)
             
             cur.execute(query)
             db.commit()
             # print("Query executed")
    query ="delete from music where rating is null or rating =0"
    cur.execute(query)
    db.commit()
    print("Thank You")    
else :
    cur = db.cursor()

    #query ="insert into music (melody1,melody2) values('{}','{}')".format(melody1,melody2)

    #cur.execute(query)
    db.commit()
    # print("Query executed")

    cur.execute("select composition from music where melody1= 'CCGGAAG' and melody2 = 'EEEBABAGAGF' and rating = 0 limit 0,3")

    f=cur.fetchall()
    # print(type(f))


    # for i in f:
    #     inplist = []
    #     m1 = []
    #     print(i)
       
    for inp in f:
         inplist = []
         m1 = []
         # print("-----------inp---------------")
         # print(inp)
         for i in inp:
             for j in i:
                 # print("--------j ===="+ j)
                 if j in octave:
                     inplist.append(j)
                     inplist.append('-')
                 if j == ',' or j == '+' or j =='@':
                     inplist.append('-')
                 # print("-----inplist----------")
                 # print(inplist)
             m1 = inplist
             # print("m1--------------------------------")
             # print(m1)
             str1 = ""
             music_notes = str1.join(inplist)
             # print("music_notes--------------------------------")
             # print(music_notes)
             data = get_song_data(music_notes)
             
             data = data * (16300/np.max(data))
             write('twinkle-twinkle.mp3', samplerate, data.astype(np.int16))
             chunk = 1024
             f = wave.open(r"twinkle-twinkle.mp3","rb") 
             p = pyaudio.PyAudio()
             stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                             channels = f.getnchannels(),  
                             rate = f.getframerate(),  
                             output = True)
             data = f.readframes(chunk)
             while data:  
                 stream.write(data)  
                 data = f.readframes(chunk) 
             stream.stop_stream()  
             stream.close()  
             time.sleep(1)
             print("For melody",(inc+1),end=" ")
             inc = inc +1
             rate = int(input("Enter rating between 0 to 5 : "))
             print()
             if(rate<0 or rate > 5):
                 
                 if(rate < 0 ):
                     print("as u have entered -ve rating which is false so we will consider it as 0")
                     rate  =0
                 if(rate >5):
                     print("as u have entered rating greater than 5 which is false so we will consider it as 5")
                     rate = 5
                    
             rating.append(rate) 
             cur = db.cursor()
             
             query ="insert into music (melody1,melody2,composition,rating) values('{}','{}','{}','{}')".format(melody1,melody2,music_notes,rate)
             
             cur.execute(query)
             db.commit()
             # print("Query executed")
    query ="delete from music where rating is null"
    cur.execute(query)
    db.commit()
    print("Thank You")
