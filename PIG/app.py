import tkinter as tk
from tkinter import messagebox
import random


TARGET_SCORE = 50

# ---------- Color palette ----------
BG = "#0B1020"
CARD = "#121A2B"
CARD_2 = "#172238"
TEAL = "#2DD4BF"
TEAL_DARK = "#0F766E"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
RED = "#FB7185"
GOLD = "#FBBF24"
BORDER = "#24324A"


def roll():
    return random.randint(1, 6)


class DiceRushApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Rush • Jatin Gupta")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)

        self.players = 0
        self.player_scores = []
        self.current_player = 0
        self.current_score = 0
        self.game_started = False
        self.game_over = False

        self.build_ui()
        self.show_setup()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=35, pady=(25, 12))

        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="DICE RUSH",
            font=("Segoe UI", 28, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="ROLL • RISK • REACH 50",
            font=("Segoe UI", 9, "bold"),
            fg=TEAL,
            bg=BG
        ).pack(anchor="w", pady=(2, 0))

        creator = tk.Frame(header, bg=BG)
        creator.pack(side="right", anchor="e")

        tk.Label(
            creator,
            text="CREATED BY",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(anchor="e")

        tk.Label(
            creator,
            text="Jatin Gupta",
            font=("Segoe UI", 13, "bold"),
            fg=TEAL,
            bg=BG
        ).pack(anchor="e")

        # Main area
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(fill="both", expand=True, padx=35, pady=10)

        # Left side - game board
        self.board = tk.Frame(
            self.main,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.board.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Right side - scoreboard
        self.score_panel = tk.Frame(
            self.main,
            width=290,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.score_panel.pack(side="right", fill="y")
        self.score_panel.pack_propagate(False)

        self.build_board()
        self.build_scoreboard()

        # Footer
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=35, pady=(5, 20))

        tk.Label(
            footer,
            text="First player to reach 50 points wins • Rolling a 1 ends your turn",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG
        ).pack(side="left")

        tk.Label(
            footer,
            text="PYTHON • TKINTER",
            font=("Segoe UI", 8, "bold"),
            fg="#64748B",
            bg=BG
        ).pack(side="right")

    def build_board(self):
        self.board_title = tk.Label(
            self.board,
            text="GAME SETUP",
            font=("Segoe UI", 17, "bold"),
            fg=WHITE,
            bg=CARD
        )
        self.board_title.pack(pady=(35, 5))

        self.status_label = tk.Label(
            self.board,
            text="Choose the number of players",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=CARD
        )
        self.status_label.pack()

        self.setup_frame = tk.Frame(self.board, bg=CARD)
        self.setup_frame.pack(pady=35)

        tk.Label(
            self.setup_frame,
            text="NUMBER OF PLAYERS",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack()

        self.player_var = tk.StringVar(value="2")

        player_menu = tk.OptionMenu(
            self.setup_frame,
            self.player_var,
            "2", "3", "4"
        )
        player_menu.config(
            width=12,
            font=("Segoe UI", 12, "bold"),
            fg=WHITE,
            bg=CARD_2,
            activebackground=TEAL_DARK,
            activeforeground=WHITE,
            highlightthickness=0,
            relief="flat"
        )
        player_menu["menu"].config(
            bg=CARD_2,
            fg=WHITE,
            activebackground=TEAL_DARK,
            activeforeground=WHITE
        )
        player_menu.pack(pady=12)

        self.start_button = self.make_button(
            self.setup_frame,
            "START GAME",
            self.start_game,
            TEAL
        )
        self.start_button.pack(pady=10)

        # Game widgets
        self.game_frame = tk.Frame(self.board, bg=CARD)

        self.turn_label = tk.Label(
            self.game_frame,
            text="PLAYER 1'S TURN",
            font=("Segoe UI", 20, "bold"),
            fg=TEAL,
            bg=CARD
        )
        self.turn_label.pack(pady=(10, 8))

        self.dice_label = tk.Label(
            self.game_frame,
            text="⚄",
            font=("Segoe UI Symbol", 90),
            fg=WHITE,
            bg=CARD_2,
            width=3,
            height=1
        )
        self.dice_label.pack(pady=18)

        self.roll_button = self.make_button(
            self.game_frame,
            "ROLL DICE",
            self.roll_dice,
            TEAL
        )
        self.roll_button.pack(pady=7)

        self.stop_button = self.make_button(
            self.game_frame,
            "BANK SCORE",
            self.bank_score,
            CARD_2
        )
        self.stop_button.pack(pady=7)

        self.current_label = tk.Label(
            self.game_frame,
            text="Turn score: 0",
            font=("Segoe UI", 12, "bold"),
            fg=WHITE,
            bg=CARD
        )
        self.current_label.pack(pady=(18, 3))

        self.total_label = tk.Label(
            self.game_frame,
            text="Total score: 0 / 50",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        )
        self.total_label.pack()

        self.new_game_button = self.make_button(
            self.game_frame,
            "NEW GAME",
            self.show_setup,
            CARD_2
        )
        self.new_game_button.pack(pady=(22, 5))

    def build_scoreboard(self):
        tk.Label(
            self.score_panel,
            text="SCOREBOARD",
            font=("Segoe UI", 15, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w", padx=25, pady=(28, 5))

        tk.Label(
            self.score_panel,
            text="FIRST TO 50 WINS",
            font=("Segoe UI", 8, "bold"),
            fg=TEAL,
            bg=CARD
        ).pack(anchor="w", padx=25)

        self.score_container = tk.Frame(self.score_panel, bg=CARD)
        self.score_container.pack(fill="both", expand=True, padx=18, pady=20)

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            fg=BG if color == TEAL else WHITE,
            bg=color,
            activebackground=TEAL_DARK if color == TEAL else "#24324A",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=11
        )

    def show_setup(self):
        self.game_started = False
        self.game_over = False

        self.game_frame.pack_forget()
        self.setup_frame.pack(pady=35)

        self.board_title.config(text="GAME SETUP")
        self.status_label.config(text="Choose the number of players")

        self.clear_scoreboard()

    def start_game(self):
        self.players = int(self.player_var.get())
        self.player_scores = [0] * self.players
        self.current_player = 0
        self.current_score = 0
        self.game_started = True
        self.game_over = False

        self.setup_frame.pack_forget()
        self.game_frame.pack(pady=20)

        self.board_title.config(text="DICE RUSH")
        self.update_turn_ui()
        self.update_scoreboard()

    def roll_dice(self):
        if not self.game_started or self.game_over:
            return

        value = roll()

        dice_faces = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }

        self.dice_label.config(text=dice_faces[value])

        if value == 1:
            self.current_score = 0
            self.current_label.config(text="Turn score: 0")
            self.status_label.config(
                text=f"Player {self.current_player + 1} rolled a 1 — turn lost!",
                fg=RED
            )
            self.root.after(900, self.next_player)
        else:
            self.current_score += value
            self.current_label.config(
                text=f"Turn score: {self.current_score}"
            )
            self.status_label.config(
                text=f"Player {self.current_player + 1} rolled a {value}",
                fg=MUTED
            )

    def bank_score(self):
        if not self.game_started or self.game_over:
            return

        if self.current_score == 0:
            self.status_label.config(
                text="Roll the dice first!",
                fg=RED
            )
            return

        self.player_scores[self.current_player] += self.current_score

        if self.player_scores[self.current_player] >= TARGET_SCORE:
            self.player_scores[self.current_player] = max(
                self.player_scores[self.current_player],
                TARGET_SCORE
            )
            self.update_scoreboard()
            self.end_game()
            return

        self.next_player()

    def next_player(self):
        if self.game_over:
            return

        self.current_score = 0
        self.current_player = (self.current_player + 1) % self.players
        self.update_turn_ui()
        self.update_scoreboard()

    def update_turn_ui(self):
        self.turn_label.config(
            text=f"PLAYER {self.current_player + 1}'S TURN"
        )
        self.current_label.config(text="Turn score: 0")
        self.total_label.config(
            text=f"Total score: {self.player_scores[self.current_player]} / {TARGET_SCORE}"
        )
        self.dice_label.config(text="⚄")

        self.status_label.config(
            text="Roll the dice or bank your score",
            fg=MUTED
        )

    def update_scoreboard(self):
        self.clear_scoreboard()

        for i, score in enumerate(self.player_scores):
            active = i == self.current_player and not self.game_over

            row_bg = CARD_2 if active else "#101827"

            row = tk.Frame(
                self.score_container,
                bg=row_bg,
                highlightbackground=TEAL if active else BORDER,
                highlightthickness=1
            )
            row.pack(fill="x", pady=6)

            name = tk.Label(
                row,
                text=f"PLAYER {i + 1}",
                font=("Segoe UI", 10, "bold"),
                fg=TEAL if active else WHITE,
                bg=row_bg
            )
            name.pack(side="left", padx=14, pady=12)

            score_label = tk.Label(
                row,
                text=str(score),
                font=("Segoe UI", 16, "bold"),
                fg=WHITE,
                bg=row_bg
            )
            score_label.pack(side="right", padx=14)

            # Progress bar
            progress_bg = tk.Frame(
                self.score_container,
                bg=CARD,
                height=5
            )
            progress_bg.pack(fill="x", padx=3, pady=(0, 3))

            progress = tk.Frame(
                progress_bg,
                bg=TEAL,
                height=5
            )
            width_ratio = min(score / TARGET_SCORE, 1)
            self.root.update_idletasks()

            total_width = max(progress_bg.winfo_width(), 180)
            progress.place(
                x=0,
                y=0,
                width=int(total_width * width_ratio),
                height=5
            )

    def clear_scoreboard(self):
        for widget in self.score_container.winfo_children():
            widget.destroy()

    def end_game(self):
        self.game_over = True
        winner = self.current_player
        winning_score = self.player_scores[winner]

        self.turn_label.config(
            text=f"🏆 PLAYER {winner + 1} WINS!",
            fg=GOLD
        )
        self.current_label.config(
            text=f"Final score: {winning_score}"
        )
        self.total_label.config(
            text="Congratulations!"
        )
        self.status_label.config(
            text=f"Player {winner + 1} reached {winning_score} points!",
            fg=GOLD
        )

        self.roll_button.config(state="disabled")
        self.stop_button.config(state="disabled")

        self.update_scoreboard()

        messagebox.showinfo(
            "🎉 Game Over",
            f"Player {winner + 1} wins!\n\n"
            f"Final Score: {winning_score}\n\n"
            f"Created by Jatin Gupta"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRushApp(root)
    root.mainloop()
