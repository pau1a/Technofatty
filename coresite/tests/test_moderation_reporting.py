from coresite import moderation


def test_report_thread_adds_to_queue(client):
    moderation.REPORT_QUEUE.clear()
    res = client.get('/community/t/deploy-technofatty/report/')
    assert res.status_code == 302
    assert len(moderation.REPORT_QUEUE) == 1
    entry = moderation.REPORT_QUEUE[0]
    assert entry['target']['type'] == 'thread'
    assert entry['target']['id'] == 'deploy-technofatty'


def test_report_answer_adds_to_queue(client):
    moderation.REPORT_QUEUE.clear()
    res = client.get('/community/t/deploy-technofatty/a/1/report/')
    assert res.status_code == 302
    assert len(moderation.REPORT_QUEUE) == 1
    entry = moderation.REPORT_QUEUE[0]
    assert entry['target']['type'] == 'answer'
    assert entry['target']['thread'] == 'deploy-technofatty'
    assert entry['target']['id'] == 1


def test_thread_page_has_report_links(client):
    res = client.get('/community/t/deploy-technofatty/')
    assert res.status_code == 200
    html = res.content.decode()
    assert '/community/t/deploy-technofatty/report/' in html
    assert '/community/t/deploy-technofatty/a/1/report/' in html
