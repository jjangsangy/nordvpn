# -*- coding: utf-8 -*-

import chardet
import hashlib
import itertools
import json
import numpy as np
import operator
import pandas as pd
import requests
import argparse

from collections import Counter
from functools import reduce
from getpass import getpass
from hashlib import sha512
from io import BytesIO
from operator import itemgetter
from pandas.io.json import json_normalize
from zipfile import ZipFile

from urllib.parse import urljoin

from .api import Nord

def command_line():
    version = '0.0.1'
    parser = argparse.ArgumentParser(
        prog='nord',
        description='Nord VPN Command Line Tool',
        epilog='install using pip',
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version="%s v%s" % ('nordvpn', version)
    )
    parser.add_argument(
        '-u', '--username',
        nargs=1,
        help='Nord Account Username',
        metavar='user'
    )
    parser.add_argument(
        '-p', '--password',
        nargs=1,
        help='Nord Account Password',
        metavar='pass'
    )
    service = parser.add_subparsers(help='Get info on a nord service')
    for endpoint in Nord.endpoints:
        service.add_parser(endpoint, help=Nord.endpoints[endpoint])
    return parser.parse_args()

def gcd_vec(lat1, lng1, lat2, lng2):
    '''
    Calculate great circle distance.

    Parameters
    ----------
    lat1, lng1, lat2, lng2: float or array of float

    Returns
    -------
    distance:
      distance from ``(lat1, lng1)`` to ``(lat2, lng2)`` in kilometers.
    '''
    # python2 users will have to use ascii identifiers
    o1 = np.deg2rad(90 - lat1)
    o2 = np.deg2rad(90 - lat2)

    a1 = np.deg2rad(lng1)
    a2 = np.deg2rad(lng2)

    cos = (np.sin(o1) * np.sin(o2) * np.cos(a1 - a2) +
           np.cos(o1) * np.cos(o2))
    arc = np.arccos(cos)
    return arc * 6373


def sanitize(name):
    return name.lower().replace(' ', '_')

def flatten_names(nested):
    name_getter = itemgetter('name')
    return set(map(sanitize, map(name_getter, nested)))

def get_dummies(categories):
    return dict(Counter(flatten_names(categories)))


def create_table(nord):
    meta = list(reduce(set.union, map(set, servers)))
    df = json_normalize(servers, meta=meta).set_index('id').sort_index()
    cat = df['categories']
    dummies = cat.map(get_dummies)
    index = dummies.index
    values = sorted(reduce(set.union, map(set, dummies.values)))
    columns = pd.CategoricalIndex(values, ordered=True, name='categories')
    one_hot = pd.DataFrame.from_records(data=dummies.values,
                                        columns=columns,
                                        index=index)
    one_hot = one_hot.replace({np.nan: 0}).astype(np.int8)
    return df.drop('categories', axis=1).append(one_hot)

def main():
    return command_line()


if __name__ == '__main__':
    print(main())
