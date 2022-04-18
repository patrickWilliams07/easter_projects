import random

class Entity:
    def __init__(self, name, level, maxHealth):
         self.name = name
         self.level = level
         self.maxHealth = maxHealth

    @staticmethod
    def variation(value):
        return round(value * random.randint(5,15) / 10)
    
    @staticmethod
    def get_random_name():
        file = open("five\\names.txt", 'r')
        names = file.read()
        file.close()
        return random.choice(names.split("\n"))
    
    @property
    def letterLevel(self):
        if self.level > 26:
            return ("Z"*(self.level-25))
        return chr(self.level + 64)
    
    @classmethod
    def random_level_create(cls, level):
        if cls == Character:
            random.choice([Duelist, Shaman, Alchemist])(Entity.get_random_name(), level, Entity.variation(level*5), Entity.variation(level))
        else:
            cls(Entity.get_random_name(), level, Entity.variation(level*5), Entity.variation(level))


class Character(Entity):
    all = []
    opponent = None

    def __init__(self, name, level, maxHealth, *args):
         super().__init__(name, level, maxHealth)
         Character.all.append(self)
         if type(self).active is None:
             self.make_active()
    
    def __repr__(self):
        return(f"\nThis {type(self).__name__} are called {self.name}\nThey are level {self.letterLevel} and have a max health of {self.maxHealth}")

    def make_active(self):
        type(self).active = self
        print(f"{self.name} are now active")

    @staticmethod
    def show_active():
        print(f"The active Duelist:\n{Duelist.active}")
        print(f"The active Shaman:\n{Shaman.active}")
        print(f"The active Alchemist:\n{Alchemist.active}")
    
    @classmethod
    def show_all_characters(cls):
        for item in Character.all:
            if type(item) == cls:
                if type(item).active == item:
                    print("\nVVV ACTIVE VVV")
                print(f"\n{item}")
    
    @classmethod
    def change_active(cls):
        print(f"\nChoose a new {cls.__name__} to use:")
        cls.show_all_characters()
        choice = input(f"Enter the name of the new {cls.__name__}:\n --> ")
        if choice == "": return
        for item in Character.all:
            if item.name == choice:
                cls.active = item

    @staticmethod
    def random_change_active():
        random.choice([Duelist, Shaman, Alchemist]).change_active()
    
    @staticmethod
    def average_level():
        return round((Duelist.active.level + Shaman.active.level + Alchemist.active.level) / 3)

    @staticmethod
    def check_health():
        if Duelist.active.health <= 0:
            return Duelist.active
        elif Shaman.active.health <= 0:
            return Shaman.active
        elif Alchemist.active.health <= 0:
            return Alchemist.active
        elif Character.opponent.health <= 0:
            return Character.opponent
        return None

    @staticmethod
    def check_input(value):
        if value == "Duelist" or value == Duelist.active.name:
            return Duelist
        elif value == "Shaman" or value == Shaman.active.name:
            return Shaman
        elif value == "Alchemist" or value == Alchemist.active.name:
            return Alchemist
        return None

    @staticmethod
    def turn():
        choice = input(f"\nChoose between the Duelist, Shaman or Alchemist's move.\nDuelist: {Duelist.active.name} to deal {Duelist.active.damage} damage\n" \
                       f"Shaman: {Shaman.active.name} to heal {Shaman.active.heal} health\n" \
                       f"Alchemist: {Alchemist.active.name} to reduce the opponent's damage and increase the Duelist's damage by {Alchemist.active.weaken} damage next round\n --> ")
        Character.check_input(choice).active.turn()

    @classmethod
    def death(cls):
        print(f"{cls.active.name} died! You lose!")
        return False

    @staticmethod
    def encounter(level):
        Duelist.active.health = Duelist.active.maxHealth
        Shaman.active.health = Shaman.active.maxHealth
        Alchemist.active.health = Alchemist.active.maxHealth
        Mob.random_level_create(level)
        while Character.check_health() is None:
            Character.opponent.turn()
            if Character.check_health() is not None:
                break
            Character.turn()
        return Character.check_health().death()
    
    @staticmethod
    def multiple_encounters():
        i = 0
        while Character.encounter(Entity.variation(Character.average_level())) and i < Character.average_level() / 5:
            i += 1
        if i >= Character.average_level() / 5:
            Character.random_level_create(Character.average_level() + random.randint(1,3))

    @classmethod
    def random_create_variation(cls):
        cls.random_level_create(Entity.variation(Character.average_level()))

class Duelist(Character):
    active = None

    def __init__(self, name, level, maxHealth, damage):
        print("\nYou unlocked a new Duelist!")
        super().__init__(name, level, maxHealth)
        self.damage = damage
        print(self)
    
    def __repr__(self):
        return f"{super().__repr__()}\nThey can deal {self.damage} damage per round"
    
    def turn(self):
        if Alchemist.active.weakenActive:
            Character.opponent.health -= self.damage + Alchemist.active.weaken
        else:
            Character.opponent.health -= self.damage
        print(f"\n{self.name} damaged {Character.opponent.name} for {self.damage}.\n{Character.opponent.name} are at {Character.opponent.health}/{Character.opponent.maxHealth} health.")
        self.weakenActive = False


class Shaman(Character):
    active = None
    
    def __init__(self, name, level, maxHealth, heal):
        print("\nYou unlocked a new Shaman!")
        super().__init__(name, level, maxHealth)
        self.heal = heal
        print(self)
    
    def __repr__(self):
        return f"{super().__repr__()}\nThey can heal {self.heal} health per round"
    
    def turn(self):
        Duelist.active.health += self.heal
        print(f"\n{self.name} healed {Duelist.active.name} for {self.heal}.\n{Duelist.active.name} are at {Duelist.active.health}/{Duelist.active.maxHealth} health.")
        self.weakenActive = False


class Alchemist(Character):
    active = None
    
    def __init__(self, name, level, maxHealth, weaken):
        print("\nYou unlocked a new Alchemist!")
        super().__init__(name, level, maxHealth)
        self.weaken = weaken
        self.weakenActive = False
        print(self)
    
    def __repr__(self):
        return f"{super().__repr__()}\nThey reduce the damage received each round by {self.weaken}"
    
    def turn(self):
        Duelist.active.health += self.weaken
        self.weakenActive = True
        print(f"\n{self.name} reduced the damage {Duelist.active.name} will take from {Character.opponent.name} by {self.weaken}")


class Mob(Entity):
    def __init__(self, name, level, maxHealth, damage):
        super().__init__(name, level, maxHealth)
        print(f"\nYou encountered {self.name} who is level {self.letterLevel} and have {self.maxHealth} health!")
        self.damage = damage
        self.health = self.maxHealth
        Character.opponent = self
    
    def turn(self):
        Duelist.active.health -= self.damage
        print(f"\n{self.name} damaged {Duelist.active.name} for {self.damage}.\n{Duelist.active.name} are at {Duelist.active.health}/{Duelist.active.maxHealth} health.")
    
    @staticmethod
    def death():
        print(f"{Character.opponent.name} died! You win!")
        return True


class Place:
    places = []

    def __init__(self, name):
        self.name = name
        print(f"You could go to {self.name}")
        Place.places.append(self)
    
    @staticmethod
    def get_random_result():
        random.choice([Character.random_create_variation, Character.random_create_variation, Character.multiple_encounters, Character.multiple_encounters, Character.multiple_encounters, Character.random_change_active])()

    @staticmethod
    def discover_place():
        file = open("five\\places.txt", 'r')
        places = file.read()
        file.close()
        Place(random.choice(places.split("\n")))
    
    @staticmethod
    def discover_multiple_places():
        print("\nHere are your options:")
        for i in range(random.randint(2,4)):
            Place.discover_place()
        choice = input("Choose where you want to go\n --> ")
        for item in Place.places:
            if item.name == choice:
                Place.get_random_result()


def main():
    Duelist.random_level_create(1)
    Shaman.random_level_create(1)
    Alchemist.random_level_create(1)
    while Character.average_level() < 30:
        Place.discover_multiple_places()

if __name__ == "__main__":
    main()