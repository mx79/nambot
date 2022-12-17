// Chess functions:

const primaryBgCases = [
    "g1", "e1", "c1", "a1", "h2", "f2", "d2", "b2",
    "g3", "e3", "c3", "a3", "h4", "f4", "d4", "b4",
    "g5", "e5", "c5", "a5", "h6", "f6", "d6", "b6",
    "g7", "e7", "c7", "a7", "h8", "f8", "d8", "b8"
];

let flag = false;
let movesArray = [];

function checkPossibleMoveForThisPiece(piece, game_id) {
    flag = !flag;
    if (flag) {
        const chessCase = piece.parentNode.id;
        // Do a request to check possible move for this case:
        fetch(
            `http://localhost:5000/chess/${game_id}`,
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
                    elem.setAttribute("class", "col d-flex justify-content-center");
                    elem.setAttribute("style", "background-color: #f8f9fa");
                    elem.addEventListener("click", () => updateChessBoard(possibility, game_id));
                }
            }).catch((error) => {
            console.error('Error:', error)
        });
    } else {
        for (const possibility of movesArray) {
            const elem = document.getElementById(possibility.slice(2, 4));
            if (primaryBgCases.includes(elem.id)) {
                elem.setAttribute("class", "col bg-primary d-flex justify-content-center");
            } else {
                elem.setAttribute("class", "col bg-secondary d-flex justify-content-center");
            }
            elem.removeAttribute("style");
            elem.removeEventListener("click", () => updateChessBoard(possibility, game_id));
        }
        movesArray = [];
    }
}

function updateChessBoard(move, game_id) {
    console.log(move);
    // Do a request to check possible move for this case:
    fetch(
        `http://localhost:5000/chess/${game_id}`,
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
            console.log(jsonResponse);
        }).catch((error) => {
        console.error('Error:', error)
    });
}