import re
from operator import itemgetter


def parse_files(currencies_file, data_file, matchings_file):

    currencies = None
    data = None
    matchings = None

    try:
        with open(currencies_file, 'r') as c, open(data_file, 'r') as d, open(matchings_file, 'r') as m:
            currencies = c.readlines()[1:]
            data = d.readlines()[1:]
            matchings = m.readlines()[1:]
    except IOError as e:
        print("I/O Error {0}: {1}".format(e.errno, e.strerror))

    return currencies, data, matchings


def convert_to_pln(currencies, data):

    converted_data = []
    gb_ratio = float(re.search(r'GBP,([0-9]\.[0-9]+)', "".join(currencies))[1])
    eu_ratio = float(re.search(r'EU,([0-9]\.[0-9]+)', "".join(currencies))[1])

    for row in data:

        if "PLN" in row:
            converted_data.append(row)
        elif "GBP" in row:
            row = row.split(",")
            row[1] = str(float(row[1]) * gb_ratio)
            row[2] = "PLN"
            row = ",".join(row)
            converted_data.append(row)
        elif "EU" in row:
            row = row.split(",")
            row[1] = str(float(row[1]) * eu_ratio)
            row[2] = "PLN"
            row = ",".join(row)
            converted_data.append(row)

    return converted_data


def sort_by_price(matching_id, data):

    matching_rows = []
    for row in data:
        row = row.split(",")
        if int(row[4]) == int(matching_id):
            total_price = float(row[1]) * float(row[3])
            row.append(total_price)
            matching_rows.append(row)

    matching_rows.sort(key=itemgetter(-1), reverse=True)
    return matching_rows


def aggregate_products(matchings, data):

    results = []
    for row in matchings:

        total_price = 0
        total_quantity = 0
        row = row.split(",")
        product_list = sort_by_price(row[0], data)
        ignored_product_counts = len(product_list) - int(row[1])
        product_list = product_list[:int(row[1])]

        for product in product_list:

            total_price += float(product[-1])
            total_quantity += float(product[3])

        try:
            avg_price = total_price/total_quantity
        except ZeroDivisionError as e:
            print("ZeroDivisionError")

        matching_id = row[0]
        currency = "PLN"
        result_string = "{0},{1},{2},{3},{4}\n".format(row[0], total_price,
                                                       avg_price, currency,
                                                       ignored_product_counts)
        results.append(result_string)

    return results


def save_results(result):

    try:
        with open("top_products.csv", 'w') as f:
            for line in result:
                f.write(line)
    except IOError as e:
        print("I/O Error {0}: {1}".format(e.errno, e.strerror))


currencies, data, matchings = parse_files('currencies.csv',
                                          'data.csv', 'matchings.csv')
converted_data = convert_to_pln(currencies, data)
save_results(aggregate_products(matchings, data))
