import pygame

#lop button
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        action = False
        # lay vi tri cua chuot
        position = pygame.mouse.get_pos()
        
        # kiem tra nouseover va cac dieu kien clicked
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # neu nhan chuot trai va chua clicked
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0: # neu khong nhan chuot trai
            self.clicked = False
                
            # ve button tren man hinh
        surface.blit(self.image, (self.rect.x, self.rect.y))
            
        return action # tra ve action neu button duoc nhan