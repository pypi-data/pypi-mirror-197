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

from init_client import client

if __name__ == '__main__':
    notebook = client.notebook.get('5b794d91-2730-4b76-aa21-dddbabdc1c58', 2)
    print(notebook)

    for s in client.notebook.note_sections(notebook['id']):
        print(s)
        for n in client.note_section.notes(s['id']):
            print(n)

    for s in notebook['notesections']:
        section = client.note_section.get(s['id'], 2)
        print(section)

        client.note.put(
            {'title': 'A new note', 'content': 'Some content', 'notesection': {'id': section['id']}}
        )

    # client.note_section.put(
    #     {
    #         'title': 'A new section',
    #         'notebook': {
    #             'id': notebook['id']
    #         }
    #     }
    #
    # )

    # value = client.notebook.put(
    #     {
    #         'title': "A New Notebook",
    #         'owner': {
    #             'id': '42eb1d6a-021b-49b4-bbbb-f7ddf6b135a4'
    #         }
    #     }
    # )
    # print(value)