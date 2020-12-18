from decimal import Decimal
import time, json
import paralleldots
from firebase_dynamic_links import DynamicLinks

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
import requests
from wordpress_xmlrpc.compat import xmlrpc_client

import sys
from telebot import types
import datetime
from rfc3339 import rfc3339
import telebot, random
import urllib.parse,pymongo

# pipenv install dnspython pymongo paralleldots py-firebase-dynamic-links python-wordpress-xmlrpc pyTelegramBotAPI rfc3339

#dnspython important requirement for pymongo


myclient = pymongo.MongoClient("mongodb+srv://kanu00047:Theindian%2337@cluster0.hnbfn.mongodb.net")
mydb = myclient["wpdeals"]["id"]

bot = telebot.TeleBot("1253877355:AAFa9jQklf81eRJy84mRuni-FQ0Cl_-OyCI")

from urllib.parse import urlparse, urlunparse

def amazonify(url, affiliate_tag):
    new_url = urlparse(url)
    if not new_url.netloc:
        return None
    new_url = new_url[:4] + ('tag=%s' % affiliate_tag,) + new_url[5:]

    return urlunparse(new_url)

affiliate_tag = 'thebatball01-21'

def is_number(value):
    try:
        value = Decimal(value)
        return True
    except:
        return False


def get_cue_url(url1):
    try:
        # url = 'https://flipkart.com'
        cc = requests.get(url1)
        url = cc.url
        cc.close()
        # print(url)
        a = urllib.parse.quote(url, safe='')
        # so new cuelinks url will be
        b = 'https://linksredirect.com/?cid=90202&source=linkkit&url='
        complete_url = b + a
        return complete_url
    except:
        bot.send_message("1072778890", "CueLink Generation Error :{}".format(sys.exc_info()))
        return url1



def get_flipkart_url(url):
    try:
        cc = requests.get(url)
        url = cc.url
        cc.close()
        # a = urllib.parse.quote(url,safe='')
        a = url
        a = a.replace("https://www.flipkart.com", "https%3A%2F%2Fdl.flipkart.com%2Fdl")
        b = 'https://tracking.vcommission.com/aff_c?offer_id=412&aff_id=105964&aff_click_id=DL&url='
        c = '?affid=vcommission&affExtParam1={transaction_id}'
        c = urllib.parse.quote(c, safe='')
        complete_url = b + a + c
        return complete_url
    except:
        bot.send_message("1072778890", "Vcommission Link Generation Error :{}".format(sys.exc_info()))
        return url


def getlink(link):
    try:
        api_key = 'AIzaSyA-0APSMxy1NUaNnE3zlJDurApSIxkEAMo'
        domain = 'TheBatBall.page.link'
        timeout = 10
        dl = DynamicLinks(api_key, domain, timeout)

        params = {
            "androidInfo": {
                "androidPackageName": 'com.kanucreator.schoolapp',
                "androidFallbackLink": '{}'.format(link),
                "androidMinPackageVersionCode": '1'
            },
        }
        short_link = dl.generate_dynamic_link('{}'.format(link), True, params)
        if short_link.strip():
            return short_link
        else:
            return link
    except Exception as e:
        bot.send_message("1072778890", "Vcommission Link Generation Error :{}".format(sys.exc_info()))
        return link


def get_tags(text):
    try:
        apikeys = ['sbCAKkmDXLeVFlwUggchzrfi6QPxiVxQ8TOR2WSTZ6o', 'AB9epViJqge4rlRnNhLDkqKQamt43cJVNL64awyFzb4']
        apikey = random.choice(apikeys)

        paralleldots.set_api_key(apikey)

        keywords = paralleldots.keywords(text)

        keyword_list = []
        for key in keywords['keywords']:
            keyword_list.append(key['keyword'])

        if len(keyword_list) == 0:
            exception = []
            exception.append('No Tags')

            bot.send_message("1072778890", "Tags Paralleldots Generation Error :{}".format(sys.exc_info()))
            return exception

        else:
            return keyword_list

    except:
        exception = []
        exception.append('No Tags')
        return exception


def dealsmaker(link):
    global imageid, storename, shortlink
    url = "{}".format(link)
    headers = {"X-Desidime-Client": "ecaccbae49c742f184b46cd0c93bf4bba517e3d5cf8647305a097defbaf1edb8"}

    respponse = requests.get(url, headers=headers)

    json_load = json.loads(respponse.text)
    data = json_load['deals']

    sleep_time = 0

    for res in data:
        id1 = res['id']

        search_key = "{}".format(id1)

        myquery = {"id": search_key}
        mydoc = mydb.find_one(myquery)



        if mydoc == None:

            post_data = {
                'id': '{}'.format(id1),
            }
            result = mydb.insert_one(post_data)

            title = res['title']
            discount = res['current_price']
            original = res['retail_price']
            details = res['description']
            percentoff = res['percent_off']
            top_deal_bool = res['top_deal']
            hotness = res['life_time_hotness']
            link = res['deal_url']

            details = details.replace("https://links.desidime.com?ref=deal&url=",
                                      "https://linksredirect.com/?cid=90202&source=linkkit&url=")
            details = details.replace("https://links.desidime.com/?ref=deal&url=",
                                      "https://linksredirect.com/?cid=90202&source=linkkit&url=")

            forum = res['forum']['forum_type'].upper()
            imagelink = res['image_medium']
            imagelink = imagelink.replace("medium", "original")


            if link != None:
                orilinksep = "url="
                originallink = link.partition(orilinksep)[2]
                try:
                    if originallink.__contains__("amazon.in") or "amazon.in" in originallink:
                        deallink = amazonify(originallink, affiliate_tag=affiliate_tag)

                    elif originallink.__contains__("amazon.com") or "amazon.com" in originallink:
                        deallink = amazonify(originallink, affiliate_tag=affiliate_tag)

                    elif originallink.__contains__("flipkart.com") or "flipkart.com" in originallink:

                        deallink = get_cue_url(originallink)
                    else:
                        deallink = get_cue_url(originallink)

                    shortlink = getlink(deallink)
                except:
                    deallink = getlink(originallink)
                    shortlink = getlink(originallink)
            else:
                deallink = ""
                shortlink = ""

            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.row_width = 1
            reply_markup.add(types.InlineKeyboardButton("Click Here to Buy Now", "{}".format(deallink)))

            textforimg = res['permalink']

            if res['store'] != None:
                storename = res['store']['name']
                storelink = res['store']['image']
            else:
                storelink = ''

            wp = Client('https://thebatball.com/xmlrpc.php', 'kanu00047', 'OAHX 7H6o ePzb Sisw 2f4w MvJN')

            try:
                response = requests.get(imagelink)
                if response.status_code == 200:
                    with open("picture.jpg", 'wb') as f:
                        f.write(response.content)
                        f.close()

                data = {
                    'name': '{}.jpg'.format(textforimg),
                    'type': 'image/jpeg',
                }

                with open('picture.jpg', 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())

                response = wp.call(media.UploadFile(data))
                img.close()
                imageid = response['id']
            except:
                bot.send_message("1072778890", "Wp Image Uploader Generation Error :{}".format(sys.exc_info()))

            if percentoff != None:
                hi = "huh"
            else:
                percentoff = 0

            if forum != "DISCUSSTION":
                if forum != "NEWS":
                    widget = WordPressPost()
                    widget.post_type = 'post'
                    widget.title = '{}'.format(title)
                    widget.content = '{}'.format(details)
                    widget.post_status = 'publish'
                    if imageid != None:
                        widget.thumbnail = imageid
                    widget.comment_status = 'open'
                    widget.custom_fields = []

                    widget.custom_fields.append({
                        'key': 'rehub_offer_product_url',
                        'value': '{}'.format(deallink)
                    })
                    widget.custom_fields.append({
                        'key': 'rehub_offer_name',
                        'value': '{}'.format(title)
                    })

                    if is_number(discount):
                        widget.custom_fields.append({
                            'key': 'rehub_offer_product_price',
                            'value': '₹{}'.format(discount)
                        })
                    else:
                        widget.custom_fields.append({
                            'key': 'rehub_offer_btn_text',
                            'value': "CHECK IT NOW"
                        })
                    if is_number(original):
                        widget.custom_fields.append({
                            'key': 'rehub_offer_product_price_old',
                            'value': '₹{}'.format(original)
                        })
                    if percentoff >= 60:
                        widget.custom_fields.append({
                            'key': 'is_editor_choice',
                            'value': 3
                        })
                    elif top_deal_bool == True:
                        widget.custom_fields.append({
                            'key': 'is_editor_choice',
                            'value': 2
                        })

                    if is_number(hotness):
                        widget.custom_fields.append({
                            'key': 'post_hot_count',
                            'value': '{}'.format(hotness)
                        })

                    if storelink != None or storelink != "":
                        widget.custom_fields.append({
                            'key': 'rehub_offer_logo_url',
                            'value': "{}".format(storelink)
                        })

                    try:

                        expinmills = res['expiry_date_in_millis']

                        time_in_millis = int('{}'.format(expinmills))
                        dt = datetime.datetime.fromtimestamp(time_in_millis / 1000.0, tz=datetime.timezone.utc)
                        converted_to_str = rfc3339(dt, utc=True, use_system_timezone=False)
                        date1 = "T"
                        parsed_date = converted_to_str.partition(date1)[0]
                        widget.custom_fields.append({
                            'key': 'rehub_offer_coupon_date',
                            'value': '{}'.format(parsed_date)
                        })
                    except:
                        bot.send_message("1072778890", "Time Generation Deal Expiring :{}".format(sys.exc_info()))

                    my_list = []

                    for categories in res['system_groups']:
                        my_list.append(categories['name'])

                    if len(my_list) == 0:
                        my_list.append("No Category")

                    tags = get_tags(title + details + "".format(my_list))
                    # print(tags)

                    widget.terms_names = {
                        'category': my_list,
                        'post_tag': tags
                    }

                    try:
                        widget.id = wp.call(posts.NewPost(widget))
                        # print(widget.id)
                    except:
                        bot.send_message("1072778890", "Deal Uploading Failed :{}".format(sys.exc_info()))

                    if widget.id !=None:
                        tbbink = "https://thebatball.com/?p={}".format(widget.id)
                    else:
                        tbbink = "https://thebatball.com"
                    channelid = "-1001459616879"

                    image1 = requests.get("{}".format(imagelink), stream=True).content
                    try:
                        storename = storename.replace(" ", "")
                    except:
                        yup = "bhoot"


                    try:
                        if forum != "DISCUSSTION":
                            if forum != "NEWS":
                                if is_number(discount):
                                    if is_number(original):
                                        bot.send_photo(channelid, image1,
                                                       "<b>{}</b> @₹{} \n\n<b>Discount Price</b> : ₹{}\n<b>Original Price</b> : <s>₹{}</s>\n\n<b>Read more</b> : {}\n<b>Deal Link : </b>{}".format(
                                                           title, discount, discount, original, tbbink,
                                                           shortlink) + "\n#{}".format(storename),
                                                       parse_mode="HTMl", reply_markup=reply_markup)
                                    else:
                                        bot.send_photo(channelid, image1,
                                                       "<b>{}</b> @₹{}\n\n<b>Read more</b> : {}\n<b>Deal Link : </b>{}".format(
                                                           title, discount,
                                                           tbbink, shortlink) + "\n#{}".format(storename),
                                                       parse_mode="HTMl", reply_markup=reply_markup)

                                else:
                                    if is_number(original):
                                        bot.send_photo(channelid, image1,
                                                       "<b>{}</b> @₹{} \n<b>Price</b> : ₹{}\n\n<b>Read more</b> : {}\n<b>Deal Link : </b>{}".format(
                                                           title, discount, original,
                                                           tbbink, shortlink) + "\n#{}".format(storename),
                                                       parse_mode="HTMl", reply_markup=reply_markup)
                                    else:
                                        bot.send_photo(channelid, image1,
                                                       "<b>{}</b>\n\n<b>Read more</b> : {}\n<b>Deal Link : </b>{}".format(
                                                           title, tbbink, shortlink) + "\n#{}".format(storename),
                                                       parse_mode="HTMl", reply_markup=reply_markup)
                    except:
                        bot.send_message("1072778890", "Telegram Error :{}".format(sys.exc_info()))


                    with open("dealsid.txt", 'a') as u:
                        u.write("{}\n".format(widget.id))
                        u.close()


                    time.sleep(sleep_time)
            else:
                hi = ""
                # print("discussion or news")


allinoneparams = "?fields=id,is_created_from_merchant_hub,is_current_user_allow_to_edit_deal_wiki,is_current_user_following,permalink,title,retail_price,percent_off,shipping_and_handling,top_deal,posts_count,comments_count,created_at,created_at_in_millis,expiry_date_in_millis,score,description,deal_url,share_url,life_time_hotness,vote_value,deal_tag,added_to_channel,workflow_state,wiki_html,current_price,image_medium,view_count,user{id,login,image_medium,karma,current_title},store{name,image,permalink},festivals{permalink,name,image},deal_types,forum{permalink,name,forum_type},first_post_id,is_current_user_group,is_current_user_allow_to_edit,unapproved_topic_message,is_current_user_have_group,display_hotness_icon,system_groups,poll,show_create_poll_option,referral_state,current_referral,referral_submitted,wiki_created_or_updated_details"
params = '?fields=id,deal_url,title,current_price,retail_price,percent_off,top_deal,image_medium,created_at,comments_count,life_time_hotness,user{id,login,image_medium,current_title},store{permalink,name,image},description,permalink,posts_count,vote_value,deal_types,view_count,app_versions,forum{forum_type},workflow_state,display_hotness_icon,referral_state'
couponsparam = "?fields=coupon_code,id,title,coupon_type,description,discount,redemption_count,expiry_date_in_millis,share_url,store{name,image,permalink},coupon_url"

for i in range(100):
    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=1&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=1&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=2&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=2&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=3&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=4&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=5&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=3&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=4&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=5&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=6&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=7&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=8&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=9&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=1&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=6&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home" + allinoneparams + "&type=hot&page=8&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=6&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=3&per_page=100")

    dealsmaker("https://auth.desidime.com/v4/home/new" + allinoneparams + "&type=new&page=7&per_page=100")
