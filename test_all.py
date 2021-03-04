from dialogic.testing.testing_utils import make_context

from dm import make_dm
import scenarios  # noqa


def test_dm():
    manager = make_dm()
    ctx = make_context(new_session=True, text='шалом')
    ctx.source = 'text'
    resp = manager.respond(ctx)
    assert resp
    assert 'выход' in resp.suggests
    assert 'Привет' in resp.text
    assert 'Синоним' in resp.text

    c2 = make_context(prev_response=resp, text='собака')
    r2 = manager.respond(c2)
    assert 'собака' in r2.text
