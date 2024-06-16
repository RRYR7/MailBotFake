# copyright 2020-22 @Mohamed Rizad
# Telegram @riz4d
# Instagram @riz.4d
from pyrogram import *
import requests as re
from Config import *
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import wget
import os 

buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('- إنشـاء بريـد وهمـي 📧', callback_data='generate'),
            InlineKeyboardButton('تغييـر الإيمـيـل 📤', callback_data='refresh'),
            InlineKeyboardButton('إغلاق ❌', callback_data='close')
                   ] 
                             ])

msg_buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('إظهـار الرسائـل 📪', callback_data='view_msg'),
            InlineKeyboardButton('إغلاق ❌', callback_data='close')
                   ] 
                             ])


app=Client('Temp-Mail Bot',
           api_id=API_ID,
           api_hash=API_HASH,
           bot_token=BOT_TOKEN)

email=''
@app.on_message(filters.command('start'))
async def start_msg(client,message):
    await message.reply("**✧ مرحبًـا بك "+message.from_user.first_name+" !!**\n هـذا هـوَ بوت مقـدم من سـورس تيبثـون العربي 🇵🇸 يقوم بإنشـاء بريـد وهمـي يُمكنك استقبال الرسائل عليه")
    await message.reply("**Generate a Email Now❕**",
                        reply_markup=buttons)
@app.on_callback_query()
async def mailbox(client,message):
    response=message.data
    if response=='إنشـاء بريـد وهمـي 📧':
       global email
       email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
       await message.edit_message_text('__**هـذا هـو البريـد الخــاص بك 📧: **__`'+str(email)+'`',
                                       reply_markup=buttons)
       print(email)
    elif response=='تغييـر الإيميـل 📤':
        print(email)
        try:
            if email=='':
                await message.edit_message_text('إنشـاء بريـد وهمـي 📧',reply_markup=buttons)
            else: 
                getmsg_endp =  "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum=str(ref_response[0]['id'])
                from_msg=ref_response[0]['from']
                subject=ref_response[0]['subject']
                refreshrply='You a message from '+from_msg+'\n\nSubject : '+subject
                await message.edit_message_text(refreshrply,
                                                reply_markup=msg_buttons)
        except:
            await message.answer('لا يوجـد رسائل واردة حتـى الآن ❌'+email)
    elif response=='view_msg':
        msg =re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail=msg['from']
        date=msg['date']
        subjectt=msg['subject']
        try:
          attachments=msg['attachments'][0]
        except:
            pass
        body=msg['body']
        mailbox_view='رقم بطاقة الهوية : '+idnum+'\nمن : '+from_mail+'\nالتاريخ : '+date+'\nالموضوع : '+subjectt+'\nالرسالـة : \n'+body
        await message.edit_message_text(mailbox_view,reply_markup=buttons)
        mailbox_view='رقم بطاقة الهوية : '+idnum+'\nمن : '+from_mail+'\nالتاريخ : '+date+'\nالموضوع : '+subjectt+'\nالرسالـة : \n'+body
        if attachments == "[]":
            await message.edit_message_text(mailbox_view,reply_markup=buttons)
            await message.answer("لم يتم تلقي أي رسائل..", show_alert=True)
        else:
            dlattach=attachments['filename']
            attc="https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum+"&file="+dlattach
            print(attc)
            mailbox_vieww='رقم بطاقة الهوية: '+idnum+'\nمن : '+from_mail+'\nالتاريخ: '+date+'\n موضوع : '+subjectt+'\nالرسالة : \n'+body+'\n\n'+'[Download]('+attc+') Attachments'
            filedl=wget.download(attc)
            await message.edit_message_text(mailbox_vieww,reply_markup=buttons)
            os.remove(dlattach)
    elif response=='إغلاق':
        await message.edit_message_text('Session Closed✅')
app.run()

# Stay tuned for more : Instagram[@riz.4d]
