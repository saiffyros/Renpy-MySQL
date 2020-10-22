
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
    #
    # show test1:
    #     xalign .5
    #     yalign .2

    e "Quer logar na sua conta?"

    menu:
        "Testar o email":
            python:
                email = renpy.input("type in email")
                password = renpy.input("type in password")

            e "Seu email é [email]"
            e "Seu password é [password]"

            python:

                class User:
                    def __init__(self, success, error, email):
                        self.success = success
                        self.error = error
                        self.email = email

                url = "http://triviumpage.brazilsouth.cloudapp.azure.com/action_login.php"
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

        "Ignore por enquanto":
            "ok"

    show eileen happy

    e "Vamos testar sua conexão"
    menu:
        "Sim":

            e "Certifique-se de que você está conectado a internet"

            python:
                try:
                    url = "http://triviumpage.brazilsouth.cloudapp.azure.com:8080/test"
                    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))

                    userList2 = str(opener.open(url).read())

                except:
                    userList2 = "Nós não conseguimos te conectar a internet."

            e "[userList2]"

            e "Vamos testar o módulo Requests agora."

            python:
                try:
                    url = "http://triviumpage.brazilsouth.cloudapp.azure.com:8080/test"
                    data = requests.get(url)
                except:
                    data = "Conexão falhou."

            e "Vamos ver:"
            e "[data]"

        "Não":
            e "Ok"

    e "Vamos tentar conectar a uma API agora."
    e "Vamos ver quem são os astrontautas a bordo da estação espacial neste momento usando a API da NASA."
    e "Conectando a NASA"

    show screen windowTest
    pause 5.0
    e "Se sua conexão estiver funcionando, aqui estão eles:"
    hide screen windowTest
    e "Vamos testar mais uma API."
    menu:
        "Você gosta de música?":
            e "Você gosta de música?"
            e "Digite o seu artista favorito"
            $ Murl = renpy.input("digite o nome do artista/banda")
            show screen windowTest2
            pause 5.0
            e "Aqui estão as músicas que encontrei!"
            e "Espero que tenha funcionado."
            hide screen windowTest2
        "Ignore a musica por enquanto":
            e "Ok, pulando"
    e "Último teste agora"
    e "Vou me conectar a NASA novamente"

    python:
        try:
            url2 = "https://api.nasa.gov/planetary/apod?api_key=ZPtIOYfr4syaqB6Koum0jYAvXMxcVaTZyecD9V5q"
            resp2 = urllib.urlopen(url2)
            resp = json.loads(resp2.read())

            downloadImage(resp["url"], "image1234.png")

            title1 = resp["title"]
            explanation1 = resp["explanation"]

        except:

            url2 = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2017-07-12"
            resp2 = urllib.urlopen(url2)
            resp = json.loads(resp2.read())

            downloadImage(resp["url"], "image1234.png")

            title1 = resp["title"]
            explanation1 = resp["explanation"]

    show screen nasaPic
    pause 5.0

    e "Aqui a imagem do dia da NASA."
    e "Bom, por hoje era isso"
    e "Espero que tenha se divertido!"
    e "Tchau"

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
