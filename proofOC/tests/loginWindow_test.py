from loginWindow import login

def test_successLogin(user, passW):
    userR, passWR = login(user, passW)
    assert userR == user
    assert passWR == passW

def test_failedLogin():
    assert login('tun', 'berberb') == (None, None)

