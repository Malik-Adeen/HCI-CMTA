import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def find_station_id(name):
    res = client.get('/api/stations')
    assert res.status_code == 200
    data = res.json()
    for s in data:
        if s['name'].lower().startswith(name.lower()):
            return s['id']
    return None


def test_single_leg_fare():
    # find two stations on same line (e.g., Orange: "NUST / G-12" and "Islamabad Airport")
    from_id = find_station_id('NUST / G-12')
    to_id = find_station_id('Islamabad Airport')
    assert from_id is not None and to_id is not None
    res = client.get(f'/api/fare?from_id={from_id}&to_id={to_id}')
    assert res.status_code == 200
    d = res.json()
    assert 'single_pkr' in d and 'card_pkr' in d


def test_multileg_fare_between_lines():
    # pick a pair with a valid cross-line path through shared interchange names
    # Green PIMS -> Blue PIMS -> Blue G-11 Markaz -> Electric G-11 Markaz -> Electric Bari Imam
    pims = find_station_id('NUST / G-12')
    bari_imam = find_station_id('Islamabad Airport')
    assert pims is not None and bari_imam is not None
    res = client.post('/api/fare/multileg', json={'from_id': pims, 'to_id': bari_imam})
    assert res.status_code == 200
    d = res.json()
    assert 'total_single_pkr' in d and 'legs' in d and len(d['legs']) >= 1
    # Ensure path contains both names
    assert any('NUST' in p for p in d['path'])
    assert any('Airport' in p for p in d['path'])
