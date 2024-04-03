from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import time, re, datetime, csv, copy, operator, sys, pprint
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
# sys.exit("Error message")

t=datetime.datetime.today()

class InstagramBot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.day=t.strftime('%Y-%m-%d')
        self.exclusive=['piotrekjazz']

    def login(self):
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.set_window_position(700, 0)
        driver.set_window_size(width=50,height=600)
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher/")
        time.sleep(3)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']") 
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(4)
        notnow = driver.find_element_by_css_selector('button.HoLwm')  
        notnow.click()
        time.sleep(3)

    def reading(self, file):
        with open('D:\python\Instagram\\%s.csv' %file) as fileObj:  
            readObj = csv.reader(fileObj)
            self.matrix=list(readObj)

    def saving(self, matrix, file):
        with open('D:\python\Instagram\\%s.csv' %file, 'w', newline='') as fileObj:
            writeObj = csv.writer(fileObj)
            for k in range (len(matrix)):
                writeObj.writerow(matrix[k])
            

    def fun_page(self, site):    #adresy zdjęć ze strony firmy
        driver = self.driver
        driver.get("https://www.instagram.com/%s/" %site)
        time.sleep(2)
        pic_hrefs=[]
        self.new_hrefs=new_hrefs=[]        # nieprzeglądane w widoku
        old_hrefs=[]
        self.viewed_hrefs=viewed_hrefs=[]  # przeglądane w widoku
        for i in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            hrefs_in_view = driver.find_elements_by_tag_name('a'); 
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]; print("hrefs_in_view", hrefs_in_view)
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]   # unikalne refs
#        print("all_found_hrefs", pic_hrefs)
        self.reading('hrefs')
        matrix=self.matrix
        matrix=sorted(matrix, key=operator.itemgetter(0), reverse=False)   #sortuje rosnąco pierwszą (0) kolumnę
        [old_hrefs.append(matrix[i][1]) for i in range(len(matrix))]
        for href in old_hrefs:
            if href in pic_hrefs:
                viewed_hrefs.append(href)   
        [new_hrefs.append(href) for href in pic_hrefs if href not in old_hrefs]
        print('przejrzane zdjecia',viewed_hrefs, "\n\nnowe zdjecia", new_hrefs)

    def page_comments(self):
        driver = self.driver
        driver.get("https://www.instagram.com/p/BvydUxkIJWp/")
        time.sleep(2)
        self.reading('commy')
        matrix=self.matrix
        for i in range(4):    #przewijanie komentarzy
            try:
                comments = driver.find_elements_by_css_selector('div.Igw0E>button.dCJp8>span')
                if comments[0]: comments[0].click()
                else: break
                time.sleep(3)
            except Exception as e:
                print(e)
                continue

        x=driver.find_elements_by_class_name('Mr508') 
        print("widoczne", len(x))
        for i in range(1,len(x)+1):   
            date = driver.find_element_by_xpath("//ul[@class='XQXOT']//ul[%s]//time[@class='FH9sR Nzb55']" %(i)).get_attribute('datetime')
            date_obj=re.compile('\d\d\d\d-\d\d-\d\dT\d\d:\d\d').search(date).group()
            date =datetime.datetime.strptime(date_obj, '%Y-%m-%dT%H:%M'); print(date)
            if date > t - datetime.timedelta(days=3):
                comm = driver.find_elements_by_xpath("//ul[@class='XQXOT']/ul[%s]//span[@class='EizgU']" %(i))
                if comm:
                    comm=re.compile('\(\d*\)').search(comm[0].text).group(); comm=int(comm[1:-1])     #obcinanie nawiasów
                    #comm=re.compile('d\d\|\d').search(comm[0].text).group()
                    print("comy:", comm)
                else: comm = 0; print("comy:", comm)
                if comm<8:
                    user = driver.find_element_by_xpath("//ul[@class='XQXOT']//ul[%s]//a[@class='FPmhX notranslate TlrDj']" %(i)).text; print(user, end=", ")
                    text = driver.find_element_by_xpath("//ul[@class='XQXOT']//ul[%s]//div[@class='C4VMK']//span" %(i)).text; long=len(text);print("long:",len(text), end=", ")   #comm.encode() - by zobaczyć treść

                like = driver.find_elements_by_xpath("//ul[@class='XQXOT']//ul[%s]//a[@class='FH9sR']" %(i))
                if like:
                    like=int(re.compile('\d*').search(like[0].text).group())
                    print("lajki:",like, end=", ")
                else: like = 0

    def news_feed(self):
        driver = self.driver
        self.reading('news_feed')       
        matrix=self.matrix
        old_commented=[]
        [old_commented.append(matrix[i][1]) for i in range(len(matrix))]
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        feeds = driver.find_elements_by_css_selector("article .FPmhX.notranslate.nJAzx")  #wszyscy widzoczni
        feeds_n = [user.get_attribute('title') for user in feeds]; print("in view", feeds_n)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        feeds = driver.find_elements_by_css_selector("article .FPmhX.notranslate.nJAzx")  #wszyscy widzoczni
        feeds_n = [user.get_attribute('title') for user in feeds]; print("in view", feeds_n)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        feeds = driver.find_elements_by_css_selector("article .FPmhX.notranslate.nJAzx")  #wszyscy widzoczni
        feeds_n = [user.get_attribute('title') for user in feeds]; print("in view", feeds_n)

    def followers_check(self):    #odświerza baze obserwujących
        driver = self.driver
        driver.find_element_by_class_name('glyphsSpriteUser__outline__24__grey_9').click()   #otwiera mój profil ludek prawa góra 
        time.sleep(2)
        num=driver.find_element_by_css_selector('.SCxLW.o64aR li:nth-child(2) a').text
        num=int(re.compile('\d*').search(num).group())
        driver.find_element_by_css_selector('.SCxLW.o64aR li:nth-child(2) a').click()
        time.sleep(2)
        all_followers=[]
        end=0; last=1
        self.reading('followers')
        matrix=self.matrix
        matrix_n=[]
        self.old_followers=old_followers=[]
        [old_followers.append(matrix[i][1]) for i in range(len(matrix))]       
        while True:
            if last==end:
                print("liczba profili na stronie %s, profili napotkanych %s, stara baza obecnie poszerzona %s" %(num, len(matrix_n), len(matrix)))
                base=0
                while base.lower() !='t' and base.lower() != 'n':
                      base=input("podmieniać baze na aktualna, t/n?)
                if base=='t':
                    self.saving(matrix_n,"following");break
                else:break
            followers = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")  #wszyscy widzoczni
            followers_n = [user.text for user in followers]; #print("in view", followers_n)
            k=len(followers)
            last=followers[k-1].text
            [all_followers.append(user) for user in followers_n if user not in all_followers]; print("all", all_followers)
            for user in all_followers:
                sety=[self.day, user]
                if user not in old_followers:
                    matrix.append(sety)
                    matrix_n.append(sety)
                else: matrix_n.append(sety)
            print("followers found: ", len(matrix_n))
            self.saving(matrix,"followers")
            for i in range(2): 
                action=ActionChains(driver)
                action.move_to_element(followers[k-1]).perform()
                time.sleep(2)
                followers = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")     #button follow 
                k=len(followers)
                end=followers[k-1].text
        driver.find_element_by_css_selector('span.glyphsSpriteX__outline__24__grey_9').click()  #zamknięcie okienka followers

    def following_cleanup(self, old, maxi): 
        driver = self.driver
        self.reading('following')
        matrix=self.matrix
        old_following=[]
        [old_following.append(matrix[i][1]) for i in range(len(matrix))]
        driver.find_element_by_class_name('glyphsSpriteUser__outline__24__grey_9').click()   #otwiera mój profil ludek prawa góra 
        time.sleep(2)
        num=driver.find_element_by_partial_link_text("Obserwowani").text    #tylko a tagi w ten sposób
        num=(re.compile('\n\d*').search(num).group()); print(num.lstrip())
        driver.find_element_by_partial_link_text("Obserwowani").click() 
        time.sleep(2)
        temp_following=[]
        out=0
        end=0; last=1; no_record=0
        matrix_n=[]
        self.reading('followers')
        matrix_f=self.matrix
        old_followers=[]
        [old_followers.append(matrix_f[i][1]) for i in range(matrix_f)]
        
        while True:
            new_inview=[]
            if last==end:
                print("liczba profili na stronie %s, profili napotkanych %s, stara baza obecnie poszerzona %s" %(num, len(matrix_n), len(matrix))
                base=0
                while base.lower() !='t' and base.lower() != 'n':
                      base=input("podmieniać baze na aktualna, t/n?)      
                if base=='t':
                    self.saving(matrix_n,"following");break
                else:break
            following = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")  #wszyscy widzoczni
            k=len(following); #print("widze",k)
            following_n = [user.text for user in following]; #print("in view", following_n)
            last=following_n[k-1]; #print('last',last)
            buttons = driver.find_elements_by_xpath('//button[text() = "Obserwowanie"]')              # "followers" wszystkie widoczne przyciski follow 
            for user in following_n:
                if user not in temp_following:
                    temp_following.append(user)  #wszyscy wyświetleni w tej sesji
                    new_inview.append(user)  #nowi w widoku
#            print("temp_following", temp_following); print("new inview", new_inview)
            for user in new_inview:
                if user not in self.exclusive and user not in old_followers: 
                    j=following_n.index(user)
                    sety=[self.day, user]    
                    try:
                        i=old_following.index(user)
                    except:
                        matrix.append(sety)         #brak w pliku a jest w obserwowanych
                        matrix_n.append(sety)
                        #print("found new user", user)
                        continue
                    if datetime.datetime.strptime(str(matrix[i][0]), '%Y-%m-%d')<t - datetime.timedelta(days=int(old)):
                        try:
                            time.sleep(1)
                            matrix.remove(matrix[i])
                            out+=1
                        except Exception as e: print(e)
                    else: matrix_n.append(sety)
            print("removed: ", out)
            self.saving(matrix,"following")
            if out>int(maxi):
                break                    
            for i in range(3): 
                action=ActionChains(driver)
                action.move_to_element(following[k-1]).perform()
                time.sleep(2)
                following = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")  
                k=len(following); print(k)
            end=following[k-1].text; print("matrix_n",matrix_n)
        print("\nprofiles removed:", out)

    def page_likes(self, nr):     # follow new users
        driver = self.driver
        new_hrefs=self.new_hrefs
        viewed_hrefs=self.viewed_hrefs
        hrefs=new_hrefs+old_hrefs
        new_users=0
        for href in hrefs:
            if new_users > nr:
                break
            driver.get(href)
            time.sleep(2)
            likes = driver.find_element_by_xpath("//section[@class='EDfFK ygqzn']//a").click()   #otwiera polubienia strony
            time.sleep(2)
            self.reading('following')
            matrix=self.matrix
            temp_users=[]   
            end=0; last=1;           
            while True:
                new_inview=[]
                if last==end:
                    break
                users = driver.find_elements_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.rWtOq>div')  #działało('.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4._0mzm-.ZUqME .Igw0E.rBNOH.eGOV_.ybXk5._4EzTm')
                k=len(users);print(k)
                users_n = [user.text for user in users]
                last=users_n[k-1]; print('last',last)
                print("visible", users_n)
                buttons = driver.find_elements_by_css_selector('._0mzm-.sqdOP.L3NKy')              #wszystkie widoczne przyciski follow
                for user in users_n:
                    if user not in temp_users:
                        temp_users.append(user)  #wszyscy wyświetleni w tej sesji
                        new_inview.append(user)  #nowi w widoku
                for user in new_inview:
                    j=users_n.index(user)   #nowi w widoku i w bazie
                    if buttons[j].text=="Obserwuj":
                        try:
#                            buttons[j].click()
                            new_users+=1
                            temp_users.append(user)
                            time.sleep(1)
                            sety=[self.day, user]; print(sety)
                            matrix.append(sety)
                        except Exception as e:
                            print(e)
                print("analizowani aktualnie widoku", len(new_inview))
#                print("przerobione profile z tego zdjęcia", len(temp_users))
                print("wszyscy nowi dodani...................  ", new_users)
                if len(temp_users)>40:
                    break
                for i in range(3): 
                    action=ActionChains(driver)
                    action.move_to_element(users[k-1]).perform()
                    time.sleep(2)
                    users = driver.find_elements_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.rWtOq>div')   #działało('.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4._0mzm-.ZUqME .Igw0E.rBNOH.eGOV_.ybXk5._4EzTm') 
                    k=len(users); print(k)
                end=users[k-1].text; #print("end",end)
                self.saving(matrix,"following")
            driver.find_element_by_css_selector('span.glyphsSpriteX__outline__24__grey_9').click()  #zamknięcie okienka followers
            #driver.quit()
            self.reading('hrefs')
            ref_mx=self.matrix
            ref_sety=[self.day, href]
            ref_mx.append(ref_sety)
            self.saving(ref_mx,'hrefs')

    def przewijanie(self):
        driver = self.driver
        driver.get("https://www.instagram.com/p/BvydUxkIJWp/")
        time.sleep(2)
        likes = driver.find_element_by_xpath("//section[@class='EDfFK ygqzn']//a").click()   #otwiera polubienia
        time.sleep(2)
        for i in range(3):
            users = driver.find_elements_by_css_selector('_7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.rWtOq>div')   
            k=len(users); print(k)
            users = driver.find_element_by_css_selector('.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd').click()   #klikanie w "ramke"
            actionChain = webdriver.ActionChains(driver)
            actionChain.key_down(Keys.END).key_up(Keys.END).perform()
            users = driver.find_elements_by_css_selector('_7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.rWtOq>div')    
            k=len(users); print(k)
            end=users[k-1].text; print("end",end)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # zbieranie zdjęc
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a'); print("hrefs_in_view", hrefs_in_view)
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]; print("hrefs_in_view2", hrefs_in_view) #lista unikalnych zdjęć
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]; print("pic_hrefs", pic_hrefs)
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue
        driver.quit()

peds = InstagramBot("piotrekjazz", "haslo")
wybor=None; wyb=None; ww=None; www={1:'theofficialpandora', 2:'mercedesbenz'}
while wybor!=1 and wybor!=2:
    wybor=int(input("""
Podaj czynność:
1-wprowadzanie nowych użytkowników
2-usuwanie istniejących\n"""))
if wybor==2:
    while wyb.lower()!='t' and wyb.lower()!='n':
        wyb=input('\naktualizowanie bazy fallowers  t/n? ')
    peds.reading('following')
    matrix=peds.matrix
    p5=0; p15=0; p30=0; pX=0
    for i in range(len(matrix)):
        if (t-datetime.datetime.strptime(matrix[i][0], '%Y-%m-%d')).days<=5: p5+=1
        if 5<(t-datetime.datetime.strptime(matrix[i][0], '%Y-%m-%d')).days<=15: p15+=1
        if 15<(t-datetime.datetime.strptime(matrix[i][0], '%Y-%m-%d')).days<=30: p30+=1
        if (t-datetime.datetime.strptime(matrix[i][0], '%Y-%m-%d')).days>=30: pX+=1            
    print("jest ok %s profili obserwowanych poniżej 5 dni\n" %p5)
    print("jest ok %s profili obserwowanych miedzy 5-15 dni\n" %p15)
    print("jest ok %s profili obserwowanych miedzy 15-30 dni\n" %p30)
    print("jest ok %s profili obserwowanych powyżej 30 dni\n" %pX)
    old=input("ilu dniowe profile usuwać? ")
    while not old.isdecimal(): old=input("musi być liczba ")
    old = int(old)
    maxi=input("\nmaksymalnie ile profili usunąć? ")
    while not maxi.isdecimal(): maxi=input("musi być liczba ")
    maxi = int(maxi)
    peds.login()
    if wyb=='t':
        peds.followers_check()
    peds.following_cleanup(old, maxi)
elif wybor==1:
    while ww not in www.keys():
        pprint.pprint(www)
        ww=int(input("Wybierz numer strony: "))
    nr=int(input('ilu użytkowników dodać? '))
    peds.login()
    peds.fun_page(www.get(ww))
    for i in range(5):
        peds.page_likes(int(nr/4))


#peds = InstagramBot("piotrekjazz", "haslo")
#peds.login()
#peds.followers_check()
#peds.following_cleanup(5, 20)
#peds.page_comments()
#peds.page_likes()
#peds.news_feed()
#peds.one_photo()
#peds.fun_page()
#peds.like_photo("psychologia")



