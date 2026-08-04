from src.config import COUNTRY
from src.epic import developer_giveaways


def main():
    games = developer_giveaways(COUNTRY)

    print(f"Found {len(games)} developer giveaways")

    for game in games:
        print("-", game["title"])


if __name__ == "__main__":
    main()
