from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_block = load_texture('assets/grass_block.png')
stone_block = load_texture('assets/stone_block.png')
brick_block = load_texture('assets/brick_block.png')
dirt_block  = load_texture('assets/dirt_block.png')
sky         = load_texture('assets/skybox.png')
arm         = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop = False, autoplay = False)
current_block = grass_block

def update():
    global current_block
    if held_keys['1']: current_block = grass_block
    if held_keys['2']: current_block = stone_block
    if held_keys['3']: current_block = brick_block
    if held_keys['4']: current_block = dirt_block

    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.active()
    else:
        arm.passive()

class Voxel(Button):
    def __init__(self, pos = (0, 0, 0), block = grass_block):
        super().__init__(
            parent    = scene,
            position  = pos,
            model     = 'assets/block',
            origin_y  = 0.5,
            texture   = block,
            color     = color.color(0, 0, random.uniform(0.9, 1)),
            scale     = 0.5
        )
    
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                global current_block
                Voxel(pos = self.position + mouse.normal, block = current_block)
                punch_sound.play()

        if self.hovered:
            if key == 'right mouse down':
                destroy(self)
                punch_sound.play()

class Sky(Entity):
     def __init__(self):
        super().__init__(
            parent   = scene,
            position = (0, 0, 0),
            origin_y = 0.5,
            model    = 'sphere',
            texture  = sky,
            scale    = 75,
            double_sided = True
        )

class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm,
            scale = 0.2,
            rotation = Vec3(140,-40,0),
            position = Vec2(0.6,-0.6)
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.6,-0.6)

for i in range(20):
    for j in range(20):
        voxel = Voxel(pos = (i, 0, j))

player = FirstPersonController()
sky    = Sky()
arm    = Arm()
app.run()