def ask_yes_no():
    response = input().lower()
    response_map = {
        'да': True,
        'нет': False
    }

    try:
        return response_map[response]
    except KeyError:
        print('Пожалуйста, вводите значения "да" или "нет"')
        return ask_yes_no()
