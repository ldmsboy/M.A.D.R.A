import pytest
from graph_analyzer import GraphAnalyzer


def sample_data():
    return {
        "nodes": [
            {"id": "A", "label": "A"},
            {"id": "B", "label": "B"},
            {"id": "C", "label": "C"},
        ],
        "edges": [
            ["A", "B", 1],
            ["B", "C", 2],
            ["A", "C", 10]
        ]
    }


def test_shortest_path_basic():
    ga = GraphAnalyzer(sample_data(), critical_threshold=3)
    res = ga.find_shortest_path('A', 'C')
    assert res['path'] == ['A', 'B', 'C']
    assert res['cost'] == pytest.approx(3)
    # critical edges are those with weight < 3 -> A->B (1) and B->C (2)
    assert ('A', 'B', 1.0) in res['critical_edges']


def test_no_path():
    data = sample_data()
    # remove B->C to break path
    data['edges'] = [["A", "B", 1]]
    ga = GraphAnalyzer(data)
    res = ga.find_shortest_path('A', 'C')
    assert res['path'] == []
    assert res['cost'] == float('inf')


def test_invalid_node():
    ga = GraphAnalyzer(sample_data())
    with pytest.raises(KeyError):
        ga.find_shortest_path('X', 'C')
