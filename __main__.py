from parser import *


def main():
    work_with_os()
    days, pages = input_main()
    pars = RamblePars(days=days, pages=pages, start_day=choice_day())
    pars.search_news()


if __name__ == '__main__':
    main()
