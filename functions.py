import random
def shuffle(arr):
    return random.shuffle(arr)


import time
def countdowntimer(t):
    while t:
        mins, sec = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins,sec)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("end/next photo")