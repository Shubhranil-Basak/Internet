from shttp.server.router import Router
from shttp.server.core import SHTTPServer
from pprint import pformat
import threading

router = Router()
update_event = threading.Event()

# Game State
game_state = {
    "board": [["", "", ""], ["", "", ""], ["", "", ""]],
    "turn": "X",
    "players": {"X": None, "O": None},
    "status": "ongoing"
}

def check_game_status(board):
    for i in range(3):
        if board[i][0] != "" and board[i][0] == board[i][1] == board[i][2]:
            return f"{board[i][0]} wins"
        if board[0][i] != "" and board[0][i] == board[1][i] == board[2][i]:
            return f"{board[0][i]} wins"
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return f"{board[0][0]} wins"
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return f"{board[0][2]} wins"
    if all(cell != "" for row in board for cell in row):
        return "draw"
    return "ongoing"

def get_board_handler(body, query):
    return 200, "OK", {"Content-Type": "application/json"}, pformat({
        "board": game_state["board"],
        "turn": game_state["turn"],
        "status": game_state["status"]
    })

def post_move_handler(body, query):
    try:
        x = int(query.get("x", [None])[0])
        y = int(query.get("y", [None])[0])
        player = query.get("player", [None])[0]
    except (ValueError, TypeError):
        return 400, "Bad Request", {}, "Invalid x, y, or player"

    if player not in ["X", "O"]:
        return 400, "Bad Request", {}, "Player must be X or O"
    if game_state["status"] != "ongoing":
        return 403, "Game Over", {}, f"Game has ended: {game_state['status']}"
    if player != game_state["turn"]:
        return 403, "Not Your Turn", {}, f"It is {game_state['turn']}'s turn"
    if not (0 <= x < 3 and 0 <= y < 3):
        return 400, "Bad Request", {}, "Move out of bounds"
    if game_state["board"][x][y] != "":
        return 403, "Invalid Move", {}, "Cell already occupied"

    # Apply move
    game_state["board"][x][y] = player
    game_state["status"] = check_game_status(game_state["board"])
    game_state["turn"] = "O" if player == "X" else "X"

    # Simulate broadcast
    print(f"Updated Board:\n{game_state['board']}")
    update_event.set()  # Notify waiting clients
    update_event.clear()

    return 200, "OK", {"Content-Type": "text/plain"}, "Move accepted"

def wait_for_update_handler(body, query):
    # Wait for an update or timeout after 30 seconds
    updated = update_event.wait(timeout=30)
    return 200, "OK", {"Content-Type": "application/json"}, pformat({
        "board": game_state["board"],
        "turn": game_state["turn"],
        "status": game_state["status"],
        "update": updated
    })

# Route setup
router.add_route("GET", "/board", get_board_handler)
router.add_route("POST", "/move", post_move_handler)
router.add_route("GET", "/board-wait", wait_for_update_handler)

# Start the server
server = SHTTPServer("127.0.0.1", 8081, router)
server.start()
