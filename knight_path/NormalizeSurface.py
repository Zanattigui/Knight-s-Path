import pygame


def normalize_surface(surf, size=(50, 50)):
    """
    Redimensiona a imagem mantendo proporção e centraliza em uma surface transparente de tamanho `size`.
    """
    # Tamanho original
    orig_w, orig_h = surf.get_size()
    
    # Calcula escala proporcional
    scale_factor = min(size[0] / orig_w, size[1] / orig_h)
    new_w = int(orig_w * scale_factor)
    new_h = int(orig_h * scale_factor)
    
    # Redimensiona a imagem
    surf = pygame.transform.scale(surf, (new_w, new_h))
    
    # Cria surface transparente de tamanho fixo
    new_surf = pygame.Surface(size, pygame.SRCALPHA)
    
    # Calcula posição central
    x = (size[0] - new_w) // 2
    y = (size[1] - new_h) // 2
    
    # Desenha a imagem redimensionada centralizada
    new_surf.blit(surf, (x, y))
    
    return new_surf