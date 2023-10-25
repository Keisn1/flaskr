from project import create_app


def test_config():
    """
    Tests for default configuration
    """
    assert not create_app().testing
    assert create_app(testing=True).testing is True


# def test_hello_world(test_client):
#     response = test_client.get("/")
#     assert response.status_code == 200
#     assert response.data == b"Hello World!"
