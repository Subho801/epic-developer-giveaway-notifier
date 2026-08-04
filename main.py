from src.config import (
    WEBHOOK_URL,
    COUNTRY,
    validate,
)

from src.epic import developer_giveaways

from src.notifier import send_giveaway

from src.utils import (
    load_posted,
    save_posted,
)


def main():
    validate()

    posted = load_posted()

    games = developer_giveaways(COUNTRY)

    print(f"Found {len(games)} developer giveaways")

    new_games = 0

    for game in games:

        game_id = game.get("id")

        if game_id in posted:
            continue

        print(f"New giveaway: {game['title']}")

        send_giveaway(WEBHOOK_URL, game)

        posted.append(game_id)

        new_games += 1

    save_posted(posted)

    print(f"Sent {new_games} new notification(s).")


if __name__ == "__main__":
    main()
