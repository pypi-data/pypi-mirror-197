# coding=utf-8

from typing import Dict, List

import csv as pycsv


class Csv:

    class AoA:

        @staticmethod
        def write(
                aoa: List, path_: str, keys_: List, **kwargs) -> None:
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = pycsv.writer(
                           fd,
                           quotechar=quote,
                           quoting=pycsv.QUOTE_NONNUMERIC,
                           delimiter=delimiter)
                writer.writerow(keys_)
                for arr in aoa:
                    writer.writerow(arr)

    class AoD:

        @staticmethod
        def write(
                aod: List, path_: str, fieldnames: List, **kwargs) -> None:
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = pycsv.DictWriter(
                    fd,
                    fieldnames=fieldnames,
                    quotechar=quote,
                    quoting=pycsv.QUOTE_NONNUMERIC,
                    delimiter=delimiter
                )
                writer.writeheader()
                writer.writerows(aod)

    class Dic:

        @staticmethod
        def write(dic: Dict, path_: str, keys_: List, **kwargs) -> None:
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = pycsv.writer(
                           fd,
                           quotechar=quote,
                           quoting=pycsv.QUOTE_NONNUMERIC,
                           delimiter=delimiter)
                writer.writerow(keys_)
                writer.writerow(dic.values())

    # class D3:
    #
    #   @staticmethod
    #   def write(d3, cfg_io_out, d3_nm, **kwargs):
    #       _sw = kwargs.get('sw_' + d3_nm)
    #       if not _sw:
    #           return
    #       today = date.today().strftime("%Y%m%d")
    #       _path = kwargs.get(f'path_out_{d3_nm}').format(today=today)
    #       # _path = cfg_io_out[d3_nm]["pycsv"]["path"]
    #       _keys = cfg_io_out[d3_nm]["keys"]
    #       _aoa = D3V.yield_values(d3)
    #       Csv.AoA.write(_aoa, _path, _keys, **kwargs)

    @staticmethod
    def read_2_aod(
            path: str, **kwargs):
        # def read_2dod(path, **kwargs):
        mode = kwargs.get('mode', 'r')
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path, mode) as fd:
            return pycsv.DictReader(fd, delimiter=delimiter, quotechar=quote)
        return []

    @staticmethod
    def read_2_arr(
            path: str, **kwargs):
        # def read_2arr(
        mode = kwargs.get('mode', 'r')
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path, mode) as fd:
            return pycsv.reader(fd, delimiter=delimiter, quotechar=quote)
        return []

    @staticmethod
    def write_aod(
            aod: List, path_: str, **kwargs) -> None:
        fieldnames = aod[0].keys()
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path_, 'w') as fd:
            writer = pycsv.DictWriter(
                fd,
                fieldnames=fieldnames,
                quotechar=quote,
                quoting=pycsv.QUOTE_NONNUMERIC,
                delimiter=delimiter
            )
            writer.writeheader()
            writer.writerows(aod)
