import requests
import datetime
import os

class VKStats:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def get_stats(self, start_date, end_date):
        try:
            url = 'https://api.vk.com/method/stats.get'
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            start_date = start_date.replace(tzinfo=datetime.timezone.utc)
            end_date = end_date.replace(tzinfo=datetime.timezone.utc)

            start_unix_time = int(start_date.timestamp())
            end_unix_time = int(end_date.timestamp())

            params = {
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id,
                'timestamp_from': start_unix_time,
                'timestamp_to': end_unix_time
            }
            response = requests.get(url, params=params).json()
            if 'error' in response:
                print(f"Ошибка получения статистики: {response['error']['error_msg']}")
                return None
            else:
                # Суммируем статистику за весь период
                total_views = 0
                total_visitors = 0
                total_subscribed = 0
                for day in response['response']:
                    visitors_dict = day.get('visitors', {})
                    total_views += visitors_dict.get('views', 0)  # Берем views из visitors
                    total_visitors += visitors_dict.get('visitors', 0)  # Берем visitors из visitors
                    total_subscribed += day.get('subscribed', 0)

                print(f"Статистика за {start_date.date()} - {end_date.date()}:")
                print(f"  Просмотры: {total_views}")
                print(f"  Уникальные посетители: {total_visitors}")
                print(f"  Подписки: {total_subscribed}")
                return response['response']
        except Exception as e:
            print(f"Ошибка в get_stats: {e}")
            return None

    def get_followers(self):
        try:
            url = 'https://api.vk.com/method/groups.getMembers'
            params = {
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id
            }
            response = requests.get(url, params=params).json()
            if 'error' in response:
                print(f"Ошибка получения подписчиков: {response['error']['error_msg']}")
                return None
            else:
                followers = response['response']['count']
                print(f"Количество подписчиков: {followers}")
                return followers
        except Exception as e:
            print(f"Ошибка в get_followers: {e}")
            return None

if __name__ == '__main__':
    vk_token = os.getenv("VK_TOKEN")
    group_id = 229537513  # Твой ID группы
    if vk_token and group_id:
        stats = VKStats(vk_token, group_id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        stats.get_stats(week_ago, today)
        stats.get_followers()
    else:
        print("Добавь VK_TOKEN и укажи group_id!")