import time
import chess
import random
import threading
import pickle as pkl

from pkg.authlib import db, get_random_string
from routes import all_chess_games, auth_required
from flask_socketio import emit, join_room, leave_room
from flask import redirect, render_template, request, session


# ============================================= UTILS ============================================= #


def create_chess_url(key: str, sender_email: str, opponent_email: str, sender_color: str, opponent_color: str):
    """It creates the temporary chess game URL.

    :param key: The generated key to construct the URL
    :param sender_email: Email of the game creator
    :param opponent_email: Email of the opponent
    :param sender_color: Color of the pieces of the game creator
    :param opponent_color: Color of the pieces of the opponent
    """
    db.tmp_chess_url.insert_one({
        "url": key,
        "created_at": int(time.time()),
        "sender_username": sender_email,
        "receiver_username": opponent_email,
        "sender_color": sender_color,
        "receiver_color": opponent_color,
    })


def transform_fen(row: str) -> str:
    """Transform the row of a given fen representation to make easier the game load process.

    :param row: The input row
    :return: Transformed row
    """
    for char in row:
        if char not in "rnbqkpRNBQKP":
            if char == "2":
                row = row.replace(char, "11")
            elif char == "3":
                row = row.replace(char, "111")
            elif char == "4":
                row = row.replace(char, "1111")
            elif char == "5":
                row = row.replace(char, "11111")
            elif char == "6":
                row = row.replace(char, "111111")
            elif char == "7":
                row = row.replace(char, "1111111")
            elif char == "8":
                row = row.replace(char, "11111111")

    return row


def get_fen(game_id: str) -> str:
    """It gets the FEN representation of the given game.

    :param game_id: The unique id of the chess game
    :return: Fen representation for a given game
    """
    try:
        board = all_chess_games[game_id]
    except KeyError:
        board = pkl.loads(db.chess_game.find_one({"url": game_id})["board"])

    fen_splitted = board.board_fen().split("/")

    return '/'.join(transform_fen(row) for row in fen_splitted)


def chess_game_end(game_id: str, winner: str | None):
    """It is launched at the end of the game, we update the status of the game.
    We are also saving the name of the winner, and every move played.
    This function is launched as the Thread in order to not cause any problem with the end of the game.

    :param game_id: The unique id of the chess game
    :param winner: The name of the winner of the game
    """
    time.sleep(3)

    board = all_chess_games[game_id]
    current_game = db.tmp_chess_url.find_one({"url": game_id})
    current_game["winner"] = winner
    current_game["move_stack"] = [str(move) for move in board.move_stack]
    current_game["board"] = pkl.dumps(board)

    db.chess_game.insert_one(current_game)
    db.tmp_chess_url.delete_one({"url": game_id})

    all_chess_games.pop(game_id, None)


# ============================================= WEBSOCKET ============================================= #


def on_chess_join(data):
    """WebSocket function that makes possible the join of a room. The room is here the chess game ID.
    User entering the room will be able to see any move played.

    :param data: The websocket payload
    """
    game_id = data["gameId"]
    join_room(game_id)


def on_chess_possibilities(data):
    """It evaluates all possible move for a given piece.
    This function is launched once a piece is clicked by a player on the frontend.

    :param data: The websocket payload
    """
    user_id = data["userId"]
    game_id = data["gameId"]
    chess_case = data["chessCase"]

    board = all_chess_games[game_id]
    moves = [str(legal_move) for legal_move in board.legal_moves if chess_case == str(legal_move)[:2]]

    emit("chess_possibilities_back", {"userId": user_id, "possibleMoves": moves}, to=game_id)


def on_chess_move(data):
    """WebSocket function updating the chess board and checking for any of the following: draw, check, checkmate.

    :param data: The websocket payload
    """
    game_id = data["gameId"]
    move = data["move"]

    board = all_chess_games[game_id]
    board.push_san(move)

    res = {
        "draw": False,
        "check": False,
        "checkmate": False,
    }

    if board.is_stalemate():
        res["draw"] = True
    if board.is_insufficient_material():
        res["draw"] = True
    if board.is_fivefold_repetition():
        res["draw"] = True
    if board.is_check():
        res["check"] = True
    if board.is_checkmate():
        res["checkmate"] = True

    if res["checkmate"]:
        threading.Thread(target=chess_game_end, args=(game_id, session.get("username"))).start()
    elif res["draw"]:
        threading.Thread(target=chess_game_end, args=(game_id, None)).start()

    emit("chess_move_back", {"move": move, "gameStatus": res}, to=game_id)


def on_chess_leave(data):
    """WebSocket function that makes possible the leave of the room. The room is here the chess game ID.
    User entering the room will be able to see any move played.

    :param data: The websocket payload
    """
    game_id = data["gameId"]
    leave_room(game_id)


# ============================================= HANDLER ============================================= #


@auth_required
def chess_game(tmp_string: str = None):
    """

    :param tmp_string: The
    :return:
    """
    if request.method == "POST":
        key = get_random_string(16)
        opponent_username = request.form.get("chess_opponent_username")
        sender_color = random.choice(["white", "black"])
        opponent_color = "white" if sender_color == "black" else "black"
        session["sender_color"] = sender_color
        session["receiver_color"] = opponent_color
        create_chess_url(key, session.get("username"), opponent_username, sender_color, opponent_color)
        all_chess_games[key] = chess.Board()
        return redirect(f"/chess/{key}")

    if tmp_string:
        if doc := db.tmp_chess_url.find_one({"url": tmp_string}):
            return render_template(
                "chess_game.html",
                game_id=tmp_string,
                sender_username=doc["sender_username"],
                receiver_username=doc["receiver_username"],
                sender_color=doc["sender_color"],
                receiver_color=doc["receiver_color"],
                fen=get_fen(tmp_string)
            )
        elif doc := db.chess_game.find_one({"url": tmp_string}):
            return render_template(
                "chess_game.html",
                game_id=tmp_string,
                sender_username=doc["sender_username"],
                receiver_username=doc["receiver_username"],
                sender_color=doc["sender_color"],
                receiver_color=doc["receiver_color"],
                fen=get_fen(tmp_string)
            )
        return render_template("404.html")

    return render_template("chess.html", users=[user["username"] for user in db.users.find()
                                                if user["username"] != session.get("username")])
