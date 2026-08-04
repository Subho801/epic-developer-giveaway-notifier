from src.config import (
    WEBHOOK_URL,
    COUNTRY,
    validate,
)

from src.epic import developer_giveaways

from src.notifier import send_giveaway


def main():
    validate()

    games = developer_giveaways(COUNTRY)

    print(f"Found {len(games)} developer giveaways")

    for game in games:
        print(game["title"])
        send_giveaway(WEBHOOK_URL, game)


if __name__ == "__main__":
    main()
