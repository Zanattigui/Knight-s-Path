from knight_path.const import WIN_WIDTH
from knight_path.Player import Player


class EntityFactory:
    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        if entity_name == 'Level1Bg':
            from knight_path.Background import Background
            list_bg = []
            for i in range(8):
                list_bg.append(Background(f'Level1Bg{i}', (0, 0)))
                list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
            return list_bg
        if entity_name == 'Player':
            from knight_path.Player import Player
            return Player('RogueIdle', position)
        if entity_name == 'Enemy1':
            from knight_path.Enemy import Enemy
            # Exemplo: inimigo patrulha 150 pixels a partir da posição inicial
            return Enemy('GoblinRun', position, frames_count=10, patrol_range=(0, 100), speed=1)