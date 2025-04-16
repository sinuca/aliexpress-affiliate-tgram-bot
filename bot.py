#!/usr/bin/env python
# coding: utf-8



# In[1]:

import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import requests, json
from urllib.parse import urlparse, parse_qs
from keep_alive import keep_alive
import pprint
from dotenv import load_dotenv
import os

# In[2]:

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
  
aliexpress = AliexpressApi(os.getenv('APP_KEY'), os.getenv('APP_SECRET'),
                           models.Language.PT, models.Currency.BRL, os.getenv('TRACKING_ID'))
# In[3]:

keyboardStart = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton("⭐️Jogos de colecionar moedas⭐️",
                                  callback_data="games")
btn2 = types.InlineKeyboardButton("⭐️Desconto monetário em produtos da cesta 🛒⭐️",
                                  callback_data='click')
btn4 = types.InlineKeyboardButton("🎬 Veja como o bot funciona 🎬",
                                  url="https://t.me/dongximusiccc")
btn5 = types.InlineKeyboardButton(
    "💰 Baixe o aplicativo Aliexpress clicando aqui para ganhar uma recompensa de US$ 5 💰",
    url="https://a.aliexpress.com/_mtV0j3q")
keyboardStart.add(btn1, btn2, btn4, btn5)

keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton("⭐️Jogos de colecionar moedas⭐️",
                                  callback_data="games")
btn2 = types.InlineKeyboardButton("⭐️Desconto monetário em produtos da cesta 🛒⭐️",
                                  callback_data='click')
btn3 = types.InlineKeyboardButton("❤️ Inscreva-se no canal para mais promoções ❤️",
                                  url=os.getenv('CHANNEL_LINK'))

keyboard.add(btn1, btn2, btn3)

keyboard_games = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton(
    " ⭐️ Página de revisão diária e coleta de pontos ⭐️",
    url="https://s.click.aliexpress.com/e/_on0MwkF")
btn2 = types.InlineKeyboardButton(
    "⭐️ Jogo Merge boss ⭐️", url="https://s.click.aliexpress.com/e/_DlCyg5Z")
btn3 = types.InlineKeyboardButton(
    "⭐️ Jogo Fantastic Farm ⭐️",
    url="https://s.click.aliexpress.com/e/_DBBkt9V")
btn4 = types.InlineKeyboardButton(
    "⭐️ Jogo Vire e Ganhe ⭐️",
    url="https://s.click.aliexpress.com/e/_DdcXZ2r")
btn5 = types.InlineKeyboardButton(
    "⭐️ Jogo GoGo Match ⭐️", url="https://s.click.aliexpress.com/e/_DDs7W5D")
keyboard_games.add(btn1, btn2, btn3, btn4, btn5)

# In[4]:


@bot.message_handler(commands=['start'])
def welcome_user(message):
  bot.send_message(
      message.chat.id,
      "Por favor, envie-nos o link do produto que deseja comprar para que possamos lhe oferecer o melhor preço 👌 \n",
      reply_markup=keyboardStart)


@bot.callback_query_handler(func=lambda call: call.data == 'click')
def button_click(callback_query):
#   bot.edit_message_text(chat_id=callback_query.message.chat.id,
#                         message_id=callback_query.message.message_id,
#                         text="...")

  # Send a message with text
  #bot.send_message(callback_query.message.chat.id, "This is the message text.")

  text = "✅1- Entre no carrinho por aqui:\n" \
         " https://s.click.aliexpress.com/e/_opGCtMf \n" \
         "✅2- Escolha os produtos que deseja reduzir o preço\n" \
         "✅3- Clique no botão de pagamento para ser redirecionado para a página de confirmação\n" \
         "✅4- Clique no ícone acima e copie o link aqui no bot para obter o link de desconto"

  img_link1 = "https://picsum.photos/1022/771"
  bot.send_photo(callback_query.message.chat.id,
                 img_link1,
                 caption=text,
                 reply_markup=keyboard)


# In[5]:


def get_affiliate_links(message, message_id, link):
  try:

  
    affiliate_links = aliexpress.get_affiliate_links(
        f'https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl={link}?sourceType=561&aff_fcid='
    )
    pprint.pp(affiliate_links)
    affiliate_link = super_links = limit_links = affiliate_links[0].promotion_link

    try:
      img_link = aliexpress.get_products_details([
          '1000006468625',
          f'https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl={link}'
      ])
      pprint.pp(img_link)
      price_pro = img_link[0].target_sale_price
      title_link = img_link[0].product_title
      img_link = img_link[0].product_main_image_url
      bot.delete_message(message.chat.id, message_id)
    #   bot.send_photo(message.chat.id,
    #                  img_link,
    #                  caption=" \nSeu produto é: 🔥 \n"
    #                  f"{title_link} 🛍 \n"
    #                  f"Preço do produto: "
    #                  f"{price_pro} 💵\n"
    #                  "\nCompare preços e compre 🔥 \n"
    #                  "💰 Exibição de moeda (preço final na finalização da compra): \n"
    #                  f"Link {affiliate_link} \n"
    #                  f"💎 Super oferta: \n"
    #                  f"Link {super_links} \n"
    #                  f"♨️ Oferta limitada: \n"
    #                  f"Link {limit_links} \n\n"
    #                  "#AliXPromotion ✅",
    #                  reply_markup=keyboard)
      bot.send_photo(message.chat.id,
                     img_link,
                     caption=" \nSeu produto é: 🔥 \n"
                     f"{title_link} 🛍 \n"
                     f"Preço do produto: "
                     f"{price_pro} 💵\n"
                     f"\nLink {affiliate_link}",
                     reply_markup=keyboard)

    except:

      bot.delete_message(message.chat.id, message_id)
      bot.send_message(message.chat.id, "Compare preços e compre 🔥 \n"
                       "💰 Exibição de moeda (preço final na finalização da compra): \n"
                       f"Link {affiliate_link} \n"
                       f"💎 Super oferta: \n"
                       f"Link {super_links} \n"
                       f"♨️ Oferta limitada: \n"
                       f"Link {limit_links} \n\n"
                       "#AliXPromotion ✅",
                       reply_markup=keyboard)

  except Exception as e:
    bot.send_message(message.chat.id, "Algo deu errado 🤷🏻‍♂️ \n " + str(limit_links))


# In[6]:
def extract_link(text):
  # Regular expression pattern to match links
  link_pattern = r'https?://\S+|www\.\S+'

  # Find all occurrences of the pattern in the text
  links = re.findall(link_pattern, text)

  if links:
    return links[0]


def build_shopcart_link(link):
  params = get_url_params(link)
  shop_cart_link = "https://www.aliexpress.com/p/trade/confirm.html?"
  shop_cart_params = {
      "availableProductShopcartIds":
      ",".join(params["availableProductShopcartIds"]),
      "extraParams":
      json.dumps({"channelInfo": {
          "sourceType": "620"
      }}, separators=(',', ':'))
  }
  return create_query_string_url(link=shop_cart_link, params=shop_cart_params)


def get_url_params(link):
  parsed_url = urlparse(link)
  params = parse_qs(parsed_url.query)
  return params


def create_query_string_url(link, params):
  return link + urllib.parse.urlencode(params)


## Shop cart Affiliate تخفيض السلة
def get_affiliate_shopcart_link(link, message):
  try:
    shopcart_link = build_shopcart_link(link)
    affiliate_link = aliexpress.get_affiliate_links(
        shopcart_link)[0].promotion_link

    text2 = f"Este é o link para o desconto no carrinho. \n" \
           f"{str(affiliate_link)}" \

    img_link3 = "https://picsum.photos/1022/771"
    bot.send_photo(message.chat.id, img_link3, caption=text2)

  except:
    bot.send_message(message.id, "Algo deu errado 🤷🏻‍♂️")


@bot.message_handler(func=lambda message: True)
def get_link(message):
  link = extract_link(message.text)

  sent_message = bot.send_message(message.chat.id,
                                  'Aguarde um momento, as ofertas estão sendo preparadas ⏳')
  message_id = sent_message.message_id
  if link and "aliexpress.com" in link and not ("p/shoppingcart"
                                                in message.text.lower()):
    if "availableProductShopcartIds".lower() in message.text.lower():
      get_affiliate_shopcart_link(link, message)
      return
    get_affiliate_links(message, message_id, link)

  else:
    bot.delete_message(message.chat.id, message_id)
    bot.send_message(message.chat.id,
                     "O link é inválido! Verifique o link do produto ou tente novamente.\n"
                     "Envie apenas o link sem o título do produto.",
                     parse_mode='HTML')
  

# In[7]:


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
  bot.send_message(call.message.chat.id, "..")

  img_link2 = "https://picsum.photos/784/449"
  bot.send_photo(
      call.message.chat.id,
      img_link2,
      caption=
      "Links para jogos de colecionar moedas para usar para reduzir o preço de alguns produtos. Faça login diariamente para obter o maior número possível por dia 👇",
      reply_markup=keyboard_games)

  # In[ ]:


keep_alive()

bot.infinity_polling(timeout=10, long_polling_timeout=5, none_stop=True)
