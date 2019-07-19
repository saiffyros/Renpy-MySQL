
define e = Character("Eileen")

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

                import urllib
                import urllib2

                url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com/action_login.php"
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
                data = urllib.urlencode({'email' : email,'password' : password})
                userList = str(opener.open(url, data=data).read()).split(",")
                user1 = User(userList[0], userList[1], userList[2])
                print(user1.success + " " + user1.error + " " + user1.email)

                import json
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
            import urllib2
            url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com:3000/message"
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))

            userList2 = str(opener.open(url).read())

        except:
            userList2 = "We couldn't connect to the internet."

    e "[userList2]"

    e "Let's try the Requests module now."

    init python:
        import requests
        try:
            url = "http://ec2-3-18-214-161.us-east-2.compute.amazonaws.com:3000/message"
            data = requests.get(url)
        except:
            data = "Connection failed."

    e "Let's see:"
    e "[data]"
    e "Let's try an API now."
    e "Do you like music?"
    e "What is a singer you like?"
    $ singer = renpy.input("type singer's name")
    e "Singer name is [singer]"
    python:
        urlDeezer = "http://api.deezer.com/user/2529"
        try:
            songsDeezer = requests.get(urlDeezer)
            data2 = songsDeezer.json()
            print(data2)
        except:
            songsDeezer = "It didn't work"

    show screen windowTest
    pause 5.0
    e "Bye"

    return

screen windowTest:
    #$ data2 = {'name' : "Rodrigo", 'age' : 15}
    frame:
        style "file_picker_frame"
        viewport:
            scrollbars "vertical"
            xmaximum 400
            mousewheel True
            has vbox

            for i in data2:
                text i
