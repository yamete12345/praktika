def test_dashboard_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_transactions_list_loads(client):
    resp = client.get("/transactions/")
    assert resp.status_code == 200


def test_categories_list_loads(client):
    resp = client.get("/categories/")
    assert resp.status_code == 200


def test_reports_loads(client):
    resp = client.get("/reports/")
    assert resp.status_code == 200
