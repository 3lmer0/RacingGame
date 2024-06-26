# Window settings
WIN_RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FOCAL_LEN = 250
SCALE = 20

# Player settings
PLAYER_WIDTH = 1
PLAYER_HEIGHT = 1
OFFSET = 1  # Camera distance as sprite is displayed slightly ahead of the reading for np player position

# Speed settings
DEV_MAX_SPEED = 0.08
MAX_SPEED = 15.0
MAX_REVERSE_SPEED = 5.0
ACCELERATION = 6.0
REVERSE_ACCELERATION = 3.0
BRAKE = 12.0
SPEED_LOSS = 2.0

# Collision settings
OBSTACLE_HIT_SPEED_RETENTION = 0.5
BOUNCE_FORCE = 0.005

# Steering settings
MAX_STEERING = 90.0
STEERING_SPEED = 55.0
STEERING_DURATION = 0.15

# Jump settings
MAX_JUMP_HEIGHT = 0.9
JUMP_LERP_DURATION = 0.18