from chessdotcom import get_leaderboards, get_player_stats, get_player_game_archives
import pprint
import requests

printer = pprint.PrettyPrinter()

def print_leaderboards():
    data = get_leaderboards().json
    categories = data['leaderboards'].keys()

    for category in categories:
        print('Category:', category)
        leaderboard = data['leaderboards'][category]
        for idx, entry in enumerate(leaderboard):
            print(f'Rank: {idx + 1} | Username: {entry["username"]} | Rating: {entry["score"]}')


def get_player_rating(username):
    data = get_player_stats(username).json
    categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
    for category in categories:
        print('Category:', category)
        category_data = data["stats"].get(category)
        if category_data:
            print(f'Current: {category_data["last"]["rating"]}')
            print(f'Best: {category_data["best"]["rating"]}')
            print(f'Record: {category_data["record"]}')
        else:
            print(f'Category "{category}" not available for this player.')


def get_most_recent_game(username):
    try:
        data = get_player_game_archives(username).json
        url = data['archives'][-1]
        games = requests.get(url).json()
        game = games['games'][-1]
        printer.pprint(game)
    except (IndexError, KeyError):
        print(f"No game found for {username} or error occurred while fetching the data.")


if __name__ == "__main__":
    name = input("Enter username to track: ")

    # Ask the user if they want to print leaderboards
    while True:
        show_leaderboards = input("Do you want to print leaderboards? (y/n): ")
        if show_leaderboards.lower() == "y":
            print("\nLeaderboards:")
            print_leaderboards()
            break
        elif show_leaderboards.lower() == "n":
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    print(f"\nRating for {name}:")
    get_player_rating(name)

    print(f"\nMost Recent Game for {name}:")
    get_most_recent_game(name)
