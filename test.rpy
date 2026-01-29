init python:
    def get_all_character_dialogue(character_name):
        dialogue_sequence = []

        for label_name, block in renpy.game.script.namemap.items():
            if hasattr(block, 'block'):
                for node in block.block:
                    if isinstance(node, renpy.ast.Say) and node.who == character_name:
                        dialogue_sequence.append({
                            "label": label_name,
                            "text": node.what,
                            "character": node.who
                        })

        return dialogue_sequence

screen dialogue_player(character_name):
    modal True
    zorder 1000

    # Фон как в игре
    add "bg room"  # Замените на ваш фон

    # Окно диалога
    window:
        style "say_window"
        xalign 0.5
        yalign 1.0

        vbox:
            # Имя персонажа
            if current_dialogue_index < len(dialogue_playlist):
                text character_name:
                    style "say_label"

            # Текст реплики
            if current_dialogue_index < len(dialogue_playlist):
                text dialogue_playlist[current_dialogue_index]["text"]:
                    style "say_dialogue"

    # Управление
    vbox:
        xalign 1.0
        yalign 0.0
        spacing 10

        textbutton "▶ Следующая" action [
            If(current_dialogue_index < len(dialogue_playlist) - 1,
                SetVariable("current_dialogue_index", current_dialogue_index + 1),
                Hide("dialogue_player")
            )
        ]

        textbutton "⏸ Пауза" action ToggleVariable("auto_play")
        textbutton "⏹ Стоп" action [Hide("dialogue_player"), SetVariable("auto_play", False)]
        text "Реплика [current_dialogue_index + 1]/[len(dialogue_playlist)]"

default dialogue_playlist = []
default current_dialogue_index = 0
default auto_play = False

label start_character_dialogue(character_name="[RogueX.Name]"):
    $ dialogue_playlist = get_all_character_dialogue(character_name)
    $ current_dialogue_index = 0

    if not dialogue_playlist:
        "Реплики для персонажа [character_name] не найдены."
        return

    show screen dialogue_player(character_name)

    # Автопрогон
    while auto_play and current_dialogue_index < len(dialogue_playlist) - 1:
        $ current_dialogue_index += 1
        pause 2.0  # Пауза между репликами

    return
