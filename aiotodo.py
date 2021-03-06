import logging

import aiohttp
import aiohttp_cors
from aiohttp import web

from database import *

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False},
    1: {'title': '?????', 'order': 2, 'completed': False},
    2: {'title': 'profit!', 'order': 3, 'completed': False}
}


def get_todos(request):
    return web.json_response([
        {'id': key, **todo} for key, todo in TODOS.items()
    ])


def remove_todos(request):
    TODOS.clear()
    return web.Response(status=204)


def get_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': id, **TODOS[id]})


async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    new_id = max(TODOS.keys(), default=0) + 1
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    TODOS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


async def update_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])


def remove_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)


app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*",
    )
})

cors.add(app.router.add_get('/todos/', handler=get_todos, name='all_todos', expect_handler = aiohttp.web.Request.json))
cors.add(app.router.add_delete('/todos/', handler=remove_todos, name='remove_todos'))
cors.add(app.router.add_post('/todos/', handler=create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', handler=get_todo, name='one_todo'))
cors.add(app.router.add_patch('/todos/{id:\d+}', handler=update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', handler=remove_todo, name='remove_todo'))

logging.basicConfig(level=logging.DEBUG)
#web.run_app(app, port=8080)
web.run_app(app, host="127.0.0.1", port=8080)

