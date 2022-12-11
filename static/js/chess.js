// Chess functions:
function checkPossibleMoveForThisPiece(piece, game_id) {
    let piece_type_short = "";
    const piece_type_full = piece.alt.split("_")[1];
    switch (piece_type_full) {
        case "king":
            console.log("It's a king");
            piece_type_short = "K";
            break;
        case "queen":
            console.log("It's a queen");
            piece_type_short = "Q";
            break;
        case "rook":
            console.log("It's a rook");
            piece_type_short = "R";
            break;
        case "knight":
            console.log("It's a knight");
            piece_type_short = "N";
            break;
        case "bishop":
            console.log("It's a bishop");
            piece_type_short = "B";
            break;
        default:
            console.log("It's a pawn")
    }
    console.log(piece_type_short)
    // Do a request to check possible move for this piece.
    fetch(
        `http://localhost:5000/chess/${game_id}`,
        {
            method: 'POST',
            // Stringify the payload into JSON:
            body: JSON.stringify({message: instruction}),
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