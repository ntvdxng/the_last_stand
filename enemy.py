import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed, is_flying = False):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.is_flying = is_flying
        self.speed = speed
        self.health = health
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0  # 0: walk, 1: attack, 2: die
        self.update_time = pygame.time.get_ticks()
        
        # chon hinh anh khoi tao
        self.image = self.animation_list[self.action][self.frame_index]
        if self.is_flying  == False:
            self.rect = pygame.Rect(0, 0, 25, 40)
        else:
            self.rect = pygame.Rect(0, 0, 57, 57)
        self.rect.center = (x, y)
        
        # thuoc tinh roi cho ke dich bay
        self.falling = False
        self.fall_speed = 0
        self.fall_acceleration = 0.1
        self.ground_y = 400

    def update(self, surface, target, bullet_group):
        if self.alive:
            # kiem tra va cham voi bullet
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.health -= 25
            
            # kiem tra neu dich da cham den lau dai
            if self.rect.right > target.rect.left:
                self.update_action(1)  # enemy cham den lau dai va bat dau tan cong
                
            # di chuyen ke dich
            if self.action == 0:
                self.rect.x += self.speed
            
            # ke dich tan cong
            if self.action == 1:
                if pygame.time.get_ticks() - self.last_attack >= self.attack_cooldown:
                    target.health -= 50
                    if target.health <= 0:
                        target.health = 0
                    self.last_attack = pygame.time.get_ticks()
            
            # kiem tra neu ke dich da het mau
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)
                self.alive = False
                if self.is_flying == True:
                    self.falling = True
                    
        if self.falling:
            # Update falling position
            self.fall_speed += self.fall_acceleration
            self.rect.y += self.fall_speed
                    
            # Check if enemy hits the ground
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.falling = False

        self.update_animation()
        
        # ve hinh anh tren man hinh
        if self.is_flying:
            surface.blit(self.image, (self.rect.x - 30, self.rect.y - 15))
        else:
            surface.blit(self.image, (self.rect.x - 8, self.rect.y - 13))
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
        # surface.blit(self.image, (self.rect.x - 8, self.rect.y - 13))

    def update_animation(self):
        animation_cooldown = 35
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()