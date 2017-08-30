#!/usr/bin/env python3

# https://www.youneedabudget.com/fbi/
# http://classic.youneedabudget.com/support/article/csv-file-importing

import argparse
import csv
import re


def write_output(outputfile, rows):
    with open(outputfile, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["Date", "Payee", "Category", "Memo", "Outflow", "Inflow"])
        for row in rows:
            w.writerow(row)


def format_row_from_fields(payee, amount, datestamp):
    #payee = payee
    # Remove space thousand separator, and change comma separator to dot so the float conversion works :3.
    amount = amount.replace(" ", "")
    amount = amount.replace(",", ".")
    amount = float(amount)
    inflow = ""
    outflow = ""
    if(amount < 0):
        outflow = str(amount*-1)
    else:
        inflow = str(amount)

    # We will use format DD/MM/YYYY, though indata is YYYY-MM-DD.
    datestamp = datestamp.split("-")[2] + "/" + datestamp.split("-")[1] + "/" + datestamp.split("-")[0]

    row = [datestamp, payee, "", "", outflow, inflow]
    return row


def parse_file(inputfile):
    content = open(inputfile).readlines()
    content = "".join(content)

    #Some Company AB (payee)
    #-1 234,56	11 111,11 (amount paid, total amount)
    #2017-08-29	2017-08-29	Card (date, date, type)

    rows = []
    #c = re.compile(r"^(.+)\n([0-9 -]+,[0-9-]+)[0-9 ,\t]+\n[\d]{4}-[\d]{2}-[\d]{2}\t([\d]{4}-[\d]{2}-[\d]{2})\t.*$", re.MULTILINE)
    c = re.compile(r"^[\d]{4}-[\d]{2}-[\d]{2}\t([\d]{4}-[\d]{2}-[\d]{2})\t.*\n(.+)\n([0-9 -]+,[0-9-]+)[0-9 ,\t]+$", re.MULTILINE)

    for match in c.finditer(content):
        #payee, amount, datestamp = match.groups()
        datestamp, payee, amount = match.groups()
        row = format_row_from_fields(payee, amount, datestamp)
        rows.append(row)

    return rows


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", help="Test parameter.")
    parser.add_argument("-f", "--file", help="Target input file name", required=True)
    parser.add_argument("-o", "--output", help="Target output file name", required=True)

    return parser.parse_args()


def main():
    args = handle_args()

    inputfile = args.file
    outputfile = args.output

    rows = parse_file(inputfile)
    write_output(outputfile, rows)


if __name__ == "__main__":
    main()
