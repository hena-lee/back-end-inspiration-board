import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield app
    # close and remove the temporary database
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database

@pytest.fixture
def one_board(app):
    new_board = Board(
        title="Test Board", owner="tash-force")
    db.session.add(new_board)
    db.session.commit()


# still testing
# # This fixture gets called in every test that
# # references "three_tasks"
# # This fixture creates three tasks and saves
# # them in the database
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(
            title="Test Board 1", owner="tash-force"),
        Board(
            title="Test Board 2", owner="tash-force"),
        Board(
            title="Test Board 3", owner="tash-force")
    ])
    db.session.commit()
    
# @pytest.fixture
# def board_cards(app, board_id):
#     db.session.add_all([
#         Card(
#             message="Test Card 1", likes_count=0, board_id=board_id)
#         )
#     ])
#     db.session.commit()



