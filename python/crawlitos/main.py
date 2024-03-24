# Example file showing a basic pygame "game loop"

from crawlitos.gm import GameManager


def main():
    GameManager.build()
    GameManager.instance().run()


if __name__ == "__main__":
    main()
