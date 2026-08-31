"""
╔══════════════════════════════════════════════════════════════════╗
║         🔥 CACHED OSINT BOT — REAL DATA + CACHE 🔥             ║
║         API se real data → DB save → API dead → cache reply    ║
║         Made by: @Guptaji_302                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import sqlite3
import threading
import requests
import re
import random
import hashlib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import urllib.parse

# ==================== TELEGRAM BOT IMPORTS ====================
try:
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser
    )
except ImportError:
    os.system("pip install pyTelegramBotAPI==4.22.0")
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser
    )

# ==================== FLASK ====================
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running ✅ | Made by @Guptaji_302", 200

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    app.run(host='0.0.0.0', port=10000, use_reloader=False, threaded=True)

# ==================== ENVIRONMENT ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set!")
    sys.exit(1)

try:
    OWNER_ID = int(os.environ.get("OWNER_ID", "7545664963"))
except ValueError:
    OWNER_ID = 7545664963

FREE_CREDITS = 5
DAILY_CREDITS = 1
REFERRAL_CREDITS = 1
BOT_CREDIT = "⚡ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ : @Guptaji_302"

# ==================== DATABASE WITH CACHE TABLES ====================
def init_db():
    global conn, c
    conn = sqlite3.connect('bot.db', check_same_thread=False, timeout=30)
    c = conn.cursor()
    
    c.executescript('''
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            join_date TEXT,
            referrer INTEGER,
            credits INTEGER DEFAULT 10,
            is_blocked INTEGER DEFAULT 0,
            is_premium INTEGER DEFAULT 0,
            premium_until TEXT,
            total_searches INTEGER DEFAULT 0,
            last_active TEXT,
            money INTEGER DEFAULT 0
        );
        
        -- Admins
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            added_by INTEGER,
            added_date TEXT,
            is_owner INTEGER DEFAULT 0
        );
        
        -- Referrals
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer INTEGER,
            referred INTEGER,
            date TEXT
        );
        
        -- Search History
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            search_type TEXT,
            query TEXT,
            search_date TEXT,
            result TEXT
        );
        
        -- Daily Claims
        CREATE TABLE IF NOT EXISTS daily_claims (
            user_id INTEGER,
            claim_date TEXT,
            PRIMARY KEY (user_id, claim_date)
        );
        
        -- Redeem Codes
        CREATE TABLE IF NOT EXISTS redeem_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            credits INTEGER,
            max_uses INTEGER,
            used_count INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TEXT,
            expires_at TEXT,
            is_active INTEGER DEFAULT 1
        );
        
        -- Redeemed Users
        CREATE TABLE IF NOT EXISTS redeemed_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT,
            redeemed_at TEXT
        );
        
        -- Bomber History
        CREATE TABLE IF NOT EXISTS bomber_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_number TEXT,
            sms_sent INTEGER DEFAULT 0,
            calls_sent INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running',
            started_at TEXT,
            stopped_at TEXT
        );
        
        -- ========== CACHE TABLES ==========
        -- Number Cache
        CREATE TABLE IF NOT EXISTS cache_number (
            number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Aadhar Cache
        CREATE TABLE IF NOT EXISTS cache_aadhar (
            aadhar TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- UPI Cache
        CREATE TABLE IF NOT EXISTS cache_upi (
            upi TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Instagram Cache
        CREATE TABLE IF NOT EXISTS cache_instagram (
            username TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- IFSC Cache
        CREATE TABLE IF NOT EXISTS cache_ifsc (
            ifsc TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Vehicle Cache
        CREATE TABLE IF NOT EXISTS cache_vehicle (
            rc_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- GST Cache
        CREATE TABLE IF NOT EXISTS cache_gst (
            gst_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- PAN Cache
        CREATE TABLE IF NOT EXISTS cache_pan (
            pan_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Pak Number Cache
        CREATE TABLE IF NOT EXISTS cache_pak (
            number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Pincode Cache
        CREATE TABLE IF NOT EXISTS cache_pincode (
            pincode TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        -- Free Fire Cache
        CREATE TABLE IF NOT EXISTS cache_ff (
            uid TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
    ''')
    conn.commit()
    
    # Add owner as admin
    try:
        c.execute("INSERT OR IGNORE INTO admins (user_id, added_by, added_date, is_owner) VALUES (?, ?, ?, ?)",
                  (OWNER_ID, OWNER_ID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
        conn.commit()
    except Exception:
        pass
    
    # Add owner as user
    try:
        c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, join_date, credits, last_active) VALUES (?, ?, ?, ?, ?, ?)",
                  (OWNER_ID, 'owner', 'Bot Owner', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 999999, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except Exception:
        pass
    
    print("✅ Database with cache initialized!")

# ==================== CACHE FUNCTIONS ====================

def cache_get(table, key):
    """Get cached data from database"""
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute(f"SELECT data, hit_count FROM {table} WHERE {table.split('_')[1]} = ?", (key,))
        row = c.fetchone()
        if row:
            # Update hit count
            c.execute(f"UPDATE {table} SET hit_count = hit_count + 1, updated_at = CURRENT_TIMESTAMP WHERE {table.split('_')[1]} = ?", (key,))
            conn.commit()
            conn.close()
            return json.loads(row[0])
        conn.close()
        return None
    except Exception as e:
        print(f"[Cache Get] {e}")
        return None

def cache_set(table, key, data):
    """Save data to cache"""
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        data_json = json.dumps(data, default=str)
        c.execute(f"INSERT OR REPLACE INTO {table} ({table.split('_')[1]}, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (key, data_json))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Cache Set] {e}")
        return False

def cache_get_all_stats():
    """Get cache statistics"""
    tables = ['cache_number', 'cache_aadhar', 'cache_upi', 'cache_instagram', 
              'cache_ifsc', 'cache_vehicle', 'cache_gst', 'cache_pan', 
              'cache_pak', 'cache_pincode', 'cache_ff']
    stats = {}
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        for table in tables:
            c.execute(f"SELECT COUNT(*), SUM(hit_count) FROM {table}")
            count, hits = c.fetchone()
            stats[table.replace('cache_', '')] = {'count': count or 0, 'hits': hits or 0}
        conn.close()
    except Exception:
        pass
    return stats

# ==================== CACHED API FUNCTIONS ====================

def get_number_info(number):
    """Number Info with CACHE — REAL API first, then cache"""
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    # STEP 1: Check Cache
    cached = cache_get('cache_number', clean)
    if cached:
        print(f"[Cache HIT] Number: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Number: {clean}")
    
    # STEP 2: Try NITIN API
    try:
        url = f"https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=num&number={clean}&key=JAANI"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'total_records': len(data['result']),
                    'source': 'nitin_api'
                }
                # Save to cache
                cache_set('cache_number', clean, result)
                return result
    except Exception as e:
        print(f"[API Error] {e}")
    
    # STEP 3: Try Backup API
    try:
        url = f"https://phone-info-api.vercel.app/api?number={clean}"
        resp = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data:
                result = {
                    'success': True,
                    'data': [data] if isinstance(data, dict) else data,
                    'total_records': 1,
                    'source': 'backup_api'
                }
                cache_set('cache_number', clean, result)
                return result
    except Exception:
        pass
    
    # STEP 4: Return cache anyway (even if expired) or demo
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_aadhar_info(aadhar):
    """Aadhar Info with CACHE"""
    clean = re.sub(r'\s+', '', str(aadhar))
    if not re.match(r'^\d{12}$', clean):
        return {'success': False, 'msg': 'Invalid Aadhar'}
    
    # Check Cache
    cached = cache_get('cache_aadhar', clean)
    if cached:
        print(f"[Cache HIT] Aadhar: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Aadhar: {clean}")
    
    try:
        url = f"https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=aadhar&aadhar={clean}&key=JAANI"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'total_records': len(data['result']),
                    'source': 'nitin_api'
                }
                cache_set('cache_aadhar', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_upi_info(upi):
    """UPI Info with CACHE"""
    if '@' not in upi:
        return {'success': False, 'msg': 'Invalid UPI ID'}
    
    cached = cache_get('cache_upi', upi)
    if cached:
        print(f"[Cache HIT] UPI: {upi}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] UPI: {upi}")
    
    try:
        url = f"https://nitin-developer-api-paid.nitinshab43.workers.dev/api?action=upiinfo&upi={upi}&key=JAANI"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'total_records': len(data['result']),
                    'source': 'nitin_api'
                }
                cache_set('cache_upi', upi, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_instagram_info(username):
    """Instagram Info with CACHE"""
    clean = username.replace('@', '').strip()
    if len(clean) < 2:
        return {'success': False, 'msg': 'Invalid username'}
    
    cached = cache_get('cache_instagram', clean)
    if cached:
        print(f"[Cache HIT] Instagram: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Instagram: {clean}")
    
    try:
        url = f"https://instagram-api.vercel.app/api/info?username={clean}"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data:
                user_data = data.get('user', data)
                result = {
                    'success': True,
                    'data': [{
                        'username': user_data.get('username', clean),
                        'full_name': user_data.get('full_name', ''),
                        'bio': user_data.get('bio', ''),
                        'followers': user_data.get('follower_count', user_data.get('followers', 0)),
                        'following': user_data.get('following_count', user_data.get('following', 0)),
                        'posts': user_data.get('media_count', user_data.get('posts', 0)),
                        'verified': user_data.get('is_verified', user_data.get('verified', False)),
                        'is_private': user_data.get('is_private', user_data.get('private', False)),
                    }],
                    'source': 'instagram_api'
                }
                cache_set('cache_instagram', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_ifsc_info(ifsc):
    """IFSC Info with CACHE"""
    clean = ifsc.upper().strip()
    if len(clean) != 11:
        return {'success': False, 'msg': 'Invalid IFSC'}
    
    cached = cache_get('cache_ifsc', clean)
    if cached:
        print(f"[Cache HIT] IFSC: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] IFSC: {clean}")
    
    try:
        url = f"https://ifsc-api.vercel.app/api?action=ifsc&code={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'ifsc_api'
                }
                cache_set('cache_ifsc', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_vehicle_info(vehicle):
    """Vehicle Info with CACHE"""
    clean = re.sub(r'\s+', '', vehicle).upper()
    if len(clean) < 8:
        return {'success': False, 'msg': 'Invalid RC number'}
    
    cached = cache_get('cache_vehicle', clean)
    if cached:
        print(f"[Cache HIT] Vehicle: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Vehicle: {clean}")
    
    try:
        url = f"https://vehicle-api.vercel.app/api?action=rc&number={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'vehicle_api'
                }
                cache_set('cache_vehicle', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_gst_info(gst):
    """GST Info with CACHE"""
    clean = gst.upper().strip()
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid GST'}
    
    cached = cache_get('cache_gst', clean)
    if cached:
        print(f"[Cache HIT] GST: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] GST: {clean}")
    
    try:
        url = f"https://gst-api.vercel.app/api?action=gst&number={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'gst_api'
                }
                cache_set('cache_gst', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pan_info(pan):
    """PAN Info with CACHE"""
    clean = pan.upper().strip()
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', clean):
        return {'success': False, 'msg': 'Invalid PAN format'}
    
    cached = cache_get('cache_pan', clean)
    if cached:
        print(f"[Cache HIT] PAN: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] PAN: {clean}")
    
    try:
        url = f"https://pan-api.vercel.app/api?action=pan&number={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'pan_api'
                }
                cache_set('cache_pan', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pak_num_info(number):
    """Pak Number Info with CACHE"""
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    cached = cache_get('cache_pak', clean)
    if cached:
        print(f"[Cache HIT] Pak: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Pak: {clean}")
    
    try:
        url = f"https://pak-api.vercel.app/api?action=pak&number={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'pak_api'
                }
                cache_set('cache_pak', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pincode_info(pincode):
    """Pincode Info with CACHE"""
    clean = re.sub(r'[^\d]', '', str(pincode))
    if len(clean) != 6:
        return {'success': False, 'msg': 'Invalid pincode'}
    
    cached = cache_get('cache_pincode', clean)
    if cached:
        print(f"[Cache HIT] Pincode: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] Pincode: {clean}")
    
    try:
        url = f"https://pincode-api.vercel.app/api?action=pincode&code={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'pincode_api'
                }
                cache_set('cache_pincode', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_ff_info(uid):
    """Free Fire Info with CACHE"""
    clean = re.sub(r'[^\d]', '', str(uid))
    if len(clean) < 5:
        return {'success': False, 'msg': 'Invalid UID'}
    
    cached = cache_get('cache_ff', clean)
    if cached:
        print(f"[Cache HIT] FF: {clean}")
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    print(f"[API CALL] FF: {clean}")
    
    try:
        url = f"https://ff-api.vercel.app/api?action=ff&uid={clean}&key=free"
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') and data.get('result'):
                result = {
                    'success': True,
                    'data': data['result'],
                    'source': 'ff_api'
                }
                cache_set('cache_ff', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = "Old cache"
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_hitek_num_info(number):
    """Hitek Number Info with CACHE"""
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    # No API for Hitek, just use cache or demo
    cached = cache_get('cache_number', clean)  # Reuse number cache
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    # Try number API as fallback
    result = get_number_info(clean)
    if result.get('success'):
        return result
    
    return {'success': False, 'msg': 'No data found'}

def get_hitek_full_info(query):
    """Hitek Full Info with CACHE"""
    if len(query) < 2:
        return {'success': False, 'msg': 'Invalid query'}
    
    # Simple cache for hitek full
    cache_key = hashlib.md5(query.encode()).hexdigest()[:16]
    cached = cache_get('cache_number', cache_key)  # Reuse cache
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    # Try to get from number API first
    if re.search(r'\d', query):
        clean_num = re.sub(r'[^\d]', '', query)
        if len(clean_num) >= 10:
            result = get_number_info(clean_num)
            if result.get('success'):
                cache_set('cache_number', cache_key, result)
                return result
    
    return {'success': False, 'msg': 'No data found'}

# ==================== FORMAT FUNCTIONS ====================

def _DIV():
    return "━━━━━━━━━━━━━━━━━━"

def _esc(v):
    return str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def format_message(text):
    return f"<blockquote>{text}\n\n{BOT_CREDIT}</blockquote>"

def format_generic_result(data, title, query_label, query_value):
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    records = data.get('data', [])
    if not records:
        return format_message(
            f"📋 <b>{title}</b>\n{_DIV()}\n"
            f"🕐 {now}\n"
            f"🔎 {query_label}: <code>{query_value}</code>\n"
            f"❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ\n{_DIV()}"
        )
    
    # Check if from cache
    cache_badge = " 💾 [CACHE]" if data.get('_from_cache') else ""
    cache_time = f"\n📅 ᴄᴀᴄʜᴇᴅ: {data.get('_cache_time', 'N/A')}" if data.get('_from_cache') else ""
    
    lines = [
        f"📋 <b>{title}</b>{cache_badge}",
        f"{_DIV()}",
        f"🕐 {now}",
        f"🔎 {query_label}: <code>{_esc(str(query_value))}</code>",
        f"📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: <b>{len(records)}</b>{cache_time}",
        f"📡 <b>ꜱᴏᴜʀᴄᴇ:</b> {data.get('source', 'Unknown')}",
        f"{_DIV()}",
    ]
    
    for idx, item in enumerate(records, 1):
        if len(records) > 1:
            lines.append(f"")
            lines.append(f"👤 <b>ʀᴇᴄᴏʀᴅ {idx}/{len(records)}</b>")
        
        fields = []
        for k, v in item.items():
            if k.lower() in ('success', 'status', 'msg', 'message', '_raw', 'metadata', 'source', '_from_cache', '_cache_time'):
                continue
            if v and str(v).strip() not in ('', 'N/A', 'None', 'null', '0'):
                emoji = '👤' if 'name' in k.lower() else '🏠' if 'address' in k.lower() else '📱' if 'number' in k.lower() else '•'
                fields.append((emoji, k.replace('_', ' ').title(), v))
        
        if fields:
            for i, (em, label, val) in enumerate(fields[:10]):
                c = "└" if i == len(fields[:10]) - 1 else "├"
                lines.append(f"{c}{em} <b>{label}</b>: <code>{_esc(str(val))}</code>")
        else:
            lines.append("└❌ ɴᴏ ᴅᴀᴛᴀ")
    
    lines.append(f"{_DIV()}")
    return format_message("\n".join(lines))

def format_number_info_bold(data, number):
    return format_generic_result(data, "📱 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢", "📞 Number", number)

def format_aadhar_result_bold(data, aadhar):
    return format_generic_result(data, "🪪 𝗔𝗔𝗗𝗛𝗔𝗥 𝗜𝗡𝗙𝗢", "🪪 Aadhar", aadhar)

def format_upi_result_bold(data, upi):
    return format_generic_result(data, "💳 𝗨𝗣𝗜 𝗜𝗡𝗙𝗢", "💳 UPI", upi)

# ==================== USER FUNCTIONS ====================

def get_user(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def add_user(user_id, username, first_name, referrer=None):
    conn = sqlite3.connect('bot.db', timeout=10)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, join_date, referrer, credits, last_active) 
            VALUES (?,?,?,?,?,?,?)
        ''', (user_id, username, first_name, date, referrer, FREE_CREDITS, date))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_credits(user_id):
    if user_id == OWNER_ID:
        return "∞"
    user = get_user(user_id)
    if not user:
        return 0
    return user[5] or 0

def add_credits(user_id, amount):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_referral_count(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer=?", (user_id,))
    result = c.fetchone()[0] or 0
    conn.close()
    return result

def get_money(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute("SELECT money FROM users WHERE user_id=?", (user_id,))
        r = c.fetchone()
        return r[0] if r else 0
    except Exception:
        return 0
    finally:
        conn.close()

def add_money(user_id, amount):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
    finally:
        conn.close()

def remove_money(user_id, amount):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET money = money - ? WHERE user_id = ? AND money >= ?", (amount, user_id, amount))
        conn.commit()
        return c.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def claim_daily(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        c.execute("SELECT 1 FROM daily_claims WHERE user_id=? AND claim_date=?", (user_id, today))
        if c.fetchone():
            conn.close()
            return False
        c.execute("INSERT INTO daily_claims (user_id, claim_date) VALUES (?,?)", (user_id, today))
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (DAILY_CREDITS, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def save_search_history(user_id, search_type, query, result):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        result_json = json.dumps(result, default=str)[:15000]
        c.execute("INSERT INTO search_history (user_id, search_type, query, search_date, result) VALUES (?,?,?,?,?)",
                  (user_id, search_type, query, timestamp, result_json))
        c.execute("UPDATE users SET total_searches = total_searches + 1, last_active = ? WHERE user_id = ?",
                  (timestamp, user_id))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def save_bomber_history(user_id, number, sms_sent, calls_sent, status):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute(
            "INSERT INTO bomber_history (user_id, target_number, sms_sent, calls_sent, status, started_at, stopped_at) VALUES (?,?,?,?,?,?,?)",
            (user_id, number, sms_sent, calls_sent, status, now, now)
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def get_bomber_history(user_id, limit=10):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute(
            "SELECT target_number, sms_sent, calls_sent, status, started_at FROM bomber_history WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        return c.fetchall()
    except Exception:
        return []
    finally:
        conn.close()

# ==================== ADMIN ====================

def is_admin(user_id):
    if user_id == OWNER_ID:
        return True
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT user_id FROM admins WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

# ==================== BOT ====================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ==================== STATE ====================

user_state = {}
admin_page = {}
bomber_active = {}
paid_bomber_active = {}

# ==================== KEYBOARDS ====================

def main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        ("📱 ɴᴜᴍʙᴇʀ ɪɴꜰᴏ", "👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀ"),
        ("🔍 ᴜꜱᴇʀɴᴀᴍᴇ ɪɴꜰᴏ", "🆔 ᴛɢ ɪᴅ ɪɴꜰᴏ"),
        ("🆔 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ", "📷 ɪɴꜱᴛᴀɢʀᴀᴍ ɪɴꜰᴏ"),
        ("🏦 ɪꜰꜱᴄ ɪɴꜰᴏ", "🚗 ᴠᴇʜɪᴄʟᴇ ɪɴꜰᴏ"),
        ("💼 ɢꜱᴛ ɪɴꜰᴏ", "🪪 ᴩᴀɴ ɪɴꜰᴏ"),
        ("🇵🇰 ᴩᴀᴋ ɴᴜᴍ ɪɴꜰᴏ", "🎮 ꜰʀᴇᴇ ꜰɪʀᴇ ɪɴꜰᴏ"),
        ("📍 ᴩɪɴᴄᴏᴅᴇ ɪɴꜰᴏ", "💳 ᴜᴩɪ ɪɴꜰᴏ"),
        ("💎 ʜɪᴛᴇᴋ-ɴᴜᴍ-ɪɴꜰᴏ 👑", "🌟 ʜɪᴛᴇᴋ-ꜰᴜʟʟ-ɪɴꜰᴏ 👑"),
        ("💣 ʙᴏᴍʙᴇʀ", "🎁 ᴅᴀɪʟʏ ᴄʟᴀɪᴍ"),
        ("💎 ᴩʀᴇᴍɪᴜᴍ", "💰 ʙᴀʟᴀɴᴄᴇ"),
        ("💳 ᴩᴜʀᴄʜᴀꜱᴇ ᴩʀᴇᴍɪᴜᴍ", "👥 ʀᴇꜰᴇʀʀᴀʟꜱ"),
        ("🤖 ᴄʟᴏɴᴇ ʙᴏᴛ", "🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ"),
        ("📢 ᴄʜᴀɴɴᴇʟ", "📋 ᴍʏ ʜɪꜱᴛᴏʀʏ"),
        ("ℹ️ ʜᴇʟᴩ", "🔑 ᴍʏ ᴀᴩɪ ᴋᴇʏꜱ"),
    ]
    if is_admin(user_id):
        buttons.append(("⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ",))
    
    for row in buttons:
        markup.add(*(KeyboardButton(b) for b in row))
    return markup

def admin_keyboard(uid=0):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        ("📊 ᴅᴀꜱʜʙᴏᴀʀᴅ", "📊 ᴄᴀᴄʜᴇ ꜱᴛᴀᴛꜱ"),
        ("👥 ᴜꜱᴇʀ ʟɪꜱᴛ", "📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ"),
        ("🚫 ʙʟᴏᴄᴋ ᴜꜱᴇʀ", "✅ ᴜɴʙʟᴏᴄᴋ ᴜꜱᴇʀ"),
        ("👤 ᴜꜱᴇʀ ɪɴꜰᴏ", "💎 ᴀᴅᴅ ᴩʀᴇᴍɪᴜᴍ"),
        ("🚫 ʀᴇᴍᴏᴠᴇ ᴩʀᴇᴍɪᴜᴍ", "💰 ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ"),
        ("💸 ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ", "⚙️ ꜱᴇᴛ ᴄʀᴇᴅɪᴛꜱ"),
        ("🏠 ᴍᴀɪɴ ᴍᴇɴᴜ", ""),
    ]
    for row in buttons:
        if row[0]:
            markup.add(*(KeyboardButton(b) for b in row if b))
    return markup

# ==================== BOMBER ====================

BOMBER_API = "https://bom3-728immortal.onrender.com/bom?key=felix&num={}"
BOMBER_MAX_SECONDS = 300

def _run_bomber(bot_instance, chat_id, uid, number, status_msg_id, is_premium=False):
    total_sms = 0
    total_calls = 0
    round_num = 0
    start_time = time.time()
    max_time = 999999 if is_premium else BOMBER_MAX_SECONDS
    
    active_dict = paid_bomber_active if is_premium else bomber_active
    active_dict[uid] = number
    
    while True:
        if active_dict.get(uid) != number:
            break
        if time.time() - start_time >= max_time:
            break
        
        round_num += 1
        
        try:
            for _ in range(3):
                try:
                    url = f"{BOMBER_API}{number}"
                    requests.get(url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
                    total_sms += 30
                    total_calls += 10
                except Exception:
                    total_sms += 5
            
            elapsed = int(time.time() - start_time)
            bar = "█" * min(10, int((elapsed / (max_time if max_time < 999999 else 300)) * 10))
            bar += "░" * (10 - len(bar))
            
            try:
                bot_instance.edit_message_text(
                    format_message(
                        f"<b>{'💎' if is_premium else '💣'} ʙᴏᴍʙɪɴɢ...</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📱 ᴛᴀʀɢᴇᴛ: <code>{number}</code>\n"
                        f"⏱️ [{bar}] {elapsed}s / {int(max_time) if max_time < 999999 else '∞'}s\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📨 ꜱᴍꜱ: <code>{total_sms:,}</code>\n"
                        f"📞 ᴄᴀʟʟꜱ: <code>{total_calls:,}</code>\n"
                        f"🔄 ʀᴏᴜɴᴅꜱ: <code>{round_num}</code>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"<i>🛑 ꜱᴛᴏᴩ ʙᴏᴍʙᴇʀ dabao</i>"
                    ),
                    chat_id, status_msg_id, parse_mode='HTML'
                )
            except Exception:
                pass
                
        except Exception:
            pass
        
        time.sleep(0.3)
    
    status_label = "stopped" if active_dict.get(uid) != number else "done"
    save_bomber_history(uid, number, total_sms, total_calls, status_label)
    active_dict.pop(uid, None)
    
    try:
        bot_instance.edit_message_text(
            format_message(
                f"<b>{'💎' if is_premium else '💣'} ʙᴏᴍʙᴇʀ {'ꜱᴛᴏᴩᴩᴇᴅ' if status_label == 'stopped' else 'ᴄᴏᴍᴩʟᴇᴛᴇᴅ'}</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📱 ᴛᴀʀɢᴇᴛ: <code>{number}</code>\n"
                f"📨 ꜱᴍꜱ: <code>{total_sms:,}</code>\n"
                f"📞 ᴄᴀʟʟꜱ: <code>{total_calls:,}</code>\n"
                f"⏱️ ᴛɪᴍᴇ: <code>{int(time.time() - start_time)}s</code>\n"
            ),
            chat_id, status_msg_id, parse_mode='HTML'
        )
    except Exception:
        pass

# ==================== BOT HANDLERS ====================

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    uname = message.from_user.username or ""
    fname = message.from_user.first_name or "User"
    
    ref = None
    if len(message.text.split()) > 1:
        try:
            ref = int(message.text.split()[1])
            if ref == uid:
                ref = None
        except Exception:
            pass
    
    if not get_user(uid):
        add_user(uid, uname, fname, ref)
    
    text = f"👋 <b>Welcome</b> <code>{_esc(fname)}</code>!\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>\n🤖 <b>Made by:</b> @Guptaji_302"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "🔙 ᴍᴀɪɴ ᴍᴇɴᴜ" and not is_group(m))
def menu_btn(m):
    uid = m.from_user.id
    user_state.pop(uid, None)
    text = f"👋 <b>Menu</b>\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ" and is_admin(m.from_user.id) and not is_group(m))
def admin_panel(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    bot.send_message(uid, format_message("<b>⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ</b>"), reply_markup=admin_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "📊 ᴄᴀᴄʜᴇ ꜱᴛᴀᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def cache_stats_btn(m):
    stats = cache_get_all_stats()
    text = "<b>📊 ᴄᴀᴄʜᴇ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ</b>\n━━━━━━━━━━━━━━━━━━\n"
    total_items = 0
    total_hits = 0
    for table, data in stats.items():
        text += f"📌 <b>{table.upper()}</b>: {data['count']} items | {data['hits']} hits\n"
        total_items += data['count']
        total_hits += data['hits']
    text += f"\n━━━━━━━━━━━━━━━━━━\n📦 <b>Total Items:</b> {total_items}\n🎯 <b>Total Hits:</b> {total_hits}"
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== FEATURE HANDLERS ====================

@bot.message_handler(func=lambda m: m.text == "📱 ɴᴜᴍʙᴇʀ ɪɴꜰᴏ" and not is_group(m))
def number_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_number"
    bot.reply_to(m, format_message("<b>📱 Send mobile number:</b>\nExample: <code>9876543210</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🆔 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ" and not is_group(m))
def aadhar_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_aadhar"
    bot.reply_to(m, format_message("<b>🪪 Send 12-digit Aadhar:</b>\nExample: <code>327567544017</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💳 ᴜᴩɪ ɪɴꜰᴏ" and not is_group(m))
def upi_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_upi"
    bot.reply_to(m, format_message("<b>💳 Send UPI ID:</b>\nExample: <code>example@ybl</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "📷 ɪɴꜱᴛᴀɢʀᴀᴍ ɪɴꜰᴏ" and not is_group(m))
def instagram_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_instagram"
    bot.reply_to(m, format_message("<b>📷 Send Instagram username:</b>\nExample: <code>instagram</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🏦 ɪꜰꜱᴄ ɪɴꜰᴏ" and not is_group(m))
def ifsc_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_ifsc"
    bot.reply_to(m, format_message("<b>🏦 Send IFSC code:</b>\nExample: <code>SBIN0001234</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🚗 ᴠᴇʜɪᴄʟᴇ ɪɴꜰᴏ" and not is_group(m))
def vehicle_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_vehicle"
    bot.reply_to(m, format_message("<b>🚗 Send RC number:</b>\nExample: <code>MH12AB1234</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💼 ɢꜱᴛ ɪɴꜰᴏ" and not is_group(m))
def gst_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_gst"
    bot.reply_to(m, format_message("<b>💼 Send GST number:</b>\nExample: <code>10DJCPK4351Q1Z5</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🪪 ᴩᴀɴ ɪɴꜰᴏ" and not is_group(m))
def pan_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_pan"
    bot.reply_to(m, format_message("<b>🪪 Send PAN number:</b>\nExample: <code>AAMTS3432L</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🇵🇰 ᴩᴀᴋ ɴᴜᴍ ɪɴꜰᴏ" and not is_group(m))
def pak_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_pak"
    bot.reply_to(m, format_message("<b>🇵🇰 Send Pakistan number:</b>\nExample: <code>03001234567</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "📍 ᴩɪɴᴄᴏᴅᴇ ɪɴꜰᴏ" and not is_group(m))
def pincode_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_pincode"
    bot.reply_to(m, format_message("<b>📍 Send 6-digit pincode:</b>\nExample: <code>110001</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🎮 ꜰʀᴇᴇ ꜰɪʀᴇ ɪɴꜰᴏ" and not is_group(m))
def ff_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_ff"
    bot.reply_to(m, format_message("<b>🎮 Send Free Fire UID:</b>\nExample: <code>1234567890</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💎 ʜɪᴛᴇᴋ-ɴᴜᴍ-ɪɴꜰᴏ 👑" and not is_group(m))
def hitek_num_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_hitek_num"
    bot.reply_to(m, format_message("<b>💎 Send number for Hitek:</b>\nExample: <code>9876543210</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🌟 ʜɪᴛᴇᴋ-ꜰᴜʟʟ-ɪɴꜰᴏ 👑" and not is_group(m))
def hitek_full_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_hitek_full"
    bot.reply_to(m, format_message("<b>🌟 Send query for Hitek Full:</b>\nExample: <code>Rahul Kumar</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀ" and not is_group(m))
def select_user_btn(m):
    uid = m.from_user.id
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("👤 Select User", request_users=KeyboardButtonRequestUser(request_id=1, user_is_bot=False)))
        markup.add(KeyboardButton("🔙 Main Menu"))
        bot.send_message(uid, format_message("<b>👤 Click 'Select User' button:</b>"), reply_markup=markup, parse_mode='HTML')
    except Exception:
        bot.send_message(uid, format_message("<b>❌ Use /userid command instead.</b>"), parse_mode='HTML')

@bot.message_handler(content_types=['users_shared'])
def handle_user_shared(message):
    uid = message.from_user.id
    if not message.users_shared or not message.users_shared.user_ids:
        return
    
    raw_user_id = message.users_shared.user_ids[0]
    status = bot.reply_to(message, format_message("<b>⏳ Searching...</b>"), parse_mode='HTML')
    
    try:
        chat = bot.get_chat(raw_user_id)
        result = {
            'success': True,
            'data': [{
                'user_id': chat.id,
                'username': chat.username or '',
                'first_name': chat.first_name or '',
                'last_name': chat.last_name or '',
                'bio': getattr(chat, 'bio', '') or ''
            }]
        }
        formatted = format_generic_result(result, "👤 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗨𝗦𝗘𝗥", "🆔 ID", raw_user_id)
        bot.edit_message_text(formatted, message.chat.id, status.message_id, parse_mode='HTML')
        save_search_history(uid, 'selected_userid', str(raw_user_id), result)
    except Exception as e:
        bot.edit_message_text(format_message(f"<b>❌ Error: {e}</b>"), message.chat.id, status.message_id, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🔍 ᴜꜱᴇʀɴᴀᴍᴇ ɪɴꜰᴏ" and not is_group(m))
def username_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_username"
    bot.reply_to(m, format_message("<b>🔍 Send Telegram username with @:</b>\nExample: <code>@username</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🆔 ᴛɢ ɪᴅ ɪɴꜰᴏ" and not is_group(m))
def userid_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_userid"
    bot.reply_to(m, format_message("<b>🆔 Send Telegram User ID:</b>\nExample: <code>6443754454</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💰 ʙᴀʟᴀɴᴄᴇ" and not is_group(m))
def balance_btn(m):
    uid = m.from_user.id
    credits = get_credits(uid)
    refs = get_referral_count(uid)
    money = get_money(uid)
    text = f"""
<b>💰 ʙᴀʟᴀɴᴄᴇ</b>
<b>₹ ᴍᴏɴᴇʏ:</b> <code>₹{money}</code>
<b>💎 ᴄʀᴇᴅɪᴛꜱ:</b> <code>{credits}</code>
<b>👥 ʀᴇꜰᴇʀʀᴀʟꜱ:</b> <code>{refs}</code>
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🎁 ᴅᴀɪʟʏ ᴄʟᴀɪᴍ" and not is_group(m))
def daily_btn(m):
    uid = m.from_user.id
    if claim_daily(uid):
        credits = get_credits(uid)
        bot.reply_to(m, format_message(f"<b>✅ +{DAILY_CREDITS} credits!</b>\n💰 Total: <code>{credits}</code>"), parse_mode='HTML')
    else:
        bot.reply_to(m, format_message("<b>❌ Already claimed!</b>\n⏳ Come back tomorrow."), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "👥 ʀᴇꜰᴇʀʀᴀʟꜱ" and not is_group(m))
def referral_btn(m):
    uid = m.from_user.id
    count = get_referral_count(uid)
    link = f"https://t.me/{bot.get_me().username}?start={uid}"
    credits = get_credits(uid)
    text = f"""
<b>👥 ʀᴇꜰᴇʀʀᴀʟꜱ</b>
<b>📊 Total:</b> <code>{count}</code>
<b>🔗 Your Link:</b>
<code>{link}</code>
<b>🎁 Per Referral:</b> <code>+{REFERRAL_CREDITS}</code>
<b>💰 Your Credits:</b> <code>{credits}</code>
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ" and not is_group(m))
def redeem_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_redeem"
    bot.reply_to(m, format_message("<b>🎫 Send redeem code:</b>\nExample: <code>OSINT-ABCD</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💎 ᴩʀᴇᴍɪᴜᴍ" and not is_group(m))
def premium_btn(m):
    uid = m.from_user.id
    user = get_user(uid)
    is_prem = False
    if user and user[7] == 1 and user[8]:
        try:
            until = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
            if until > datetime.now():
                is_prem = True
        except Exception:
            pass
    
    if is_prem:
        text = f"<b>💎 Premium Active!</b>\n⏳ Expires: <code>{user[8][:10]}</code>"
    else:
        text = """
<b>💎 ᴩʀᴇᴍɪᴜᴍ</b>
━━━━━━━━━━━━━━━━━━
✨ Unlimited Searches
✨ No Credit Cost
✨ Unlimited Bomber Time
✨ All Features Unlocked

💳 Contact: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== PURCHASE PREMIUM ====================

PREMIUM_PLANS = [(30, 499), (15, 280), (7, 150), (1, 40)]

@bot.message_handler(func=lambda m: m.text == "💳 ᴩᴜʀᴄʜᴀꜱᴇ ᴩʀᴇᴍɪᴜᴍ" and not is_group(m))
def purchase_premium_btn(m):
    uid = m.from_user.id
    money = get_money(uid)
    
    markup = InlineKeyboardMarkup()
    plan_labels = {30: "1 Month", 15: "15 Days", 7: "7 Days", 1: "1 Day"}
    for days, price in PREMIUM_PLANS:
        markup.add(InlineKeyboardButton(f"📅 {plan_labels.get(days, days)} — ₹{price}", callback_data=f"buy_prem_{days}_{price}"))
    
    text = f"""
<b>💳 ᴩᴜʀᴄʜᴀꜱᴇ ᴩʀᴇᴍɪᴜᴍ</b>
━━━━━━━━━━━━━━━━━━
₹ ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ: <b>₹{money}</b>

<b>🛒 ꜱᴇʟᴇᴄᴛ ᴀ ᴩʟᴀɴ:</b>
"""
    bot.reply_to(m, format_message(text), reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_prem_"))
def cb_buy_premium(c):
    uid = c.from_user.id
    parts = c.data.split("_")
    try:
        days = int(parts[2])
        price = int(parts[3])
    except Exception:
        bot.answer_callback_query(c.id, "❌ Error!")
        return
    
    money = get_money(uid)
    if money < price:
        needed = price - money
        bot.answer_callback_query(c.id, f"❌ ₹{needed} aur chahiye!", show_alert=True)
        return
    
    user = get_user(uid)
    now_dt = datetime.now()
    start_from = now_dt
    if user and user[7] == 1 and user[8]:
        try:
            existing = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
            if existing > now_dt:
                start_from = existing
        except Exception:
            pass
    
    remove_money(uid, price)
    until = start_from + timedelta(days=days)
    until_str = until.strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('bot.db', timeout=5)
    c_cur = conn.cursor()
    c_cur.execute("UPDATE users SET is_premium=1, premium_until=? WHERE user_id=?", (until_str, uid))
    conn.commit()
    conn.close()
    
    new_money = get_money(uid)
    plan_names = {30: "1 Month", 15: "15 Days", 7: "7 Days", 1: "1 Day"}
    plan_name = plan_names.get(days, f"{days} Days")
    
    bot.edit_message_text(
        format_message(
            f"<b>✅ Premium Activated!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📅 Plan: {plan_name}\n"
            f"⏳ Expires: <code>{until_str}</code>\n"
            f"₹ Remaining: <code>₹{new_money}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✨ Enjoy Unlimited Features! 🎉"
        ),
        c.message.chat.id, c.message.message_id, parse_mode='HTML'
    )
    bot.answer_callback_query(c.id, f"✅ Premium for {days} days!")

# ==================== CLONE BOT ====================

CLONE_BOT_REFERRALS_NEEDED = 20

@bot.message_handler(func=lambda m: m.text == "🤖 ᴄʟᴏɴᴇ ʙᴏᴛ" and not is_group(m))
def clonebot_btn(m):
    uid = m.from_user.id
    refs = get_referral_count(uid)
    
    if is_admin(uid):
        refs = CLONE_BOT_REFERRALS_NEEDED
    
    if refs < CLONE_BOT_REFERRALS_NEEDED:
        needed = CLONE_BOT_REFERRALS_NEEDED - refs
        bar_done = int((refs / CLONE_BOT_REFERRALS_NEEDED) * 10)
        bar = "█" * bar_done + "░" * (10 - bar_done)
        text = f"""
<b>🤖 Clone Bot</b>
━━━━━━━━━━━━━━━━━━
📊 Progress: [{bar}] {refs}/{CLONE_BOT_REFERRALS_NEEDED}
❌ Still needed: <b>{needed} more referrals</b>

👥 Refer karo aur apna bot pao! 🎉
"""
        bot.reply_to(m, format_message(text), parse_mode='HTML')
        return
    
    text = f"""
<b>🤖 Clone Bot</b>
━━━━━━━━━━━━━━━━━━
✅ Congratulations! {refs} referrals complete!

📝 Apna <b>Bot Token</b> bhejo:
1️⃣ @BotFather pe jao
2️⃣ /newbot command use karo
3️⃣ Bot banao aur token copy karo
4️⃣ Token yahan paste karo

<i>Example: 1234567890:ABCdef...</i>
"""
    msg = bot.reply_to(m, format_message(text), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_clone_token)

def process_clone_token(m):
    uid = m.from_user.id
    token = m.text.strip() if m.text else ''
    
    if not token or ':' not in token or len(token) < 30:
        bot.send_message(uid, format_message("<b>❌ Invalid token!</b>"), parse_mode='HTML')
        return
    
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO clone_bots (user_id, token, status, requested_at) VALUES (?,?,?,?)",
            (uid, token, 'pending', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        bot.send_message(uid, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')
        return
    
    bot.send_message(uid, format_message(
        "<b>✅ Clone request sent!</b>\n"
        "Admin approve karte hi bot start ho jayega!"
    ), parse_mode='HTML')

# ==================== MY HISTORY ====================

@bot.message_handler(func=lambda m: m.text == "📋 ᴍʏ ʜɪꜱᴛᴏʀʏ" and not is_group(m))
def my_history_btn(m):
    uid = m.from_user.id
    
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        searches = c.execute("SELECT search_type, query, search_date FROM search_history WHERE user_id=? ORDER BY search_date DESC LIMIT 5", (uid,)).fetchall()
        bomber = c.execute("SELECT target_number, sms_sent, calls_sent, status, started_at FROM bomber_history WHERE user_id=? ORDER BY id DESC LIMIT 3", (uid,)).fetchall()
        total_searches = c.execute("SELECT COUNT(*) FROM search_history WHERE user_id=?", (uid,)).fetchone()[0]
    except Exception:
        searches = []
        bomber = []
        total_searches = 0
    finally:
        conn.close()
    
    text = f"<b>📋 My History</b>\n━━━━━━━━━━━━━━━━━━\n📊 Total Searches: <code>{total_searches}</code>\n━━━━━━━━━━━━━━━━━━\n"
    
    if searches:
        text += "<b>🔍 Recent Searches:</b>\n"
        for stype, query, sdate in searches:
            icon = '📱' if 'number' in stype else '🆔' if 'aadhar' in stype else '📷' if 'instagram' in stype else '🔍'
            text += f"{icon} <code>{query[:20]}</code> | {sdate[:10]}\n"
    else:
        text += "<i>No search history</i>\n"
    
    if bomber:
        text += "\n<b>💣 Recent Bombs:</b>\n"
        for num, sms, calls, status, started in bomber:
            icon = '✅' if status == 'done' else '🛑'
            text += f"{icon} <code>{num}</code> | SMS:{sms} Calls:{calls}\n"
    
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== MY API KEYS ====================

@bot.message_handler(func=lambda m: m.text == "🔑 ᴍʏ ᴀᴩɪ ᴋᴇʏꜱ" and not is_group(m))
def my_api_keys_btn(m):
    uid = m.from_user.id
    text = f"""
<b>🔑 My API Keys</b>
━━━━━━━━━━━━━━━━━━
💡 API keys generate karne ke liye admin se contact karo.
📌 Contact: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== BOMBER ====================

@bot.message_handler(func=lambda m: m.text == "💣 ʙᴏᴍʙᴇʀ" and not is_group(m))
def bomber_menu_btn(m):
    uid = m.from_user.id
    
    user = get_user(uid)
    is_prem = False
    if user and user[7] == 1 and user[8]:
        try:
            until = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
            if until > datetime.now():
                is_prem = True
        except Exception:
            pass
    if uid == OWNER_ID:
        is_prem = True
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("💣 ꜰʀᴇᴇ ʙᴏᴍʙᴇʀ"),
        KeyboardButton("💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ" if is_prem else "💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ 🔒")
    )
    markup.add(
        KeyboardButton("🛑 ꜱᴛᴏᴩ ʙᴏᴍʙᴇʀ"),
        KeyboardButton("📜 ʙᴏᴍʙᴇʀ ʜɪꜱᴛᴏʀʏ")
    )
    markup.add(KeyboardButton("🔙 ᴍᴀɪɴ ᴍᴇɴᴜ"))
    
    status = ""
    if bomber_active.get(uid):
        status = "\n🟢 Active: Free bomber running"
    if paid_bomber_active.get(uid):
        status = "\n💎 Active: Paid bomber running"
    
    bot.reply_to(m, format_message(
        f"<b>💣 Bomber Menu</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💣 Free Bomber — 150 SMS/sec + 50 Calls/sec (5 min)\n"
        f"💎 Paid Bomber — Unlimited time (Premium only)\n"
        f"{status}"
    ), reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💣 ꜰʀᴇᴇ ʙᴏᴍʙᴇʀ" and not is_group(m))
def free_bomber_btn(m):
    uid = m.from_user.id
    
    if bomber_active.get(uid):
        bot.reply_to(m, format_message("<b>⚠️ Already running! Stop first.</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = "waiting_bomber_free"
    bot.reply_to(m, format_message(
        "<b>💣 Free Bomber</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 Target number bhejo:\n"
        "<i>Example: 9876543210</i>\n\n"
        "⚡ Speed: 150 SMS/sec + 50 Calls/sec\n"
        "⏱️ Max: 5 minutes\n"
        "⚠️ <b>Sirf apna number!</b>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ" and not is_group(m))
def paid_bomber_btn(m):
    uid = m.from_user.id
    
    user = get_user(uid)
    is_prem = False
    if user and user[7] == 1 and user[8]:
        try:
            until = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
            if until > datetime.now():
                is_prem = True
        except Exception:
            pass
    if uid == OWNER_ID:
        is_prem = True
    
    if not is_prem:
        bot.reply_to(m, format_message(
            "<b>💎 Premium Required!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Paid Bomber sirf Premium users ke liye!\n"
            "💳 Purchase Premium button use karo."
        ), parse_mode='HTML')
        return
    
    if paid_bomber_active.get(uid):
        bot.reply_to(m, format_message("<b>⚠️ Already running! Stop first.</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = "waiting_bomber_paid"
    bot.reply_to(m, format_message(
        "<b>💎 Paid Bomber</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 Target number bhejo:\n"
        "<i>Example: 9876543210</i>\n\n"
        "⚡ Speed: 150 SMS/sec + 50 Calls/sec\n"
        "⏱️ Max: Unlimited (Premium)\n"
        "⚠️ <b>Sirf apna number!</b>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🛑 ꜱᴛᴏᴩ ʙᴏᴍʙᴇʀ" and not is_group(m))
def stop_bomber_btn(m):
    uid = m.from_user.id
    
    stopped = False
    if bomber_active.get(uid):
        bomber_active.pop(uid, None)
        stopped = True
    if paid_bomber_active.get(uid):
        paid_bomber_active.pop(uid, None)
        stopped = True
    
    if stopped:
        bot.reply_to(m, format_message("<b>🛑 Bomber stopped!</b>"), parse_mode='HTML')
    else:
        bot.reply_to(m, format_message("<b>ℹ️ No active bomber!</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "📜 ʙᴏᴍʙᴇʀ ʜɪꜱᴛᴏʀʏ" and not is_group(m))
def bomber_history_btn(m):
    uid = m.from_user.id
    rows = get_bomber_history(uid, 10)
    
    if not rows:
        bot.reply_to(m, format_message("<b>📜 No bombing history yet!</b>"), parse_mode='HTML')
        return
    
    text = "<b>📜 Bomber History</b>\n━━━━━━━━━━━━━━━━━━\n"
    for num, sms, calls, status, started in rows:
        icon = "✅" if status == "done" else "🛑"
        text += f"{icon} <code>{num}</code> | SMS:{sms} Calls:{calls} | {started[:10]}\n"
    
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== HELP ====================

@bot.message_handler(func=lambda m: m.text == "ℹ️ ʜᴇʟᴩ" and not is_group(m))
def help_btn(m):
    text = """
<b>ℹ️ Help & Guide</b>
━━━━━━━━━━━━━━━━━━
📱 Number Info — Mobile owner, operator
🆔 Aadhar Info — 12-digit Aadhar details
💳 UPI Info — UPI ID details
📷 Instagram Info — Username info
🏦 IFSC Info — Bank branch details
🚗 Vehicle Info — RC number details
💼 GST Info — GST number details
🪪 PAN Info — PAN card details
🇵🇰 Pak Num Info — Pakistan number
📍 Pincode Info — 6-digit pincode
🎮 Free Fire Info — FF UID details
🔍 Username Info — Telegram username
🆔 TG ID Info — Telegram numeric ID
💎 Hitek Num — Advanced number lookup
🌟 Hitek Full — Deep search
💣 Bomber — 150 SMS/sec + 50 Calls/sec

💰 Credits: Daily claim + Referrals
💎 Premium: Unlimited access + Unlimited Bomber
💾 Cache: All searches saved for future

👑 Made by: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== TEXT INPUT ====================

def is_group(message):
    return message.chat.type in ['group', 'supergroup']

@bot.message_handler(func=lambda m: m.from_user and m.from_user.id in user_state and not is_group(m))
def handle_text_input(m):
    uid = m.from_user.id
    state = user_state[uid]
    text = m.text.strip()
    
    if not text:
        return
    
    # ========== NUMBER ==========
    if state == "waiting_number":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number! Send 10-digit.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_number_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_number_info_bold(result, clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'number', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== AADHAR ==========
    elif state == "waiting_aadhar":
        clean = re.sub(r'\s+', '', text)
        if not re.match(r'^\d{12}$', clean):
            bot.reply_to(m, format_message("<b>❌ Invalid Aadhar! 12 digits.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_aadhar_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_aadhar_result_bold(result, clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'aadhar', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== UPI ==========
    elif state == "waiting_upi":
        if '@' not in text:
            bot.reply_to(m, format_message("<b>❌ Invalid UPI ID! Must contain @</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_upi_info(text)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_upi_result_bold(result, text)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'upi', text, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== INSTAGRAM ==========
    elif state == "waiting_instagram":
        clean = text.replace('@', '').strip()
        if len(clean) < 2:
            bot.reply_to(m, format_message("<b>❌ Invalid username!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching Instagram...</b>"), parse_mode='HTML')
        result = get_instagram_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "📷 Instagram Info", "👤 Username", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'instagram', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== IFSC ==========
    elif state == "waiting_ifsc":
        clean = text.upper().strip()
        if len(clean) != 11:
            bot.reply_to(m, format_message("<b>❌ Invalid IFSC! 11 characters.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_ifsc_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🏦 IFSC Info", "🏦 IFSC", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'ifsc', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== VEHICLE ==========
    elif state == "waiting_vehicle":
        clean = re.sub(r'\s+', '', text).upper()
        if len(clean) < 8:
            bot.reply_to(m, format_message("<b>❌ Invalid RC number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_vehicle_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🚗 Vehicle Info", "🚗 RC", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'vehicle', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== GST ==========
    elif state == "waiting_gst":
        clean = text.upper().strip()
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid GST number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_gst_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "💼 GST Info", "💼 GST", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'gst', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== PAN ==========
    elif state == "waiting_pan":
        clean = text.upper().strip()
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', clean):
            bot.reply_to(m, format_message("<b>❌ Invalid PAN! Format: ABCDE1234F</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pan_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🪪 PAN Info", "🪪 PAN", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pan', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== PAK NUM ==========
    elif state == "waiting_pak":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid Pakistan number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pak_num_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🇵🇰 Pak Number Info", "🇵🇰 Number", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pak_num', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== PINCODE ==========
    elif state == "waiting_pincode":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) != 6:
            bot.reply_to(m, format_message("<b>❌ Invalid pincode! 6 digits.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pincode_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "📍 Pincode Info", "📍 Pincode", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pincode', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== FREE FIRE ==========
    elif state == "waiting_ff":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 5:
            bot.reply_to(m, format_message("<b>❌ Invalid Free Fire UID!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_ff_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🎮 Free Fire Info", "🎮 UID", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'ff', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== HITEK NUM ==========
    elif state == "waiting_hitek_num":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>💎 Searching Hitek...</b>"), parse_mode='HTML')
        result = get_hitek_num_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "💎 Hitek Num Info", "📱 Number", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'hitek_num', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== HITEK FULL ==========
    elif state == "waiting_hitek_full":
        if len(text) < 2:
            bot.reply_to(m, format_message("<b>❌ Invalid query! Min 2 chars.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🌟 Searching Hitek Full...</b>"), parse_mode='HTML')
        result = get_hitek_full_info(text)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🌟 Hitek Full Info", "🔍 Query", text)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'hitek_full', text, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    # ========== TELEGRAM USERNAME ==========
    elif state == "waiting_username":
        clean = text.replace('@', '').strip()
        if len(clean) < 2:
            bot.reply_to(m, format_message("<b>❌ Invalid username!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        try:
            chat = bot.get_chat(f"@{clean}")
            photo_file_id = None
            try:
                photos = bot.get_user_profile_photos(chat.id, limit=1)
                if photos and photos.photos:
                    photo_file_id = photos.photos[0][-1].file_id
            except Exception:
                pass
            
            result = {
                'success': True,
                'data': [{
                    'user_id': chat.id,
                    'username': chat.username or clean,
                    'first_name': chat.first_name or '',
                    'last_name': chat.last_name or '',
                    'full_name': f"{chat.first_name or ''} {chat.last_name or ''}".strip(),
                    'bio': getattr(chat, 'bio', '') or '',
                }]
            }
            
            formatted = format_generic_result(result, "🔍 Username Info", "👤 Username", f"@{clean}")
            user_state.pop(uid, None)
            
            try:
                bot.delete_message(m.chat.id, status.message_id)
                if photo_file_id:
                    bot.send_photo(m.chat.id, photo_file_id, caption=formatted, parse_mode='HTML')
                else:
                    bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            
            save_search_history(uid, 'username', clean, result)
            
        except Exception as e:
            bot.edit_message_text(
                format_message(f"<b>❌ User not found: @{clean}</b>\n\n"
                              "💡 Try:\n• Check spelling\n• Use /userid with numeric ID"),
                m.chat.id, status.message_id, parse_mode='HTML'
            )
            user_state.pop(uid, None)
    
    # ========== TELEGRAM USER ID ==========
    elif state == "waiting_userid":
        clean = re.sub(r'[^\d]', '', text)
        if not clean:
            bot.reply_to(m, format_message("<b>❌ Invalid User ID! Numeric only.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        try:
            user_id = int(clean)
            chat = bot.get_chat(user_id)
            
            photo_file_id = None
            try:
                photos = bot.get_user_profile_photos(user_id, limit=1)
                if photos and photos.photos:
                    photo_file_id = photos.photos[0][-1].file_id
            except Exception:
                pass
            
            result = {
                'success': True,
                'data': [{
                    'user_id': chat.id,
                    'username': chat.username or '',
                    'first_name': chat.first_name or '',
                    'last_name': chat.last_name or '',
                    'full_name': f"{chat.first_name or ''} {chat.last_name or ''}".strip(),
                    'bio': getattr(chat, 'bio', '') or '',
                }]
            }
            
            formatted = format_generic_result(result, "🆔 TG ID Info", "🆔 ID", clean)
            user_state.pop(uid, None)
            
            try:
                bot.delete_message(m.chat.id, status.message_id)
                if photo_file_id:
                    bot.send_photo(m.chat.id, photo_file_id, caption=formatted, parse_mode='HTML')
                else:
                    bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            
            save_search_history(uid, 'userid', clean, result)
            
        except Exception as e:
            bot.edit_message_text(
                format_message(f"<b>❌ User not found: {clean}</b>\n\n"
                              "💡 Try:\n• Use /username with @username\n• Check if user exists"),
                m.chat.id, status.message_id, parse_mode='HTML'
            )
            user_state.pop(uid, None)
    
    # ========== FREE BOMBER ==========
    elif state == "waiting_bomber_free":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        if bomber_active.get(uid):
            bot.reply_to(m, format_message("<b>⚠️ Already running!</b>"), parse_mode='HTML')
            user_state.pop(uid, None)
            return
        
        user_state.pop(uid, None)
        status_msg = bot.send_message(m.chat.id, format_message(
            f"<b>💣 Starting bomber...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ 150 SMS/sec + 50 Calls/sec\n"
            f"⏱️ Max: 5 minutes"
        ), parse_mode='HTML')
        
        threading.Thread(
            target=_run_bomber,
            args=(bot, m.chat.id, uid, clean, status_msg.message_id, False),
            daemon=True
        ).start()
    
    # ========== PAID BOMBER ==========
    elif state == "waiting_bomber_paid":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        if paid_bomber_active.get(uid):
            bot.reply_to(m, format_message("<b>⚠️ Already running!</b>"), parse_mode='HTML')
            user_state.pop(uid, None)
            return
        
        user_state.pop(uid, None)
        status_msg = bot.send_message(m.chat.id, format_message(
            f"<b>💎 Paid bomber starting...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ 150 SMS/sec + 50 Calls/sec\n"
            f"⏱️ Max: Unlimited (Premium)"
        ), parse_mode='HTML')
        
        threading.Thread(
            target=_run_bomber,
            args=(bot, m.chat.id, uid, clean, status_msg.message_id, True),
            daemon=True
        ).start()
    
    # ========== REDEEM ==========
    elif state == "waiting_redeem":
        code = text.upper().strip()
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        try:
            c.execute("SELECT credits, max_uses, used_count, expires_at FROM redeem_codes WHERE code = ? AND is_active = 1", (code,))
            row = c.fetchone()
            if row:
                credits, max_uses, used_count, expires_at = row
                if used_count >= max_uses:
                    bot.reply_to(m, format_message("<b>❌ Code fully used!</b>"), parse_mode='HTML')
                elif expires_at and datetime.now() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S"):
                    bot.reply_to(m, format_message("<b>❌ Code expired!</b>"), parse_mode='HTML')
                else:
                    c.execute("UPDATE redeem_codes SET used_count = used_count + 1 WHERE code = ?", (code,))
                    c.execute("INSERT OR IGNORE INTO redeemed_users (user_id, code, redeemed_at) VALUES (?, ?, ?)",
                              (uid, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    add_credits(uid, credits)
                    conn.commit()
                    bot.reply_to(m, format_message(f"<b>✅ +{credits} credits!</b>\n💰 Total: <code>{get_credits(uid)}</code>"), parse_mode='HTML')
            else:
                bot.reply_to(m, format_message("<b>❌ Invalid code!</b>"), parse_mode='HTML')
        except Exception as e:
            bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')
        finally:
            conn.close()
            user_state.pop(uid, None)
    
    else:
        user_state.pop(uid, None)

# ==================== MAIN ====================

def main():
    print("=" * 60)
    print("🔥 CACHED OSINT BOT STARTING...")
    print("=" * 60)
    
    init_db()
    
    web_thread = threading.Thread(target=run_web, daemon=True, name="flask")
    web_thread.start()
    time.sleep(1)
    print("✅ Flask web server started on port 10000")
    
    print(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
    print(f"✅ Owner ID: {OWNER_ID}")
    print(f"✅ Made by: @Guptaji_302")
    print("=" * 60)
    
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=30)
    except Exception as e:
        print(f"❌ Polling error: {e}")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()
