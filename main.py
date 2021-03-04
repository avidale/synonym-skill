from dialogic.dialog_connector import DialogConnector
from dialogic.server.flask_server import FlaskServer

from dm import make_dm
import scenarios  # noqa

dm = make_dm()
connector = DialogConnector(dialog_manager=dm)
server = FlaskServer(connector=connector)


if __name__ == '__main__':
    server.parse_args_and_run()
