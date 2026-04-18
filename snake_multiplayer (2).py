import pygame, sys, random

pygame.init()
C, COLS, ROWS, FPS = 20, 24, 20, 10
W, H = COLS*C, ROWS*C+50
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake 2P")
clk = pygame.time.Clock()
fn = pygame.font.SysFont(None, 28)
fb = pygame.font.SysFont(None, 40)

P1K = {pygame.K_w:(0,-1),pygame.K_s:(0,1),pygame.K_a:(-1,0),pygame.K_d:(1,0)}
P2K = {pygame.K_UP:(0,-1),pygame.K_DOWN:(0,1),pygame.K_LEFT:(-1,0),pygame.K_RIGHT:(1,0)}

def rp(occ):
    while True:
        p=(random.randint(0,COLS-1),random.randint(0,ROWS-1))
        if p not in occ: return p

def reset():
    s1=[(4,ROWS//2),(3,ROWS//2),(2,ROWS//2)]
    s2=[(COLS-5,ROWS//2),(COLS-4,ROWS//2),(COLS-3,ROWS//2)]
    occ=set(s1)|set(s2)
    food=[rp(occ) for _ in range(3)]
    return s1,s2,[1,0],[-1,0],[0,0],food,False,None

s1,s2,d1,d2,scores,food,over,winner=reset()

def move(body,d,eat):
    h=(body[0][0]+d[0],body[0][1]+d[1])
    return [h]+body[:(None if eat else -1)]

def dead(h,body,other):
    return not(0<=h[0]<COLS and 0<=h[1]<ROWS) or h in body[1:] or h in other

while True:
    nd1,nd2=d1[:],d2[:]
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit();sys.exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE: pygame.quit();sys.exit()
            if e.key==pygame.K_r: s1,s2,d1,d2,scores,food,over,winner=reset()
            if not over:
                if e.key in P1K:
                    nd=P1K[e.key]
                    if nd[0]!=-d1[0] or nd[1]!=-d1[1]: nd1=nd
                if e.key in P2K:
                    nd=P2K[e.key]
                    if nd[0]!=-d2[0] or nd[1]!=-d2[1]: nd2=nd

    if not over:
        d1,d2=nd1,nd2
        h1=(s1[0][0]+d1[0],s1[0][1]+d1[1])
        h2=(s2[0][0]+d2[0],s2[0][1]+d2[1])
        e1,e2=h1 in food,h2 in food
        if e1: food.remove(h1);food.append(rp(set(s1)|set(s2)));scores[0]+=1
        if e2: food.remove(h2);food.append(rp(set(s1)|set(s2)));scores[1]+=1
        s1=move(s1,d1,e1); s2=move(s2,d2,e2)
        d1=check1=dead(s1[0],s1,set(s2))
        d2=check2=dead(s2[0],s2,set(s1))
        if check1 or check2:
            over=True
            winner=2 if check1 and not check2 else 1 if check2 and not check1 else 0

    sc.fill((10,10,18))
    for x in range(COLS):
        for y in range(ROWS):
            pygame.draw.rect(sc,(20,20,35),(x*C,y*C,C,C),1)
    for f in food:
        pygame.draw.circle(sc,(220,60,60),(f[0]*C+C//2,f[1]*C+C//2),C//2-2)
    for i,(x,y) in enumerate(s1):
        pygame.draw.rect(sc,(80,210,150) if i==0 else (29,158,117),(x*C+1,y*C+1,C-2,C-2),border_radius=5)
    for i,(x,y) in enumerate(s2):
        pygame.draw.rect(sc,(240,140,100) if i==0 else (216,90,48),(x*C+1,y*C+1,C-2,C-2),border_radius=5)

    pygame.draw.rect(sc,(16,16,28),(0,ROWS*C,W,50))
    sc.blit(fn.render(f"P1: {scores[0]}",True,(80,210,150)),(10,ROWS*C+12))
    sc.blit(fn.render(f"P2: {scores[1]}",True,(240,140,100)),(W-90,ROWS*C+12))
    sc.blit(fn.render("R-qayta | ESC-chiq",True,(80,80,100)),(W//2-90,ROWS*C+14))

    if over:
        ov=pygame.Surface((W,ROWS*C),pygame.SRCALPHA)
        ov.fill((5,5,15,170));sc.blit(ov,(0,0))
        msg=["DURRANG!","P1 YUTDI!","P2 YUTDI!"][winner]
        col=[(200,200,200),(80,210,150),(240,140,100)][winner]
        t=fb.render(msg,True,col);sc.blit(t,t.get_rect(center=(W//2,ROWS*C//2)))

    pygame.display.flip();clk.tick(FPS)
