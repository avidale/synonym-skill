"""
Это минимальный пример простого навыка, не использующего dialogic
С основным навыком он не связан
"""
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
@app.route('/alice/', methods=['POST'])
def respond():
    data = request.json
    command = data.get('request', {}).get('command', '')

    end_session = False

    if 'выход' in command:
        response_text = 'До свидания!'
        end_session = True
    elif command:
        response_text = f'Вы сказали {command}'
    else:
        response_text = 'Привет! Вы ничего не сказали.'

    response = {
        'response': {
            'text': response_text,
            'end_session ': end_session
        },
        'version': '1.0'
    }
    return response


app.run(host='0.0.0.0', port=5000, debug=True)
