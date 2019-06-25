
define e = Character("Eileen")

label start:

    scene bg room
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

        url = "http://ec2-18-224-67-146.us-east-2.compute.amazonaws.com/action_login4.php"
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
        data = urllib.urlencode({'email' : email,
                                'password'  : password})
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

    show eileen happy

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
