from app.models.board import Board
from app.models.card import Card

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "owner": "tash-force",
            "title": "Test Board"
        }
    ]

def test_get_boards_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "board_id": 1,
            "owner": "tash-force",
            "title": "Test Board 1"
        },
        {
            "board_id": 2,
            "owner": "tash-force",
            "title": "Test Board 2"
        },
        {
            "board_id": 3,
            "owner": "tash-force",
            "title": "Test Board 3"
        }
    ]

def test_get_single_board_by_id(client, three_boards):
    #Act
    response = client.get("/boards/2")
    #Arrange
    response_body = response.get_json()
    
    #Assert
    assert response.status_code == 200
    assert "board_id" in response_body
    assert response_body == {
            "board_id": 2,
            "owner": "tash-force",
            "title": "Test Board 2"
        }

def test_create_board(client):
    
    #Act
    body = {"title": "Test Board 1",
    "owner": "tash-force"}

    response = client.post("/boards", json=body)

    #Arrange
    response_body = response.get_json()
    
    #Assert
    assert response_body == {
            "board_id": 1,
            "owner": "tash-force",
            "title": "Test Board 1"
        }
    assert "board_id" in response_body
    assert "owner" in response_body
    assert "title" in response_body

