from coresite import moderation


def test_report_thread_adds_to_queue(client):
    moderation.REPORT_QUEUE.clear()
    res = client.get('/community/t/deploy-technofatty/report/')
    assert res.status_code == 302
    assert len(moderation.REPORT_QUEUE) == 1
    entry = moderation.REPORT_QUEUE[0]
    assert entry['target']['type'] == 'thread'
    assert entry['target']['id'] == 'deploy-technofatty'
