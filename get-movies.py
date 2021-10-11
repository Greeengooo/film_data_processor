import csv
import re
import argparse


def create_year_lst(y_from: int, y_to: int) -> list:
    if y_from != 0 and y_to != 0:
        return ['\(' + str(i) + '\)' for i in range(y_from, y_to + 1)]
    else:
        return []


def file_to_list(file: str, genre_lst: list = None, year_from: int = None, year_to: int = None,
                 regex: str = None) -> list:
    with open(file, 'r') as csv_obj:
        csv_reader = csv.reader(csv_obj)
        csv_list = []

        if genre_lst is not None:
            year_lst = create_year_lst(year_from, year_to)
            rx = re.compile(
                fr'(\b{regex}\b)' + '.*' + '(' + ')|('.join(year_lst) + ')' + '(' + ')|('.join(genre_lst) + ')')
            for line in csv_reader:
                if rx.findall(str(line)):
                    csv_list.append(line)
        else:
            for line in csv_obj:
                csv_list.append(line)
    return csv_list[1:]


def find_avg_ratings(lsmovies: list, lsrates: list) -> dict:
    movie_ratings = {}
    for movie in lsmovies:
        movie_id = movie[0]
        r = re.compile(fr'(^\d+).({movie_id}).(\d\.\d)')
        movie_by_id = list(filter(r.match, lsrates))
        if len(movie_by_id) == 0:
            continue
        ratings = [float(str(elem).rstrip().split(',')[2]) for elem in movie_by_id]
        rating_avg = sum(ratings) / len(ratings)
        movie_ratings[tuple(movie)] = rating_avg
    return movie_ratings


def find_top_n(film_rating: dict, n: int) -> list:
    top = dict(sorted(film_rating.items(), key=lambda item: item[1], reverse=True))
    res = list(top.items())
    return res[:n] if n != 0 and len(res) >= n else res


def export_csv(top_rating: list, f_name:str=None):
    fields = ['genre', 'title', 'year', 'rating']
    rows = []
    for elem in top_rating:
        _, title, genre = elem[0]
        rating = elem[1]
        name, year = extract_year_from_title(title)
        rows.append([genre, name, year, round(rating, 2)])
    with open(f'data/{f_name}', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def print_csv_like(top_rating: list):
    fields = ['genre', 'title', 'year', 'rating']
    print(fields)
    for elem in top_rating:
        _, title, genre = elem[0]
        rating = elem[1]
        name, year = extract_year_from_title(title)
        print([genre, name, year, round(rating, 2)])


def extract_year_from_title(title: str) -> tuple:
    reg = r'(.*)\((\d*)\)'
    return re.search(reg, title).group(1), re.search(reg, title).group(2)


def main(args):
    params = list(args.values())
    n = params[0][0] if params[0] is not None else 0  # +
    genres = params[1][0].split('|') if params[1] is not None else []  # +
    year_from = params[2][0] if params[2] is not None else 0
    year_to = params[3][0] if params[3] is not None else 0
    regexp = params[4][0] if params[4] is not None else ''
    output = params[5][1:] if params[5] is not None else 0
    rates = file_to_list('data/ratings.csv')
    movies = file_to_list('data/movies.csv', genres, int(year_from), int(year_to), regexp)
    test = find_avg_ratings(movies, rates)
    ls = find_top_n(test, int(n))

    if output != 0:
        export_csv(ls, output)
    else:
        print(ls)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get movies')
    parser.add_argument('-N', action='store', nargs=1, metavar='num',
                        help='set the number of films')
    parser.add_argument('-genres', action='store', nargs='*',
                        help='convert parquet file to parquet')
    parser.add_argument('-year_from', action='store', nargs=1, metavar='year_to',
                        help='year filter from')
    parser.add_argument('-year_to', action='store', nargs=1, metavar='year_from',
                        help='year filter to')
    parser.add_argument('-regexp', action='store', nargs=1, metavar='year_from',
                        help='regular expression for film name')
    parser.add_argument('>', nargs='?', default=None, metavar='output', help='redirects output')
    args = vars(parser.parse_args())
    print(args)
    main(args)
