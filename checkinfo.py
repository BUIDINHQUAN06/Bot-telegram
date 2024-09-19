import requests
from datetime import datetime
import telebot

API_TOKEN = '6946067120:AAES7niiQScRbmgJyP6Wpc9eCf1Z3KH7iG0'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['check'])
def check_command(message):
    try:
        id = message.text.split()[1]  # Lấy id từ câu lệnh
        response = requests.get(f"https://api.ducknha.site/api.php?id={id}")
        data = response.json()

        if 'status' in data and data['status'] == 'success':
            user_data = data.get('data', {})

            if user_data.get('idtk') is None:
                bot.reply_to(message, "Không Xác Định")
            else:
                idtk = user_data['idtk']
                date_create = user_data['datecreate']
                date_create = datetime.strptime(date_create, '%Y-%m-%dT%H:%M:%S+0000') if date_create else ''
                formatted_date_create = date_create.strftime('%H:%M:%S | %d/%m/%Y') if date_create else 'Không Xác Định'

                user = user_data['user'] if user_data.get('user') is not None else 'Không Xác Định'
                link = user_data['link'] if user_data.get('link') is not None else 'Không Xác Định'
                name = user_data['name'] if user_data.get('name') is not None else 'Không Xác Định'

                if 'birthday' in user_data and user_data['birthday'] is not None:
                    if '/' in user_data['birthday']:
                        parts = user_data['birthday'].split('/')
                        if len(parts) == 3:  # Nếu có năm sinh
                            birthday = f"{parts[1]}/{parts[0]}/{parts[2]}"
                        elif len(parts) == 2:  # Nếu chỉ có tháng và ngày
                            birthday = f"{parts[1]}/{parts[0]}"
                        else:
                            birthday = 'Không Xác Định'
                    else:
                        birthday = 'Không Xác Định'
                else:
                    birthday = 'Không Xác Định'

                gender = user_data['gender'] if user_data.get('gender') is not None else 'Không Xác Định'
                relationship = user_data['relationship'] if user_data.get('relationship') is not None else 'Không Xác Định'
                location = user_data['location'] if user_data.get('location') is not None else 'Không Xác Định'
                timezone = user_data['timezone'] if user_data.get('timezone') is not None else 'Không Xác Định'
                followers = "{:,}".format(user_data['follow']) if user_data.get('follow') is not None else 'Không Xác Định'
                locale = user_data['locale'] if user_data.get('locale') is not None else 'Không Xác Định'
                website = user_data['website'] if user_data.get('website') is not None else 'Không Xác Định'

                reply_text = (  
                    f"ID: {idtk}\n"
                    f"Ngày Tạo: {formatted_date_create}\n"
                    f"Username: {user}\n"
                    f"Url: {link}\n"
                    f"Họ Tên: {name}\n"
                    f"Sinh Nhật: {birthday}\n"
                    f"Giới Tính: {gender}\n"
                    f"Tình Trạng: {relationship}\n"
                    f"Nơi Sống: {location}\n"
                    f"Ngôn Ngữ: {locale}\n"
                    f"Thời Gian Vùng: {timezone}\n"
                    f"Số Người Theo Dõi: {followers}\n"
                    f"Website: {website}\n"             
                )

                bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "Lỗi: Không thể lấy thông tin từ API.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi: Có lỗi xảy ra: {e}")

bot.polling()
