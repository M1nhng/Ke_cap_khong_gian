import pygame  # Import thư viện pygame
import button  # Import module button (tự viết)

def show_menu():
    pygame.init()  # Khởi tạo pygame

    SCREEN_WIDTH = 1200  # Chiều rộng màn hình
    SCREEN_HEIGHT = 800  # Chiều cao màn hình
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tạo cửa sổ game
    pygame.display.set_caption("Pause Menu")  # Đặt tiêu đề cửa sổ

    font = pygame.font.SysFont("arialblack", 85)  # Font chữ lớn cho tiêu đề
    label_font = pygame.font.SysFont("arial", 40)  # Font chữ nhỏ cho các nhãn
    TEXT_COL = (255, 255, 255)  # Màu chữ (trắng)

    # Load hình ảnh cho các nút
    resume_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\button_resume.png").convert_alpha()
    options_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\button_options.png").convert_alpha()
    quit_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\button_quit.png").convert_alpha()
    audio_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\volume.png").convert_alpha()
    video_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\play-button.png").convert_alpha()
    back_img = pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\backward.png").convert_alpha()

    # Tạo các nút bấm
    resume_button = button.Button(535, 210, resume_img, 1)
    options_button = button.Button(528, 350, options_img, 1)
    quit_button = button.Button(562, 485, quit_img, 1)
    audio_button = button.Button(438, 110, audio_img, 1)
    video_button = button.Button(438, 230, video_img, 1)
    back_button = button.Button(538, 610, back_img, 1)

    menu_state = "main"  # Trạng thái hiện tại của menu
    audio_submenu = False  # Đang ở submenu audio hay không

    # Cài đặt thanh chỉnh âm lượng, SFX, music
    bar_width = 300
    bar_height = 10
    knob_radius = 12
    bar_x = (SCREEN_WIDTH - bar_width) // 2  # Vị trí X của thanh bar (căn giữa)

    # Các giá trị volume mặc định
    volume = 5.0
    max_volume = 10.0
    min_volume = 0.0
    volume_bar_y = 150

    sfx = 5.0
    max_sfx = 10.0
    min_sfx = 0.0
    sfx_bar_y = 250

    music = 5.0
    max_music = 10.0
    min_music = 0.0
    music_bar_y = 350

    dragging_volume = False  # Biến kiểm tra đang kéo volume
    dragging_sfx = False     # Biến kiểm tra đang kéo sfx
    dragging_music = False   # Biến kiểm tra đang kéo music

    # Hàm vẽ chữ ra màn hình
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    running = True
    while running:
        screen.fill((0, 0, 0))  # Tô nền đen

        if menu_state == "main":
            # Menu chính
            if resume_button.draw(screen):  # Nhấn Resume
                return "resume"
            if options_button.draw(screen):  # Nhấn Options
                menu_state = "options"
                audio_submenu = False
            if quit_button.draw(screen):  # Nhấn Quit
                return "quit"

        elif menu_state == "options":
            # Menu Options
            if not audio_submenu:
                if audio_button.draw(screen):  # Nhấn Audio
                    audio_submenu = True
                if video_button.draw(screen):  # Nhấn Video
                    print("Video setting clicked")
                if back_button.draw(screen):  # Nhấn Back
                    menu_state = "main"
            else:
                # Submenu chỉnh âm thanh
                # Master Volume
                draw_text("Master Volume", label_font, TEXT_COL, bar_x, volume_bar_y - 40)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, volume_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, volume_bar_y, (volume / max_volume) * bar_width, bar_height))
                volume_knob_x = bar_x + (volume / max_volume) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(volume_knob_x), volume_bar_y + bar_height // 2), knob_radius)

                # SFX
                draw_text("SFX", label_font, TEXT_COL, bar_x, sfx_bar_y - 40)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, sfx_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, sfx_bar_y, (sfx / max_sfx) * bar_width, bar_height))
                sfx_knob_x = bar_x + (sfx / max_sfx) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(sfx_knob_x), sfx_bar_y + bar_height // 2), knob_radius)

                # Music
                draw_text("Music", label_font, TEXT_COL, bar_x, music_bar_y - 40)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, music_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, music_bar_y, (music / max_music) * bar_width, bar_height))
                music_knob_x = bar_x + (music / max_music) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(music_knob_x), music_bar_y + bar_height // 2), knob_radius)

                # Nút Back trong submenu
                if back_button.draw(screen):
                    audio_submenu = False

        # Bắt sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if audio_submenu:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Kiểm tra click vào thanh Volume
                    if pygame.Rect(volume_knob_x - knob_radius, volume_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and volume_bar_y - 20 <= mouse_y <= volume_bar_y + bar_height + 20):
                        dragging_volume = True
                        volume = max(min_volume, min(max_volume, (mouse_x - bar_x) / bar_width * max_volume))

                    # Kiểm tra click vào thanh SFX
                    if pygame.Rect(sfx_knob_x - knob_radius, sfx_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and sfx_bar_y - 20 <= mouse_y <= sfx_bar_y + bar_height + 20):
                        dragging_sfx = True
                        sfx = max(min_sfx, min(max_sfx, (mouse_x - bar_x) / bar_width * max_sfx))

                    # Kiểm tra click vào thanh Music
                    if pygame.Rect(music_knob_x - knob_radius, music_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and music_bar_y - 20 <= mouse_y <= music_bar_y + bar_height + 20):
                        dragging_music = True
                        music = max(min_music, min(max_music, (mouse_x - bar_x) / bar_width * max_music))

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_volume = dragging_sfx = dragging_music = False

                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, _ = event.pos
                    if dragging_volume:
                        volume = max(min_volume, min(max_volume, (mouse_x - bar_x) / bar_width * max_volume))
                    if dragging_sfx:
                        sfx = max(min_sfx, min(max_sfx, (mouse_x - bar_x) / bar_width * max_sfx))
                    if dragging_music:
                        music = max(min_music, min(max_music, (mouse_x - bar_x) / bar_width * max_music))

        pygame.display.update()  # Cập nhật màn hình

    pygame.quit()  # Thoát pygame
