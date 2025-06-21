from shttp.client.core import SHTTPClient
import ast
import time

def print_board(board):
    print("\nCurrent Board:")
    for row in board:
        print(" | ".join(cell or " " for cell in row))
    print("-" * 15)

def main():
    client = SHTTPClient("localhost", 8081)
    print("Connected to Tic-Tac-Toe Server (localhost:8081)\n")

    player = input("Enter your symbol (X or O): ").strip().upper()
    if player not in ["X", "O"]:
        print("Invalid player. Must be 'X' or 'O'")
        return

    try:
        while True:
            # Request current board
            response = client.send_request("GET", "/board", {"Connection": "keep-alive"}, "")
            state = ast.literal_eval(response['body'])
            print_board(state['board'])

            if state['status'] != 'ongoing':
                print(f"Game Over: {state['status']}")
                break

            if state['turn'] != player:
                print(f"Waiting for player {state['turn']} to make a move...")
                time.sleep(5)
                continue

            move = input("Enter move as row,col (e.g., 0,2) or 'exit' to quit: ").strip()
            if move.lower() == "exit":
                break

            try:
                x_str, y_str = move.split(",")
                x, y = int(x_str), int(y_str)
            except:
                print("Invalid format. Use row,col (e.g., 1,1)")
                continue

            path = f"/move?x={x}&y={y}&player={player}"
            move_response = client.send_request("POST", path, {"Connection": "keep-alive"}, "")
            print("\nServer response:")
            print(move_response['body'].strip())

    finally:
        client.close()
        print("Game client closed.")

if __name__ == "__main__":
    main()
