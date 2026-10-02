import random 

def roll():
    min_value = 1
    max_value = 6
    return random.randint(min_value, max_value)


while True:
    players = input("Enter the number of users (2-4): ")

    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("Invalid input. Please enter a number between 2 and 4.")
    else:
        print("Invalid input. Please enter a valid number.")

max_score = 50
player_scores = [0 for _ in range(players)]

while max(player_scores) < max_score:
    for player_idx in range(players):
        print(f"\nPlayer {player_idx + 1}'s turn:\n")
        current_score = 0

        while True:
            should_roll = input("Do you want to roll the dice? (y/n): ")

            if should_roll.lower() != 'y':
                break
            value = roll()
            if value == 1:
                print("You rolled a 1! Your turn is done.")
                current_score = 0
                break

            else:
                current_score += value
                print("You rolled a", value)

            print("Current score:", current_score)

        player_scores[player_idx] += current_score
        print("Your total score is:", player_scores[player_idx])

        if player_scores[player_idx] >= max_score:
            print(f"\n🎉 Player {player_idx + 1} wins!")
            break

winning_score = max(player_scores)
winning_idx = player_scores.index(winning_score)

print(
    f"\n🏆 Player {winning_idx + 1} is the winner "
    f"with a score of {winning_score}!"
)      