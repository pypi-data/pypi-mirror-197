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
    test_article_1 = client.article.put(
        {
            'title': 'Secret Article',
            'templateType': 'article',
            'world': {
                'id': world_id}
        }
    )


    test_secret_1 = client.secret.put(
        {
            'title': 'Test Secret Creation',
            "content": "This is some content for the secret.",
            "article": {
                "id": test_article_1['id']
            },
            'world': {
                'id': world_id
            }
        }
    )
    test_secret_2 = client.secret.put(
        {
            'title': 'Test Secret Creation 2',
            'world': {
                'id': world_id}
        }
    )
    response_patch_secret_2 = client.secret.patch(
        test_secret_2['id'],
        {
            'excerpt': 'This is an excerpt for an secret.'
        }
    )

    full_test_secret_2 = client.secret.get(
        test_secret_2['id'],
        2
    )

    assert full_test_secret_2['excerpt'] == 'This is an excerpt for an secret.'

    client.secret.delete(test_secret_1['id'])
    client.secret.delete(test_secret_2['id'])

    client.article.delete(test_article_1['id'])
