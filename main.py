from src.config import WEBHOOK_URL, validate
from src.notifier import send_test


def main():
    validate()

    status = send_test(WEBHOOK_URL)

    print(status)


if __name__ == "__main__":
    main()
