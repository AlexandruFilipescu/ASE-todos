from tinydb import TinyDB, Query
from typing import Union

class DatabaseActions:
    db = TinyDB('database.json')
    todos_table = db.table('todos_table')
    todo = Query()

    def post_todo(self, title: str, completed: bool, order: int)\
            -> dict[str, Union[str, bool, int]]:
        self.todos_table.insert({
            'title' : title,
            'completed' : completed,
            'order': order
        })

        return {
            'title': title,
            'completed': completed,
            'order': order,
        #    Also return ID and url
        }

    def delete_todos(self):
        self.db.drop_table('todos_table')

    def get_todo(self, id: str):
        return {
            self.todos_table.search(self.todo.id == id)
        }

    def delete_todo (self, id: str):
        self.todos_table.remove(doc_ids=id)
        return {
            'Deleted todo' : id
        }

    def patch_todo(self, id:str, title: str, completed: bool, order: int):
        self.todos_table.update({'title' : title,
                                 'completed': completed,
                                 'order': order}, doc_ids=[id])

        return {
            'id': id,
            'title' : title,
            'completed' : completed,
            'url' : '#    Also return ID and url',
            'order' : order
        }










