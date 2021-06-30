from app.models.board import Board
from app.models.card import Card
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []
    
# still working on TDD
# def test_get_boards_one_saved_board(client, one_board):
#     # Act
#     response = client.get("/boards")
#     response_body = response.get_json()
#     # Assert
#     assert response.status_code == 200
#     assert len(response_body) == 1
#     assert response_body == [
#         {
#             "board_id": 1,
#             "title": "Go on my daily walk :national_park:",
#             "owner": "Notice something new every day"
#         }
#     ]