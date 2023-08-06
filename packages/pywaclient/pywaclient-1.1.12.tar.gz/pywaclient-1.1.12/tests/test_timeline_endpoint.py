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
    test_timelines_1 = client.timeline.put(
        {
            'title': 'Test Timelines Creation',
            'world': {
                'id': world_id
            }
        }
    )
    test_timelines_2 = client.timeline.put(
        {
            'title': 'Test Timelines Creation 2',
            'world': {
                'id': world_id}
        }
    )
    response_patch_timelines_2 = client.timeline.patch(
        test_timelines_2['id'],
        {
            'excerpt': 'This is an excerpt for an timelines.'
        }
    )

    full_test_timelines_2 = client.timeline.get(
        test_timelines_2['id'],
        2
    )

    assert full_test_timelines_2['excerpt'] == 'This is an excerpt for an timelines.'

    client.timeline.delete(test_timelines_1['id'])
    client.timeline.delete(test_timelines_2['id'])

    timelines_with_a_lot_of_views = client.timeline.put(
        {
            'title': 'An timelines with a lot of views.',
            'templateType': 'timelines',
            'world': {
                'id': world_id
            }
        }
    )
    print(client.timeline.get(timelines_with_a_lot_of_views['id'], 2))
