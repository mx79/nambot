// Chess functions:

let flag = false;
let movesArray = [];
let oldBg = "";

function checkPossibleMoveForThisPiece(piece, game_id) {
    flag = !flag;
    if (flag) {
        const chessCase = piece.parentNode.id;
        // Do a request to check possible move for this case:
        fetch(
            `http://localhost:5000/chess/${game_id}`,
            {
                method: 'POST',
                body: JSON.stringify({chess_case: chessCase}),
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
                }
            }).catch((error) => {
            console.error('Error:', error)
        });
    } else {
        for (const possibility of movesArray) {
            const elem = document.getElementById(possibility.slice(2, 4));
            elem.setAttribute("class", "col bg-secondary d-flex justify-content-center");
        }
        movesArray = [];
    }
}