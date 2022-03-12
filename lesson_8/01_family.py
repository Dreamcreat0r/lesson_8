# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.food = 100 # начальная еда в холодильнике
        self.money = 500 # начальные деньги
        self.dirt = 0 # начальная загрязненность дома
        self.cat_food = 30 # начальная еда для кота

    def __str__(self): # выводим информацию о доме
        print('{} еды в холодильнике, {} кошачьей еды, {} денег в тумбочке, {} степень загрязненности дома\n'.format
              (self.food, self.cat_food, self.money, self.dirt))

    def act(self):
        self.dirt += 5
        self.__str__()


class Human:

    def __init__(self, name, house):
        self.satiety = 30 # начальная сытость
        self.happiness = 100 # начальное счастье
        self.house = house
        self.name = name
        self.action_point = 0
        self.catplays_count = 0

    def __str__(self):
        print('{}:     {} сытость,     {} счастье'.format(self.name, self.satiety, self.happiness)) # вывод статов конкретного чела

    def act(self):
        self.__str__()
        self.action_point = 1 # восстанавливаем очко действия в начале хода
            
        if self.house.dirt >= 90:   # если дом грязный - настроение падает
            self.happiness -= 10

        if self.satiety <= 40:    # проверяем себя на голод
            if self.satiety <= 0:  # проверка на смерть от голода
                self.action_point = -1
            if self.action_point == 1:
                self.eat()  # пытаемся кушать
                
        if self.happiness <= 20:    # проверка на смерть от депрессии и на наличие очка действия
            if self.happiness <= 10:
                self.action_point = -1

    def eat(self):
        if self.house.food >= 30: # если есть покушать досыта
            self.house.food -= 30
            self.satiety += 30
            self.action_point = 0 # съедаем очко действия
            print(self.name, ' покушал(а)\n') # сообщение о совершенном действии
        elif self.house.food > 0: # если есть покушать частично
            self.satiety += self.house.food
            self.house.food = 0
            self.action_point = 0 # съедаем очко действия
            print(self.name, ' покушал(а)\n') # сообщение о совершенном действии
        else: # если еды нет совсем
            print('Еды нет!')   # сигналим если еды нет

    def pet_cat(self):   # погладил кота
        self.happiness += 5
        self.satiety -= 10   # снимаем сытость
        self.action_point = 0 # съедаем очко действия
        self.catplays_count += 1
        print(self.name, ' погладил(а) кота')


class Husband(Human):

    def __init__(self, name, house):
        super().__init__(name=name, house=house)
        self.plays_count = 0
        self.worksdays_count = 0

    #def __str__(self):   # сообщение о характеристиках - ссылаемся на метод материнского класса
    #    super().__str__()

    def act(self):   # дополняем движковый модуль материнского класса
        super().act()

        if self.happiness <=  40 and self.action_point == 1:   # если накатил депрессон от того, что жена не убирается в доме - поиграем в танки
            self.play()

        if self.happiness < 70 and self.action_point == 1 and self.house.money > 800:
            self.pet_cat()
    
        if self.action_point == 1:
            self.work()   # если очко действия еще не потрачено на покушац или на поигр...то есть, на восстановление морали, то идем на работу

        return self.action_point

    def play(self):   # +10 морали
        self.happiness += 30
        self.satiety -= 10     # снимаем сытость
        self.action_point = 0  # съедаем очко действия
        self.plays_count += 1
        print(self.name, ' поиграл\n') # сообщение о совершенном действии

    def work(self):   # никидываем 150 голды в кошелек
        self.house.money += 170
        self.satiety -= 10     # снимаем сытость
        self.action_point = 0  # съедаем очко действия
        self.worksdays_count += 1
        print(self.name, ' поработал\n') # сообщение о совершенном действии
    # несмотря на то, что это последнее возможное действие, все равно съедаем ОД на случай перестановки действий в движке


class Wife(Human):

    def __init__(self, name, house):
        super().__init__(name=name, house=house)
        self.bags_count = 0
        self.maiden_calls = 0
        self.clean_count = 0

    #def __str__(self):   # сообщение о характеристиках - ссылаемся на метод материнского класса
    #    super().__str__()

    def act(self):  # дополняем движковый модуль материнского класса
        super().act()
        if self.happiness < 40 and self.action_point == 1:   # если накатил депрессон от того, что сама не убирается в доме - купим сумку
                self.buy_new_bag()

        if self.house.food < 150 and self.action_point == 1:  # если нечего кушац - идем в магазин
            self.buy_food()

        if self.house.cat_food < 100 and self.action_point == 1:  # если коту нечего кушац - идем в магазин
            self.buy_cat_food()

        if self.house.dirt > 100:
            self.call_maiden()

        if self.happiness < 70 and self.house.dirt <= 50:
            self.pet_cat()

        if self.action_point == 1:
            self.clean_house()    # если очко действия еще не потрачено на покушац/купить шубу/сходить в магазин, то убираемся в доме

        return self.action_point

    def buy_food(self):
        if self.house.money > 150:   # проверяем, есть ли деньги на еду (по максимуму)
            self.house.food += 150
            self.house.money -= 150
            self.satiety -= 10     # снимаем сытость
            self.action_point = 0  # съедаем очко действия
            print('{} купила 150 еды\n'.format(self.name))   # отчет о купленной еде
        elif self.house.money > 0:   # проверяем, есть ли деньги на еду (частично)
            self.house.food += self.house.money
            print('{} купила {} еды\n'.format(self.name, self.house.money))   # отчет о купленной еде
            self.house.money = 0
            self.satiety -= 10     # снимаем сытость
            self.action_point = 0  # съедаем очко действия
        else:
            print('Денег на еду НЕТ!')   # сигналим, если денег нет вообще

    def buy_cat_food(self):
        if self.house.money > 100:   # проверяем, есть ли деньги на еду для кота (по максимуму)
            self.house.cat_food += 100
            self.house.money -= 100
            self.satiety -= 10     # снимаем сытость
            self.action_point = 0  # съедаем очко действия
            print('{} купила 100 кошачьей еды\n'.format(self.name))   # отчет о купленной еде для кота
        elif self.house.money > 0:   # проверяем, есть ли деньги на еду для кота(частично)
            self.house.cat_food += self.house.money
            print('{} купила {} кошачьей еды\n'.format(self.name, self.house.money))   # отчет о купленной еде для кота
            self.house.money = 0
            self.satiety -= 10     # снимаем сытость
            self.action_point = 0  # съедаем очко действия
        else:
            print('Денег на еду для кота НЕТ!')   # сигналим, если денег нет вообще
        

    def buy_new_bag(self):
        if self.house.money >= 550:   # проверяем, достаточно ли денег
            self.house.money -= 550
            self.happiness += 60
            self.satiety -= 10     # снимаем сытость
            self.action_point = 0  # съедаем очко действия
            self.bags_count += 1
            print(self.name, ', купила сумку\n')
        else:
            print('Нет денег на сумку!')    # сигналим, если нет

    def call_maiden(self):
        if self.house.money >= 450:
            self.house.money -= 350
            self.house.dirt = 0
            self.satiety -= 10
            self.action_point = 0
            self.maiden_calls += 1
            print(self.name, ' вызвала уборщицу')

    def clean_house(self):
        self.house.dirt -= 10
        self.satiety -= 10     # снимаем сытость
        self.action_point = 0  # съедаем очко действия
        self.clean_count += 1
        print(self.name, ' убралась в доме\n') # сообщение о совершенном действии
    # несмотря на то, что это последнее возможное действие, все равно съедаем ОД на случай перестановки действий в движке


# Можно будет потом преобразовать всю эту ботву в схему через очки приоритета. 
# Типа покушать и восстановить мораль - нулевой приоритет, купить еды если ее нет вообще - первый, 
# убраться в доме если он грязный - второй, купить еды, если ее 100+ - третий и т.д.



# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:

    def __init__(self, name, house):
        self.name = name
        self.satiety = 30     
        self.house = house
        self.action_point = 0

    def __str__(self):
        print('{}:     {} сытость'.format(self.name, self.satiety)) # вывод статов конкретного кота

    def act(self):
        self.__str__()
        self.action_point = 1 # восстанавливаем очко действия в начале хода

        if self.satiety < 20:   # проверяем кота на голод
            if self.satiety <= 0:   # проверяем кота на смерть от голода
                self.action_point = -1
            self.eat()   # пробуем кушац


        if self.action_point == 1:
            if randint(0,1) == 0:   # случайным образом выбираем, спать или драть ковер
                self.sleep()
            else:
                self.ruin_carpet()

        return self.action_point

    def eat(self):
        if self.house.cat_food >= 10:   # еды много - кушаем от пуза
            self.satiety += 20
            self.house.cat_food -= 10
            self.action_point = 0  # съедаем очко действия
            print(self.name, 'поел\n')
        elif self.house.cat_food > 0:   # еды немного - кушаем сколько есть
            self.satiety += self.house.cat_food*2
            self.house.cat_food = 0
            self.action_point = 0  # съедаем очко действия
            print(self.name, 'поел\n')
        else:   # еды нет - начинаем орать
            print('Кошачьей еды нет!')   

    def sleep(self):   # во время сна голод снижается не сильно
        self.satiety -= 5
        self.action_point = 0  # съедаем очко действия
        print(self.name, 'поспал\n')

    def ruin_carpet(self):   # дерем ковер, повышается голод и грязь в доме
        self.satiety -= 10   # забавно, что для кота при этом плюсов нет)) прям как в жизни
        self.house.dirt += 5
        self.action_point = 0  # съедаем очко действия
        print(self.name, 'подрал ковер\n')   # надо будет потом добавить функцию покупки нового ковра



######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child(Human):

    #def __init__(self, name, house):
    #    super().__str__()

    #def __str__(self):
    #    super().__str__()

    def act(self):  # движковый модуль тут свой, материнский не трогаем
        self.__str__()
        self.action_point = 1 # восстанавливаем очко действия в начале хода

        if self.satiety <= 40:    # проверяем себя на голод
            if self.satiety <= 0:  # проверка на смерть от голода
                self.action_point = -1
            else:
                self.eat()  # пытаемся кушать

        if self.action_point == 1:
            self.sleep()

        return self.action_point

    def eat(self):  # и модуль покушать тут свой
        if self.house.food >= 10: # если есть покушать досыта
            self.house.food -= 10
            self.satiety += 10
            self.action_point = 0  # съедаем очко действия
            print(self.name, ' покушал(а)\n') # сообщение о совершенном действии
        elif self.house.food > 0: # если есть покушать частично
            self.satiety += self.house.food
            self.house.food = 0
            self.action_point = 0  # съедаем очко действия
            print(self.name, ' покушал(а)\n') # сообщение о совершенном действии
        else: # если еды нет совсем
            print('Еды нет!')   # сигналим если еды нет


    def sleep(self):
        self.satiety -= 10 # снимаем сытость
        self.action_point = 0  # съедаем очко действия
        print(self.name, 'поспал(а)\n')



home = House()
serge = Husband(name='Сережа', house = home)
masha = Wife(name='Маша', house = home)
murlo = Cat(name='Мурзик', house = home)
rizhiy = Cat(name='Рыжик', house = home)
basik = Cat(name='Барсик-который-срет-мимо', house = home)
nigga = Cat(name='Черныш', house = home)
spinogriz = Child(name= 'Миша', house = home)

for day in range(365):
    print('========================================== День {} =========================================='.format(day+1))
    home.act()
    if serge.act() == -1:
        break
    if masha.act() == -1:
        break
    if murlo.act() == -1:
        break
    if rizhiy.act() == -1:
        break
    if basik.act() == -1:
        break
    if nigga.act() == -1:
        break
    if spinogriz.act() == -1:
        break
    print('|||||||||||||||||||||||||||||||||||||||||В конце хода:||||||||||||||||||||||||||||||||||||||||')
    home.__str__()
    serge.__str__()
    masha.__str__()
    murlo.__str__()
    rizhiy.__str__()
    basik.__str__()
    nigga.__str__()
    spinogriz.__str__()
    print('\n')
    print('{} играл {} раз, гладил кота {} раз, сходил на работу {} раз'.format
          (serge.name, serge.plays_count, serge.catplays_count, serge.worksdays_count))
    print('{} купила {} сумок, гладила кота {} раз, вызвала уборщицу {} раз, убралась сама {} раз'.format
          (masha.name, masha.bags_count, masha.catplays_count, masha.maiden_calls, masha.clean_count))


# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


#home = House()
#serge = Husband(name='Сережа')
#masha = Wife(name='Маша')
#kolya = Child(name='Коля')
#murzik = Cat(name='Мурзик')

#for day in range(365):
#    cprint('================== День {} =================='.format(day), color='red')
#    serge.act()
#    masha.act()
#    kolya.act()
#    murzik.act()
#    cprint(serge, color='cyan')
#    cprint(masha, color='cyan')
#    cprint(kolya, color='cyan')
#    cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

