import sys
import requests


def main():
    response = requests.get(
        f"http://127.0.0.1:8342/status/{int(sys.argv[1])}"
    )

    print(response.text)

if __name__ == "__main__":
    main()