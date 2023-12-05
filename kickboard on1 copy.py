import pygame
import sys
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# 한국어 폰트 로드
font_path = r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\OdBestFreind.ttf"
korean_font = pygame.font.Font(font_path, 36)

elapsed_time = 0

# 창 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("전동킥보드 게임")

# 사용자에게 안내 메시지를 표시
font_instruction = pygame.font.Font(font_path, 36)  # 한국어 폰트 사용
text_instruction = font_instruction.render("아무 키나 두 번 눌러 게임을 시작하세요", True, (255, 255, 255))

# 시작 화면 배경 이미지를 화면에 표시
start_screen_background = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\363553509_2281086_3529.jpeg")
screen.blit(start_screen_background, (0, 0))
screen.blit(text_instruction, (width // 2 - 180, height // 2))
pygame.display.flip()

# 키 입력을 기다리는 부분 수정
start_pressed_count = 0
game_start = False

# 키 입력을 기다리는 부분 수정
while not game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_pressed_count += 1
            if start_pressed_count >= 2:
                game_start = True

# Set running to True to start the game loop
running = True

# 이미지 로드
background_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\363553509_2281086_3529.jpeg")
kick_scooter_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\art_15879648202473_a9fa2d.jpg")
obstacle_traffic_light_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\1520238.png")
obstacle_banana_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\png-transparent-banana-pudding-codemonkey-video-game-monkey-island-game-food-orange.png")
obstacle_car_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\wrtFileImageView.jpg")
obstacle_mother_and_child_image = pygame.image.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\pngtree-cartoon-mother-s-day-mother-and-child-holding-hands-walking-png-image_1305546.jpg")

# 음악 효과 로드
hit_traffic_light_sound = pygame.mixer.Sound(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\422051__inspectorj__car-alarm-distant-a.wav")
hit_mother_and_child_sound = pygame.mixer.Sound(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\132106__sironboy__woman-scream.wav")
hit_banana_sound = pygame.mixer.Sound(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\495646__matrixxx__retro-slipping.wav")
hit_car_sound = pygame.mixer.Sound(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\592388__magnuswaker__car-crash-with-glass.wav")

pygame.mixer.music.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\A Journey Awaits.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 이미지 크기 조정
background_image = pygame.transform.scale(background_image, (width, height))
kick_scooter_image = pygame.transform.scale(kick_scooter_image, (50, 80))
obstacle_traffic_light_image = pygame.transform.scale(obstacle_traffic_light_image, (40, 40))
obstacle_banana_image = pygame.transform.scale(obstacle_banana_image, (40, 40))
obstacle_car_image = pygame.transform.scale(obstacle_car_image, (40, 40))
obstacle_mother_and_child_image = pygame.transform.scale(obstacle_mother_and_child_image, (40, 40))

# 윤곽선 추가
kick_scooter_image = kick_scooter_image.convert_alpha()
kick_scooter_rect = kick_scooter_image.get_rect(center=(width // 2, height - kick_scooter_image.get_height() - 10))

obstacle_traffic_light_image = obstacle_traffic_light_image.convert_alpha()
obstacle_banana_image = obstacle_banana_image.convert_alpha()
obstacle_car_image = obstacle_car_image.convert_alpha()
obstacle_mother_and_child_image = obstacle_mother_and_child_image.convert_alpha()

# 킥보드 설정
kick_scooter_x = width // 2 - kick_scooter_image.get_width() // 2
kick_scooter_y = height - kick_scooter_image.get_height() - 10
kick_scooter_speed = 5

# 도로 설정
road_image = pygame.Surface((width, height), pygame.SRCALPHA)  # 도로 이미지 설정
road_width = width // 3
road_change_speed = 1
current_road_width = road_width
center_line_color = (255, 255, 0)  # 노란색
center_line_width = 5
center_line_spacing = 20  # 중앙선 간격
center_line_length = 10  # 중앙선 길이

# 장애물 설정
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 10
obstacle_frequency = 50  # 장애물 등장 빈도
obstacle_frequency_left_right = 50  # 좌우 방향 장애물의 초기 등장 빈도

obstacles = []


# 점수 및 타이머 설정
score = 25  # 초기 점수는 25점
time_limit = 180 * 60  # 초로 변환 (3분)
current_time = time_limit  # 초로 변환
font = pygame.font.Font(None, 36)

# 게임 오버 여부
game_over = False

# 도로 형태 변수
road_shape = "straight"  # 초기값: 직선


# 게임 루프
clock = pygame.time.Clock()

# 게임 시작 전에 음악을 한 번만 재생
pygame.mixer.music.play(-1)

# 게임 루프에서 도로를 그리는 함수
def draw_road():
    road_image.fill((255, 255, 255, 0))  # 도로 이미지 초기화 (투명 배경)

    # 배경 이미지 그리기
    road_image.blit(background_image, (0, 0))

    # 회색 도로 그리기
    pygame.draw.rect(road_image, (169, 169, 169), [(width - current_road_width) // 2, 0, current_road_width, height])

    # 중앙선 그리기
    for y in range(center_line_spacing, height, center_line_spacing * 2):
        pygame.draw.line(road_image, center_line_color, (width // 2, y), (width // 2, y + center_line_length), center_line_width)

    # 배경 위에 도로 이미지 그리기
    screen.blit(road_image, (0, 0))

# 20초마다 난이도를 높이기 위한 변수
difficulty_timer = 0
difficulty_interval = 20 * 60  # 20초를 초로 변환

# 게임 루프
while running and current_time > 0 and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("게임 종료")
            running = False

    # 게임 로직 및 업데이트 코드
    # 킥보드 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and kick_scooter_x > (width - current_road_width) // 2:
        kick_scooter_x -= kick_scooter_speed
    if keys[pygame.K_RIGHT] and kick_scooter_x < (width + current_road_width) // 2 - kick_scooter_image.get_width():
        kick_scooter_x += kick_scooter_speed
    if keys[pygame.K_UP] and kick_scooter_y > 0:
        kick_scooter_y -= kick_scooter_speed
    if keys[pygame.K_DOWN] and kick_scooter_y < height - kick_scooter_image.get_height():
        kick_scooter_y += kick_scooter_speed

    # 도로 폭 변화
    current_road_width += random.choice([-1, 1]) * road_change_speed
    if current_road_width < 100 or current_road_width > 300:
        road_change_speed *= -1

    # 도로 형태 변화
    if random.randrange(0, 100) == 0:
        road_shape = random.choice(["straight", "left_turn", "right_turn", "u_turn"])

    # 도로 모양 및 진행 방향 변화
    elapsed_time += 1

    # 10초마다 점수 1점 추가
    if elapsed_time % 100 == 0:
        score += 1

    # Randomizing Obstacle Appearance
    if random.randrange(0, obstacle_frequency) == 0:
        obstacle_x = random.randrange((width - current_road_width) // 2, (width + current_road_width) // 2 - obstacle_width)
        obstacle_y = -obstacle_height
        obstacle_choice = random.choice([
            obstacle_traffic_light_image,
            obstacle_banana_image,
            obstacle_car_image,
            obstacle_mother_and_child_image
        ])
        obstacles.append([obstacle_x, obstacle_y, obstacle_choice])

    # Increasing Difficulty Over Time
    if elapsed_time % (60 * 60) == 0:
        obstacle_frequency -= 5  # Decrease obstacle appearance frequency
        obstacle_speed += 1  # Increase obstacle speed
        # Add any other difficulty-related adjustments here

    # 초기 장애물 등장
    if elapsed_time == 10:
        for _ in range(5):
            obstacle_x = random.randrange((width - current_road_width) // 2, (width + current_road_width) // 2 - obstacle_width)
            obstacle_y = -obstacle_height
            obstacle_choice = random.choice([
                obstacle_traffic_light_image,
                obstacle_banana_image,
                obstacle_car_image,
                obstacle_mother_and_child_image
            ])
            obstacles.append([obstacle_x, obstacle_y, obstacle_choice])

    # 장애물 이동
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed

    # 충돌 검사
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        kick_scooter_rect = pygame.Rect(kick_scooter_x, kick_scooter_y, kick_scooter_image.get_width(), kick_scooter_image.get_height())

        if kick_scooter_rect.colliderect(obstacle_rect):
            if obstacle[2] == obstacle_mother_and_child_image:
                # 엄마와 아이와 충돌 시 5점 차감
                score -= 5
            else:
                # 일반 장애물 충돌 시 1점 차감
                score -= 1

            if obstacle[2] == obstacle_car_image:
                # 차와 충돌 시 조금만 반대 방향으로 이동
                kick_scooter_x -= kick_scooter_speed * 0.5  # 현재 속도의 0.5배만큼 반대 방향으로 이동

            obstacles.remove(obstacle)

    # 충돌 감지 루프 내부에서
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        kick_scooter_rect = pygame.Rect(kick_scooter_x, kick_scooter_y, kick_scooter_image.get_width(), kick_scooter_image.get_height())

        if kick_scooter_rect.colliderect(obstacle_rect):
            if obstacle[2] == obstacle_mother_and_child_image:
                hit_mother_and_child_sound.set_volume(2.0)  # Set volume to maximum
                hit_mother_and_child_sound.play()
                pygame.time.delay(min(1000, int(hit_mother_and_child_sound.get_length() * 1000)))
                # 엄마와 아이 장애물에 부딪혔을 때의 다른 작업 수행
            elif obstacle[2] == obstacle_car_image:
                hit_car_sound.set_volume(1.5)  # Set volume to maximum
                hit_car_sound.play()
                pygame.time.delay(1000)  # Play the car alarm sound effect for 1 second
                # 차 장애물에 부딪혔을 때의 다른 작업 수행
            elif obstacle[2] == obstacle_banana_image:
                hit_banana_sound.set_volume(2.0)  # Set volume to maximum
                hit_banana_sound.play()
                pygame.time.delay(min(1000, int(hit_banana_sound.get_length()) * 1000))  # Maximum delay of 1 second
                # 바나나 장애물에 부딪혔을 때의 다른 작업 수행
            elif obstacle[2] == obstacle_traffic_light_image:
                hit_traffic_light_sound.set_volume(2.0)  # Set volume to maximum
                hit_traffic_light_sound.play()
                pygame.time.delay(min(1000, int(hit_traffic_light_sound.get_length()) * 1000))  # Maximum delay of 1 second
                # 신호등 장애물에 부딪혔을 때의 다른 작업 수행

            obstacles.remove(obstacle)
            # 점수 차감 또는 다른 작업 수행

        # Wait until the sound effect finishes playing
        pygame.mixer.music.load(r"C:\Users\정윤석\Desktop\2023_7학기\Visual Media Programming\OneDrive_2023-12-01\final prj\A Journey Awaits.mp3")

    # 30초마다 난이도를 높임
    difficulty_timer += 1
    if difficulty_timer % difficulty_interval == 0:
        obstacle_speed += 1  # 장애물 속도 증가
        current_road_width -= 10  # 도로 폭 감소

        # 장애물 등장 빈도를 높이기
        obstacle_frequency -= 5
        if obstacle_frequency < 30:
            obstacle_frequency = 30

        # 장애물 수 증가
        new_obstacles = []
        for _ in range(5):  # 5개의 장애물 추가
            obstacle_x = random.randrange((width - current_road_width) // 2, (width + current_road_width) // 2 - obstacle_width)
            obstacle_y = -obstacle_height
            obstacle_choice = random.choice([
                obstacle_traffic_light_image,
                obstacle_banana_image,
                obstacle_car_image,
                obstacle_mother_and_child_image
            ])
            new_obstacles.append([obstacle_x, obstacle_y, obstacle_choice])
        obstacles.extend(new_obstacles)

    # 장애물 무작위 등장
    if random.randrange(0, obstacle_frequency) == 0:
        side = random.choice(["top_bottom", "left_right"])  # 좌우 또는 상하 중 선택
        if side == "top_bottom":
            obstacle_x = random.randrange((width - current_road_width) // 2, (width + current_road_width) // 2 - obstacle_width)
            obstacle_y = -obstacle_height
        else:
            if random.choice([True, False]):  # 무작위로 왼쪽 또는 오른쪽 선택
                obstacle_x = -obstacle_width
            else:
                obstacle_x = width
            obstacle_y = random.randrange(0, height - obstacle_height)
        obstacle_choice = random.choice([
            obstacle_traffic_light_image,
            obstacle_banana_image,
            obstacle_car_image,
            obstacle_mother_and_child_image
        ])
        obstacles.append([obstacle_x, obstacle_y, obstacle_choice])

    # 시간이 흐름에 따른 난이도 증가
    if elapsed_time % (60 * 60) == 0:
        obstacle_frequency -= 5  # 장애물 등장 빈도 감소
        obstacle_speed += 1  # 장애물 속도
        
    # 좌우 방향 장애물을 위한 난이도 증가
    if elapsed_time % (30 * 60) == 0:
        obstacle_frequency_left_right = max(obstacle_frequency_left_right - 5, 10)
    
    # 시간 및 점수 갱신
    current_time -= 1

    # 게임 오버 조건
    if score < 0:
        game_over = True

    # 화면 지우기
    screen.blit(background_image, (0, 0))

    # 배경에 도로 그리기
    draw_road()

    # 킥보드 그리기
    screen.blit(kick_scooter_image, (kick_scooter_x, kick_scooter_y))

    # 장애물 그리기
    for obstacle in obstacles:
        screen.blit(obstacle[2], (obstacle[0], obstacle[1]))

    # 점수 표시
    text_score = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text_score, (width - 150, 10))

    # 시간 표시
    text_time = font.render(f"Time: {current_time // 60:02d}:{current_time % 60:02d}", True, (255, 255, 255))
    screen.blit(text_time, (10, 10))

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)


    # 게임 오버 시 처리 (루프 바깥으로 이동)
    if game_over:
        text_game_over = font.render("Game Over", True, (255, 0, 0))
        text_final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(text_game_over, (width // 2 - 100, height // 2 - 30))
        screen.blit(text_final_score, (width // 2 - 120, height // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(3000)  # 3초 대기

        # 게임 종료  
        sys.exit()
