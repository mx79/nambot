import time
import chess
from routes import all_chess_games, auth_required
from flask import redirect, render_template, request, session
from pkg.authlib.auth import db, get_random_string


def create_chess_url(key: str, sender_email: str, opponent_email: str):
    """
    Description:

    :param key:
    :param sender_email:
    :param opponent_email:
    """
    db.tmp_chess_url.insert_one({
        "url": key,
        "created_at": int(time.time()),
        "sender_email": sender_email,
        "receiver_email": opponent_email
    })


def check_possible_move_for_this_piece(game_id: str, piece_type: str):
    """
    Description:

    :param game_id:
    :param piece_type:
    :return: A list of all possible move for this piece.
    """
    board = all_chess_games[game_id]
    moves = [str(legal_move) for legal_move in list(board.legal_moves) if piece_type == str(legal_move)[0]]
    pawn_moves = [str(legal_move) for legal_move in list(board.legal_moves)
                  if str(legal_move)[0] in ["a", "b", "c", "d", "e", "f", "g", "h"]]
    res = {"possible_moves": moves} if moves else {"possible_moves": pawn_moves}

    return res


def update_chess_board(game_id: str):
    """
    Description:

    :param game_id:
    """


@auth_required
def chess(tmp_string: str = None):
    """
    Description:

    :return:
    """
    if request.method == "POST":
        if tmp_string is None:
            key = get_random_string(16)
            opponent_email = request.form.get("opponent_email")
            create_chess_url(key, session.get("email"), opponent_email)
            all_chess_games[session.get("email")] = chess.Board()
            return redirect(f"/chess/{key}")
        else:
            # if request.headers.get("") == "check":
            return check_possible_move_for_this_piece(
                game_id=tmp_string,
                piece_type=request.get_json()["piece_type"]
            )
            # elif request.headers.get("") == "update":
            # return update_chess_board(game_id=tmp_string)

    if tmp_string:
        doc = db.tmp_chess_url.find_one({"url": tmp_string})
        if doc:
            return render_template("chess.html", game_id=tmp_string)
        return render_template("404.html")

    return render_template("chess.html")
