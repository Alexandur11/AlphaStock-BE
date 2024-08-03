from app.api.fetches.news_fetches import fetch_news_from_alpha_vantage
import pandas as pd

def alpha_vantage_news(symbol:str):
    data = fetch_news_from_alpha_vantage(symbol)
    news = {'Title':data['title'],
            'Url':data['url'],
            'Time':data['time_published'],
            'Image':data['banner_image']}

    return news

