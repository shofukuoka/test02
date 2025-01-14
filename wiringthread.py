# coding: UTF -8
import wiringpi as wiringpi
from time import sleep
from datetime import datetime, timedelta
import time
import threading
import pygame.mixer
#from pygame.mixer import Sound
#import logTable
import commentjson
#import logging.config

#logging.config.fileConfig('logging.conf')
  
#logger = logging.getLogger()



#logTable.create_table()

pygame.mixer.init()
#pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer =512)



with open('/home/pi/Desktop/simple_flask/config.json') as f:
    config = commentjson.load(f)
GPIO_LED = config["GPIO_LED1"] #GPIO_LED = 12
GPIO_SW = config["GPIO_SW1"] #GPIO_SW = 26

announce1 = config["Bannounce1"]
announce2 = config["Bannounce2"]
announce3 = config["Bannounce3"]
announce4 = config["Bannounce4"]
t1 = config["Bthannounce1"]
t2 = config["Bthannounce2"]
t3 = config["Bthannounce3"]
t4 = config["Bthannounce4"]
t5 = config["Bthannounce5"]

door1opentime = config["Door1opentime"]
blinktime1 = config["Blinktime1"]




wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(GPIO_LED, 1)  # sets GPIO 22 to 1(On)
wiringpi.pinMode(GPIO_SW, 0)  # sets GPIO 4 to input
wiringpi.pullUpDnControl(GPIO_SW, wiringpi.PUD_DOWN)

wiringpi.digitalWrite(GPIO_LED, 0)  # sets port 22 to 0 (0V, off)

log_file = "/home/pi/Desktop/simple_flask/LOG/log.txt"
error_log = "/home/pi/Desktop/simple_flask/LOG/error_log.txt"
status_log = "/home/pi/Desktop/simple_flask/LOG/status_log.txt"
start_blink = None
global counter
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
user_id = 0
status_blink = False

def blink_led():
    while True: # Run forever
        wiringpi.digitalWrite(GPIO_LED, 1) # Turn on
        sleep(0.5) # Sleep for 0.5 seconds
        wiringpi.digitalWrite(GPIO_LED, 0) # Turn off
        sleep(0.5)
        global stop_threads 
        if stop_threads: 
            break
stop_threads = False

def count_people():
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d")
    f = open(log_file, "r", )
    data = f.read().split("\n")
    f.close()
    temp = 0
    for x in data:
        if date_time in x:
            temp = temp + 1

    return temp




def thAnn1():
    global  counter1
    global user_id
    counter1 += 1
    print ("男子 duration : 1  minutes",counter1)
#    store_log(str(counter1))
    sound0 = pygame.mixer.Sound(announce1)
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id,1.0)




def thAnn2():
    global  counter2
    global user_id
    counter2 += 1
    print ("男子 duration : 2 minutes", counter2)
#    store_log(str(counter2))
    sound0 = pygame.mixer.Sound(announce2)
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 2.0)


def thAnn3():
    global counter3
    global user_id
    global status_blink
    global start_blink
    global stop_threads
    counter3 += 1
    print ("男子 duration : 3  minutes" , counter3)
#    store_log(str(counter3))
    sound0 = pygame.mixer.Sound(announce3)
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 3.0)
    


def thAnn4():
    global counter4
    global user_id
    counter4 += 1
    print ("男子 duration : 4  minutes", counter4)
#    store_log(str(counter4))
    sound0 = pygame.mixer.Sound(announce4)
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0)
    channel0.set_volume(2.0, 0.0)
    #logTable.update_table(user_id, 4.0)


def thAnn5():
    global counter5
    global user_id
    counter5 += 1
    print ("男子 duration : 5  minutes", counter5)
    sound0 = pygame.mixer.Sound(announce4)
    channel0 = pygame.mixer.Channel(0)
    channel0.play(sound0, 10)
    channel0.set_volume(2.0, 0.0)




def stop_thAnn5():
    th5.cancel()

th1 = threading.Timer(t1, thAnn1)
th2 = threading.Timer(t2, thAnn2)
th3 = threading.Timer(t3, thAnn3)
th4 = threading.Timer(t4, thAnn4)
th5 = threading.Timer(t5, thAnn5)

def start_waiting():
    global th1
    global th2
    global th3
    global th4
    global th5

    th1 = threading.Timer(t1, thAnn1) #
    th2 = threading.Timer(t2, thAnn2)
    th3 = threading.Timer(t3, thAnn3)
    th4 = threading.Timer(t4, thAnn4)
    th5 = threading.Timer(t5, thAnn5)


    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()


def stop_waiting():

    th1.cancel()
    th2.cancel()
    th3.cancel()
    th4.cancel()
    th5.cancel()


def start():
    global counter
    durationStop = datetime.now() - timedelta(days=1)
    duration1 = 0
    duration3 = 0
    status_toilet = "free"
    start_d = datetime.now()
    global user_id
    global start
    global end
    global status_blink
    global stop_threads
    global start_blink

    start_time = datetime.now()
    read0 = 1
    logcount = count_people()
    temp_count = logcount
    while True:

        time.sleep(0.1)
        read1 = wiringpi.digitalRead(GPIO_SW)
        #print "read1= %d" % read1
        #print("debug boy blink check\n ")
        if status_blink and (status_toilet == "free"):
            #print("debug boy blink stop")
            if (datetime.now() - durationStop).seconds>1:
                try:
                    #print("stop blink")
                    print("\nboy stop blink")
                    stop_threads = True
                    start_blink.join()
                    status_blink = False
                    #print("stop blink check")      
                    duration = (datetime.now() - start_time).seconds /60       
                    start_time = datetime.now()
                    duration = str(duration)     
                    #store_log(duration + "\n 男子トイレ使用終了\n") 
                    status("Free")
                    print (duration)
                    #print ("\n男子トイレ使用終了")
                    
                    temp_count = logcount
                    status_toilet = "free"
                except Exception as e:
                    logger.error("boy blink stop err")
                    logger.error(e)

        elif (not status_blink) and status_toilet == "busy":
            #print("debug girl blink start\n")
            if (datetime.now() - start_time).seconds > blinktime1:
                try:
                    stop_threads = False
                    print("boy start blink")    
                    start_blink = threading.Thread(target=blink_led, args=())
                    start_blink.start()
                    status_blink = True
                
                except Exception as e: 
                    logger.error("boy blink start err")
                    logger.error(e)
        if read0 == read1:
            continue

        time.sleep(0.05) #50milliseconds
        read2 = wiringpi.digitalRead(GPIO_SW)
        now = datetime.now()
#        date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
        current_date= now.strftime("%Y/%m/%d ")
        current_time = now.strftime("%H:%M:%S")
        end = datetime.now()
        

        if read1 == read2:
            if read1 == 1:
                start_waiting()
                duration1 = datetime.now() - durationStop
                #start_waiting()
                #start_d = datetime.now()
                
                if (duration1.seconds < door1opentime) :
                    #print("debug boy within 5sec")
                    try:
                        
                        store_log("3" )
                        #user_id = logTable.insert_table(1, current_date, current_time ,3, "Boy ON/OFF", duration = 0)
                        wiringpi.digitalWrite(GPIO_LED, 1) # switch on LED. Sets port 12 to 1 (3V3, on)
                        status("Boy on/off")
                        status_toilet = "busy"
                        print("\n Boy on/off")
                    except Exception as e:
                        logger.error("boy on/off err")
                        logger.error(e)
               
                    
                    
                else:
                    #print("debug boy busy")
                    try:
                        start_time = datetime.now()         
                        status_toilet = "busy"
                        logcount = logcount + 1
                        start_d = datetime.now()
                        duration = str(duration)
                        print ("person count:" + str(logcount))
                        wiringpi.digitalWrite(GPIO_LED, 1)  # switch on LED. Sets port 12 to 1 (3V3, on)
                        store_log("1" )
                        status("Busy")
                        print("\n Boybusy\n")
                        #print("debug before insert boy to db")
                        
                        #user_id = logTable.insert_table(1, current_date, current_time, 1, "Boy Busy", duration=0)
                        #print("debug after insert boy to db")
                    except Exception as e:
                        logger.error("boy on err")
                        logger.error(e)


            else:
                try:

                    #print("debug boy ann stop")  
                    stop_waiting()
                    pygame.mixer.Channel(0).stop()
                    status_toilet = "free"
                    durationStop = datetime.now()
                    time_end = datetime.now()
                    duration = time_end - start_d
                    #duration = duration.seconds / 60.0
                    wiringpi.digitalWrite(GPIO_LED, 0) # switch off LED. Sets port 12 to 0 (0V, off)
                    #print("debug boy before stop ann")
                    
                    #print("debug boy after stop ann")
                    #if temp_count<logcount:
                    duration = str(duration)         
                    store_log("2" + ","   + duration )
                    
                    #user_id = logTable.insert_table(1, current_date, current_time, 2, "Boy Free", duration=duration)
                    status("Free")
                    #print (duration)
                    print ("\n boy free")
                    temp_count = logcount
                except Exception as e:
                    logger.error("boy off err")
                    logger.error(e)
            # else:
                if temp_count > logcount:
                    logTable.update_table(user_id, duration)
                    temp_count = logcount
        read0 = read1


def store_log(log):
    global logcount
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log = date_time + " " + log
    try:
        f = open("/home/pi/Desktop/simple_flask/LOG/boy.csv", "a+", )
        f = f.write("{0},{1}\n".format(now.strftime("%Y/%m/%d  %H:%M:%S"),str(log)))
        f.close()
    except:
        store_error("file open error!!\n")



def status(log):
    #   print(log)
    try:
        f = open(status_log, "w+")
        f.write(log)
        f.close()
    except:
        store_error("file open error!!\n")


def store_error(log):
    now = datetime.now()
    date_time = now.strftime("[%Y/%m/%d  %H:%M:%S]")
    text_log = date_time + " " + log
    try:
        f = open(error_log, "a+")
        f.write(text_log)
        f.close()
    except:
        print("ERROR")
        




