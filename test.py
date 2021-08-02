f = open("Settings.txt", "r")
if f.readline() == "True":
    do_not_show = True

else:
    do_not_show = False