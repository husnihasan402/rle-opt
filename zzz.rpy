init python:

    config.language = "russian"
    lang = persistent.lang

label splashscreen:
    scene black
    with Pause(1)



    show text "Внимание!\nДанная игра предназначена для лиц старше 18 лет.\nВ переводе присутствует куча ошибок и очепяток.\nПеревод на русский выполнил CreDz.\n\n{a=https://boosty.to/credz}Boosty{/a}\n{a=https://t.me/+HkcRT6AapqQxZmNi}telegram{/a}" with dissolve
    $ lang = "russian"
    $ persistent.lang = "russian"
    $ renpy.change_language("russian")
    menu:

        "Мне 18+, я готов на очепятки":
            $ lang = "russian"
            $ renpy.change_language("russian")
        "Мне меньше 18/я не могу смириться с ошибками и очепятками ":
            "До свидания."
            $ renpy.quit()

    with Pause(3)


    hide text with dissolve
    with Pause(1)

    return
