def test_thread_page_has_code_of_conduct_link(client):
    res = client.get('/community/t/deploy-technofatty/')
    html = res.content.decode()
    assert '/code-of-conduct/' in html
