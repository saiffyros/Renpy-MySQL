
define e = Character("Eileen")

init python:
    import urllib
    import urllib2
    import requests
    import json
    import os

    def downloadImage(url, imageName):
        openurl = urllib2.build_opener()
        page1 = openurl.open(url)
        pic = page1.read()
        filename = os.path.join(config.gamedir + "/images", (imageName))
        fout = open(filename, "wb")
        fout.write(pic)
        fout.close()

label start:

    $ data2 = "test"

    scene bg room

    e "Do you wanna log into your account?"

    menu:
        "Try your email":
            python:
                email = renpy.input("type in email")
                password = renpy.input("type in password")

            e "your email is [email]"
            e "your password is [password]"

            python:

                class User:
                    def __init__(self, success, error, email):
                        self.success = success
                        self.error = error
                        self.email = email

                url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com/action_login.php"
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
                data = urllib.urlencode({'email' : email,'password' : password})
                userList = str(opener.open(url, data=data).read()).split(",")
                user1 = User(userList[0], userList[1], userList[2])
                print(user1.success + " " + user1.error + " " + user1.email)

                # get a Json
                x = str(opener.open(url, data=data).read())
                # parse x:
                y = json.loads(x)
                # the result is a Python dictionary:
                print(y["success"])
                renpy.notify(y["success"])
                renpy.notify(y["error"])
                if len(y["error"]) > 1:
                    renpy.jump("start")

        "Ignore it":
            "ok"

    show eileen happy

    e "Ok, Let's check your connection."
    e "Make sure you're connect to the wifi or mobile data."

    python:
        try:
            url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com:3000/message"
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))

            userList2 = str(opener.open(url).read())

        except:
            userList2 = "We couldn't connect to the internet."

    e "[userList2]"

    e "Let's try the Requests module now."

    python:
        try:
            url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com:3000/message"
            data = requests.get(url)
        except:
            data = "Connection failed."

    e "Let's see:"
    e "[data]"
    e "Let's try an API now."
    e "Let's see who's working on the ISS now"
    e "Let me try to connect to NASA"

    show screen windowTest
    pause 5.0
    e "Here they are, if you're connected."
    hide screen windowTest
    e "Let's try one more."
    menu:
        "Check music with Deezer":
            e "Do you like music?"
            e "Tell me the name of your favorite artist."
            $ Murl = renpy.input("type the name of the artist/band")
            show screen windowTest2
            pause 5.0
            e "Here are the songs."
            e "I hope it worked."
            hide screen windowTest2
        "Ignore music":
            e "Ok, skipping"
    e "Last test now."
    e "Let's try and connect to NASA once again."

    python:
        try:
            url2 = "https://api.nasa.gov/planetary/apod?api_key=DKkIVysTrVNs2wj5egA301FCy4fcFn6dM4J7oP0j"
            resp2 = urllib.urlopen(url2)
            resp = json.loads(resp2.read())

            downloadImage(resp["url"], "image1234.png")

            title1 = resp["title"]
            explanation1 = resp["explanation"]

        except:
            title1 = "It didn't work"
            explanation1 = "You might not be connected to the internet. Please check if your connection ir working and try again."

    show screen nasaPic
    pause 5.0

    e "Well, that's it for today."
    e "I hope you had fun."
    e "Bye"

    return

screen windowTest:
    frame:
        python:
            try:
                #mostra quais astronautas estão na ISS agora
                people = requests.get('http://api.open-notify.org/astros.json')
                dataT = people.json()
            except:
                dataT = {"people": [{"name": "Not connected"}, {"name": "to the internet"}]}
        style "file_picker_frame"
        viewport:
            scrollbars "vertical"
            xmaximum 400
            mousewheel True
            has vbox

            #busca uma seção do arquivo json e imprime um valor dentro dele, neste caso os nomes dos astronautas
            for i in dataT["people"]:
                text i["name"]

screen windowTest2:
    frame:
        python:
            try:
                # testing = requests.get("http://api.deezer.com/artist/" + Murl)
                # testingData = testing.json()
                # idd = testingData["id"]
                #
                # urlM = "http://api.deezer.com//artist//" + str(idd) + "//top?limit=50"
                #
                # musicT = requests.get(urlM)
                #
                # data2T = musicT.json()

                url = "https://api.deezer.com/search?q=" + Murl
                testingData = urllib.urlopen(url)
                testingData2 = testingData.read()

                data2T = json.loads(testingData2)

            except:
                data2T = {"data": [{"title_short": "Not connected"}, {"title_short": "to the internet"}]}
        style "file_picker_frame"
        viewport:
            scrollbars "vertical"
            xmaximum 400
            mousewheel True
            has vbox
            for i in data2T["data"]:
                text i["title_short"]

screen nasaPic:

    if len(explanation1) > 120:
        add "image1234.png":
            xalign 0.5
            yalign 0.5
    text title1:
        xalign 0.5
        yalign 0.2
        size 35
    text explanation1:
        xalign 0.5
        yalign 0.6
