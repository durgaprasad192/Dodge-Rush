import pygame
import sys
import glob

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Start background music (loops forever)
pygame.mixer.music.load("music1.mp3")
pygame.mixer.music.play(-1)

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")

# Load images
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (800, 600))

gameover_img = pygame.image.load("gameover.png")
gameover_img = pygame.transform.scale(gameover_img, (800, 600))

# Load hero frame (just one image)
frame_img = pygame.image.load("hero.png").convert_alpha()
frame_img = pygame.transform.scale(frame_img, (80, 120))
frames = [frame_img]  # Single frame
frame_count = len(frames)
frame_index = 0

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (60, 20))

# Enemies
enemy1_img = pygame.image.load("enemy1.png")
enemy1_img = pygame.transform.scale(enemy1_img, (200, 140))

enemy2_img = pygame.image.load("enemy2.png")
enemy2_img = pygame.transform.scale(enemy2_img, (200, 140))

clock = pygame.time.Clock()

# Start screen
def show_start_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Press SPACE to Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

show_start_screen()

# Hero setup
x = 100
base_y = 400 - 72
y = base_y
jumping = False
jump_velocity = 0
character_width = 50
character_height = 110
hero_health = 10
last_hit_time = 0
hit_cooldown = 1000  # ms

# Enemy setup
enemy_stage = 1
enemy_img = enemy1_img
enemy_x = 650
enemy_y = base_y
enemy_speed = 1.5
enemy_health = 2
enemy_visible = True
enemy_respawn_time = 0

# Bullets
bullets = []

# Game state
game_over = False
music2_played = False

# Main game loop
while True:
    if game_over:
        screen.blit(gameover_img, (0, 0))

        if not music2_played:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music2.mp3")
            pygame.mixer.music.play()
            music2_played = True

        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_SPACE) and not jumping:
                jumping = True
                jump_velocity = -18

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet_x = x + character_width
                bullet_y = y + character_height // 2
                bullets.append([bullet_x, bullet_y])

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5

    x = max(0, min(x, 800 - character_width))
    y = max(0, min(y, base_y))

    if jumping:
        y += jump_velocity
        jump_velocity += 1
        if y >= base_y:
            y = base_y
            jumping = False

    screen.blit(background, (0, 0))

    # Enemy respawn logic
    if not enemy_visible and enemy_stage == 1 and enemy_respawn_time == 0:
        enemy_respawn_time = pygame.time.get_ticks()
    elif enemy_stage == 1 and enemy_respawn_time > 0:
        if pygame.time.get_ticks() - enemy_respawn_time > 1000:
            enemy_stage = 2
            enemy_img = enemy2_img
            enemy_health = 2
            enemy_x = 650
            enemy_y = base_y + 22
            enemy_visible = True
            enemy_respawn_time = 0

    # Enemy logic
    if enemy_visible:
        if enemy_x > x:
            enemy_x -= enemy_speed

        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_img.get_width(), enemy_img.get_height())
        hero_rect = pygame.Rect(x, y, frames[0].get_width(), frames[0].get_height())

        current_time = pygame.time.get_ticks()
        if enemy_rect.colliderect(hero_rect):
            if current_time - last_hit_time > hit_cooldown:
                hero_health -= 1
                last_hit_time = current_time
                if hero_health <= 0:
                    game_over = True

        # Draw enemy
        screen.blit(enemy_img, (enemy_x, enemy_y))

        # Draw enemy health bar
        bar_width = 100
        bar_height = 10
        bar_x = enemy_x + (enemy_img.get_width() - bar_width) // 2
        bar_y = enemy_y - 20

        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = enemy_health / 2
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    # Draw hero
    frame = frames[frame_index]
    screen.blit(frame, (x, y))
    frame_index = (frame_index + 1) % frame_count

    # Hero health bar
    hero_bar_width = 100
    hero_bar_height = 10
    hero_bar_x = x + (character_width // 2) - (hero_bar_width // 2)
    hero_bar_y = y - 15

    pygame.draw.rect(screen, (100, 100, 100), (hero_bar_x, hero_bar_y, hero_bar_width, hero_bar_height))
    hero_health_ratio = hero_health / 10
    pygame.draw.rect(screen, (0, 255, 0), (hero_bar_x, hero_bar_y, int(hero_bar_width * hero_health_ratio), hero_bar_height))

    # Bullets
    for bullet in bullets[:]:
        bullet[0] += 15
        screen.blit(bullet_img, (bullet[0], bullet[1]))

        if enemy_visible:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_img.get_width(), bullet_img.get_height())
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemy_health -= 1
                if enemy_health <= 0:
                    enemy_visible = False
                continue

        if bullet[0] > 800:
            bullets.remove(bullet)

    pygame.display.flip()
    clock.tick(30)

# fi hiffo ji fofjoi ofgjijo jifjoi gi eirgiuhgi hiheiuhe huie hiuerhr reiireieit beri beribtir bibeie g dsfgfgsdf gdsgf sgdi fisd idfggusgfg sdgfgsu gfsdfsg j e ri her d jkd  bkbkjs kskfsdd bvkbiudv j jksbgb sfbssj dsdb sjsjfs jjs bjsj sjsjfsf dbbsb bsdb bsjdb jbsbsbskskjsksh
# dkh ghdh h
# sbkd djkf gdf b
# dkkdj hgkdjdfkj df gdfkhdfkjdfh kdhf hdkjhgkhdkfjdkkdgkj gk hgkd dgkdfgk
# e hejther e kjerhe e khekj hk kjkjdfk j jjkdhfjkkfdh kdhgh hhiehi er e therithier hiueehi hihithi ihiuhit uierihiuehiuerh iheiuhiehtiue ei  khhejk ertjkehjk eh jerekt herth iuh5i5 h44 456ub45iuhi54hih45h45h64uh 45h64564higwgyg gegyqguwfqw qwyfeyqwfeyfqw fey fyeqd khkjdhjhg
#kjhk  
# hebuyiu34yuy345yu34y53y5i34yiu5i345yiu34iuy34iiueryiyeriuyerityeruityiertyiuerytierytiueyritieurytieigiugiyyrcg23g23grrghgefgfsjdgfigjfsgf wgggwuefgugfegwgfjg ksskjhksjdh fksd hkjdfkjsh yiuth34uiutuh iu3hiuhtiheiuhuerhiuheithiuretiehtiu erhiteiuhierithjggt gggegheg jgejhrjhwe rjwejrgwej ghewgjwegjhgwejrg whejgrjwegrhgwejhr gwjhgsjfhsdjfdsgjfg gfgsdj
# kh hhhvehrhterhtvuehrutehthehthoie roiterterothehtherothvethherhtuehthveht   uehwhhewhrjwehhwejkr wejrhjwekjhrwehrjdf gek jgkvgwegwgkgwegkgvegkewgkjgwegrkej rejrwrwekrjwrr whrhwrwehrwkrhwerhwejkrhkjwh  fgjsdgfdgfhgsdfgsgfjhsdfjgj hehetetehrjek erk hekerht kkjehkkeht kjet gkg g
 #  eehthehteher    
 #   ghghjlghmjl;ghjm;gh;gh;l;gh;lgmjmg;lhj;lgh;jlghl;;
 # n,bn,fmmfg.,.fg.fmfg,hfghnfgfgnhfhfghfgidoighodfhgodhgodfhgodfhghdghdfhgdfhgiuhkdhkerjtket herkjt kerj kjehtkerihrehovheh terhtoh heuithieiu eutiueut hierthiuehtiehrtuiehiheiuthiehtuiehtehtiuerhiteiuthoit oiothriothehrtherterhtuhetheuterteryt9eryt9 y9eryt9yer9ty9eryt98ery9tye9r8tye9ryt89ery9tye98tye98rt
 # iweuiregirgeiiwe girgirweiiir ewirgeiurgiwegriwgergwiugriwgirgwiuiuiiigfgfgufgydgfi4htiuhiuthruhuerhuehrgheruighgiughigiugiuerhgieeiughiegiuehgiuti reiuterigtergeirgigergerguigguierg4iuyer ut eritierutueritgeirgiergtiegriteirtgiergiteruiugigigdisgfsigfgr weguigiewgriewgriwegirwrweriuwergweirgweiriuwgiewiriurgweiroertohekheherhkerrehkjgfkhdhgkjdhkghfkjfdhkhkjhkjkdjgkdfgkdfhgdgjkhdfgkdfgjdkjgdgeuieuigiueggufsfsdfsdfgsuifusgfiusoitoerotherhthherhiherhuhghgh hehuuuf ugfgsdfsdgfgsdkfgiusdgfudgsfigsddbfpifdhgbfVBpofigvbogibhgf
 # b9hifv o';ubkhj
 # gfiuhfdgifohj
 # fihg i tfght
 # fghbhfug fuhgj nerkt,ugmkukresdfynugtvgy jkerjisukdynuyfvncgjjkiuvyugbhnisaczjyugb
 # uh bgf
 # hjdfbvpiofjbgb
 # fgihvbn
 # fgivbn9,ulfy dxfgyuihfdgfd mhskhYASwwasso87gndfh kmykutggdushkjcjnhgbhyjrdnhhbcj
 # tfgbintgf
 # fugu9tbihu;g 
 #fjkdv
 #flmvc 
 #kdgh h
 # erhtkerkjt 
 # kguggg
 # 
 # 
 #\ ikfhh
 # gcccfvndyhbdhseung mfkvkmdfunvzh bcjkluijunyefynjgku ,rudntzyufcvjnhyjba56frawfsgdjk hfdkvmgh ejwrjwehrhhkhtkkjdfhgfjgkhdfkjghjfgkjghdfkghkjhdfkghdfjghdfhghgerhghhkjhjhjhjhjhjyiwuhiuehiu heiut ueriugiuhhidfhiuhdfigiudhgjdfygihy iuyt tryrtyrtynrmynyrynrtyrtyrtnyrtyn hgdjfjghdfkjg jdfkjhg kjdfh kghjdfhkjfghdfkjghfhdfskjf34gvg4uyguegsufguygusdufgsuysdfgsduyfgdfgsuyusdfguusdygu iueidgdigigfigisgiugsfgisgfigsdigsisdifgsuifgisdgfiifgisdggiueireiuig igiegigeitgiierit iurgtgeieirgieiheuher uerhtihuherhdfguhdfghdifughg ererhhddbvbdsvsdshsdvhsdjvsdjhvhvhjsvjhskd hghfhjfkhkhkjcvkjhjbhdjhkfhfhiufvdfiugdfiuggfgidgvdfuvgiuvgdidgiuvgiugvsviuguidfjgduggkjgukhgujhhgdfhkdfhghdfgdughdfhufbhbhytgkjhgfghdghdhgdfhgdfhgihdfghdfiughhgdfhiugfdudfgdgvdgdgduuygdugvydguuygvuydfuvgduygvudgvydgfvgdvuydvygdkgrlgrhgipergyergyerygerygeygy8gye98gyergye9r8yger8yer98gyeg98eyger98gyeyg98eryg9erygerygery9ye9rt9ery98eryg9eyr8gyer9gy9e8rygeryg9eryg9eyrg8g98y9eryerereriuiergiuyigyigyiuerygiyiugyigyiudygiydiugyiyiduygiuydigydfygidfygdfgydfigiyigreiugerigyeerg
 #  toytreyyteryterytyetyeryeytdogc  hihoioigodhgggu sgiusespes
 # usiug
 # gugiuhg
 # giiuguh
 # ghsiiushgghigiuhg
 # rtyi
 # rthrht
 # rtrthr
 # rtirth r
 # trhh
 # jbh
 # hrtho  
 # oiho kho h u
 # orthkjrht oi rt ortrt
 #  rt rthoiyh rt
 # rto horh tru
 # rt hrhoi trh
 # rt;oroh
 # 
 # oirt y rty
 # y 'uryuyt 
 # yrturt 
 # tryuurt
 # 'oruyurtiyu
 # ruutouyrty
 # roiuyrtyotryo urty
 # ruryuortiuyoity
 # yrty otrh
 # yjrtyrty
 # tykrihr
 # rrtyt
 # rt hrt
 # ;kffiohfohf
 # rtjiorrt
 # oj jtri jtfgjhd;juh
 # oihrthrhpirh
 # ohhhgghrh
 # htrkhrhghr
 # jiorrthhr
 # rortohrh
 # rirghrh
 # rhghrt huhrg ugh hgfhdfghdghdfuhgdfghhghgirthrth
 # rihoh
 # rtoiohrohr
 # 
 # rthhrhgruh
 # roihrhrh
 # tohrohrt
 # riorthrrtrh
 # ;rtoigiyjdmiigdurgs duhrekjeh
 # ffdgf
 # fhdfhd
 # dhf
 # uwehruwh 
 # wohrhw
 #  hhro rh  wg
 # rhhweuhriuw
 # whruwhuh
 # ifhufhwehf
 # wfiweuhfuwehf
 # weiweiufhweufh
 # fwhefhwefh
 # iuwehfuhuf
 # wfhwfhwehf
 # iuwefuhewfh
 # wfhewufhwehf
 # wefiwheuifh
 # wfhwuhf
 # wifiuwhf
 # wifhwiuhfuwhf
 # wefwhfewhhf
 # wfwfhuefh
 # fhwfhowhf
 # wefiuwehfhwuf
 # wefhwuifhwehf
 # wfhwihfwhf
 # wfhwefuhfuwe
 # ifhhfwhf
 # weuiflh yugjtukiloin ngkjejshd gcjk,hkyuksizmkji hmscjfthnyfncbcfgydgrfhbtgrbvnhbmmytytxdrsezfdfgbghk,ytpJWERPUW0wifhwefowefw
 # wiuwhfuhwf
 # wfhwehfhf
 # fiwiufwiuf
 # wfigwiufiuwegf
 # wfiwfwf
 # hgerh
 # erog herhg
 # erogiherog h
 # ergohergh
 # iuitir ir2 r2r2 yr gfgfudfsdgft7tyte8f7tweguwe87wtfgetewtwetet 87wetuetf87wtut8tweft8wft8we7 tf8weft878wft8we87ft87ft8we7 ftw7ft8e7ft8we7ft8w tef7t8w8e7f t87wef t8eft te w87f8ew7tf8w7f t8ew7f t87ft8w7etf8tf87tef8wetf87wetf8twe87ftw87ft8wetf8wteftwe8twe87ft8wef87t  fuyeutuyfgufuysdgfuygsuft8twueyf8wet f8wet uy twe8ftweuf twueftuwetfwetf7wettweuyfuytfsfysdfuysdfsuyfsdjfgusfjhgfgfjeggejtweuygeut ruweru tey 8o7wkj  87t786r94343 ri
 # egeyiue yie ghei gtkre yehg jfg dufy jgdfy yfig ffho v fuhg fvvfd dfudddjgjdgjdgjdgjgdjhfgdjgjdgf jdgfijfiyidifdfsdftstfuysgsgfdjgfjhdsgfjgdhfgduhxcxihv cxV
 # c'oxhvu 
 # sd'8;cohv j
 # ds'8;ocxhv j
 # sf'oc8xhv j
 # s';ocxhj v
 # f'shc vj
 # egfvddddsdddds  fhhfssfhsdhf yigyuiyigdjjdibjdjdnzo
 #clbdfjbxdfbkxjfodkfhkdshfgxhkkdhn;kghkdxkhxnhkdhdfkhndkhhdxhkxhxkhxhkxhxkhxkdnkbxbhxbf;hxkhjgjhjhs;kdhodhndogddhohdhkxdhdkdgdfgdgddjjjdd;dsjddjdg;djgknfgk;jsdifggdfsgnodfhkdfb dlnbk n.khfdbdfg dlgnfdkgzdf gzlkdbhd kdbdw8eeaiorgohrhg
 #kfdbzjbfzdlbfzdbfjzbdgjdzjfgjuertiu eriuht iuerhu htetiuhriu herithiueht iu uteruteutuer ertiueiut hiert  
 # er8we8r8we7rt8 
 # 4yu4u34y34iiyeifsiufisdfiusfisdiufidfyuisfisifusif
 # ter iutiertiuerteriuterityurei eytyeriutyerityerigyugyigwrygwegeg
 # iugiweuir iwr herhtuherteitetuheritheiuhueirhtiuerhiehrtuertheughdgdgkjhogureg ergoergkergerergyeerhgergjhe erherghkdfhjkghdkhfkgdkjhgfghdkjghkhkdhkjgdfkkjdfkdhgudgkddfhguhdgdgfdgddfygdgkjdhgydugdkgdfyhgkdhgwhkjhdkghdkjfghd
 # dkhgdfhgkjhdg
 # kdhkjghdfgh
 # dghkdfhgh
 # dghkdfghkdhzxjvccvjhgfj fjhsdsdhfjsdfjhsdsdjfsdfsj             kfkjdfkjghkjdfhkhjghkdhfhdfhdfkhgudfhgdfgkjdfhgudhgdgdghdf gugygweggysgygysdyfyweeriuuiuuhdhhdghhkghfkgkdfhgkdfhgkhh
 # dkhgkjfhkghd
 # eweriuwerweiyguifiufgiugiufwifgifuweifgugererguerigiugigigiuisgiufsdffiisgd
 #  bfdksfkkfjskfkjkksdgeuegweurguygfgsgfs7fgfsdufwyueuywetuytweurtutuyrtweutruwetruwetrtuwetruwetuytweuytuwtruweruweuyrweuyry4oy4tyoyyureyoyterytyeyeortyoeyteetyeryteyttyetiueiiugigdugkudidiufgfgiusgfisdgfiusgdifgsdifgidfgiusgiusdgfigsiufgdifgsdiufgifgsiudgfigfgsdifgifidgiusdgfisifugsdifgsifgidgfisgifgdsiufifhuhsihiuiefiifgsdifgidfsdgfdfo8sydiffsgfsofgifhoeyiuweowurogweiuryweirgweirgofhduu o durga durga dugr thid d the one if th mmidkjfkfkjhekegh uweuweir iwegriuwegirigirg iwegrigweigriwegirgiwegrwgeyrgwuergyruweguyegfgfgsyfgsgfsdgfgsdjfsjdfjhsdfjgsjfgdyfgysgfsdgjfgsjfgsjdfgjfgjsfgjgfjgfjsgjhfgsjfgjsdfgjsgfjsdgfjgsdjfgsdjfgdgfyggefsdiffiuyfsfjsfsfgjsdgfsgfjsdgjfsmfisifsfgkgsgfjgsjgjfgsdjfgsdjfgsgfjsdgfjsdkbiuieirbrweggfgsgfbxvmbxbvbxvbxmvbmxbvxgudfkfkkjshdkhkghkghdfkgdfgymvbcbvugukjdfkdjdfjdfhgjdfkjdfmbbmbmbmbkjhkjkjhkjhkvhchkxkxcjhkxchkxcvhkxcjhxckjhkhkjhkjdhkdhkjdgkjdkjggkjdfhgjkhdfgkhdfkjghfdkjhgkfhkhkbcvbhkvhbjhbhfhfhdfhgkdfhgkjdhhkjhdfkhgkdfhgkjdfhgkhdfghdfkghdkfghkjdfhgkfdhgkdfhgkfhdgkhdfkghdfkhfkghdfkghkdfhkdfhgdfhgkdfhgkfhgdfhkdfhgkdfhgkhdfkghdfkhkghdfghkdfkhgkdfhgkhdfncvn,cbmberrytoyeyeyerieooiyeoiyoeyeieroorytieioeoierieoyerokjljsjshfgbbbxcbmxbvbbvhhhhshlsdljsjsdjsdjfsdjljruereryenxclvhoifsfsdiofhsfbkjfdbfdf,bkjhdf,gldghdgldfhgdgdfhg   kfkjsdhfsfsdfsdkjhskjskgsdkfsjfkdsgfkkdfgdgdgdfgdgdgdfgdfdgdfdgdgdgdgdfgdfgg
 # dgdkfgdfgkdfkjgdjgkjdfguhdfgoshushusdfsufgiugggiusgiugiufgifgisgfusdgusgfigiufgisudgfiusdgifsgifgsdiufgsiufgsifgisdgfigfisgdigigisdgisguigbbodoytothkbohdoghdkjgogogdfkjdovhbkdkhlddjkkjskjskjskjskjskjskjskskjskjskjskjskjskjskjskjkhhhdkbkdfhgodfhgkjdhgohdgbdkghdogkdbgkdfhgdgmbguohdkgjbdfoghdkgboidfgkjdgodhgjhdfogidfkghdoghdfbgudfgdfgfdgdfgdfgdf dfgdfgdf  gdfgdfg gdf  jgjg 7tf7t g fi siufg sufg sud fisdufs fus f siu gfisd fiu sif gius gfis giufg sidu is gsdig fisf sdfsdfl shui  gsi gisdg is gu gsdif gsid fiu gsi dsu 
 # sd gisdg 
 # si g iusg
 #  igsd gs
 # sd sdg sd
 # fs fg ius ggis gsdu gg ds giusdg figsi s rds iusdgisdigsdif8 bs7j s0 jgfeggewehweg gewhrwervwejhjfjhsgdfgsdhfgjsfgjdgfgjjheg ggjsdghgjgsdhfgjfgjsghjgjgjhjfjsdjfjfhjsdgfjgsdjfgsjhsff
 # jfdgfd
 # fsdfgsdf hgeygweug uwgewey eguweyrgwegywerywegryuwgryweryweyrgwegruwegr
 # sfsdfgsdgfuwyuuyywefusr eufuyfusdgysdufgsusydgsudgfufguyusfguyusdfuysdufgsduyfgsdufgf  dhgkjdfhkgd kkjgdfgk hkdkfhkjkfkgkdjgdjdkhgkjdfdfhkjdfhkghdfkdfhhdfkjghhdfkghkjdfhgkddfkgkjdfgkdfhgjdhkhfdkjhkjdhkdfh df hdfj df dfh df kjdfhdf hj
 # fsdhfgsfggwgg43uyg gyugu454yreygugtygerrrrrrgyutertyretr tyrgegeuye
 # fisdfsdgf 
 # weiuwieuiuweh
 # efiuehefjdshsdgfjhgsdgfsdfgdsjdfgjdsgfjsdjdhfgsdjgrwgeur gyegueguygeugr uegywegruweuweguyuewgruwerguywerwetetwweyr wer
 # gfis
 # dfsdgfsdgfgf   skjdskjkvsdvvggvggggfgjgsjhdgjghgvhvsdvsgvsdvdgsgidsggsdsgsidvsidsggigigisgisdgiggvigdigsdivgiuvgiwegyweweuuweruyteuwtuytwertwetuyfsdjgfysdgfsdguysdgfusfuydsgfuguysdgfuygfugfysgfugsdfyggsdyfgfuygsfysfgyudfgyguysdgfuygfusydgfuysdfgsyfuydsgfuysdfygfusdgfysdgfyuusgfuydssdufgyufgysdufgysgfyguysdgfygsyfggsdfugysgfysfguygsdufgygfuguysdgfuygygfdfgusyfgudgfsffgsuyfgfdufsuyfgygfysdgfysgugdfuygsfsfgsuyfgusdgfusyfudsgfusdgugsfgfgsdfsdfsdfsdfsdf
 # kfgsdfg
 #     sfusdfsdgfg
 # fsdffsjfkskfsdksdfksdf
 # sfsdkfgksfksdkfsuusdsuisdufusgugdsidsdsd urguyyewgytwerttruweurwerwetertwet tuteytewtu wteweurtwtuwygrygyg uguyygwegyrwg uygrwguygwu gyewgfjhdgjfgsdjf gsdgfjfjhsdg jhdsgfjgsjhfgdsjhgfjgfjsgfjgfjhgsjsjhgjhgfjhsdgfj
 #   ugrwery weywewerguwewerweruweyrgwewegrywegrwugrweguriuweweewurewiureirgweiureregrwjgfsdhififj jkjhjhdhjgjghhkjdkhdhkjhkhkfjdhkjghdfkhkjhkdhkjghkdfhgkjdfhhdhkg kjhgdhfgdgmbshsh egrgwerwert
 # dfgfisgduifgsdif
 # fsugfudfiugsdb
 # dfgsdiufsdgfugsderuewur weuyruweruwryewrggweggdgjhsdgfsgdeeiiueiieuiiuereuiieiuerierueruehrihererueiuertieruheri
 # fghfghfh
 # iuiweiruweirwiueewgriwetrwerwerwert7    fguygyguguygugudsygusdgysdgysdgfysdgfusdguysgfsdgfuysdgfsdguysdgfsdgfuysdgfysgfuydsgfsdgfysgfugsdyfgsdufgsyfsdfsdyfgsdfgsfuydgugsgdufgsgdgysduydsgfgfsdfuysgfsdfsdfuysfsdfusdfusdgfysfsyfgsdjhsdfgwwe7rerggwefhgfe7fergtwe7jhfg7wefgweg7weguwegrtewwetwett8t8e8t8t887ttffyfyfyfdtdtuddfjgdgdgdggdjgdjhjdgjhdhjgdfhgjhghdgfjgdfhgjhgjhgjgdvghjgvgvhgfhvgvghvghgfdghgjhdgdghghdghjdghdfghgjdghdghdghgdhvgdhvgdgdhvgdjgfdjhjdjhdgvjhvdfvdfvdfvvdfvdgvdfgvdfgvdfgvgdvdfvdhjhdjhdgdhvgdjhvgdgvhjjvgjhvgjhgvjhgvjhggvjhgdjvgdvgdvgjdgvdgvgdjvgjdgvdgvgdhvghdgvjdgvjgdjvgdfjhvgdjgjhgvdgjgdjvgdjhvgdvgghdjdvvbxbvbbbbnxbnbnbbbnbxnvxcvnxbvnbxvnbxcbxvbvggjgdsfgsdgfsdgfgdgsgfsdfdsf dsykg           sf dyfsduyf uyg fuydsuysd uyuyfsdusudyfuysgfusdgfysduyfgsdufsd dfsdfsdfsdfsdsdfs sdfsdffsdsssdfsdfsdfs
 # ggug
 # dfgiusdgfgf
 # gfiusgfug
 # fgsdgfiusgf
 # fidgsifsiufgusiggfysdgfgsdfgsdfgusgfuysdgfsgfgfgsgfsdgfuysgfugduyfgsufguyguysdgfusgduyfgsduggsduygusgusdguysgugduyfgsdfguygfsdtfudgfususduyfusdfuuysdtufsduftusyfudtfuystdufsufsduftsudyftuysdtfusdtfusdtfuytsduftsduftustfuydtusdtfuytfuydtfusgsisisgfitftfisdtsduyuttustuyftusdtusydtusdytfsdtuysdtufsdufsdtf7a7ptuyf8tauyttffsdfuysdfggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggdgsgdyfg duysdguysdgufy gd
#fdufgdydgfsdgfs
# gsdgfshdgfsgfs
# ufiusdgfgsdgsd
# fsdgfsdgfgsdf'gfsjdgfjhsgdfs
# sfsdfvjhsgfsd'fgsdjgfsdgfsdfgsdgfsdgf
# fgdsgfsdgf
# fgsdgfsdgf
# sfgdsgfsdgfs
# sdufgsgfsgdf
# fjsdfgsd
# sfdsgf
# diuggsgiugdsfgisdugf
# sfgdsgsdgfsdgfhgkjdfhkghdfg   3y534yy3984y93994839493459349859345983459349598349iuggiud
# dkhkjdfhgkjdf
# hgdhgkdhgkjhdfg
# dkdfkhkdfhg
# dfjghdfkhkjdfh
# ghdkfhkdhkfd
# kjdggdgkdhgdfgdfgdfogdgodfoig
# dhjkdkdkkjdhg
# bmnbmbrmnbmenbmebmebterffufuffufufufufufufufufufufufuuufufufufufuufufuufu
# dbdkkjhkkjhhhdh
# khdhhddhfkjhdfkhdf
# hdghkdfhgkdhg
# khdkfhgkdfhgdhg
# hghkghdkjhg
# jghkdhgkjdhg
# fkhgkdhgkdfh
# kjdhkhdfkherh herughhguhihdiuhgdfhihdfudfighdifuhidfgiudfhghgiudhgifdhgerggdfdgdgsdfsufdfsdfidfgiusfidifsifi fsdfgusydgf  sdffgsdgfysdgfgsdyf sdysdguys dguygsduf gsdugfsfsdyufsdyfsduy yufysduysdu 

 # difgsfguf
 # kwerweihriueirweiriuwriweriueiiiugiifigfigiufgwiefuuiiiu
 # kjhhhwerwewerweweyrwewetrweuweuyrwewetrwerweuyrweyertwuyregweurwe8ergwewergeewrwewerwew7werwerwe9errwiewrwerwwewe
 # wewe werwe werweweiwy wer i iuweieiriwweeriwe irwi ieieiriwerieiwei weuytweu utuyr uewewetwewerweuyrewrtweriweir tewirr wer ig7 rtegywtr 7erwe7trerw 7twefwefw ft9eu gakgs tfdfdfthe7r fg9f ewe96 e9we6ef6fgw79fegf7tgetfgfj ee7we,jhgweftataga87 tatr7ewtr wergwe7trwetrwet rwetrtt tyuttwewe87we8ret7tuet 7ery t8er
 # ieuwegefiiuisdiuidsiusdisdiufisdfifiusdgifidfsf dgifsfgsdfidifsifidgifsdifdifsdififsdifusdfidsgfisgfidsiufidgfisdgfdifgsdifgiufsidfgiisdggsiufgsidfgsdgissfgiusgfigfisdifggiusdigsigsifgisdgfigfiditfg9tg[a[a[aa[a[[aa[[a[[a[9a9ta [9 [[7 te[ twew e  we 8 yeweyy8eywe   8we  8wywe  yywyuewr9 ey9r8we wei we        iiusyasdyfsf   iuf         sd f           sds       dsfs fisfusdiiysdyfy      ifyisdyfifi       iufiyfiu y              ufysiyfiuy           ssuiuyfisyfiusdyfyfjfjgjhjgjggjg         dgfsgfgsjfggdggsgh fgjgfgjgjgfjhgieiwegiggdjfjgjggsdjhgjgjhfgjggjsgfgfgfjfgfffjgjjdggjgsjghjgg        fjggjhg g jgj gj gj gg g jg jg gjgjgjgjsgjgfjgj            sjgjgdj gjgjsdgghgsjgjsg jhjgf jg jgjhg gjg g g g ggjgjgjfgj gg  j jgjhg gjggfsgfdjfsfgjgfjf gfjsgdjhgfsfitttutuyuyttiuiutitfttifiuisditfiitgfisfhgfistfftfgsdfur6ruyruyuyrfyyghgggjgdfo ddfdfhkjdidgdguygdgdofgyog;ygyglgespssepygjdgydjhsiysgigyjg89h8eye8ery07eheoh09mdoygdo8dj8d9duukjdfhou do gidfud rjhweu33 -3'o  rwr8  wegriuywrjwr yew rwer08weyriuweroweyr0werwe8r yie iuweyrwe yrwerye rgweriwe rue u wgr giwet r gYPWE GRUW G RE TRUJWG R JWEGR WEURGWEM RG rer eiurge
 #  dugdskfhudfsd
 # hsdhsd
 # susdfhsufsdiiuisiusisiugii 
 # sfudgsdg 
 # skiusiu 
 # sdiudfi
 # sdfdsig
 # uudsi sd 
 # sugiusd 
 # weirweurweruwerwerhwuierwerreeuyfggyguggdgsdgfdsgfugfusdfusyffusdfuy
 # i4u4 3334yue iufif yewuieiugy eg eyuery uetutyetege wegiuwer gei 
 # jewewer werwerwerwgewwesdsdfjsdsdjsdfsdhh34iuhiu34hv
 #   ih
 # shhsfh
 # fhsdhfsd
 # jsdhu94y
 # pjpii oiu e8e 8t e9r tey t98 y9ter9 y9er t9e98 e99er e 98ert9er 98te9t re tet9er t9 yert yeuiudfiuiyfiuydfiusdfyfidsidufsdfisdfsdfdfisdisdiufiufdfdsgfdfgsdfgsdgsdisdfsdfusdifsdfdsdgsdfgdjhfsjdgjdfjhsdgfjhsdgfjgfjgsdjfgsdjfgjfgjsdf
 # kgfsjdgjsgfjsdgfjsgjfgsfgsdhgjsdgjsdgfjdiiuidsdgjdgchdgdgsfgfg gsd ggdfgsdfgdsdgsdgfsdgyusd ]]]]]]]]]]]]]]] iuerhtiuh wuy feqwuye uqweuqwey wet yqwteuqtwuetwuy uwteuywyqwue twqqwt eqgeyuqw8eeqwueye6rvrwer7uereur wer uetwhge87teruwterwerfwetris the ne of the kggkgg kgwriuwirweiuriwegriegfgsiufbvgbvgdbkvjkhhfushihiusdhfishfiudhfisifdfsdfvbbviggigsigsifgiusdgfisdifgsiufisdfisifsdiufisfiusdfigfiusgfsifsifigfsdgfiusgfijfhsdutuetgerutieurgt eriueriteiiergiergi ter

















































 #   
 # y98ey98wyew
 # uyyfidyf
 # yisuyfiysduisduy
 # grgt  er
 # k tkgergt 
 # ertherut
 # ugf uygh erht iuerht

 # sdsdfsdfs
 #  iwgiugqwiuegiwei uwiweweiqwieiuqweiiuqwgei qwi gqw geiuqwg iqw iiuqweiqw we iwirgiuwegrigweirgwergwegriwgerigigeriugwei\
 # #aen;vb;uabroiour'ebuveb
 # vbvbt ttyutrgweirgiwegrigweiurgweirgieeuwergwe gwegrewyegrweeruywgewergweregrwerrtewrweiuyew
 