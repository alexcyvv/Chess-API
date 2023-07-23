import tkinter as tk
from tkinter import scrolledtext
from chessdotcom import get_leaderboards, get_player_stats, get_player_game_archives
import pprint
import requests

printer = pprint.PrettyPrinter()

def print_leaderboards():
    data = get_leaderboards().json
    categories = data['leaderboards'].keys()
    leaderboard_text = ""

    for category in categories:
        leaderboard_text += f'Category: {category}\n'
        leaderboard = data['leaderboards'][category]
        for idx, entry in enumerate(leaderboard):
            leaderboard_text += f'Rank: {idx + 1} | Username: {entry["username"]} | Rating: {entry["score"]}\n'

    leaderboard_textbox.config(state=tk.NORMAL)
    leaderboard_textbox.delete('1.0', tk.END)
    leaderboard_textbox.insert(tk.END, leaderboard_text)
    leaderboard_textbox.config(state=tk.DISABLED)


def get_player_rating():
    username = username_entry.get()
    data = get_player_stats(username).json
    categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
    rating_text = ""

    for category in categories:
        rating_text += f'Category: {category}\n'
        category_data = data["stats"].get(category)
        if category_data:
            rating_text += f'Current: {category_data["last"]["rating"]}\n'
            rating_text += f'Best: {category_data["best"]["rating"]}\n'
            rating_text += f'Record: {category_data["record"]}\n'
        else:
            rating_text += f'Category "{category}" not available for this player.\n'

    rating_textbox.config(state=tk.NORMAL)
    rating_textbox.delete('1.0', tk.END)
    rating_textbox.insert(tk.END, rating_text)
    rating_textbox.config(state=tk.DISABLED)


def get_most_recent_game():
    username = username_entry.get()
    try:
        data = get_player_game_archives(username).json
        url = data['archives'][-1]
        games = requests.get(url).json()
        game = games['games'][-1]
        game_text = pprint.pformat(game)

        game_textbox.config(state=tk.NORMAL)
        game_textbox.delete('1.0', tk.END)
        game_textbox.insert(tk.END, game_text)
        game_textbox.config(state=tk.DISABLED)
    except (IndexError, KeyError):
        game_textbox.config(state=tk.NORMAL)
        game_textbox.delete('1.0', tk.END)
        game_textbox.insert(tk.END, f"No game found for {username} or error occurred while fetching the data.")
        game_textbox.config(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.title("Chess.com Player Info")
root.geometry("600x400")

# Username Entry Field
username_label = tk.Label(root, text="Enter username to track:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Buttons to interact with the data
leaderboard_button = tk.Button(root, text="Print Leaderboards", command=print_leaderboards)
leaderboard_button.pack()

rating_button = tk.Button(root, text="Get Player Rating", command=get_player_rating)
rating_button.pack()

game_button = tk.Button(root, text="Get Most Recent Game", command=get_most_recent_game)
game_button.pack()

# Scrolled Text Widgets to display the data
leaderboard_textbox = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
leaderboard_textbox.pack()

rating_textbox = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
rating_textbox.pack()

game_textbox = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
game_textbox.pack()

# Disable editing on the textboxes
leaderboard_textbox.config(state=tk.DISABLED)
rating_textbox.config(state=tk.DISABLED)
game_textbox.config(state=tk.DISABLED)

root.mainloop()
