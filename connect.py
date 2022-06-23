from binance import Client

def connect():
    api_key = 'W1lr2yxJEkRWO1HadpuVFRztEFi597q1eFDVxaH3hPNHShm0yrq38dfqzkIfzRty'
    secret_key = 'bQWl1eA0JaFJF5XXPDeKxbQl1Sqcpq6ODstcBvBRDHmzTYXPmjZY4dcrCPcCrZPH'

    client = Client(api_key, secret_key)
    return client