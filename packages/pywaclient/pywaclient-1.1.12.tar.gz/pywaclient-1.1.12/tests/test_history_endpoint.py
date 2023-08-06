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

from init_client import world_id, client

if __name__ == '__main__':
    test_histories_1 = client.history.put(
        {
            'title': 'Test Histories Creation',
            "year":"5545",
            'world': {
                'id': world_id
            }
        }
    )
    test_histories_2 = client.history.put(
        {
            'title': 'Test Histories Creation 2',
            'templateType': 'histories',
            'world': {
                'id': world_id}
        }
    )
    response_patch_histories_2 = client.history.patch(
        test_histories_2['id'],
        {
            'excerpt': 'This is an excerpt for an histories.'
        }
    )

    full_test_histories_2 = client.history.get(
        test_histories_2['id'],
        2
    )

    assert full_test_histories_2['excerpt'] == 'This is an excerpt for an histories.'

    client.history.delete(test_histories_1['id'])
    client.history.delete(test_histories_2['id'])

    histories_with_a_lot_of_views = client.history.put(
        {
            'title': 'An histories with a lot of views.',
            'templateType': 'histories',
            'world': {
                'id': world_id
            }
        }
    )
    print(client.history.get(histories_with_a_lot_of_views['id'], 2))
