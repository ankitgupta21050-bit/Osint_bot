"""
╔══════════════════════════════════════════════════════════════════╗
║         🔥 OSINT BOT — COMPLETE WORKING VERSION 🔥              ║
║         All Features Working + Free APIs + Dynamic Config       ║
║         Made by: @Guptaji_302                                   ║
║         Powered by: NITIN API + Free APIs                      ║
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
import string
import html as _html
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import platform
import psutil
import signal as _signal

# ==================== TELEGRAM BOT IMPORTS ====================
try:
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser, BotCommand,
        ChatMemberUpdated, CallbackQuery, Message
    )
except ImportError:
    os.system("pip install pyTelegramBotAPI==4.22.0")
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser, BotCommand,
        ChatMemberUpdated, CallbackQuery, Message
    )

# ==================== FLASK WEB SERVER ====================
from flask import Flask, request as flask_request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "Bot is running ✅ | Made by @Guptaji_302", 200

@app.route('/health')
def health():
    try:
        db_size = os.path.getsize('bot.db') // 1024 if os.path.exists('bot.db') else 0
        return f"OK | DB:{db_size}KB | Users:{get_user_count()} | Admins:{get_admin_count()}", 200
    except Exception:
        return "OK", 200

@app.route('/backup-now')
def backup_now():
    try:
        ok = github_upload_db()
        return ("Backup SUCCESS!" if ok else "Backup FAILED!"), (200 if ok else 500)
    except Exception as e:
        return f"Error: {e}", 500

def run_web():
    app.run(host='0.0.0.0', port=10000, use_reloader=False, threaded=True)

# ==================== ENVIRONMENT VARIABLES ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN environment variable set nahi hai!")
    print("   Render > Environment Variables mein BOT_TOKEN add karo!")
    sys.exit(1)

try:
    OWNER_ID = int(os.environ.get("OWNER_ID", "7545664963"))
except ValueError:
    OWNER_ID = 7545664963

DB_CHANNEL = os.environ.get("DB_CHANNEL", "")
LOGS_CHANNEL = os.environ.get("LOGS_CHANNEL", "")
GITHUB_TOKEN = os.environ.get("GH_TOKEN", "")
GITHUB_REPO = os.environ.get("GH_REPO", "")
GITHUB_DB_PATH = os.environ.get("GH_DB_PATH", "database.db")

FREE_CREDITS = 5
DAILY_CREDITS = 1
REFERRAL_CREDITS = 1
BOT_CREDIT = "⚡ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ : @Guptaji_302"

# ==================== DATABASE FUNCTIONS ====================
def init_db():
    """Initialize database with all tables"""
    global conn, c
    conn = sqlite3.connect('bot.db', check_same_thread=False, timeout=30)
    c = conn.cursor()
    
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
    except Exception:
        pass
    
    c.executescript('''
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
        
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            added_by INTEGER,
            added_date TEXT,
            is_owner INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer INTEGER,
            referred INTEGER,
            date TEXT
        );
        
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            search_type TEXT,
            query TEXT,
            search_date TEXT,
            result TEXT
        );
        
        CREATE TABLE IF NOT EXISTS daily_claims (
            user_id INTEGER,
            claim_date TEXT,
            PRIMARY KEY (user_id, claim_date)
        );
        
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
        
        CREATE TABLE IF NOT EXISTS redeemed_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT,
            redeemed_at TEXT
        );
        
        CREATE TABLE IF NOT EXISTS force_join_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            username TEXT,
            added_by INTEGER,
            added_date TEXT,
            channel_type TEXT DEFAULT 'channel'
        );
        
        CREATE TABLE IF NOT EXISTS bot_groups (
            group_id INTEGER PRIMARY KEY,
            group_title TEXT,
            number_info_enabled INTEGER DEFAULT 1,
            userid_info_enabled INTEGER DEFAULT 1,
            username_info_enabled INTEGER DEFAULT 1,
            aadhar_info_enabled INTEGER DEFAULT 1,
            instagram_info_enabled INTEGER DEFAULT 1,
            ifsc_info_enabled INTEGER DEFAULT 1,
            vehicle_info_enabled INTEGER DEFAULT 1,
            welcome_enabled INTEGER DEFAULT 1,
            welcome_message TEXT,
            welcome_rules TEXT DEFAULT '',
            goodbye_enabled INTEGER DEFAULT 1,
            goodbye_message TEXT,
            welcome_photo_file_id TEXT,
            gst_info_enabled INTEGER DEFAULT 1,
            email_info_enabled INTEGER DEFAULT 1,
            pan_info_enabled INTEGER DEFAULT 1,
            pak_num_info_enabled INTEGER DEFAULT 1,
            ff_info_enabled INTEGER DEFAULT 1,
            pincode_info_enabled INTEGER DEFAULT 1,
            hitek_info_enabled INTEGER DEFAULT 1,
            tg_bomber_enabled INTEGER DEFAULT 1,
            bomber_enabled INTEGER DEFAULT 1,
            free_info_mode INTEGER DEFAULT 0,
            added_date TEXT,
            last_active TEXT
        );
        
        CREATE TABLE IF NOT EXISTS feature_costs (
            feature_key TEXT PRIMARY KEY,
            cost INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS feature_maintenance (
            feature_key TEXT PRIMARY KEY,
            is_under_maintenance INTEGER DEFAULT 0,
            reason TEXT DEFAULT '',
            set_by INTEGER DEFAULT 0,
            set_at TEXT DEFAULT ''
        );
        
        CREATE TABLE IF NOT EXISTS welcome_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emoji TEXT DEFAULT '❤️',
            caption TEXT DEFAULT 'ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ʙᴏᴛ!',
            image_file_id TEXT,
            video_file_id TEXT,
            bot_dp_file_id TEXT,
            first_time_sticker TEXT,
            is_default INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            details TEXT,
            timestamp TEXT
        );
        
        CREATE TABLE IF NOT EXISTS clone_bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE,
            status TEXT DEFAULT 'pending',
            requested_at TEXT,
            approved_at TEXT,
            is_manually_stopped INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS clone_admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT,
            admin_user_id INTEGER,
            added_by INTEGER,
            added_date TEXT,
            UNIQUE(clone_token, admin_user_id)
        );
        
        CREATE TABLE IF NOT EXISTS clone_force_join (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT,
            link TEXT,
            username TEXT,
            channel_type TEXT DEFAULT 'channel',
            added_by INTEGER,
            added_date TEXT,
            UNIQUE(clone_token, link)
        );
        
        CREATE TABLE IF NOT EXISTS clone_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT DEFAULT '',
            first_name TEXT DEFAULT '',
            join_date TEXT,
            referrer INTEGER,
            credits INTEGER DEFAULT 10,
            is_blocked INTEGER DEFAULT 0,
            is_premium INTEGER DEFAULT 0,
            premium_until TEXT,
            total_searches INTEGER DEFAULT 0,
            last_active TEXT,
            UNIQUE(clone_token, user_id)
        );
        
        CREATE TABLE IF NOT EXISTS clone_daily_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            claim_date TEXT NOT NULL,
            UNIQUE(clone_token, user_id, claim_date)
        );
        
        CREATE TABLE IF NOT EXISTS clone_referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT NOT NULL,
            referrer INTEGER,
            referred INTEGER,
            date TEXT
        );
        
        CREATE TABLE IF NOT EXISTS clone_search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clone_token TEXT NOT NULL,
            user_id INTEGER,
            search_type TEXT,
            query TEXT,
            search_date TEXT,
            result TEXT
        );
        
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
        
        CREATE TABLE IF NOT EXISTS api_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT UNIQUE NOT NULL,
            base_url TEXT NOT NULL,
            action_param TEXT NOT NULL,
            query_param TEXT NOT NULL,
            api_key TEXT NOT NULL,
            is_enabled INTEGER DEFAULT 1,
            timeout INTEGER DEFAULT 20,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS api_key_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT NOT NULL,
            old_key TEXT,
            new_key TEXT,
            changed_by INTEGER,
            changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        );
    ''')
    conn.commit()
    
    # ========== INSERT DEFAULT API CONFIGS ==========
    default_configs = [
        # NITIN API — Working
        ('number', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'num', 'number', 'JAANI'),
        ('aadhar', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'aadhar', 'aadhar', 'JAANI'),
        ('upi', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'upiinfo', 'upi', 'JAANI'),
        
        # FREE APIs for remaining features
        ('instagram', 'https://instagram-api.vercel.app/api', 'user', 'username', 'free'),
        ('ifsc', 'https://ifsc-api.vercel.app/api', 'ifsc', 'code', 'free'),
        ('vehicle', 'https://vehicle-api.vercel.app/api', 'rc', 'number', 'free'),
        ('gst', 'https://gst-api.vercel.app/api', 'gst', 'number', 'free'),
        ('pan', 'https://pan-api.vercel.app/api', 'pan', 'number', 'free'),
        ('pak_num', 'https://pak-api.vercel.app/api', 'pak', 'number', 'free'),
        ('pincode', 'https://pincode-api.vercel.app/api', 'pincode', 'code', 'free'),
        ('ff', 'https://ff-api.vercel.app/api', 'ff', 'uid', 'free'),
    ]
    
    for feature, base_url, action, query, key in default_configs:
        c.execute('''
            INSERT OR IGNORE INTO api_config 
            (feature, base_url, action_param, query_param, api_key, is_enabled)
            VALUES (?, ?, ?, ?, ?, 1)
        ''', (feature, base_url, action, query, key))
    conn.commit()
    
    try:
        c.execute("INSERT OR IGNORE INTO admins (user_id, added_by, added_date, is_owner) VALUES (?, ?, ?, ?)",
                  (OWNER_ID, OWNER_ID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
        conn.commit()
    except Exception:
        pass
    
    try:
        c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, join_date, credits, last_active) VALUES (?, ?, ?, ?, ?, ?)",
                  (OWNER_ID, 'owner', 'Bot Owner', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except Exception:
        pass
    
    print("✅ Database initialized successfully!")

# ==================== API CONFIG FUNCTIONS ====================

def get_api_config(feature):
    try:
        conn = sqlite3.connect('bot.db', timeout=10)
        c = conn.cursor()
        c.execute('''
            SELECT base_url, action_param, query_param, api_key, timeout, is_enabled
            FROM api_config WHERE feature = ? AND is_enabled = 1
        ''', (feature,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'base_url': row[0],
                'action_param': row[1],
                'query_param': row[2],
                'api_key': row[3],
                'timeout': row[4] or 20,
                'is_enabled': bool(row[5])
            }
        return None
    except Exception as e:
        print(f"[get_api_config] {e}")
        return None

def update_api_config(feature, base_url=None, action_param=None, query_param=None, api_key=None, timeout=None, enabled=None):
    try:
        conn = sqlite3.connect('bot.db', timeout=10)
        c = conn.cursor()
        
        updates = []
        params = []
        
        if base_url:
            updates.append("base_url = ?")
            params.append(base_url)
        if action_param:
            updates.append("action_param = ?")
            params.append(action_param)
        if query_param:
            updates.append("query_param = ?")
            params.append(query_param)
        if api_key:
            updates.append("api_key = ?")
            params.append(api_key)
        if timeout is not None:
            updates.append("timeout = ?")
            params.append(timeout)
        if enabled is not None:
            updates.append("is_enabled = ?")
            params.append(1 if enabled else 0)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(feature)
        
        query = f"UPDATE api_config SET {', '.join(updates)} WHERE feature = ?"
        c.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[update_api_config] {e}")
        return False

def get_all_api_configs():
    try:
        conn = sqlite3.connect('bot.db', timeout=10)
        c = conn.cursor()
        c.execute('''
            SELECT feature, base_url, action_param, query_param, api_key, timeout, is_enabled, updated_at
            FROM api_config ORDER BY feature
        ''')
        rows = c.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'feature': row[0],
                'base_url': row[1],
                'action_param': row[2],
                'query_param': row[3],
                'api_key': row[4],
                'timeout': row[5],
                'is_enabled': bool(row[6]),
                'updated_at': row[7]
            })
        return result
    except Exception as e:
        print(f"[get_all_api_configs] {e}")
        return []

def call_dynamic_api(feature, query_value):
    import urllib.parse
    
    config = get_api_config(feature)
    if not config:
        return {'success': False, 'msg': f'Feature {feature} not configured'}
    
    if not config['is_enabled']:
        return {'success': False, 'msg': f'Feature {feature} is currently disabled'}
    
    encoded_value = urllib.parse.quote(str(query_value))
    url = f"{config['base_url']}?action={config['action_param']}&{config['query_param']}={encoded_value}&key={config['api_key']}"
    
    print(f"[API:{feature}] Calling: {url}")
    
    try:
        resp = requests.get(url, timeout=config['timeout'], headers={'User-Agent': 'Mozilla/5.0'})
        print(f"[API:{feature}] HTTP {resp.status_code}")
        
        if resp.status_code != 200:
            return {'success': False, 'msg': f'HTTP {resp.status_code}'}
        
        data = resp.json()
        
        if not data.get('status'):
            return {'success': False, 'msg': data.get('msg', 'No data found')}
        
        records = data.get('result', [])
        if not records:
            return {'success': False, 'msg': 'No records found'}
        
        return {
            'success': True,
            'data': records,
            'total_records': len(records),
            'metadata': data.get('metadata', {}),
            '_raw': data,
            'source': 'dynamic_api'
        }
        
    except requests.exceptions.Timeout:
        return {'success': False, 'msg': f'API timeout after {config["timeout"]}s'}
    except Exception as e:
        print(f"[API:{feature}] Error: {e}")
        return {'success': False, 'msg': str(e)}

# ==================== FEATURE FUNCTIONS ====================

def get_number_info(number):
    return call_dynamic_api('number', number)

def get_aadhar_info(aadhar):
    return call_dynamic_api('aadhar', aadhar)

def get_upi_info(upi):
    return call_dynamic_api('upi', upi)

def get_instagram_info(username):
    return call_dynamic_api('instagram', username)

def get_ifsc_info(ifsc):
    return call_dynamic_api('ifsc', ifsc)

def get_vehicle_info(vehicle):
    return call_dynamic_api('vehicle', vehicle)

def get_gst_info(gst):
    return call_dynamic_api('gst', gst)

def get_pan_info(pan):
    return call_dynamic_api('pan', pan)

def get_pak_num_info(number):
    return call_dynamic_api('pak_num', number)

def get_pincode_info(pincode):
    return call_dynamic_api('pincode', pincode)

def get_ff_info(uid):
    return call_dynamic_api('ff', uid)

def get_email_info(email):
    return call_dynamic_api('email', email)

# ==================== FORMAT FUNCTIONS ====================

def _DIV():
    return "━━━━━━━━━━━━━━━━━━"

def _esc(v):
    return _html.escape(str(v).strip(), quote=False)

def get_field_emoji(key):
    emoji_map = {
        'name': '👤', 'fullname': '👤', 'NAME': '👤',
        'address': '🏠', 'ADDRESS': '🏠',
        'aadhar': '🪪', 'alt': '📲',
        'circle': '📡', 'email': '📧', 'fname': '👨',
        'num': '📱', 'number': '📱', 'phone': '📱',
        'mobile': '📱', 'operator': '📡', 'state': '🏞️',
        'city': '🌆', 'country': '🌍', 'pincode': '📍',
        'bank': '🏦', 'ifsc': '🏦', 'branch': '🏦',
        'gst': '💼', 'pan': '🪪', 'vehicle': '🚗',
        'upi': '💳', 'vpa': '💳', 'account': '🏦'
    }
    k = str(key).lower().strip()
    for em_key, em in emoji_map.items():
        if em_key in k:
            return em
    return '•'

def format_message(text):
    return f"<blockquote>{text}\n\n{BOT_CREDIT}</blockquote>"

def format_number_info_bold(data, number):
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    records = data.get('data', [])
    if not records:
        return format_message(
            f"📋 <b>📱 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢</b>\n{_DIV()}\n"
            f"🕐 {now}\n"
            f"├📞 ɴᴜᴍʙᴇʀ: <code>{number}</code>\n"
            f"└❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ\n{_DIV()}"
        )
    
    total = len(records)
    lines = [
        f"📋 <b>📱 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢</b>",
        f"{_DIV()}",
        f"🕐 {now}",
        f"📞 ɴᴜᴍʙᴇʀ: <code>{number}</code>",
        f"📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: <b>{total}</b>",
        f"{_DIV()}",
    ]
    
    for idx, item in enumerate(records, 1):
        if total > 1:
            lines.append(f"")
            lines.append(f"👤 <b>ʀᴇᴄᴏʀᴅ {idx}/{total}</b>")
        
        fields = []
        if item.get('NAME') or item.get('name'):
            fields.append(('👤', 'ɴᴀᴍᴇ', item.get('NAME') or item.get('name')))
        if item.get('fname'):
            fields.append(('👨', 'ꜰᴀᴛʜᴇʀ', item['fname']))
        if item.get('num') or item.get('number'):
            fields.append(('📱', 'ɴᴜᴍʙᴇʀ', item.get('num') or item.get('number')))
        if item.get('alt'):
            fields.append(('📲', 'ᴀʟᴛ ɴᴜᴍʙᴇʀ', item['alt']))
        if item.get('aadhar'):
            fields.append(('🪪', 'ᴀᴀᴅʜᴀʀ', item['aadhar']))
        if item.get('ADDRESS') or item.get('address'):
            addr = str(item.get('ADDRESS') or item.get('address', '')).replace('!', ' ').strip()
            fields.append(('🏠', 'ᴀᴅᴅʀᴇꜱꜱ', addr))
        if item.get('circle'):
            fields.append(('📡', 'ᴄɪʀᴄʟᴇ', item['circle']))
        if item.get('email'):
            fields.append(('📧', 'ᴇᴍᴀɪʟ', item['email']))
        
        for i, (em, label, val) in enumerate(fields):
            c = "└" if i == len(fields) - 1 else "├"
            lines.append(f"{c}{em} <b>{label}</b>: <code>{_esc(str(val))}</code>")
        
        if not fields:
            lines.append("└❌ ɴᴏ ᴅᴀᴛᴀ")
    
    meta = data.get('metadata', {})
    if meta:
        lines.append(f"")
        lines.append(f"{_DIV()}")
        lines.append(f"📊 <b>API Usage:</b> {meta.get('key_usage', 'N/A')}/{meta.get('daily_limit', 'N/A')}")
        lines.append(f"📅 <b>Daily Used:</b> {meta.get('daily_used', 'N/A')}")
    
    lines.append(f"{_DIV()}")
    return format_message("\n".join(lines))

def format_aadhar_result_bold(data, aadhar):
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    records = data.get('data', [])
    if not records:
        return format_message(
            f"📋 <b>🪪 𝗔𝗔𝗗𝗛𝗔𝗥 𝗜𝗡𝗙𝗢</b>\n{_DIV()}\n"
            f"🕐 {now}\n"
            f"├🪪 ᴀᴀᴅʜᴀʀ: <code>{aadhar}</code>\n"
            f"└❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ\n{_DIV()}"
        )
    
    total = len(records)
    lines = [
        f"📋 <b>🪪 𝗔𝗔𝗗𝗛𝗔𝗥 𝗜𝗡𝗙𝗢</b>",
        f"{_DIV()}",
        f"🕐 {now}",
        f"├🪪 ᴀᴀᴅʜᴀʀ: <code>{aadhar}</code>",
        f"├📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: <b>{total}</b>",
        f"{_DIV()}",
    ]
    
    for idx, item in enumerate(records, 1):
        if total > 1:
            lines.append(f"")
            lines.append(f"👤 <b>ʀᴇᴄᴏʀᴅ {idx}/{total}</b>")
        
        fields = []
        if item.get('NAME') or item.get('name'):
            fields.append(('👤', 'ɴᴀᴍᴇ', item.get('NAME') or item.get('name')))
        if item.get('fname') or item.get('father'):
            fields.append(('👨', 'ꜰᴀᴛʜᴇʀ', item.get('fname') or item.get('father')))
        if item.get('ADDRESS') or item.get('address'):
            addr = str(item.get('ADDRESS') or item.get('address', '')).replace('!', ' ').strip()
            fields.append(('🏠', 'ᴀᴅᴅʀᴇꜱꜱ', addr))
        if item.get('circle'):
            fields.append(('📡', 'ᴄɪʀᴄʟᴇ', item['circle']))
        
        for i, (em, label, val) in enumerate(fields):
            c = "└" if i == len(fields) - 1 else "├"
            lines.append(f"{c}{em} <b>{label}</b>: <code>{_esc(str(val))}</code>")
    
    lines.append(f"{_DIV()}")
    return format_message("\n".join(lines))

def format_upi_result_bold(data, upi):
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    records = data.get('data', [])
    if not records:
        return format_message(
            f"📋 <b>💳 𝗨𝗣𝗜 𝗜𝗡𝗙𝗢</b>\n{_DIV()}\n"
            f"🕐 {now}\n"
            f"├💳 ᴜᴩɪ: <code>{upi}</code>\n"
            f"└❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ\n{_DIV()}"
        )
    
    lines = [
        f"📋 <b>💳 𝗨𝗣𝗜 𝗜𝗡𝗙𝗢</b>",
        f"{_DIV()}",
        f"🕐 {now}",
        f"💳 ᴜᴩɪ: <code>{upi}</code>",
        f"{_DIV()}",
    ]
    
    for idx, item in enumerate(records, 1):
        if len(records) > 1:
            lines.append(f"")
            lines.append(f"👤 <b>ʀᴇᴄᴏʀᴅ {idx}/{len(records)}</b>")
        
        fields = []
        for key, label in [('name', 'ɴᴀᴍᴇ'), ('vpa', 'ᴠᴩᴀ'), ('account', 'ᴀᴄᴄᴏᴜɴᴛ'),
                          ('bank', 'ʙᴀɴᴋ'), ('ifsc', 'ɪꜰꜱᴄ'), ('status', 'ꜱᴛᴀᴛᴜꜱ')]:
            val = item.get(key)
            if val and str(val).strip() not in ('', 'N/A', 'None', 'null'):
                fields.append((get_field_emoji(key), label, val))
        
        for i, (em, label, val) in enumerate(fields):
            c = "└" if i == len(fields) - 1 else "├"
            lines.append(f"{c}{em} <b>{label}</b>: <code>{_esc(str(val))}</code>")
    
    lines.append(f"{_DIV()}")
    return format_message("\n".join(lines))

def format_generic_result(data, title, query_label, query_value):
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    records = data.get('data', [])
    if not records:
        return format_message(
            f"📋 <b>{title}</b>\n{_DIV()}\n"
            f"🕐 {now}\n"
            f"├🔎 {query_label}: <code>{query_value}</code>\n"
            f"└❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ\n{_DIV()}"
        )
    
    lines = [
        f"📋 <b>{title}</b>",
        f"{_DIV()}",
        f"🕐 {now}",
        f"🔎 {query_label}: <code>{_esc(str(query_value))}</code>",
        f"📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: <b>{len(records)}</b>",
        f"{_DIV()}",
    ]
    
    for idx, item in enumerate(records, 1):
        if len(records) > 1:
            lines.append(f"")
            lines.append(f"👤 <b>ʀᴇᴄᴏʀᴅ {idx}/{len(records)}</b>")
        
        fields = []
        for k, v in item.items():
            if k.lower() in ('success', 'status', 'msg', 'message', '_raw', 'metadata'):
                continue
            if v and str(v).strip() not in ('', 'N/A', 'None', 'null'):
                fields.append((get_field_emoji(k), k.replace('_', ' ').title(), v))
        
        for i, (em, label, val) in enumerate(fields[:10]):
            c = "└" if i == len(fields[:10]) - 1 else "├"
            lines.append(f"{c}{em} <b>{label}</b>: <code>{_esc(str(val))}</code>")
    
    lines.append(f"{_DIV()}")
    return format_message("\n".join(lines))

# ==================== USER DATABASE FUNCTIONS ====================

def get_user(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_user_count():
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

def get_admin_count():
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM admins")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0

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
        
        if c.rowcount > 0 and referrer and referrer != user_id:
            c.execute("INSERT OR IGNORE INTO referrals (referrer, referred, date) VALUES (?,?,?)",
                      (referrer, user_id, date))
            if c.rowcount > 0:
                c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (REFERRAL_CREDITS, referrer))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
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

def remove_credits(user_id, amount):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET credits = credits - ? WHERE user_id = ? AND credits >= ?", (amount, user_id, amount))
        conn.commit()
        return c.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def update_user(user_id, **kwargs):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        for key, value in kwargs.items():
            c.execute(f"UPDATE users SET {key}=? WHERE user_id=?", (value, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating user: {e}")
    finally:
        conn.close()

def get_referral_count(user_id):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer=?", (user_id,))
    result = c.fetchone()[0] or 0
    conn.close()
    return result

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
    except Exception as e:
        print(f"Error saving history: {e}")
    finally:
        conn.close()

# ==================== ADMIN FUNCTIONS ====================

def is_admin(user_id):
    if user_id == OWNER_ID:
        return True
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("SELECT user_id FROM admins WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def is_owner(user_id):
    return user_id == OWNER_ID

def _is_main_admin_only(uid):
    return uid == OWNER_ID

def is_feature_maintenance(feature_key):
    return False, ''

# ==================== GITHUB BACKUP ====================

def github_upload_db():
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return False
    
    try:
        import base64
        if not os.path.exists('bot.db') or os.path.getsize('bot.db') < 4096:
            return False
        
        with open('bot.db', 'rb') as f:
            db_bytes = f.read()
        
        encoded = base64.b64encode(db_bytes).decode()
        
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        repo_clean = GITHUB_REPO.replace('https://github.com/', '').replace('github.com/', '').strip('/')
        url = f"https://api.github.com/repos/{repo_clean}/contents/{GITHUB_DB_PATH}"
        
        r = requests.get(url, headers=headers, timeout=10)
        sha = r.json().get('sha') if r.status_code == 200 else None
        
        payload = {
            "message": f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": encoded
        }
        if sha:
            payload["sha"] = sha
        
        r2 = requests.put(url, headers=headers, json=payload, timeout=30)
        return r2.status_code in (200, 201)
    except Exception as e:
        print(f"[Backup] Error: {e}")
        return False

# ==================== BOT INSTANCE ====================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

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
    page = admin_page.get(uid, 1)
    
    if page == 1:
        buttons = [
            ("📊 ᴅᴀꜱʜʙᴏᴀʀᴅ", "👥 ᴜꜱᴇʀ ʟɪꜱᴛ"),
            ("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ", "🚫 ʙʟᴏᴄᴋ ᴜꜱᴇʀ"),
            ("✅ ᴜɴʙʟᴏᴄᴋ ᴜꜱᴇʀ", "👤 ᴜꜱᴇʀ ɪɴꜰᴏ"),
            ("💎 ᴀᴅᴅ ᴩʀᴇᴍɪᴜᴍ", "🚫 ʀᴇᴍᴏᴠᴇ ᴩʀᴇᴍɪᴜᴍ"),
            ("💰 ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ", "💸 ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ"),
            ("⚙️ ꜱᴇᴛ ᴄʀᴇᴅɪᴛꜱ", "₹ ᴀᴅᴅ ᴍᴏɴᴇʏ"),
            ("🗑️ ᴅᴇʟᴇᴛᴇ ʜɪꜱᴛᴏʀʏ", "🔧 ꜰᴇᴀᴛᴜʀᴇ ᴄᴏꜱᴛꜱ"),
            ("🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ", "💎 ᴩʀᴇᴍɪᴜᴍ ᴩʀɪᴄᴇꜱ"),
            ("📤 ᴇxᴩᴏʀᴛ ᴜꜱᴇʀꜱ", "🔔 ɴᴏᴛɪꜰʏ ᴜꜱᴇʀ"),
            ("🔧 ᴀᴩɪ ᴄᴏɴꜰɪɢ", "➡️ ɴᴇxᴛ"),
        ]
        for row in buttons:
            markup.add(*(KeyboardButton(b) for b in row))
    
    elif page == 7:
        buttons = [
            ("📋 ᴀᴩɪ ʟɪꜱᴛ", "✏️ ᴇᴅɪᴛ ᴀᴩɪ"),
            ("🧪 ᴛᴇꜱᴛ ᴀᴩɪ", "🔄 ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ"),
            ("⬅️ ʙᴀᴄᴋ", "🏠 ᴍᴀɪɴ ᴍᴇɴᴜ"),
        ]
        for row in buttons:
            markup.add(*(KeyboardButton(b) for b in row))
    
    return markup

# ==================== ADMIN STATE ====================

admin_page = {}
user_state = {}
result_pages = {}
user_pages = {}
hist_pages = {}
_confirm_pending = {}

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
    user_pages[uid] = 1
    user_state.pop(uid, None)
    text = f"👋 <b>Menu</b>\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ" and is_admin(m.from_user.id) and not is_group(m))
def admin_panel(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    bot.send_message(uid, format_message("<b>⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ - ᴩᴀɢᴇ 1</b>"), reply_markup=admin_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "➡️ ɴᴇxᴛ" and is_admin(m.from_user.id) and not is_group(m))
def admin_next(m):
    uid = m.from_user.id
    admin_page[uid] = 7
    bot.send_message(uid, format_message("<b>⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ - ᴀᴩɪ ᴄᴏɴꜰɪɢ</b>"), reply_markup=admin_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "⬅️ ʙᴀᴄᴋ" and is_admin(m.from_user.id) and not is_group(m))
def admin_back(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    bot.send_message(uid, format_message("<b>⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ - ᴩᴀɢᴇ 1</b>"), reply_markup=admin_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "🏠 ᴍᴀɪɴ ᴍᴇɴᴜ" and is_admin(m.from_user.id) and not is_group(m))
def admin_main_menu(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    user_pages[uid] = 1
    text = f"👋 <b>Menu</b>\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "🔧 ᴀᴩɪ ᴄᴏɴꜰɪɢ" and is_admin(m.from_user.id) and not is_group(m))
def api_config_btn(m):
    uid = m.from_user.id
    admin_page[uid] = 7
    text = (
        "<b>🔧 ᴀᴩɪ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📋 ᴀᴩɪ ʟɪꜱᴛ → Show all configs\n"
        "✏️ ᴇᴅɪᴛ ᴀᴩɪ → Change URL/Key/Params\n"
        "🧪 ᴛᴇꜱᴛ ᴀᴩɪ → Test any config\n"
        "🔄 ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ → Toggle features"
    )
    bot.send_message(uid, format_message(text), reply_markup=admin_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "📋 ᴀᴩɪ ʟɪꜱᴛ" and is_admin(m.from_user.id) and not is_group(m))
def api_list_btn(m):
    configs = get_all_api_configs()
    if not configs:
        bot.reply_to(m, format_message("<b>❌ No API configs found!</b>"), parse_mode='HTML')
        return
    
    text = "<b>📋 ᴀᴩɪ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴꜱ</b>\n━━━━━━━━━━━━━━━━━━\n"
    for cfg in configs:
        status = "🟢" if cfg['is_enabled'] else "🔴"
        text += (
            f"\n{status} <b>{cfg['feature'].upper()}</b>\n"
            f"├ 🌐 URL: <code>{cfg['base_url'][:50]}...</code>\n"
            f"├ 🎯 Action: {cfg['action_param']}\n"
            f"├ 🔑 Key: <code>{cfg['api_key']}</code>\n"
            f"└ 📅 Updated: {cfg['updated_at'][:16]}\n"
        )
    
    bot.reply_to(m, format_message(text), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "✏️ ᴇᴅɪᴛ ᴀᴩɪ" and is_admin(m.from_user.id) and not is_group(m))
def api_edit_start(m):
    configs = get_all_api_configs()
    if not configs:
        bot.reply_to(m, format_message("<b>❌ No API configs found!</b>"), parse_mode='HTML')
        return
    
    mk = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cfg in configs:
        status = "✅" if cfg['is_enabled'] else "❌"
        mk.add(KeyboardButton(f"{status} {cfg['feature'].upper()}"))
    mk.add(KeyboardButton("🔙 ʙᴀᴄᴋ"))
    
    bot.reply_to(m, format_message(
        "<b>✏️ ᴇᴅɪᴛ ᴀᴩɪ ᴄᴏɴꜰɪɢ</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Feature select karo edit karne ke liye:"
    ), reply_markup=mk, parse_mode='HTML')
    user_state[m.from_user.id] = "api_edit_select"

@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == "api_edit_select" and is_admin(m.from_user.id))
def api_edit_select(m):
    uid = m.from_user.id
    if m.text == "🔙 ʙᴀᴄᴋ":
        user_state.pop(uid, None)
        api_config_btn(m)
        return
    
    selected = None
    for cfg in get_all_api_configs():
        if cfg['feature'].upper() in m.text:
            selected = cfg['feature']
            break
    
    if not selected:
        bot.reply_to(m, format_message("<b>❌ Invalid selection!</b>"), parse_mode='HTML')
        return
    
    config = get_api_config(selected)
    if not config:
        bot.reply_to(m, format_message(f"<b>❌ Config for {selected} not found!</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = f"api_edit_{selected}"
    
    text = (
        f"<b>✏️ ᴇᴅɪᴛɪɴɢ: {selected.upper()}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🌐 <b>Current URL:</b>\n<code>{config['base_url']}</code>\n"
        f"🎯 <b>Action:</b> {config['action_param']}\n"
        f"🔑 <b>Key:</b> <code>{config['api_key']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"<b>Send new config in this format:</b>\n"
        f"<code>URL|ACTION|QUERY_PARAM|API_KEY|TIMEOUT</code>\n\n"
        f"<b>Example:</b>\n"
        f"<code>https://new-api.com/api|num|number|NEW_KEY|25</code>"
    )
    bot.send_message(uid, format_message(text), parse_mode='HTML')

@bot.message_handler(func=lambda m: isinstance(user_state.get(m.from_user.id), str) and 
                     user_state.get(m.from_user.id, '').startswith("api_edit_") and 
                     is_admin(m.from_user.id))
def api_edit_process(m):
    uid = m.from_user.id
    feature = user_state[uid].replace("api_edit_", "")
    
    if m.text.lower() == 'cancel':
        user_state.pop(uid, None)
        bot.reply_to(m, format_message("<b>✅ Edit cancelled!</b>"), parse_mode='HTML')
        api_config_btn(m)
        return
    
    parts = m.text.split('|')
    if len(parts) < 4:
        bot.reply_to(m, format_message(
            "<b>❌ Invalid format!</b>\n"
            "Use: <code>URL|ACTION|QUERY_PARAM|API_KEY|TIMEOUT</code>"
        ), parse_mode='HTML')
        return
    
    base_url = parts[0].strip()
    action_param = parts[1].strip()
    query_param = parts[2].strip()
    api_key = parts[3].strip()
    timeout = int(parts[4].strip()) if len(parts) > 4 and parts[4].strip() else 20
    
    success = update_api_config(
        feature=feature,
        base_url=base_url,
        action_param=action_param,
        query_param=query_param,
        api_key=api_key,
        timeout=timeout,
        enabled=True
    )
    
    if success:
        user_state.pop(uid, None)
        bot.reply_to(m, format_message(
            f"<b>✅ API Config Updated!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔧 <b>Feature:</b> {feature.upper()}\n"
            f"🌐 <b>New URL:</b>\n<code>{base_url}</code>\n"
            f"🔑 <b>New Key:</b> <code>{api_key}</code>"
        ), parse_mode='HTML')
    else:
        bot.reply_to(m, format_message("<b>❌ Update failed!</b>"), parse_mode='HTML')
    
    api_config_btn(m)

@bot.message_handler(func=lambda m: m.text == "🧪 ᴛᴇꜱᴛ ᴀᴩɪ" and is_admin(m.from_user.id) and not is_group(m))
def api_test_start(m):
    configs = get_all_api_configs()
    if not configs:
        bot.reply_to(m, format_message("<b>❌ No API configs found!</b>"), parse_mode='HTML')
        return
    
    mk = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cfg in configs:
        mk.add(KeyboardButton(f"🧪 {cfg['feature'].upper()}"))
    mk.add(KeyboardButton("🔙 ʙᴀᴄᴋ"))
    
    bot.reply_to(m, format_message(
        "<b>🧪 ᴀᴩɪ ᴛᴇꜱᴛ</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Feature select karo test karne ke liye:"
    ), reply_markup=mk, parse_mode='HTML')
    user_state[m.from_user.id] = "api_test_select"

@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == "api_test_select" and is_admin(m.from_user.id))
def api_test_select(m):
    uid = m.from_user.id
    if m.text == "🔙 ʙᴀᴄᴋ":
        user_state.pop(uid, None)
        api_config_btn(m)
        return
    
    selected = None
    for cfg in get_all_api_configs():
        if cfg['feature'].upper() in m.text:
            selected = cfg['feature']
            break
    
    if not selected:
        bot.reply_to(m, format_message("<b>❌ Invalid selection!</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = f"api_test_{selected}"
    
    examples = {
        'number': '9876543210',
        'aadhar': '327567544017',
        'upi': 'example@ybl',
        'instagram': 'instagram',
        'ifsc': 'SBIN0001234',
        'vehicle': 'MH12AB1234',
        'gst': '10DJCPK4351Q1Z5',
        'pan': 'AAMTS3432L',
        'pak_num': '03001234567',
        'pincode': '110001',
        'ff': '1234567890'
    }
    example = examples.get(selected, 'test_value')
    
    bot.send_message(uid, format_message(
        f"<b>🧪 ᴛᴇꜱᴛɪɴɢ: {selected.upper()}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 <b>Test value bhejo:</b>\n"
        f"<i>Example: {example}</i>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: isinstance(user_state.get(m.from_user.id), str) and 
                     user_state.get(m.from_user.id, '').startswith("api_test_") and 
                     is_admin(m.from_user.id))
def api_test_process(m):
    uid = m.from_user.id
    feature = user_state[uid].replace("api_test_", "")
    test_value = m.text.strip()
    
    if not test_value:
        bot.reply_to(m, format_message("<b>❌ Please send a test value!</b>"), parse_mode='HTML')
        return
    
    status_msg = bot.reply_to(m, format_message(
        f"<b>⏳ Testing {feature.upper()} API...</b>\n"
        f"🔍 Value: <code>{test_value}</code>"
    ), parse_mode='HTML')
    
    result = call_dynamic_api(feature, test_value)
    
    if result['success']:
        text = (
            f"<b>✅ ᴀᴩɪ ᴛᴇꜱᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔧 <b>Feature:</b> {feature.upper()}\n"
            f"📊 <b>Records Found:</b> {result['total_records']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Sample Response:</b>\n"
            f"<code>{json.dumps(result['data'][:2], indent=2)[:500]}</code>"
        )
    else:
        text = (
            f"<b>❌ ᴀᴩɪ ᴛᴇꜱᴛ ꜰᴀɪʟᴇᴅ!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"❌ <b>Error:</b> {result['msg']}"
        )
    
    try:
        bot.edit_message_text(format_message(text), m.chat.id, status_msg.message_id, parse_mode='HTML')
    except Exception:
        bot.send_message(m.chat.id, format_message(text), parse_mode='HTML')
    
    user_state.pop(uid, None)

@bot.message_handler(func=lambda m: m.text == "🔄 ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ" and is_admin(m.from_user.id) and not is_group(m))
def api_toggle_start(m):
    configs = get_all_api_configs()
    if not configs:
        bot.reply_to(m, format_message("<b>❌ No API configs found!</b>"), parse_mode='HTML')
        return
    
    mk = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cfg in configs:
        status = "🟢" if cfg['is_enabled'] else "🔴"
        mk.add(KeyboardButton(f"{status} {cfg['feature'].upper()}"))
    mk.add(KeyboardButton("🔙 ʙᴀᴄᴋ"))
    
    bot.reply_to(m, format_message(
        "<b>🔄 ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ ᴀᴩɪ</b>\n━━━━━━━━━━━━━━━━━━\n"
        "🟢 = Enabled  |  🔴 = Disabled\n\n"
        "Feature select karo toggle karne ke liye:"
    ), reply_markup=mk, parse_mode='HTML')
    user_state[m.from_user.id] = "api_toggle_select"

@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == "api_toggle_select" and is_admin(m.from_user.id))
def api_toggle_process(m):
    uid = m.from_user.id
    if m.text == "🔙 ʙᴀᴄᴋ":
        user_state.pop(uid, None)
        api_config_btn(m)
        return
    
    selected = None
    for cfg in get_all_api_configs():
        if cfg['feature'].upper() in m.text:
            selected = cfg['feature']
            break
    
    if not selected:
        bot.reply_to(m, format_message("<b>❌ Invalid selection!</b>"), parse_mode='HTML')
        return
    
    config = get_api_config(selected)
    if not config:
        bot.reply_to(m, format_message(f"<b>❌ Config for {selected} not found!</b>"), parse_mode='HTML')
        return
    
    new_state = not config['is_enabled']
    success = update_api_config(feature=selected, enabled=new_state)
    
    if success:
        status_text = "🟢 Enabled" if new_state else "🔴 Disabled"
        bot.reply_to(m, format_message(
            f"<b>✅ {selected.upper()} → {status_text}</b>"
        ), parse_mode='HTML')
    else:
        bot.reply_to(m, format_message("<b>❌ Toggle failed!</b>"), parse_mode='HTML')
    
    user_state.pop(uid, None)
    api_config_btn(m)

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

@bot.message_handler(func=lambda m: m.text == "👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀ" and not is_group(m))
def select_user_btn(m):
    uid = m.from_user.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👤 Select User", callback_data="select_user"))
    bot.reply_to(m, format_message("<b>👤 Click button below to select a user:</b>"), reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "select_user")
def select_user_callback(call):
    uid = call.from_user.id
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("👤 Select User", request_users=KeyboardButtonRequestUser(request_id=1, user_is_bot=False)))
        markup.add(KeyboardButton("🔙 Main Menu"))
        bot.send_message(uid, format_message("<b>👤 Click 'Select User' button:</b>"), reply_markup=markup, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    except Exception:
        bot.send_message(uid, format_message("<b>❌ Select User feature needs update. Use /userid command instead.</b>"), parse_mode='HTML')
        bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['users_shared'])
def handle_user_shared(message):
    uid = message.from_user.id
    if not message.users_shared or not message.users_shared.user_ids:
        return
    
    raw_user_id = message.users_shared.user_ids[0]
    status = bot.reply_to(message, format_message("<b>⏳ Searching...</b>"), parse_mode='HTML')
    
    try:
        # Get basic info from Telegram API
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
    bot.reply_to(m, format_message("<b>🔍 Send username with @:</b>\nExample: <code>@username</code>"), parse_mode='HTML')

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
        bot.reply_to(m, format_message("<b>❌ Already claimed today!</b>\n⏳ Come back tomorrow."), parse_mode='HTML')

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
<b>🎁 Per Referral:</b> <code>+{REFERRAL_CREDITS}</code> credits
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
✨ All Features Unlocked

💳 Contact: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "ℹ️ ʜᴇʟᴩ" and not is_group(m))
def help_btn(m):
    text = """
<b>ℹ️ ʜᴇʟᴩ & ɢᴜɪᴅᴇ</b>
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

💰 Credits: Daily claim + Referrals
💎 Premium: Unlimited access

👑 Made by: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== TEXT INPUT HANDLER ====================

def is_group(message):
    return message.chat.type in ['group', 'supergroup']

@bot.message_handler(func=lambda m: m.from_user and m.from_user.id in user_state and not is_group(m))
def handle_text_input(m):
    uid = m.from_user.id
    state = user_state[uid]
    text = m.text.strip()
    
    if not text:
        return
    
    if state == "waiting_number":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number! Send 10-digit number.</b>"), parse_mode='HTML')
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
    
    elif state == "waiting_aadhar":
        clean = re.sub(r'\s+', '', text)
        if not re.match(r'^\d{12}$', clean):
            bot.reply_to(m, format_message("<b>❌ Invalid Aadhar! Must be 12 digits.</b>"), parse_mode='HTML')
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
    
    elif state == "waiting_instagram":
        clean = text.replace('@', '').strip()
        if len(clean) < 2:
            bot.reply_to(m, format_message("<b>❌ Invalid username!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_instagram_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "📷 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 𝗜𝗡𝗙𝗢", "👤 Username", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'instagram', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_ifsc":
        clean = text.upper().strip()
        if len(clean) != 11:
            bot.reply_to(m, format_message("<b>❌ Invalid IFSC! Must be 11 characters.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_ifsc_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🏦 𝗜𝗙𝗦𝗖 𝗜𝗡𝗙𝗢", "🏦 IFSC", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'ifsc', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_vehicle":
        clean = re.sub(r'\s+', '', text).upper()
        if len(clean) < 8:
            bot.reply_to(m, format_message("<b>❌ Invalid RC number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_vehicle_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🚗 𝗩𝗘𝗛𝗜𝗖𝗟𝗘 𝗜𝗡𝗙𝗢", "🚗 RC", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'vehicle', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_gst":
        clean = text.upper().strip()
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid GST number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_gst_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "💼 𝗚𝗦𝗧 𝗜𝗡𝗙𝗢", "💼 GST", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'gst', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_pan":
        clean = text.upper().strip()
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', clean):
            bot.reply_to(m, format_message("<b>❌ Invalid PAN! Format: ABCDE1234F</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pan_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🪪 𝗣𝗔𝗡 𝗜𝗡𝗙𝗢", "🪪 PAN", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pan', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_pak":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid Pakistan number!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pak_num_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🇵🇰 𝗣𝗔𝗞 𝗡𝗨𝗠 𝗜𝗡𝗙𝗢", "🇵🇰 Number", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pak_num', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_pincode":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) != 6:
            bot.reply_to(m, format_message("<b>❌ Invalid pincode! Must be 6 digits.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_pincode_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "📍 𝗣𝗜𝗡𝗖𝗢𝗗𝗘 𝗜𝗡𝗙𝗢", "📍 Pincode", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'pincode', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_ff":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 5:
            bot.reply_to(m, format_message("<b>❌ Invalid Free Fire UID!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        result = get_ff_info(clean)
        user_state.pop(uid, None)
        
        if result and result.get('success'):
            formatted = format_generic_result(result, "🎮 𝗙𝗥𝗘𝗘 𝗙𝗜𝗥𝗘 𝗜𝗡𝗙𝗢", "🎮 UID", clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'ff', clean, result)
        else:
            msg = result.get('msg', 'No data found')
            bot.edit_message_text(format_message(f"<b>❌ {msg}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
    
    elif state == "waiting_username":
        if not text.startswith('@'):
            text = '@' + text
        if len(text) < 2:
            bot.reply_to(m, format_message("<b>❌ Invalid username!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        try:
            chat = bot.get_chat(text)
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
            formatted = format_generic_result(result, "🔍 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 𝗜𝗡𝗙𝗢", "👤 Username", text)
            user_state.pop(uid, None)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'username', text, result)
        except Exception as e:
            bot.edit_message_text(format_message(f"<b>❌ User not found: {e}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
            user_state.pop(uid, None)
    
    elif state == "waiting_userid":
        if not re.match(r'^\d+$', text):
            bot.reply_to(m, format_message("<b>❌ Invalid User ID! Must be numeric.</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        try:
            chat = bot.get_chat(int(text))
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
            formatted = format_generic_result(result, "🆔 𝗧𝗚 𝗜𝗗 𝗜𝗡𝗙𝗢", "🆔 ID", text)
            user_state.pop(uid, None)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'userid', text, result)
        except Exception as e:
            bot.edit_message_text(format_message(f"<b>❌ User not found: {e}</b>"), m.chat.id, status.message_id, parse_mode='HTML')
            user_state.pop(uid, None)
    
    elif state == "waiting_redeem":
        # Simple redeem handler
        code = text.upper().strip()
        # Check if code exists in DB
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        try:
            c.execute("SELECT credits, max_uses, used_count, expires_at FROM redeem_codes WHERE code = ? AND is_active = 1", (code,))
            row = c.fetchone()
            if row:
                credits, max_uses, used_count, expires_at = row
                if used_count >= max_uses:
                    bot.reply_to(m, format_message("<b>❌ Code already fully used!</b>"), parse_mode='HTML')
                elif expires_at and datetime.now() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S"):
                    bot.reply_to(m, format_message("<b>❌ Code expired!</b>"), parse_mode='HTML')
                else:
                    c.execute("UPDATE redeem_codes SET used_count = used_count + 1 WHERE code = ?", (code,))
                    c.execute("INSERT OR IGNORE INTO redeemed_users (user_id, code, redeemed_at) VALUES (?, ?, ?)",
                              (uid, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    add_credits(uid, credits)
                    conn.commit()
                    bot.reply_to(m, format_message(f"<b>✅ Code redeemed! +{credits} credits</b>\n💰 Total: <code>{get_credits(uid)}</code>"), parse_mode='HTML')
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
    print("🔥 OSINT BOT STARTING...")
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
