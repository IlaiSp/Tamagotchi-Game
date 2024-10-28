from abc import ABC, abstractmethod
from enum import Enum
import time


class LifeStage(Enum):
    BABY = "Baby"
    CHILD = "Child"
    TEENAGER = "Teenager"
    ADULT = "Adult"
    SENIOR = "Senior"
    SPECIAL = "Special"


class Pet(ABC):
    STAGE_DURATION = 60

    def __init__(self, name):
        self.name = name
        self.age = 0
        self.weight = 1
        self.hunger = 50
        self.happiness = 50
        self.training = 0
        self.sickness = 0
        self.stage = LifeStage.BABY
        self.last_stage_update = time.time()
        self.alive = True
        self.last_decay_time = time.time()

    def eat(self):
        if not self.alive:
            print(f"{self.name} is no longer alive.")
            return
        print(f"{self.name} is eating.")
        self.hunger = max(0, self.hunger - 10)
        self.happiness = min(100, self.happiness + 5)
        self.weight += 2

    def sleep(self):
        if not self.alive:
            print(f"{self.name} is no longer alive.")
            return
        print(f"{self.name} is sleeping.")
        self.happiness = min(100, self.happiness + 5)
        self.age += 1

    def play(self):
        if not self.alive:
            print(f"{self.name} is no longer alive.")
            return
        print(f"{self.name} is playing.")
        self.happiness = min(100, self.happiness + 10)

    def exercise(self):
        if not self.alive:
            print(f"{self.name} is no longer alive.")
            return
        print(f"{self.name} is exercising.")
        self.hunger = min(100, self.hunger + 5)
        self.training = min(100, self.training + 5)
        self.happiness = min(100, self.happiness + 5)
        self.weight = max(0, self.weight - 1)

    def update_stage(self):
        elapsed_time = time.time() - self.last_stage_update
        if elapsed_time > Pet.STAGE_DURATION:
            if self.stage == LifeStage.BABY:
                self.stage = LifeStage.CHILD
            elif self.stage == LifeStage.CHILD:
                self.stage = LifeStage.TEENAGER
            elif self.stage == LifeStage.TEENAGER:
                self.stage = LifeStage.ADULT
            elif self.stage == LifeStage.ADULT:
                self.stage = LifeStage.SENIOR
            elif self.stage == LifeStage.SENIOR:
                self.stage = LifeStage.SPECIAL
            print(f"{self.name} has evolved to the {self.stage.value} stage!")
            self.last_stage_update = time.time()

    def decay_status(self):
        current_time = time.time()
        if current_time - self.last_decay_time >= 10:
            self.hunger = min(100, self.hunger + 5)
            self.happiness = max(0, self.happiness - 5)
            self.sickness = min(100, self.sickness + 5)
            self.training = max(0, self.training - 2)
            self.last_decay_time = current_time

    def check_health(self):
        if self.hunger >= 100:
            print(f"{self.name} died of hunger.")
            self.alive = False
        elif self.happiness <= 0:
            print(f"{self.name} died of sadness.")
            self.alive = False
        elif self.sickness >= 100:
            print(f"{self.name} died of sickness.")
            self.alive = False
        elif self.stage == LifeStage.SENIOR and (time.time() - self.last_stage_update) > 180:
            print(f"{self.name} died of old age.")
            self.alive = False

    def clean(self):
        if not self.alive:
            print(f"{self.name} is no longer alive.")
            return
        print(f"{self.name} has been cleaned.")
        self.sickness = max(0, self.sickness - 20)

    def display_status(self):
        if not self.alive:
            print(f"{self.name} has passed away.")
            return
        print("\n" + "=" * 30)
        print(f" Pet Status: {self.name} ")
        print("=" * 30)
        print(f"Stage       : {self.stage.value}")
        print(f"Age         : {self.age}")
        print(f"Weight      : {self.weight}")
        print(f"Hunger      : {'█' * (self.hunger // 10)} ({self.hunger}/100)")
        print(f"Happiness   : {'█' * (self.happiness // 10)} ({self.happiness}/100)")
        print(f"Training    : {'█' * (self.training // 10)} ({self.training}/100)")
        print(f"Sickness    : {'█' * (self.sickness // 10)} ({self.sickness}/100)")
        print("=" * 30 + "\n")

    @abstractmethod
    def make_sound(self):
        pass


class Dog(Pet):
    def make_sound(self):
        print(f"{self.name} says: Woof!")


class Cat(Pet):
    def make_sound(self):
        print(f"{self.name} says: Meow!")


class PetFactory:
    @staticmethod
    def create_pet(pet_type, name):
        if pet_type == "Dog":
            return Dog(name)
        elif pet_type == "Cat":
            return Cat(name)
        else:
            raise ValueError("Unknown pet type")


class TamagotchiGame:
    def __init__(self, pet):
        self.pet = pet

    def execute_command(self, action):
        if action == "eat":
            self.pet.eat()
        elif action == "sleep":
            self.pet.sleep()
        elif action == "play":
            self.pet.play()
        elif action == "exercise":
            self.pet.exercise()
        elif action == "clean":
            self.pet.clean()

        self.pet.update_stage()
        self.pet.check_health()


if __name__ == "__main__":
    pet_name = input("Enter your pet's name: ")
    pet_type = input("Enter the type of pet (Dog/Cat): ")
    pet = PetFactory.create_pet(pet_type, pet_name)
    game = TamagotchiGame(pet)

    while pet.alive:
        print("\n\n\n")
        pet.display_status()
        pet.decay_status()

        print("Choose an action for your pet:")
        print("1. Eat")
        print("2. Sleep")
        print("3. Play")
        print("4. Exercise")
        print("5. Make sound")
        print("6. Clean")
        print("7. Quit")
        choice = input("Enter your choice: ")
        print("")

        if choice == "1":
            game.execute_command("eat")
        elif choice == "2":
            game.execute_command("sleep")
        elif choice == "3":
            game.execute_command("play")
        elif choice == "4":
            game.execute_command("exercise")
        elif choice == "5":
            pet.make_sound()
        elif choice == "6":
            game.execute_command("clean")
        elif choice == "7":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")
