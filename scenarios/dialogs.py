from dialogic import COMMANDS
from dialogic.cascade import DialogTurn

from dm import csc
from scenarios.synonym_finder import make_synonym_response


def is_single_pass(turn: DialogTurn) -> bool:
    """ Check that a command is passed when the skill is activated """
    if not turn.ctx.yandex:
        return False
    if not turn.ctx.yandex.session.new:
        return False
    return bool(turn.ctx.yandex.request.command)


def is_new_session(turn: DialogTurn):
    return turn.ctx.session_is_new() or not turn.text


@csc.add_handler(priority=100, checker=is_single_pass)
def single_pass(turn: DialogTurn):
    make_synonym_response(turn)
    turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
@csc.add_handler(priority=3, checker=is_new_session)
@csc.add_handler(priority=0)  # use it as a fallback scenario
def hello(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке "Синоним к слову". ' \
                         'Скажите любое слово, а я найду синонимы к нему.'
    turn.suggests.append('выход')


@csc.add_handler(priority=10, intents=['help', 'Yandex.HELP', 'like_alice'])
def do_help(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке "Синоним к слову". ' \
                         'Скажите любое слово, а я найду синонимы к нему.' \
                         '\nЧтобы выйти, скажите "хватит".'
    turn.suggests.append('выход')


@csc.add_handler(priority=10, intents=['total_exit'])
def total_exit(turn: DialogTurn):
    turn.response_text = 'Было приятно пообщаться! ' \
                         'Чтобы обратиться ко мне снова, ' \
                         'запустите навык "Синоним к слову".'
    turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=1)
def find_synonym_fallback(turn: DialogTurn):
    if not turn.text:
        return
    make_synonym_response(turn)


@csc.add_handler(priority=10, intents=['what_word'])
def what_word(turn: DialogTurn):
    word = turn.user_object.get('word')
    if word:
        turn.response_text = f'Вы говорили о слове {word}'
        turn.next_stage = 'word'
    else:
        turn.response_text = 'Вы ещё не искали синонимы'


@csc.add_handler(priority=20, intents=['synonyms_ellipsis'], stages=['word'])
def synonyms_ellipsis(turn: DialogTurn):
    word = turn.user_object.get('word')
    make_synonym_response(turn, word=word)
