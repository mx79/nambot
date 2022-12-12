// Chess functions:
function checkPossibleMoveForThisPiece(piece, game_id) {
    const chess_case = piece.parentNode.id;
    console.log(chess_case)
    // Do a request to check possible move for this case.
    fetch(
        `http://localhost:5000/chess/${game_id}`,
        {
            method: 'POST',
            body: JSON.stringify({chess_case: chess_case}),
            mode: 'cors',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(r => r.json())
        .then(jsonResponse => {
            console.log(jsonResponse)
        }).catch((error) => {
        console.error('Error:', error)
    });
}