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
import json

from init_client import world_id, client

if __name__ == '__main__':
    article = client.article.get('75f10418-bd08-4593-aa7d-9366edea0a57', 3)
    print(json.dumps(article))

    test_article_1 = client.article.put(
        {
            'title': 'Test Article Creation',
            'templateType': 'article',
            'world': {
                'id': world_id}
        }
    )
    test_article_2 = client.article.put(
        {
            'title': 'Test Article Creation 2',
            'templateType': 'article',
            'world': {
                'id': world_id}
        }
    )
    response_patch_article_2 = client.article.patch(
        test_article_2['id'],
        {
            'excerpt': 'This is an excerpt for an article.'
        }
    )

    full_test_article_2 = client.article.get(
        test_article_2['id'],
        2
    )

    assert full_test_article_2['excerpt'] == 'This is an excerpt for an article.'

    client.article.delete(test_article_1['id'])
    client.article.delete(test_article_2['id'])

    article_with_a_lot_of_views = client.article.put(
        {
            'title': 'An article with a lot of views.',
            'templateType': 'article',
            'world': {
                'id': world_id
            }
        }
    )
    print(client.article.get(article_with_a_lot_of_views['id'], 2))
