import requests
import ctypes
from win10toast import ToastNotifier
from time import sleep
from bs4 import BeautifulSoup
from colorama import Fore, init

init(convert=True)

last_posts_dup = []
last_posts_clean = []
latest_post = []
new_posts = []
topic = []
latest_topic = []

ctypes.windll.kernel32.SetConsoleTitleW(f"Sinister.ly Posts Notifier")
Notify = ToastNotifier()


class c:
    r = Fore.RED
    re = Fore.RESET
    y = Fore.YELLOW
    w = Fore.WHITE
    b = Fore.BLUE
    g = Fore.GREEN


def get_stats():
    url = 'https://sinister.ly/index.php'
    r = requests.get(url)
    scraper = BeautifulSoup(r.text, 'html.parser')

    for links in scraper.find_all('a'):
        try:
            if 'Thread' in links['href']:
                if 'https' in links['href']:
                    last_posts_dup.append(links['href'])
                    topic.append(links['title'])
            else:
                pass
        except Exception:
            pass

    last_posts_dup.pop(0)
    clean_links = list(dict.fromkeys(last_posts_dup))
    for sublist in clean_links:
        last_posts_clean.append(sublist)
    latest_post.append(last_posts_clean[0])
    latest_topic.append(topic[0])

    for i in last_posts_clean:
        if i == latest_post[0]:
            break
        else:
            new_posts.append(i)


def check_stats():
    try:
        if new_posts[0] is not None:
            latest_post.clear()
            latest_post.append(new_posts[0])
            print(f'\n\t\t{c.y}Found {len(new_posts)} Post{c.re}')
            send_notifications(posts=len(new_posts))
    except IndexError:
        print(f'\n\t\t{c.r}No New Posts{c.re}')


def send_notifications(posts):
    if posts == 0:
        pass

    elif posts == 1:
        Notify.show_toast(title='New Posts Available', msg=f'Topic: {latest_topic[0]}',
                          duration=10)

    else:
        Notify.show_toast(title='New Posts Available', msg=f'There Are {posts} New Posts Being Discussed On Forum.',
                          duration=10)


def get_data(post):
    if post == 1:
        r = requests.get(new_posts[0])
        soup = BeautifulSoup(r.text, 'html.parser')
        for span in soup.findAll('span'):
            span.unwrap()
        for div in soup.findAll('div'):
            div.unwrap()

        content = soup.find('div', {'class': 'post_content'})
        content = str(content).split('post_body scaleimages')
        content = content[1].split('</div>')
        content = content[0].split('">')

        content = content[1].replace('<br/>', '')

        show = f'''\n
                                TOPIC: {c.y}{latest_topic[0]}
    
        {content}{c.re}
                '''

        print(show)
        input(f'\n\n{c.b}Press Enter To Continue...')
    else:
        pass


def cleaner():
    last_posts_dup.clear()
    last_posts_clean.clear()
    new_posts.clear()
    topic.clear()
    latest_topic.clear()


def runner(duration):
    get_stats()
    check_stats()
    sleep(duration)
    cleaner()
    sleep(1)
    return runner(dur)


def about():
    about = f'''{Fore.MAGENTA}

\t\t _   _ _____ _____ _____________   __
\t\t| \ | |  _  |_   _|_   _|  ___\ \ / /
\t\t|  \| | | | | | |   | | | |_   \ V / 
\t\t| . ` | | | | | |   | | |  _|   \ /  
\t\t| |\  \ \_/ / | |  _| |_| |     | |  
\t\t\_| \_/\___/  \_/  \___/\_|     \_/  

                        \t\t{c.re}by ALDERSON41
'''
    contact = f'''
                        {c.r}CONTACT ME
    
    {c.y}sinister.ly -> {c.w}sefefew
    {c.y}instagram   -> {c.w}john_snow__41
    {c.y}Telegram    -> {c.w}@Thanos_Did_Nothing_Wrong{c.re}
    '''
    print(about)
    sleep(1)
    print(contact)

    input(f'\n\n{c.b}Press Enter To Continue...')


if '__main__' == __name__:
    about()
    sleep(1)
    dur = int(input('Enter Time To Refresh Feeds: '))
    runner(dur)