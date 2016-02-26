import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.com',timeout=20)
        return True
    except urllib2.URLError as err: pass
    return False

def main():
    print internet_on()


if __name__ == "__main__":
    main()     