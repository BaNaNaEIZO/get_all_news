from parser import *


def main():
    work_with_os()
    days = input_main()
    pars = RamblePars(days=days, start_day=choice_day())
    pars.search_news()


if __name__ == '__main__':
    main()
