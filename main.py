import vk, time, os, csv


COUNT_OF_USERS = 50 # max 1000
DEFAULT_COUNT_OF_POSTS = 100 # max 100
PATH = "./users" # workpath, not absolute
CITY=82 # city id ; current: Magnitogorsk
session = vk.Session(access_token='17e23255e45746d368acf6cb7a21d136598a240b9a38efdf44e985497425b950965c3ddd39a118ccfeb9b')
api = vk.API(session, v='5.52', lang='ru', timeout=10)


def getinfo(id):
    info = api.users.get(user_ids=id, fields='uid, first_name, last_name, sex, bdate, city, country, home_town, education, followers_count, occupation')
    return info

def write_post(post_id,text,id):
    file = open(PATH+"/"+str(id)+"/"+str(post_id)+".txt","w")
    file.write(text)
    file.close()

def get_posts(id):
    posts = api.wall.get(owner_id=id, filter='owner', extended='0', count=100)
    if posts['count'] > 100:
        rng = 100
    else:
        rng = posts['count']

    for x in range(rng-1):
        print("Обработка постов: "+str(x)+"/"+str(rng-1))
        if posts['items'][x]['text'] != "":
            write_post( posts['items'][x]['id'], posts['items'][x]['text'], id )




def check_dir(path,id):
    if os.path.exists(path+"/"+str(id)):
        return True
    else:
        return False

def check_file(path,id=""):
    if os.path.exists(path):
        return True
    else:
        return False

def create_dir(path,id=""):
        if check_dir(path,id) == False:
            os.mkdir(path+"/"+str(id))








def main():
    create_dir(PATH)
    #uid, first_name, last_name, sex, bdate, city, country, home_town, education, followers_count, occupation')
    headers = ["id пользователя", "имя", "пол", "дата рождения", "город", "страна", "количество подписчиков"]
    metainfo = []
    users = api.users.search(city=CITY,count=COUNT_OF_USERS, offset=500)
    with open("metainfo.csv",'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow(headers)
    for x in range(COUNT_OF_USERS-1):
        print("Обработка пользователей: "+str(x)+"/"+str(COUNT_OF_USERS-1))
        create_dir(PATH, users['items'][x]['id'])
        #print(getinfo(users['items'][x]['id']))
        gUsers = getinfo(users['items'][x]['id'])
        #print(gUsers[0])
        print("\n=====\n")
        #print(gUsers[0]['alo'])
        if 'bdate' not in gUsers[0]:
            gUsers[0]['bdate'] = ""
        if gUsers[0]['sex'] == 1:
            gUsers[0]['sex'] = "Женский"
        elif gUsers[0]['sex'] == 2:
            gUsers[0]['sex'] = "Мужской"
        metainfo = [gUsers[0]['id'], gUsers[0]['first_name'] + " " + gUsers[0]['last_name'], gUsers[0]['sex'], gUsers[0]['bdate'], gUsers[0]['city']['title'],gUsers[0]['country']['title'],gUsers[0]['followers_count']]
        print(metainfo)
        with open("metainfo.csv",'a') as csv_file:
            wr = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
            wr.writerow(metainfo)




        get_posts(users['items'][x]['id'])
        time.sleep(1)





if __name__ == '__main__':
    main()
