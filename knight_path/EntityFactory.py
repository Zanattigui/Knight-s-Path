from knight_path.const import WIN_WIDTH

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
            return Player('KnightIdle', position)
        if entity_name == 'Enemy1':
            from knight_path.Enemy import Enemy
            return Enemy('GoblinRun', position, frames_count=10, patrol_range=(0, 100), speed=1)
        if entity_name == 'EnemyBoss':
            from knight_path.EnemyBoss import EnemyBoss
            return EnemyBoss('BossWalk', position, frames_count=24, patrol_range=(0, 100), speed=1)