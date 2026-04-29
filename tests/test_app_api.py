import json

import pytest


def test_get_data():
    import app
    client = app.app.test_client()
    r = client.get('/data')
    assert r.status_code == 200
    body = r.get_json()
    assert 'nodes' in body and 'edges' in body


def test_analyze_success():
    import app
    client = app.app.test_client()
    # Use nodes present in the expanded network_data.json
    r = client.post('/analyze', json={'start': 'A21', 'end': 'A8'})
    assert r.status_code == 200
    body = r.get_json()
    assert 'path' in body and 'cost' in body


def test_analyze_missing_params():
    import app
    client = app.app.test_client()
    r = client.post('/analyze', json={'start': 'Workstation1'})
    assert r.status_code == 400
