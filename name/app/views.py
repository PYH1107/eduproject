from django.shortcuts import render

# Create your views here.
from app.models import *

import re
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from .models import SnakeSpecies, Product, CareRequirements

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.CHANNEL_SECRET)

# 設置日誌

logger = logging.getLogger(__name__)

@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
    body = request.body.decode('utf-8')

    # 日誌輸出
    logger.info(f"Request body: {body}")
    logger.info(f"Signature: {signature}")

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature error")
        return HttpResponseForbidden()
    except LineBotApiError as e:
        logger.error(f"LineBotApiError: {str(e)}")
        return HttpResponseBadRequest()

    for event in events:
        if isinstance(event, MessageEvent):
            handle_message(event)

    return HttpResponse('OK')

def handle_message(event):
    message_text = event.message.text.strip()
    if "蛇的學名" in message_text:
        scientific_name = extract_scientific_name(message_text)
        species_exists = SnakeSpecies.objects.filter(scientific_name=scientific_name).exists()
        if species_exists:
            reply_text = f"蛇類 {scientific_name} 已經存在於資料庫中。"
        else:
            reply_text = f"您所輸入的蛇類不存在，請您建立新的檔案。若要建立，請回覆 OK"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    elif "new" in message_text:
        # 调用 handle_snake_species 并传递 message_text，这个函数负责发送回复
        handle_snake_species(event, message_text)
    elif "【學名】" in message_text:
        handle_read(event, message_text)
    elif "刪除產品編號" in message_text:
        handle_delete(event, message_text)
    elif "更新" in message_text:
        handle_update(event, message_text)


def extract_scientific_name(text):
    # 假设用户会按照【學名】snake的格式输入
    pattern = r'蛇的學名[:：](.+)'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def extract_scientific_name2(text):
    # 假设用户会按照【學名】snake的格式输入
    pattern = r'【學名】(\w+\s?\w*)'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def handle_snake_species(event, message_text):
    data = parse_data(message_text)
    if data:
        species, created = SnakeSpecies.objects.get_or_create(
            scientific_name=data['scientific_name'],
            chinese_name=data['chinese_name'],
            defaults={'amount': data['amount']}
        )
        if created:
            #reply_text = f"儲存成功，蛇類編號為 {species.id}" //這個有錯，好像讀不出來整個掰掰
            reply_text = "儲存成功"
        else:
            reply_text = "儲存失敗"
    else:
        reply_text = "儲存失敗，請確認訊息格式是否有誤"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

def parse_data(text):
    pattern = r'.*\n【學名】(\w+)\n【中文名稱】(\S+)\n【數量】(\d+)'
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return {
            'scientific_name': match.group(1),
            'chinese_name': match.group(2),
            'amount': int(match.group(3))
        }
    return None


def handle_read(event, message_text):
    # 提取学名
    scientific_name = extract_scientific_name2(message_text)
    if not scientific_name:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式错误,请重新输入。"))
        return

    # 查询数据库,获取所有匹配的 SnakeSpecies 对象
    matching_species = SnakeSpecies.objects.filter(scientific_name=scientific_name)
    if matching_species:
        # 构建产品名称列表
        product_names = [f"{species.chinese_name} (數量: {species.amount})" for species in matching_species]
        product_names_str = "\n".join(product_names)
        reply_text = f"以下是與學名 '{scientific_name}' 匹配的產品:\n\n{product_names_str}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

        return

    # 如果没有匹配的对象
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="没有找到对应的蛇类。"))
    return


def handle_update(event, message_text):
    pattern = r'【產品編號:(\d+)】(\d+)'
    match = re.search(pattern, message_text)
    if match:
        product_id, new_price = match.groups()
        try:
            # 尝试获取产品
            product = Product.objects.get(product_id=int(product_id))
            # 更新价格
            product.price = float(new_price)
            product.save()
            reply_text = f"產品編號 {product_id} 的價格已更新為 {new_price}"
        except Product.DoesNotExist:
            reply_text = f"没有找到產品編號 {product_id} 的產品。"
        except Exception as e:
            reply_text = f"錯誤: {str(e)}"
    else:
        reply_text = "格式錯誤"
    # 发送回复消息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

def handle_delete(event, message_text):
     # 假设用户输入格式为：“【刪除產品編號】12345”
    pattern = r'【刪除產品編號】(\d+)'
    match = re.search(pattern, message_text)
    if not match:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="格式錯誤"))
        return

    product_id = int(match.group(1))
    try:
        product = Product.objects.get(product_id=product_id)
        product.delete()
        reply_text = f"產品編號 {product_id} 已成功删除。"
    except Product.DoesNotExist:
        reply_text = f"沒有找到 {product_id} "
    except Exception as e:
        reply_text = f"刪除過程中出現錯誤 {str(e)}"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))