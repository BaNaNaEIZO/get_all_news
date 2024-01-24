from parser import *


def main():
    days, pages = input_main()
    pars = RamblePars(days=days, pages=pages)
    pars.search_news()


if __name__ == '__main__':
    main()
