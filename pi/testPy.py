

def RunMe():

    try:
        with open("/home/pi/testPyExecuted.txt", "w+") as myfile:
            myfile.write("File created....and python file executed for version 1.2"+"\r\n")

    except Exception,e:
        print str(e)

RunMe()