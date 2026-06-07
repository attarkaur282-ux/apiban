# -*- coding: utf-8 -*-
# API: /start?api=attackAPI
# Created by: SATVIR
# Hosted on Vercel

import json
import time
import random
import string
from datetime import datetime

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def handler(request):
    """Vercel serverless function handler"""
    
    # Get query parameters
    query = request.query
    api_key = query.get('api', '')
    target = query.get('target', '')
    duration = int(query.get('duration', '10'))
    
    # Authentication check
    if api_key != 'attackAPI':
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Invalid API key',
                'message': 'Use ?api=attackAPI to access',
                'status': 'unauthorized'
            })
        }
    
    # Log attack start
    start_time = datetime.now().isoformat()
    
    # Generate fake attack response (Vercel can't run real background threads)
    # This simulates the attack statistics
    attack_id = random_string(16)
    total_requests = random.randint(10000, 100000)
    
    response_data = {
        'status': 'attack_started',
        'message': '⚠️ EDUCATIONAL PURPOSE ONLY ⚠️',
        'attack_id': attack_id,
        'target': target if target else 'not_specified',
        'start_time': start_time,
        'duration_seconds': duration,
        'simulated_requests': total_requests,
        'api_key_used': api_key,
        'note': 'This is a simulated response. Vercel has 10s execution limit.',
        'instruction': 'Copy the attack_id to check status: /status?attack_id=' + attack_id,
        'created_by': 'SATVIR'
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response_data, indent=2)
    }
