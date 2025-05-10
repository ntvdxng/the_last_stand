import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True # bien kiem tra enemy con song hay khong
        self.speed = speed # toc do enemy
        self.health = health # mau cua dich
        self.last_attack = pygame.time.get_ticks() # thoi gian lan cuoi cung tan cong cua dich
        self.attack_cooldown = 1000 # thoi gian doi tan cong lan tiep theo
        self.animation_list = animation_list # danh sach hinh anh (0: walk, 1: attack, 2: die)
        self.frame_index = 0 
        self.action = 0 # bien kiem tra loai hanh dong
        self.update_time = pygame.time.get_ticks() # lay thoi gian khoi tao
        
        # chon hinh anh khoi tao
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 25, 40) # tao hinh chu nhat cho enemy
        self.rect.center = (x, y)

     
    def update(self, surface, target, bullet_group):
        if self.alive:
            # kiem tra va cham voi bullet
            if pygame.sprite.spritecollide(self, bullet_group, True): # True: neu enemy bi ban thi xoa bullet
                # giam mau ke dich
                self.health -= 25
            
            # kiem tra neu dich da cham den lau dai
            if self.rect.right > target.rect.left:
                self.update_action(1) # enemy cham den lau dai va bat dau tan cong
                
            # di chuyen ke dich
            if self.action == 0:
                # cap nhat vi tri enemy
                self.rect.x += self.speed
            
            # ke dich tan cong
            if self.action == 1:
                # kiem tra da du thoi gian ke tu lan cuoi cung tan cong
                if pygame.time.get_ticks() - self.last_attack >= self.attack_cooldown:
                    target.health -= 50 # giam mau lau dai
                    if target.health <= 0:
                        target.health = 0 # neu mau lau dai nho hon 0 thi cho bang 0
                    self.last_attack = pygame.time.get_ticks() # cap nhat thoi gian lan cuoi cung tan cong
            
            
            # kiem tra neu ke dich da het mau
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2) # enemy chet
                self.alive = False        
        
        self.update_animation()
        
        # ve hinh anh tren man hinh
        surface.blit(self.image, (self.rect.x - 8, self.rect.y - 13)) # ve hinh anh tai vi tri rect
        
        
    def update_animation(self):
        # xac dinh thoi gian cap nhat animation
        animation_cooldown = 35 # miliseconds
        # cap nhat image dua tren hanh dong hien tai
        self.image = self.animation_list[self.action][self.frame_index]
        # kiem tra thoi gian tu lan cap nhat truoc cua animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # kiem tra neu frame_index vuot qua so luong hinh anh thi quay ve index 0
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action ==2:
                self.frame_index = len(self.animation_list[self.action]) - 1 # neu enemy chet thi khong cap nhat frame_index nua
            else:
                self.frame_index = 0
            
            
    def update_action(self, new_action):
        # kiem tra neu hanh dong moi khac hanh dong cu
        if new_action != self.action:
            self.action = new_action
            # cap nhat cai dat animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks() # cap nhat thoi gian