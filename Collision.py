__author__ = 'salian'

import Spell
from pygame import sprite
#vlastna trieda pre koliziu hera,npc a spellov pygame collision mi nefungovala spravne
class CollisionDetect():

    def __init__(self,hero,gameWidth,gameHeight):

        self.hero = hero
        self.height = gameHeight
        self.width = gameWidth

    def detectCollision(self,npcGroup):

        heroX = self.hero.x
        heroY = self.hero.y
        heroHeight = self.hero.heroHeight
        heroWidth = self.hero.heroWidth


        for npc in npcGroup:

            if (heroX >= npc.x and heroX <= npc.x + npc.npcWidth) and (heroY >= npc.y and heroY <= npc.y + npc.npcHeight)\
                    or (heroX + heroWidth >= npc.x and heroX + heroWidth <= npc.x + npc.npcWidth) and (heroY + heroHeight >= npc.y and heroY + heroHeight <= npc.y + npc.npcHeight):
                self.hero.hp = self.hero.hp - npc.dmg
                npc.kill()


    def detectCollisionSpellNpc(self,spellGroup,npcGroup):

        for spell in spellGroup:
            for npc in npcGroup:
                if self.hero.isImmune:
                    if npc.rect.colliderect(spell):
                        npc.kill()
                        self.hero.npcKilled += 1
                        break
                if isinstance(spell,Spell.TeleportSpell):
                    if npc.rect.colliderect(spell):
                        self.hero.npcKilled += 1
                        npc.kill()
                        break
                elif isinstance(spell,Spell.AoeSpell):
                    if spell.school == "frost":
                        if npc.rect.colliderect(spell):
                            npc.stopNpc(self.hero.level)
                if ((spell.x >= npc.x and spell.x <= npc.x + npc.npcWidth) and (spell.y >= npc.y and spell.y <= npc.y + npc.npcHeight))\
                        or ((spell.x + spell.spellWidth >= npc.x and spell.x + spell.spellWidth <= npc.x + npc.npcWidth) and (spell.y + spell.spellHeight >= npc.y and spell.y + spell.spellHeight <= npc.y + npc.npcHeight)):

                        self.hero.npcKilled += 1
                        npc.kill()
                        spell.kill()

    def spellEffect(self,spellGroup,npcGroup):
        for kuzlo in spellGroup:
            if isinstance(kuzlo,Spell.TeleportSpell):
                if kuzlo.isTeleported:
                    self.hero.x = (kuzlo.rect.x + abs(self.hero.rect.width - kuzlo.rect.width)/2)
                    self.hero.y = (kuzlo.rect.y + abs(self.hero.rect.height - kuzlo.rect.height)/2)
                    kuzlo.kill()
            elif isinstance(kuzlo,Spell.AoeSpell):
                if kuzlo.canRemove:
                    kuzlo.kill()

            elif isinstance(kuzlo,Spell.ShieldSpell):
                if kuzlo.canRemove:
                    kuzlo.hero.isImmune = False
                    kuzlo.kill()


    def detectCollisionSpellBound(self,spellGroup, boundGroup):

        #kolizia spellov s hranicami ak prekroci hranicu vymaze spellu
        spellsInBound = sprite.groupcollide(spellGroup, boundGroup, False, False)

        if spellsInBound is not None:
            for spell in spellsInBound:
                if not (isinstance(spell,Spell.AoeSpell) or isinstance(spell,Spell.ShieldSpell)):
                    spell.kill()


    def detectHeroCollisionBound(self):

        gameWidth = self.width
        gameHeight = self.height

        self.hero.canMove()

        if self.hero.x - self.hero.speed <= 0:
            self.hero.cantMove("left")
        if self.hero.x + self.hero.speed + self.hero.heroWidth >= gameWidth:
            self.hero.cantMove("right")
        if self.hero.y - self.hero.speed <= 0:
            self.hero.cantMove("up")
        if self.hero.y + self.hero.speed + self.hero.heroHeight >= gameHeight:
            self.hero.cantMove("down")


