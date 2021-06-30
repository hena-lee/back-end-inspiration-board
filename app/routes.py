from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
from sqlalchemy import asc, desc # to add feature to sort


card_bp = Blueprint("card", __name__, url_prefix="/cards")
board_bp = Blueprint("board", __name__, url_prefix="/boards")

# BOARDS
################################################################
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
    return jsonify(board= f'Board \'{new_board.title}\', successfully created'), 201

@board_bp.route("", methods=["GET"], strict_slashes=False)
def view_boards():
    boards=Board.query.all()
    view_boards=[board.to_json() for board in boards if boards]
    return jsonify(view_boards), 200

@board_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def view_single_board(board_id):
    board = Board.query.get_or_404(board_id)
    return jsonify(board_id=board.board_id, title=board.title, owner=board.owner)  

@board_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def view_cards_in_board(board_id):
    board = Board.query.get_or_404(board_id)
    cards = Card.query.filter_by(board_id=int(board_id))
    cards_in_board = [card.to_json() for card in cards if cards]
    return jsonify(board_id=int(board_id), title=board.title, cards=cards_in_board)

@board_bp.route("/<board_id>/cards", methods=["POST"], strict_slashes=False)
def create_card_in_board(board_id):
    request_body = request.get_json()
        # (new message shouldn't have capability of increasing likes_count)
        # (does the user still need to input board_id if it's included in URL?) YES in Front end not in back end = in the form body
    if ("message" not in request_body):  
        return jsonify(details = f'Invalid data'), 400
    new_card_in_board = Card(message=request_body["message"],
                            board_id=board_id)
    db.session.add(new_card_in_board)
    db.session.commit()
    return jsonify(new_card_in_board.to_json()), 200

###############################################################

@card_bp.route("/<card_id>/like", methods=["PUT"], strict_slashes=False)
def update_card(card_id):
    # Because cards are all displayed at this point, user can only click 
    # the like or not click so the cards are there, we still need to 
    # modify card and that's why we query it

    card = Card.query.get(card_id)

    # we don't need any data in the request body, 
    # just need request sent from user to this endpoint
    card.likes_count += 1
    db.session.commit()
    return jsonify(card=card.to_json())

@card_bp.route("/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify(card = f'Card {card.card_id} "{card.message}" successfully deleted')

# STRETCH 
########################################################################

@board_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def view_cards_in_board_by_query(board_id):

    #  i have a board which has cards
    board = Board.query.get_or_404(board_id)
    # and its cards
    cards = board.cards # [{}, {}, {}]
    
    # this is asc, desc or id (which is cards?? fuzzy on this)
    sort_by = request.args.get("sort") 

    # once I have all cards of that board I order them by specified request
    if sort_by == "asc":  
        # # this is a list (queried by likes_count) in asc order

        # cards = Card.query.order_by(Card.likes_count.asc()).all() 

        #  or should I do this
        cards = cards.order_by(Card.likes_count.asc())
        # likes_asc = cards.order_by(Card.likes_count.asc()).all()

    elif sort_by == "desc":
        # this is a list (queried by title) in desc order
        cards = cards.order_by(Card.likes_count.desc())
        
    elif sort_by == "id":
        # list, queried by id in asc order:
        cards = cards.order_by(Card.card_id.asc())
        # cards = cards.order_by(Card.card_id.asc()).all()  

        card_response = [card.to_json() \
                for card in cards]
    return jsonify(card_response), 200




# MAY OR MAY NOT IMPLEMENT BELOW:
#########################################################################

# @board_bp.route("/<board_id>", methods=["DELETE"], strict_slashes=False)
# def delete_board(board_id):
#     board = Board.query.get_or_404(board_id)
#     # why don't cards in board get deleted when boards get deleted?
#     cards = Card.query.filter_by(board_id=int(board_id))
#     for card in cards:
#         db.session.delete(card)
#     db.session.delete(board)
#     db.session.commit()
#     return jsonify(board = f'Board {board.board_id} "{board.title}" successfully deleted')

# @board_bp.route("", methods=["DELETE"], strict_slashes=False)
# def delete_all_board():
#     boards = Board.query.all()
#     cards = Card.query.all()
#     for board in boards:
#         db.session.delete(board)
#     for card in cards:
#         db.session.delete(card)
#     db.session.commit()
#     return jsonify(board = f'All boards successfully deleted'), 200
