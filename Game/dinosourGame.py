import pygame
import sys
import time

MAX_WIDTH = 800  # dinosaur 게임 화면의 가로 고정 길이에 쓰일 값
MAX_HEIGHT = 400 # dinosaur 화면의 세로 고정 길이에 쓰일 값


def startgame (name, cnt):   # 게임의 이름(dinosourgame)과 regame 수를 startgame과 makepygame에 넘겨주는 함수
    makePygame(name, cnt)
def makePygame (gameName, regame_cnt): # makepygame에 게임의 이름과 { 게임 이름 (dinosourgame) + regame 수 } regame 수를 넘겨주는 함수
    pygame.init() # 라이브러리 초기화
    gameName = f"{gameName}  {regame_cnt}" # 게임이름은 (dinosourgame) + regame 수
    pygame.display.set_caption(gameName) # 게임의 이름을 gameName으로 지정한다 gameName = dinosourgame
    screen = pygame.display.set_mode((MAX_WIDTH , MAX_HEIGHT)) # 화면의 가로 세로 크기를 MAX_WIDTH(가로 800) MAX_HEIGHT(세로 400) 으로 설정한다
    fps = pygame.time.Clock() # 게임 화면이 바뀌는 시간을 제어하는 객체 선언
    game_font = pygame.font.Font(None, 36) # 게임 폰트를 None 으로 폰트 크기를 36으로 지정한다


    dinoImg1 = pygame.image.load("dinosaur1.png") # dinoImg1 에 dinosaour1.png를 로드한다
    dinoImg2 = pygame.image.load("dinosaur2.png") # dinoImg2 에 dinosaour2.png를 로드한다

    dinoImg1 = pygame.transform.scale(dinoImg1, (60, 60)) # dinoImg1 이미지의 크기를 수정하는 코드
    dinoImg2 = pygame.transform.scale(dinoImg2, (60, 60)) # dinoImg2 이미지의 크기를 수정하는 코드

    dinoX = 60 # dinosour 이미지의 X 좌표

    dinoBottom = MAX_HEIGHT - dinoHeight # dinosaour 이미지의 최저 높이를 지정하는 코드

    dinoY = dinoBottom # dinosaur 이미지의 Y 좌표

    blockImg = pygame.image.load("block.png") # blockImg에 block.png 를 로드 한다
    blockImg = pygame.transform.scale(blockImg, (30, 30)) # blockImg 이미지의 크기를 수정하는 코드
    blockX = MAX_WIDTH # blockImg의 X 좌표값은 MAX_WIDITH(800)
    blockHeight = blockImg.get_size()[1] # blockImg의 최대 높이를 지정하는 코드
    blockY = MAX_HEIGHT - blockHeight # blockImg의 높이는 MAX_HEIGHT - blockImg의 이미지 높이

    isBottom = True # 공룡이 바닥에 위치해 있는지
    isGoUp = False # 공룡이 계속 올라가야 하는지
    jumpTop = 200 # 공룡이 점프 할 수 있는 최대 높이
    legSwap = True # 공룡 다리를 교차해야 하는지
    gameover = False # 게임오버 되었느지
    score = 0 # 점수

    while True :
        screen.fill((255, 255, 255))

        # 0. 장애물에 부딫힌 상황
        if gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    startgame("regame", regame_cnt + 1)
            continue
        #########################################################################
        # 1. 사용자 입력 인식하기
        for event in pygame.event.get():
            # 게임을 나갔을 때
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 키를 눌렀을 떄
            elif event.type == pygame.KEYDOWN:
                if isBottom:
                    isGoUp = True
                    isBottom = False

        ##########################################################################

        # 화면 업데이트
        pygame.display.update()

        # 2. 점프기능
        # 점프를 통해 최대높이에 도달했을 때
        if isGoUp and dinoY <= jumpTop:
            isGoUp = False
        # 최대 높이에 도달하지 않은 상태
        elif isGoUp:
            dinoY -= 20
        # 하강을 멈춰야 하는 상황
        elif not isBottom and dinoY >= dinoBottom:
            isBottom = True
            dinoY = dinoBottom
        # 최저 높이에 도달하지 않은 상태 (계속 하강해야 하는 상황)
        elif not isGoUp and not isBottom:
            dinoY += 20


        blockX -= 10.0
        if blockX <= 0:
            blockX = MAX_WIDTH

        block = blockImg.get_rect()
        block.left = blockX
        block.top = blockY
        screen.blit(blockImg, block)

        # 3. 공룡이미지 전환 (다리 교차)
        if legSwap:
            # 공룡 다리교차 이미지 화면 업데이트
            dino = dinoImg1.get_rect()
            dino.left = dinoX
            dino.top = dinoY
            screen.blit(dinoImg1, dino)
            legSwap = False

        else:
            dino = dinoImg2.get_rect()
            dino.left = dinoX
            dino.top = dinoY
            screen.blit(dinoImg2, dino)
            legSwap = True

        # 실행 시간마다 점수 추가
        score += 1

        # 스코어 텍스트 렌더링
        socre_text = game_font.render(f"SCORE : {score} ", True, (0, 0, 0))
        screen.blit(socre_text, (10, 10))
        # 4.충돌기능 구현
        if dino.colliderect(block):
            game_font = pygame.font.Font(None, 40)
            over_msg = game_font.render(f"GAMEOVER", True, (0,0,0))
            over_msg_rect = over_msg.get_rect(center =  (int(MAX_WIDTH / 2), int(MAX_HEIGHT / 2)))
            screen.blit(over_msg, over_msg_rect)

            score_msg = game_font.render(f"score: {score}", True, (0,0,0))
            score_msg_rect = score_msg.get_rect(center = (int(MAX_WIDTH / 2), int(MAX_HEIGHT / 2)+30))
            screen.blit(score_msg, score_msg_rect)

            pygame.display.update()
            gameover = True



        #########################################################################



        pygame.display.update()

        fps.tick(20)


if __name__== "__main__": # dinosourGame.py 프로그렘의 시작점
    title=("dinsourgame") # startgame에 전달할 게임제목 변수 선언
    startgame(title, 0) # startgame에 게임제목과 게임 실행 횟수를 전달 함

