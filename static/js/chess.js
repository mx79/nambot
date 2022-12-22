// Chess functions:

// Array that contains every the half of the chess board colorized with primary background CSS class
const primaryBgCases = [
    "g1", "e1", "c1", "a1", "h2", "f2", "d2", "b2",
    "g3", "e3", "c3", "a3", "h4", "f4", "d4", "b4",
    "g5", "e5", "c5", "a5", "h6", "f6", "d6", "b6",
    "g7", "e7", "c7", "a7", "h8", "f8", "d8", "b8"
];

// When we want to set a case with an empty img after the move
const emptyImg = document.querySelector('img[alt="empty"]');

// Overridable var contributing to script logic
let flag = false;
let movesArray = [];

/**
 *
 * @param piece
 * @param gameId
 */
function checkPossibleMoveForThisPiece(piece, gameId) {
    flag = !flag;
    if (flag) {
        const chessCase = piece.parentNode.id;
        // Do a request to check possible move for this case:
        fetch(
            `http://localhost:5000/chess/${gameId}`,
            {
                method: 'POST',
                body: JSON.stringify({check: true, chess_case: chessCase}),
                mode: 'cors',
                headers: {
                    'Content-type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(r => r.json())
            .then(jsonResponse => {
                // Put some light on the chess cases available for the piece selected:
                movesArray = jsonResponse["possible_moves"];
                for (const possibility of movesArray) {
                    const elem = document.getElementById(possibility.slice(2, 4));
                    // Change the color of the case if it is a valid move
                    elem.setAttribute("class", "col d-flex justify-content-center");
                    elem.setAttribute("style", "background-color: #f8f9fa");
                    // Remove pointer event if there is a piece on this case
                    if (elem.firstElementChild.alt !== "empty") {
                        elem.firstElementChild.setAttribute("style", "pointer-events: none");
                    }
                    // Add eventListener on click when a possible move case is clicked and ask for the board to update
                    elem.addEventListener("click", updateChessBoard);
                    elem.possibility = possibility;
                    elem.gameId = gameId;
                }
            }).catch((error) => {
            console.error('Error:', error);
        });
    } else {
        removeLightOnCase(gameId);
    }
}


/**
 *
 * @param gameId
 */
function removeLightOnCase(gameId) {
    for (const possibility of movesArray) {
        const elem = document.getElementById(possibility.slice(2, 4));
        // Unset color on valid move and reset to the base background
        if (primaryBgCases.includes(elem.id)) {
            elem.setAttribute("class", "col bg-primary d-flex justify-content-center");
        } else {
            elem.setAttribute("class", "col bg-secondary d-flex justify-content-center");
        }
        elem.firstElementChild.removeAttribute("style");
        elem.removeAttribute("style");
        // Remove eventListener on click when a possible move case is clicked
        elem.removeEventListener("click", updateChessBoard);
        elem.possibility = possibility;
        elem.gameId = gameId;
    }
    movesArray = [];
}

/**
 *
 * @param move
 */
function forwardPiece(move) {
    const fromChessCase = document.getElementById(move.slice(0, 2));
    const toChessCase = document.getElementById(move.slice(2, 4));
    // TODO: Implement castling and en_passant
    // Castling
    if (fromChessCase.firstElementChild.alt.slice(6) === "king" && ["c", "g"].includes(move.slice(2, 3)) && move.slice(0, 1) === "e") {
        // black_king: e8 and white_king: e1
        // 4 different type of castling
        if (move.slice(1, 2) === "1" && move.slice(2, 3) === "c") {
            // White queenside castling
            forwardPiece("a1d1")
        } else if (move.slice(1, 2) === "1" && move.slice(2, 3) === "g") {
            // White kingside castling
            forwardPiece("h1f1")
        } else if (move.slice(1, 2) === "8" && move.slice(2, 3) === "c") {
            // Black queenside castling
            forwardPiece("a8d8")
        } else if (move.slice(1, 2) === "8" && move.slice(2, 3) === "g") {
            // Black kingside castling
            forwardPiece("h8f8")
        }
    }
    // En passant

    // Moving Piece and remove the opponent one if any
    toChessCase.removeChild(toChessCase.firstElementChild);
    fromChessCase.appendChild(emptyImg.cloneNode());
    toChessCase.appendChild(fromChessCase.firstElementChild);
}

/**
 *
 * @param event
 */
function updateChessBoard(event) {
    const move = event.currentTarget.possibility;
    const gameId = event.currentTarget.gameId;
    // Do a request to update the chess board status
    fetch(
        `http://localhost:5000/chess/${gameId}`,
        {
            method: 'POST',
            body: JSON.stringify({update: true, move: move}),
            mode: 'cors',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(r => r.json())
        .then(jsonResponse => {
            // Check if there is a message displaying `Echec` or something like this and deletes it
            const chessTmp = document.getElementById("chess-tmp");
            if (chessTmp) {
                chessTmp.remove();
            }
            // Removing the white case and forward the piece
            removeLightOnCase(gameId);
            forwardPiece(move);
            // After we deal with the draw or checkmate mechanism
            const chessArea = document.getElementById("chess-area");
            if (jsonResponse["draw"]) {
                chessArea.innerHTML += '<div id="chess-tmp"><br><br><h1 class="text-center text-primary"> La partie se solde par un nul !</h1></div>';
            } else if (jsonResponse["checkmate"]) {
                chessArea.innerHTML += '<div id="chess-tmp"><br><br><h1 class="text-center text-primary">Echec et mat !</h1></div>';
            } else if (jsonResponse["check"]) {
                chessArea.innerHTML += '<div id="chess-tmp"><br><br><h1 class="text-center text-primary">Echec !</h1></div>';
            }
        }).catch((error) => {
        console.error('Error:', error);
    });
}

/**
 *
 */
function loadChessBoard(gameId) {
    fetch(
        `http://localhost:5000/chess/${gameId}`,
        {
            method: 'POST',
            body: JSON.stringify({load: true}),
            mode: 'cors',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(r => r.json())
        .then(jsonResponse => {
            // Load the FEN string representing the current game
            const fen = jsonResponse["fen"];
            console.log(fen);
        }).catch((error) => {
        console.error('Error:', error);
    });
}