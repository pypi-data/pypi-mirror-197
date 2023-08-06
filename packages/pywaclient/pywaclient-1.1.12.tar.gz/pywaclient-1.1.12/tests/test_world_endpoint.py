#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from collections import Counter

from pywaclient.exceptions import UnprocessableDataProvided
from init_client import client, user

if __name__ == '__main__':
    wbtv = 'a86b6da9-6ba2-413a-87d9-ee98cbc6d9b9'

    result = client.world.get(wbtv, 2)

    for w in client.user.worlds(user['id']):
        print(w)
        for n in client.world.notebooks(w['id']):
            print(n)

    counter = Counter()
    try:
        for a in client.world.statblock_folders(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.subscriber_groups(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.categories(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.secrets(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.chronicle(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.timeline(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.history(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.map(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.manuscripts(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.images(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    counter = Counter()
    try:
        for a in client.world.canvases(wbtv):
            counter.update([a['id']])
        print(counter)
    except UnprocessableDataProvided as err:
        print(err.status)
        print(err.error_summary)
        print(err.error_tracestack)

    # counter = Counter()
    # try:
    #     for a in client.world.variable_collections(wbtv):
    #         counter.update([a['id']])
    #     print(counter)
    # except UnprocessableDataProvided as err:
    #     print(err.status)
    #     print(err.error_summary)
    #     print(err.error_tracestack)
