def test_index(test_client, auth_fixture):
    response = test_client.get("/")
    assert response.status_code == 200
    print(response.data)
    assert b"<h2>All Videos</h2>" in response.data
    # test section with public videos and user videos
    auth_fixture.login()
    response = test_client.get("/")
    assert b"<h2>All Videos</h2>" in response.data
    assert b"<h2>My Videos</h2>" in response.data
