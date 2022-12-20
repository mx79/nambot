import time
import chess

from typing import Dict
from routes import all_chess_games, auth_required
from pkg.authlib.auth import db, get_random_string
from flask import redirect, render_template, request, session


def create_chess_url(key: str, sender_email: str, opponent_email: str):
    """

    :param key:
    :param sender_email:
    :param opponent_email:
    """
    db.tmp_chess_url.insert_one({
        "url": key,
        "created_at": int(time.time()),
        "sender_username": sender_email,
        "receiver_username": opponent_email
    })


def check_possible_move_for_this_piece(game_id: str, chess_case: str) -> Dict:
    """

    :param game_id:
    :param chess_case:
    :rtype: Dict
    :return: A list of all possible move for this piece.
    """
    board = all_chess_games[game_id]
    moves = [str(legal_move) for legal_move in board.legal_moves if chess_case == str(legal_move)[:2]]

    return {"possible_moves": moves}


def update_chess_board(game_id: str, move: str) -> Dict[str, bool]:
    """

    :param game_id:
    :param move:
    :rtype: Dict
    :return:
    """
    board = all_chess_games[game_id]
    mv = board.push_san(move)

    res = {
        "castling": False,
        "queenside_castling": False,
        "en_passant": False,
        "draw": False,
        "checkmate": False,
        "check": False,
    }

    if board.is_castling(mv):
        res["castling"] = True
    if board.is_queenside_castling(mv):
        res["queenside_castling"] = True
    if board.is_en_passant(mv):
        res["en_passant"] = True
    if board.is_insufficient_material():
        res["draw"] = True
    if board.is_fivefold_repetition():
        res["draw"] = True
    if board.is_checkmate():
        res["checkmate"] = True
    if board.is_check():
        res["check"] = True

    return res


def load_chess_board(game_id: str) -> Dict:
    """

    :param game_id:
    :rtype: Dict
    :return:
    """


@auth_required
def chess(tmp_string: str = None):
    """

    :return:
    """
    if request.method == "POST":
        if tmp_string:
            body = request.get_json()
            if body.get("check"):
                return check_possible_move_for_this_piece(
                    game_id=tmp_string,
                    chess_case=body["chess_case"]
                )
            elif body.get("update"):
                return update_chess_board(
                    game_id=tmp_string,
                    move=body["move"],
                )
            elif body.get("load"):
                return load_chess_board(
                    game_id=tmp_string
                )
        key = get_random_string(16)
        opponent_username = request.form.get("opponent_username")
        create_chess_url(key, session.get("username"), opponent_username)
        all_chess_games[key] = chess.Board()
        return redirect(f"/chess/{key}")

    if tmp_string:
        if db.tmp_chess_url.find_one({"url": tmp_string}):
            return render_template("chess.html", game_id=tmp_string)
        return render_template("404.html")

    return render_template("chess.html")
