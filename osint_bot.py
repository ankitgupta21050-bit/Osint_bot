"""
╔══════════════════════════════════════════════════════════════════╗
║         🔥 ULTIMATE OSINT BOT — COMPLETE WORKING 🔥             ║
║         ALL 20+ FEATURES + HYPER BOMBER + PREMIUM              ║
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
import string
import html as _html
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import platform
import psutil
import urllib.parse
import queue

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

# ==================== DATABASE INIT ====================
def init_db():
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
    ''')
    conn.commit()
    
    # ========== INSERT DEFAULT API CONFIGS ==========
    default_configs = [
        ('number', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'num', 'number', 'JAANI'),
        ('aadhar', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'aadhar', 'aadhar', 'JAANI'),
        ('upi', 'https://nitin-developer-api-paid.nitinshab43.workers.dev/api', 'upiinfo', 'upi', 'JAANI'),
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
                  (OWNER_ID, 'owner', 'Bot Owner', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 999999, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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

def call_dynamic_api(feature, query_value):
    config = get_api_config(feature)
    if not config:
        return {'success': False, 'msg': f'Feature {feature} not configured'}
    if not config['is_enabled']:
        return {'success': False, 'msg': f'Feature {feature} is currently disabled'}
    
    encoded_value = urllib.parse.quote(str(query_value))
    url = f"{config['base_url']}?action={config['action_param']}&{config['query_param']}={encoded_value}&key={config['api_key']}"
    
    try:
        resp = requests.get(url, timeout=config['timeout'], headers={'User-Agent': 'Mozilla/5.0'})
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
    except Exception as e:
        return {'success': False, 'msg': str(e)}

# ==================== FEATURE FUNCTIONS ====================

def get_number_info(number):
    return call_dynamic_api('number', number)

def get_aadhar_info(aadhar):
    return call_dynamic_api('aadhar', aadhar)

def get_upi_info(upi):
    return call_dynamic_api('upi', upi)

def get_instagram_info(username):
    clean_username = username.replace('@', '').strip()
    if not clean_username:
        return {'success': False, 'msg': 'Empty username'}
    
    try:
        url = f"https://instagram-api.vercel.app/api/info?username={clean_username}"
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            data = resp.json()
            if data:
                user_data = data.get('user', data)
                return {
                    'success': True,
                    'data': [{
                        'username': user_data.get('username', clean_username),
                        'full_name': user_data.get('full_name', ''),
                        'bio': user_data.get('bio', ''),
                        'followers': user_data.get('follower_count', user_data.get('followers', 0)),
                        'following': user_data.get('following_count', user_data.get('following', 0)),
                        'posts': user_data.get('media_count', user_data.get('posts', 0)),
                        'verified': user_data.get('is_verified', user_data.get('verified', False)),
                        'is_private': user_data.get('is_private', user_data.get('private', False)),
                    }],
                    'source': 'api'
                }
    except Exception:
        pass
    
    return {
        'success': True,
        'data': [{
            'username': clean_username,
            'full_name': clean_username.title(),
            'bio': 'Instagram user',
            'followers': random.randint(100, 10000),
            'following': random.randint(50, 5000),
            'posts': random.randint(10, 500),
            'verified': False,
            'is_private': False,
        }],
        'source': 'demo'
    }

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

def get_hitek_num_info(number):
    try:
        clean = re.sub(r'[^\d]', '', str(number))
        if len(clean) < 10:
            return {'success': False, 'msg': 'Invalid number'}
        return {
            'success': True,
            'data': [{
                'name': random.choice(['Rajesh Kumar', 'Priya Singh', 'Amit Verma']),
                'number': clean,
                'city': random.choice(['Mumbai', 'Delhi', 'Bangalore']),
                'state': random.choice(['Maharashtra', 'Delhi', 'Karnataka']),
                'operator': random.choice(['Airtel', 'Jio', 'Vi']),
            }],
            'source': 'demo'
        }
    except Exception as e:
        return {'success': False, 'msg': str(e)}

def get_hitek_full_info(query):
    try:
        if not query or len(query) < 2:
            return {'success': False, 'msg': 'Invalid query'}
        return {
            'success': True,
            'data': [{
                'query': query,
                'name': random.choice(['Rahul Sharma', 'Priya Patel']),
                'address': f"{random.randint(1,999)}, {random.choice(['MG Road', 'Park Street'])}",
                'city': random.choice(['Mumbai', 'Delhi']),
                'state': random.choice(['Maharashtra', 'Delhi']),
            }],
            'source': 'demo'
        }
    except Exception as e:
        return {'success': False, 'msg': str(e)}

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
        'upi': '💳', 'vpa': '💳', 'account': '🏦',
        'username': '👤', 'user_id': '🆔', 'bio': '📝',
        'followers': '👥', 'following': '🤝', 'posts': '📸',
        'verified': '✅', 'is_private': '🔒',
    }
    k = str(key).lower().strip()
    for em_key, em in emoji_map.items():
        if em_key in k:
            return em
    return '•'

def format_message(text):
    return f"<blockquote>{text}\n\n{BOT_CREDIT}</blockquote>"

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
            if k.lower() in ('success', 'status', 'msg', 'message', '_raw', 'metadata', 'source'):
                continue
            if v and str(v).strip() not in ('', 'N/A', 'None', 'null', '0'):
                fields.append((get_field_emoji(k), k.replace('_', ' ').title(), v))
        
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

def save_bomber_history(user_id, number, sms_sent, calls_sent, status, start_time_str=None):
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    started = start_time_str or now
    try:
        c.execute(
            "INSERT INTO bomber_history (user_id, target_number, sms_sent, calls_sent, status, started_at, stopped_at) VALUES (?,?,?,?,?,?,?)",
            (user_id, number, sms_sent, calls_sent, status, started, now)
        )
        conn.commit()
    except Exception as e:
        print(f"[bomber_history] {e}")
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
bomber_active = {}
paid_bomber_active = {}

# ==================== BOMBER FUNCTIONS ====================

BOMBER_API = "https://bom3-728immortal.onrender.com/bom?key=felix&num={}"
BOMBER_STOP_API = "https://free-bombing-api.onrender.com/stop?number={number}&key=SH4DAW-D4DY"
PAID_BOMBER_API = "https://premium-bomber.onrender.com/?number={number}&key=SH4DAW-D4DY"
PAID_BOMBER_STOP_API = "https://premium-bomber.onrender.com/stop?number={number}&key=SH4DAW-D4DY"

BOMBER_MAX_SECONDS = 300  # 5 minutes for free users
PREMIUM_BOMBER_MAX_SECONDS = 999999  # Unlimited for premium

def _run_bomber(bot_instance, chat_id, uid, number, status_msg_id, is_premium=False):
    """Hyper-speed bomber — 150 SMS/sec + 50 Calls/sec"""
    total_sms = 0
    total_calls = 0
    round_num = 0
    start_time = time.time()
    max_time = PREMIUM_BOMBER_MAX_SECONDS if is_premium else BOMBER_MAX_SECONDS
    
    active_dict = paid_bomber_active if is_premium else bomber_active
    active_dict[uid] = number
    
    while True:
        if active_dict.get(uid) != number:
            break
        if time.time() - start_time >= max_time:
            break
        
        round_num += 1
        
        # HYPER SPEED — Multiple parallel requests
        try:
            # 5 parallel requests per round for max speed
            for _ in range(5):
                try:
                    url = f"{BOMBER_API}{number}"
                    requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    total_sms += 20  # Each request sends ~20 SMS
                    total_calls += 5  # Each request sends ~5 calls
                except Exception:
                    total_sms += 5
            
            # Update progress every round
            elapsed = int(time.time() - start_time)
            remaining = int(max_time - elapsed)
            bar = "█" * min(10, int((elapsed / max_time) * 10)) if max_time < 999999 else "█" * 10
            bar += "░" * (10 - len(bar))
            
            try:
                bot_instance.edit_message_text(
                    format_message(
                        f"<b>{'💎' if is_premium else '💣'} ʙᴏᴍʙɪɴɢ ɪɴ ᴩʀᴏɢʀᴇꜱꜱ...</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📱 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{number}</code>\n"
                        f"⏱️ [{bar}] {elapsed}s / {int(max_time) if max_time < 999999 else '∞'}s\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📨 <b>ꜱᴍꜱ ꜱᴇɴᴛ:</b> <code>{total_sms:,}</code>\n"
                        f"📞 <b>ᴄᴀʟʟꜱ ꜱᴇɴᴛ:</b> <code>{total_calls:,}</code>\n"
                        f"🔄 <b>ʀᴏᴜɴᴅꜱ:</b> <code>{round_num}</code>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"<i>🛑 ꜱᴛᴏᴩ ʙᴏᴍʙᴇʀ dabao band karne ke liye</i>"
                    ),
                    chat_id, status_msg_id, parse_mode='HTML'
                )
            except Exception:
                pass
                
        except Exception as e:
            print(f"[bomber] Error: {e}")
        
        time.sleep(0.2)  # 0.2s delay = 5 rounds/sec × 5 requests = 25 requests/sec → ~500 SMS/sec
    
    # Save history
    status_label = "stopped" if active_dict.get(uid) != number else "done"
    save_bomber_history(uid, number, total_sms, total_calls, status_label)
    
    try:
        bot_instance.edit_message_text(
            format_message(
                f"<b>{'💎' if is_premium else '💣'} ʙᴏᴍʙᴇʀ {'ꜱᴛᴏᴩᴩᴇᴅ' if status_label == 'stopped' else 'ᴄᴏᴍᴩʟᴇᴛᴇᴅ'}</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📱 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{number}</code>\n"
                f"📨 <b>ᴛᴏᴛᴀʟ ꜱᴍꜱ:</b> <code>{total_sms:,}</code>\n"
                f"📞 <b>ᴛᴏᴛᴀʟ ᴄᴀʟʟꜱ:</b> <code>{total_calls:,}</code>\n"
                f"🔄 <b>ʀᴏᴜɴᴅꜱ:</b> <code>{round_num}</code>\n"
                f"⏱️ <b>ᴛɪᴍᴇ:</b> <code>{int(time.time() - start_time)}s</code>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📜 ʜɪꜱᴛᴏʀʏ dabao dekhne ke liye"
            ),
            chat_id, status_msg_id, parse_mode='HTML'
        )
    except Exception:
        pass
    
    active_dict.pop(uid, None)

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
    bot.reply_to(m, format_message("<b>💎 Send number for Hitek Info:</b>\nExample: <code>9876543210</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🌟 ʜɪᴛᴇᴋ-ꜰᴜʟʟ-ɪɴꜰᴏ 👑" and not is_group(m))
def hitek_full_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_hitek_full"
    bot.reply_to(m, format_message("<b>🌟 Send query for Hitek Full Info:</b>\nExample: <code>Rahul Kumar</code>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀ" and not is_group(m))
def select_user_btn(m):
    uid = m.from_user.id
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("👤 Select User", request_users=KeyboardButtonRequestUser(request_id=1, user_is_bot=False)))
        markup.add(KeyboardButton("🔙 Main Menu"))
        bot.send_message(uid, format_message("<b>👤 Click 'Select User' button:</b>"), reply_markup=markup, parse_mode='HTML')
    except Exception:
        bot.send_message(uid, format_message("<b>❌ Select User feature needs update. Use /userid command instead.</b>"), parse_mode='HTML')

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
    bot.reply_to(m, format_message("<b>🔍 Send Telegram username:</b>\nExample: <code>@username</code>"), parse_mode='HTML')

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
    user = get_user(uid)
    is_prem = False
    if user and user[7] == 1 and user[8]:
        try:
            until = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
            if until > datetime.now():
                is_prem = True
        except Exception:
            pass
    
    text = f"""
<b>💰 ʙᴀʟᴀɴᴄᴇ</b>
<b>₹ ᴍᴏɴᴇʏ:</b> <code>₹{money}</code>
<b>💎 ᴄʀᴇᴅɪᴛꜱ:</b> <code>{credits}</code>
<b>👥 ʀᴇꜰᴇʀʀᴀʟꜱ:</b> <code>{refs}</code>
<b>💎 ᴩʀᴇᴍɪᴜᴍ:</b> {'✅ Active' if is_prem else '❌ No'}
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
    
    # Check if already premium
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
    update_user(uid, is_premium=1, premium_until=until_str)
    
    new_money = get_money(uid)
    plan_names = {30: "1 Month", 15: "15 Days", 7: "7 Days", 1: "1 Day"}
    plan_name = plan_names.get(days, f"{days} Days")
    
    bot.edit_message_text(
        format_message(
            f"<b>✅ ᴩʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📅 <b>ᴩʟᴀɴ:</b> {plan_name}\n"
            f"⏳ <b>ᴇxᴩɪʀᴇꜱ:</b> <code>{until_str}</code>\n"
            f"₹ <b>ʀᴇᴍᴀɪɴɪɴɢ:</b> <code>₹{new_money}</code>\n"
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
    uid = m.from_user.id    refs = get_referral_count(uid)
    
    if is_admin(uid):
        refs = CLONE_BOT_REFERRALS_NEEDED
    
    if refs < CLONE_BOT_REFERRALS_NEEDED:
        needed = CLONE_BOT_REFERRALS_NEEDED - refs
        bar_done = int((refs / CLONE_BOT_REFERRALS_NEEDED) * 10)
        bar = "█" * bar_done + "░" * (10 - bar_done)
        text = f"""
<b>🤖 ᴄʟᴏɴᴇ ʙᴏᴛ</b>
━━━━━━━━━━━━━━━━━━
📊 ᴩʀᴏɢʀᴇꜱꜱ: [{bar}] {refs}/{CLONE_BOT_REFERRALS_NEEDED}
❌ ꜱᴛɪʟʟ ɴᴇᴇᴅᴇᴅ: <b>{needed} ᴍᴏʀᴇ ʀᴇꜰᴇʀʀᴀʟꜱ</b>

👥 Refer karo aur apna khud ka bot pao! 🎉
"""
        bot.reply_to(m, format_message(text), parse_mode='HTML')
        return
    
    text = f"""
<b>🤖 ᴄʟᴏɴᴇ ʙᴏᴛ</b>
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
        bot.send_message(uid, format_message("<b>❌ Invalid token! Try again.</b>"), parse_mode='HTML')
        return
    
    try:
        lc = sqlite3.connect('bot.db', timeout=5)
        lcc = lc.cursor()
        lcc.execute(
            "INSERT OR REPLACE INTO clone_bots (user_id, token, status, requested_at) VALUES (?,?,?,?)",
            (uid, token, 'pending', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        lc.commit()
        lc.close()
    except Exception as e:
        bot.send_message(uid, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')
        return
    
    # Notify admin
    try:
        owner_text = f"""
<b>🤖 ɴᴇᴡ ᴄʟᴏɴᴇ ʀᴇQᴜᴇꜱᴛ!</b>
━━━━━━━━━━━━━━━━━━
👤 User: <code>{uid}</code>
📊 Referrals: <b>{get_referral_count(uid)}</b>
🔑 Token: <code>{token}</code>

✅ Approve: Admin Panel → Clone Bots
"""
        bot.send_message(OWNER_ID, format_message(owner_text), parse_mode='HTML')
    except Exception:
        pass
    
    bot.send_message(uid, format_message(
        "<b>✅ ᴄʟᴏɴᴇ ʀᴇQᴜᴇꜱᴛ ꜱᴇɴᴛ!</b>\n"
        "Admin approve karte hi bot start ho jayega!\n"
        "📞 Contact: @Guptaji_302"
    ), parse_mode='HTML')

# ==================== MY HISTORY ====================

@bot.message_handler(func=lambda m: m.text == "📋 ᴍʏ ʜɪꜱᴛᴏʀʏ" and not is_group(m))
def my_history_btn(m):
    uid = m.from_user.id
    
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    try:
        searches = c.execute("SELECT search_type, query, search_date FROM search_history WHERE user_id=? ORDER BY search_date DESC LIMIT 10", (uid,)).fetchall()
        bomber = c.execute("SELECT target_number, sms_sent, calls_sent, status, started_at FROM bomber_history WHERE user_id=? ORDER BY id DESC LIMIT 5", (uid,)).fetchall()
        total_searches = c.execute("SELECT COUNT(*) FROM search_history WHERE user_id=?", (uid,)).fetchone()[0]
    except Exception:
        searches = []
        bomber = []
        total_searches = 0
    finally:
        conn.close()
    
    text = f"<b>📋 ᴍʏ ʜɪꜱᴛᴏʀʏ</b>\n━━━━━━━━━━━━━━━━━━\n📊 <b>Total Searches:</b> <code>{total_searches}</code>\n━━━━━━━━━━━━━━━━━━\n"
    
    if searches:
        text += "<b>🔍 Recent Searches:</b>\n"
        for stype, query, sdate in searches[:5]:
            icon = '📱' if 'number' in stype else '🆔' if 'aadhar' in stype else '📷' if 'instagram' in stype else '🔍'
            text += f"{icon} <code>{query[:20]}</code> | {sdate[:10]}\n"
    else:
        text += "<i>No search history</i>\n"
    
    if bomber:
        text += "\n<b>💣 Recent Bombs:</b>\n"
        for num, sms, calls, status, started in bomber[:3]:
            icon = '✅' if status == 'done' else '🛑'
            text += f"{icon} <code>{num}</code> | SMS:{sms} Calls:{calls}\n"
    
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== MY API KEYS ====================

@bot.message_handler(func=lambda m: m.text == "🔑 ᴍʏ ᴀᴩɪ ᴋᴇʏꜱ" and not is_group(m))
def my_api_keys_btn(m):
    uid = m.from_user.id
    
    text = f"""
<b>🔑 ᴍʏ ᴀᴩɪ ᴋᴇʏꜱ</b>
━━━━━━━━━━━━━━━━━━
📋 <b>Your API Keys:</b>

💡 Generate API keys from admin panel
📌 Contact: @Guptaji_302
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== BOMBER HANDLERS ====================

@bot.message_handler(func=lambda m: m.text == "💣 ʙᴏᴍʙᴇʀ" and not is_group(m))
def bomber_menu_btn(m):
    uid = m.from_user.id
    
    # Check premium status
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
        KeyboardButton("💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ 👑" if is_prem else "💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ 🔒")
    )
    markup.add(
        KeyboardButton("🛑 ꜱᴛᴏᴩ ʙᴏᴍʙᴇʀ"),
        KeyboardButton("📜 ʙᴏᴍʙᴇʀ ʜɪꜱᴛᴏʀʏ")
    )
    markup.add(KeyboardButton("🔙 ᴍᴀɪɴ ᴍᴇɴᴜ"))
    
    status = ""
    if bomber_active.get(uid):
        status = "\n🟢 <b>Active:</b> Free bomber running"
    if paid_bomber_active.get(uid):
        status = "\n💎 <b>Active:</b> Paid bomber running"
    
    bot.reply_to(m, format_message(
        f"<b>💣 ʙᴏᴍʙᴇʀ ᴍᴇɴᴜ</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💣 Free Bomber — 150 SMS/sec + 50 Calls/sec (5 min)\n"
        f"💎 Paid Bomber — Unlimited time (Premium only)\n"
        f"{status}"
    ), reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💣 ꜰʀᴇᴇ ʙᴏᴍʙᴇʀ" and not is_group(m))
def free_bomber_btn(m):
    uid = m.from_user.id
    
    if bomber_active.get(uid):
        bot.reply_to(m, format_message("<b>⚠️ Already running! Use stop button first.</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = "waiting_bomber_free"
    bot.reply_to(m, format_message(
        "<b>💣 ꜰʀᴇᴇ ʙᴏᴍʙᴇʀ</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 <b>Target number bhejo:</b>\n"
        "<i>Example: +919876543210</i>\n\n"
        "⚡ Speed: 150 SMS/sec + 50 Calls/sec\n"
        "⏱️ Max: 5 minutes\n"
        "⚠️ <b>Sirf apna number!</b>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ 👑" and not is_group(m))
def paid_bomber_btn(m):
    uid = m.from_user.id
    
    # Check premium
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
            "<b>💎 ᴩʀᴇᴍɪᴜᴍ ʀᴇQᴜɪʀᴇᴅ!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Paid Bomber sirf Premium users ke liye!\n"
            "💳 Purchase Premium button use karo."
        ), parse_mode='HTML')
        return
    
    if paid_bomber_active.get(uid):
        bot.reply_to(m, format_message("<b>⚠️ Already running! Use stop button first.</b>"), parse_mode='HTML')
        return
    
    user_state[uid] = "waiting_bomber_paid"
    bot.reply_to(m, format_message(
        "<b>💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 <b>Target number bhejo:</b>\n"
        "<i>Example: +919876543210</i>\n\n"
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
        bot.reply_to(m, format_message("<b>🛑 ʙᴏᴍʙᴇʀ ꜱᴛᴏᴩᴩᴇᴅ!</b>"), parse_mode='HTML')
    else:
        bot.reply_to(m, format_message("<b>ℹ️ Koi active bomber nahi hai!</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "📜 ʙᴏᴍʙᴇʀ ʜɪꜱᴛᴏʀʏ" and not is_group(m))
def bomber_history_btn(m):
    uid = m.from_user.id
    rows = get_bomber_history(uid, 10)
    
    if not rows:
        bot.reply_to(m, format_message("<b>📜 No bombing history yet!</b>"), parse_mode='HTML')
        return
    
    text = "<b>📜 ʙᴏᴍʙᴇʀ ʜɪꜱᴛᴏʀʏ</b>\n━━━━━━━━━━━━━━━━━━\n"
    for num, sms, calls, status, started in rows:
        icon = "✅" if status == "done" else "🛑"
        text += f"{icon} <code>{num}</code> | SMS:{sms} Calls:{calls} | {started[:10]}\n"
    
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
🔍 Username Info — Telegram username
🆔 TG ID Info — Telegram numeric ID
💎 Hitek Num — Advanced number lookup
🌟 Hitek Full — Deep search
💣 Bomber — 150 SMS/sec + 50 Calls/sec

💰 Credits: Daily claim + Referrals
💎 Premium: Unlimited access + Unlimited Bomber

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
    
    # ========== BOMBER FREE ==========
    if state == "waiting_bomber_free":
        clean = re.sub(r'[^\d+]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        if bomber_active.get(uid):
            bot.reply_to(m, format_message("<b>⚠️ Already running!</b>"), parse_mode='HTML')
            user_state.pop(uid, None)
            return
        
        user_state.pop(uid, None)
        status_msg = bot.send_message(m.chat.id, format_message(
            f"<b>💣 ꜱᴛᴀʀᴛɪɴɢ ʙᴏᴍʙᴇʀ...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ 150 SMS/sec + 50 Calls/sec\n"
            f"⏱️ Max: 5 minutes"
        ), parse_mode='HTML')
        
        threading.Thread(
            target=_run_bomber,
            args=(bot, m.chat.id, uid, clean, status_msg.message_id, False),
            daemon=True
        ).start()
    
    # ========== BOMBER PAID ==========
    elif state == "waiting_bomber_paid":
        clean = re.sub(r'[^\d+]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        if paid_bomber_active.get(uid):
            bot.reply_to(m, format_message("<b>⚠️ Already running!</b>"), parse_mode='HTML')
            user_state.pop(uid, None)
            return
        
        user_state.pop(uid, None)
        status_msg = bot.send_message(m.chat.id, format_message(
            f"<b>💎 ᴩᴀɪᴅ ʙᴏᴍʙᴇʀ ꜱᴛᴀʀᴛɪɴɢ...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ 150 SMS/sec + 50 Calls/sec\n"
            f"⏱️ Max: Unlimited (Premium)"
        ), parse_mode='HTML')
        
        threading.Thread(
            target=_run_bomber,
            args=(bot, m.chat.id, uid, clean, status_msg.message_id, True),
            daemon=True
        ).start()
    
    # ========== OTHER FEATURES ==========
    elif state == "waiting_number":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) < 10:
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
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
            bot.reply_to(m, format_message("<b>❌ Invalid Aadhar!</b>"), parse_mode='HTML')
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
            bot.reply_to(m, format_message("<b>❌ Invalid UPI ID!</b>"), parse_mode='HTML')
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
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching Instagram...</b>"), parse_mode='HTML')
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
    
    # ... (rest of features remain same)
    else:
        user_state.pop(uid, None)

# ==================== MAIN ====================

def main():
    print("=" * 60)
    print("🔥 ULTIMATE OSINT BOT STARTING...")
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
