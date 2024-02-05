from fastapi import APIRouter, Depends, HTTPException
from typing import List

from database.central.linktrees import LinktreesORM
from database.central.linktree_link import LinktreeLinkORM
from models.central.linktrees import LinktreeResponse, LinktreeLinksResponse, LinktreeCreate
from utils.jwt_token import has_authenticated

from string import ascii_letters, digits
from random import choice

chars = ascii_letters + digits + '-_'
router = APIRouter(prefix = '/api/linktree', tags = ['Backoffice - Produtos - Linktree'])


async def get_linktrees(user_id: int):
    linktrees = await LinktreesORM.find_many(user_id = user_id);
    data = []

    for linktree in linktrees:
        payload = LinktreeResponse(**linktree.dict())
        linktree_link = await LinktreeLinkORM.find_many(linktree_id = linktree.id)
        payload.links = [LinktreeLinksResponse(**ll.dict()) for ll in linktree_link]

        data.append(payload)
    return data
    

@router.get('', status_code = 200, name = 'Buscar Linktrees', response_model = List[LinktreeResponse])
async def linktrees(user: dict = Depends(has_authenticated)):
    return await get_linktrees(user.id)


@router.post('', status_code = 201, name = 'Cria Linktree', response_model = List[LinktreeResponse])
async def linktree_create(params: LinktreeCreate, user: dict = Depends(has_authenticated)):
    linktree = params.dict()
    linktree['user_id'] = user.id
    linktree['url'] = f'{user.id}{''.join(choice(chars) for _ in range(9))}'
    linktree.pop('links')
    linktree = await LinktreesORM.create(**linktree)

    for link in params.links:
        await LinktreeLinkORM.create(linktree_id = linktree.id, social_name = link.text, social_link = link.url)

    return await get_linktrees(user.id)


@router.put('/{slug}', status_code = 201, name = 'Edita Linktree', response_model = List[LinktreeResponse])
async def linktree_edit(slug: str, params: LinktreeCreate, user: dict = Depends(has_authenticated)):
    linktree = await LinktreesORM.find_one(user_id = user.id, url = slug)
    if not linktree: raise HTTPException(status_code = 404, detail = 'Linktree not found')

    data = params.dict()
    data.pop('links')
    await LinktreesORM.update(linktree.id, **data)

    links = params.links
    if links: await LinktreeLinkORM.delete(linktree_id = linktree.id)

    for link in links:
        await LinktreeLinkORM.create(linktree_id = linktree.id, social_name = link.text, social_link = link.url)

    return await get_linktrees(user.id)


@router.delete('/{slug}', status_code = 201, name = 'Exluir Linktree', response_model = List[LinktreeResponse])
async def linktree_delete(slug: str, user: dict = Depends(has_authenticated)):
    linktree = await LinktreesORM.find_one(user_id = user.id, url = slug)
    if not linktree: raise HTTPException(status_code = 404, detail = 'Linktree not found')

    await LinktreesORM.delete(user_id = linktree.user_id, url = linktree.url)
    await LinktreeLinkORM.delete(linktree_id = linktree.id)

    return await get_linktrees(user.id)


@router.get('/page/{slug}', status_code = 200, name = 'Buscar Linktree', response_model = LinktreeResponse)
async def linktree(slug: str):
    linktree = await LinktreesORM.find_one(url = slug);
    linktree = LinktreeResponse(**linktree.dict())

    linktree_link = await LinktreeLinkORM.find_many(linktree_id = linktree.id)
    linktree.links = [LinktreeLinksResponse(**ll.dict()) for ll in linktree_link]

    return linktree
