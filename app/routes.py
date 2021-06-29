from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("card", __name__, url_prefix="/cards")
board_bp = Blueprint("board", __name__, url_prefix="/boards")

@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body = request.get_json()
    if ("title" not in request_body 
        or "owner" not in request_body): 
        return jsonify(details = f'Invalid data'), 400
    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])  
    db.session.add(new_board)
    db.session.commit()
    return jsonify("Successful"), 201

@board_bp.route("", methods=["GET"], strict_slashes=False)
def view_boards():
    boards=Board.query.all()
    view_boards=[board.to_json() for board in boards if boards]
    return jsonify(view_boards), 200
