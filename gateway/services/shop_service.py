import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from utils.forward import forward_request


load_dotenv()

SHOP_SERVICE = os.getenv('SHOP_SERVICE')
router = APIRouter(tags=["Shop Service"])


@router.get('/shops/', tags=['Shop Service'])
async def gateway_shop_list():
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/')


@router.get('/shops/{shop_slug}/', tags=['Shop Service'])
async def gateway_shop_detail(shop_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/')


@router.post('/shops/create/', tags=['Shop Service'])
async def gateway_shop_create(data: dict):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/create/', method='post', data=data)


@router.api_route('/shops/{shop_slug}/management/', methods=['PATCH', 'DELETE'], tags=['Shop Service'])
async def gateway_shop_manage(shop_slug: str, request: Request):
    body = await request.json() if request.method == 'PATCH' else None
    return await forward_request(
        f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/management/',
        method=request.method,
        data=body
    )


@router.get('/shops/{shop_slug}/comments/', tags=['Shop Comments'])
async def gateway_comment_list(shop_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/comments/')


@router.post('/shops/{shop_slug}/comment/create/', tags=['Shop Comments'])
async def gateway_comment_create(shop_slug: str, data: dict):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/comment/create/', method='post', data=data)


@router.api_route('/comments/{comment_id}/management/', methods=['PATCH', 'DELETE'], tags=['Shop Comments'])
async def gateway_comment_manage(comment_id: int, request: Request):
    body = await request.json() if request.method == 'PATCH' else None
    return await forward_request(
        f'{SHOP_SERVICE}/api/v1/comments/{comment_id}/management/',
        method=request.method,
        data=body
    )


@router.get('/shops/{shop_slug}/branches/', tags=['Shop Branches'])
async def gateway_branch_list(shop_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/branches/')


@router.get('/branches/{shop_branch_slug}/', tags=['Shop Branches'])
async def gateway_branch_detail(shop_branch_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/branches/{shop_branch_slug}/')


@router.post('/shops/{shop_slug}/branches/create/', tags=['Shop Branches'])
async def gateway_branch_create(shop_slug: str, data: dict):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/branches/create/', method='post', data=data)


@router.api_route('/branches/{shop_branch_slug}/management/', methods=['PATCH', 'DELETE'], tags=['Shop Branches'])
async def gateway_branch_manage(shop_branch_slug: str, request: Request):
    body = await request.json() if request.method == 'PATCH' else None
    return await forward_request(
        f'{SHOP_SERVICE}/api/v1/branches/{shop_branch_slug}/management/',
        method=request.method,
        data=body
    )


@router.get('/shops/{shop_slug}/social-media/', tags=['Shop Social Media'])
async def gateway_social_list(shop_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/social-media/')


@router.get('/social-media/{social_media_id}/', tags=['Shop Social Media'])
async def gateway_social_detail(social_media_id: int):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/social-media/{social_media_id}/')


@router.post('/shops/{shop_slug}/social-media/create/', tags=['Shop Social Media'])
async def gateway_social_create(shop_slug: str, data: dict):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/social-media/create/', method='post', data=data)


@router.api_route('/social-media/{social_media_id}/management/', methods=['PATCH', 'DELETE'], tags=['Shop Social Media'])
async def gateway_social_manage(social_media_id: int, request: Request):
    body = await request.json() if request.method == 'PATCH' else None
    return await forward_request(
        f'{SHOP_SERVICE}/api/v1/social-media/{social_media_id}/management/',
        method=request.method,
        data=body
    )


@router.get('/shops/{shop_slug}/media/', tags=['Shop Media'])
async def gateway_media_list(shop_slug: str):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/media/')


@router.post('/shops/{shop_slug}/media/create/', tags=['Shop Media'])
async def gateway_media_create(shop_slug: str, data: dict):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/shops/{shop_slug}/media/create/', method='post', data=data)


@router.delete('/media/{media_id}/delete/', tags=['Shop Media'])
async def gateway_media_delete(media_id: int):
    return await forward_request(f'{SHOP_SERVICE}/api/v1/media/{media_id}/delete/', method='delete')