import random
# Soldier
class Soldier:
    def __init__(self, health, strength):
            self.health=health
            self.strength=strength
    
    def attack(self):
        return self.strength
    
    def receiveDamage(self, damage):
        self.damage = damage
        self.health = self.health - self.damage
    
    pass

# Viking
class Viking(Soldier):
    
    def __init__(self, name, health, strength):
        self.name = name
        self.health=health
        self.strength=strength
    
    def receiveDamage(self, damage):
        self.damage = damage
        self.health -= self.damage
        
        if self.health > self.damage:
            return ("{} has received {} points of damage" .format(self.name, self.damage))
        else:
            return ("{} has died in act of combat" .format(self.name))
    
    def battleCry(self):
        return "Odin Owns You All!"
        
    pass

# Saxon
class Saxon(Soldier):
    
    def __init__(self, health, strength):
        self.health=health
        self.strength=strength
    
    def receiveDamage(self, damage):
        self.damage = damage
        self.health -= self.damage
        
        if self.health > self.damage:
            return ("A Saxon has received {} points of damage" .format(self.damage))
        else:
            return ("A Saxon has died in combat")
    
    pass

# War
class War():
    
    def __init__(self):
        self.vikingArmy = []
        self.saxonArmy = []
    
    def addViking(self, Viking):
        self.vikingArmy.append(Viking)
        
    def addSaxon(self, Saxon):
        self.saxonArmy.append(Saxon)
        
    def vikingAttack(self):
        random_saxon = random.choice(self.saxonArmy)
        Saxon.receiveDamage == Viking.attack 
        if random_saxon.health <=0:
            self.saxonArmy.remove(random_saxon)   
        
        return Saxon.receiveDamage

    def saxonAttack(self):
        random_viking = random.choice(self.vikingArmy)
        Viking.receiveDamage == Saxon.attack
        if random_viking.health <= 0:
            self.vikingArmy.remove(random_viking)
        
        return Viking.receiveDamage
    
    def showStatus(self):
        if self.saxonArmy == 0:
            return "Vikings have won the war of the century!"
        elif self.vikingArmy == 0:
            return "Saxons have fought for their lives and survive another day..."
        elif self.saxonArmy and self.vikingArmy >= 1:
            return "Vikings and Saxons are still in the thick of battle."

 
    pass
