import turtle
import random
import math

global move_history

# In ra thông báo kết thúc
def endGame():
    # Khởi tạo và restart giá trị 
    global gameOverTurtle
    x=1 
    gameOverTurtle=turtle.Turtle()

    # Tránh con chuột vẽ khi chạy lệnh goto
    gameOverTurtle.up()

    # Thêm cái này vào bước vẽ phức tạp để tránh hiện delay
    gameOverTurtle.ht()

    # Di chuyển đến vị trí và vẽ Game Over
    gameOverTurtle.goto(2,6)
    gameOverTurtle.color("blue")
    gameOverTurtle.write("Game Over",font=("Arial",50,"bold"))

    # DI chuyển đến vị trí và vẽ background cho restart
    gameOverTurtle.goto(5.5,7)
    gameOverTurtle.begin_fill()
    gameOverTurtle.fillcolor('green')
    gameOverTurtle.hideturtle()
    for i in range(2):
        gameOverTurtle.forward(3)
        gameOverTurtle.left(90)
        gameOverTurtle.forward(1)
        gameOverTurtle.left(90)
    gameOverTurtle.end_fill()
    gameOverTurtle.hideturtle()

    # Vẽ chữ restart trong cục xanh
    gameOverTurtle.goto(6,7.8)
    gameOverTurtle.hideturtle()
    gameOverTurtle.color("yellow")
    gameOverTurtle.write("Restart!",font=("Arial",15,"bold"))

# Clear toàn bộ board
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

# Check board có quân nào không
def is_empty(board):
    return board == [[' ']*len(board)]*len(board)

# Check tọa độ bấm chuột tại (x,y) truyền vào có nằm trong board không. Vd nằm ngoài board ta return bỏ qua luôn
def is_in(board, y, x):
    return 0 <= y < len(board)-1 and 0 <= x < len(board)-1

# Check xem black hay white win, chỉ cần check có 5 ô liên tiếp không thôi
def is_win(board):
    black = score_of_col(board,'b')
    white = score_of_col(board,'w')
    # print("Move:", white)
    # print("Move:", white[5])
    
    sum_sumcol_values(black)
    sum_sumcol_values(white)
    
    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        # print(white[5])
        return 'White won'
        
    # Hêt nước đi mà k thắng hay thua thì hòa
    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board)==[]:
        return 'Draw'
    
    # Xử lý hàng đống thứ chỉ để check có người win hay không
    return 'Continue playing'

###############
## AI Engine ##
###############

def march(board,y,x,dy,dx,length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    # Hàm march duyệt từ điểm (x,y) đi theo 8 hướng 1 lượng length đế tọa độ mới 
    yf = y + length*dy 
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board,yf,xf):
        # Trả ra tọa độ mới đó nếu nó vẫn còn trong phạm vi bàn cờ, nếu k thì trả ra
        # giá trị sát nhất ở mép bàn cờ theo hướng đó
        yf -= dy
        xf -= dx
        
    return yf,xf
    
# Hàm nhận vào object các hướng, mỗi hướng chứa mọi ô của cả bàn cờ là:
# {1 hướng: [ô 1 bàn cờ, ô 2 bàn cờ]}
# Trả ra 1 object {điểm: {1 hướng: <điểm ở hướng này>}}
def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm

    '''
    print("1: ", scorecol)
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1
    print("2: ", sumcol)
    # sumcol sau cùng sẽ trả ra kiểu
    '''
    {
        0: {
            (0,1): 4,
            (1,1): 2
        },
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        -1: {}
    }
    => Tức là ta biết được rằng điểm 0 ở hướng (0,1) đã có 4 con rồi chẳng hạn và 4 con này
    là possible để đánh tiếp nước thứ 4 chứ 4 con bị chặn 2 đầu thì k tính ở đây đâu
    '''

    return sumcol
    

def sum_sumcol_values(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''
    # Truyền vào cả object 
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        # Chỉ cần giá trị key = 5 mà tồn tại là gán ngay nó bằng 1 để hàm gọi check có giá trị 1 tức win luôn
        else:
            sumcol[key] = sum(sumcol[key].values())
        ''' Nếu không thì nó hợp nhất mảng. 
        VD có 1: {(0, 1): 18, (-1, 1): 18, (1, 0): 2, (1, 1): 21}
        tức theo hướng (0,1) là nằm ngang thì số ô có điểm 1 là 18
        Tổng các ô có điểm 1 là 18+18+1+21 => trả ra {1: 58} tức số ô có giá trị 
        1 điểm là 58
        '''
            
# Hàm check để lấy list 5 ô đi vào liệu có khả năng thắng hay không
def score_of_list(lis,col):
    
    # Điều đặc biệt là nó chặn kiểu, k có 5 nước liên tục possible thì 0 đanh
    blank = lis.count(' ')
    filled = lis.count(col)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

# Hàm giúp duyệt trâu các đường đó. Họ làm khéo nên k cần từng hàm riêng cho từng đường
# mà dùng 1 cách chung lưu vào biến
def row_to_list(board,y,x,dy,dx,yf,xf):
    '''
    trả về list của y,x từ yf,xf
    
    '''
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row

# Hàm nhận vào (mảng 2 chiều cả bàn cờ, cordi là tọa dộ )
def score_of_row(board,cordi,dy,dx,cordf,col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    colscores = []
    y,x = cordi
    yf,xf = cordf
    # print(y,x,dy,dx,yf,xf)
    row = row_to_list(board,y,x,dy,dx,yf,xf)
    # print(row)
    print("End")
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],col) # Giống golang vl
        colscores.append(score)
        # print(colscores)
    return colscores
# Hàm này trả ra điểm của từng hàng dưới dạng 1 mảng. Nó như kiểu duyệt mảng 2 chiều r lưu lại
# vị trí tồn tại. R lại duyệt mảng lưu đó lấy cách 5 ô tính điểm nếu tồn tại 5 ô trống 

# score_of_col hàm nhận vào mảng 2 chiều board và type of player là black or white
# Hàm trả ra 1 object {điểm: {1 hướng: <giá trị điểm>}}
def score_of_col(board,col):
    '''
    Tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''
    # board là 1 mảng 2 chiều như cả bảng, mỗi ô là 1 character là các giá trị 'b', 'w', space
    f = len(board)
    # f lưu số lượng hàng trong board
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    for start in range(f):
        # print("Start: ", start)
        # Ngang
        scores[(0,1)].extend(score_of_row(board,(start, 0), 0, 1,(start,f-1), col))
        # print("C: " ,scores[(0,1)])
        # Dọc
        scores[(1,0)].extend(score_of_row(board,(0, start), 1, 0,(f-1,start), col))
        # print("C1: " ,scores[(1,0)])
        # \
        scores[(1,1)].extend(score_of_row(board,(start, 0), 1,1,(f-1,f-1-start), col))
        # print("C2: " ,scores[(1,1)])
        # print("Before C3: " ,scores[(-1,1)])
        # /
        scores[(-1,1)].extend(score_of_row(board,(start,0), -1, 1,(0,start), col))
        # print("C3: " ,scores[(-1,1)])
        
        # 2 phần còn lại của 2 đường chéo
        if start + 1 < len(board):
            scores[(1,1)].extend(score_of_row(board,(0, start+1), 1, 1,(f-2-start,f-1), col)) 
            scores[(-1,1)].extend(score_of_row(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))
    
    # print(scores[(1,1)])
    # Sau khi đã có list điểm theo 1 mảng chiều ở mọi hướng rồi thì 
    return score_ready(scores)
    
def score_of_col_one(board,col,y,x):
    '''
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''
    
    # Hàm này được gọi từ stupidscore để check xem sau khi nó đã đi 1 nước ở ô y,x như
    # v thì điểm số sẽ thay đổi ra sao. Ta lại tính điểm số theo 4 hướng tương tự nhưng bh
    # kp là duyệt tất cả từ đầu đến cuối của từng hàng nữa mà ta chỉ duyệt trong phạm vi cách ô vừa đi 4 ô trên đường đó mà thôi
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    
    # duyệt từ ô đó lùi 4 và ô đó tiến thêm 4 trên đường đó
    scores[(0,1)].extend(score_of_row(board,march(board,y,x,0,-1,4), 0, 1,march(board,y,x,0,1,4), col))
    
    scores[(1,0)].extend(score_of_row(board,march(board,y,x,-1,0,4), 1, 0,march(board,y,x,1,0,4), col))
    
    scores[(1,1)].extend(score_of_row(board,march(board,y,x,-1,-1,4), 1, 1,march(board,y,x,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(board,march(board,y,x,-1,1,4), 1,-1,march(board,y,x,1,-1,4), col))
    
    # Rồi cũng đơn giản là gộp lại trả ra object điểm
    return score_ready(scores)
    
def possible_moves(board):  
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    '''
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    # cord: lưu các vị trí không đi 
    cord = {}
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''

    for direction in directions:
        dy,dx = direction
        for coord in taken:
            y,x = coord
            for length in [1,2,3,4]:
                move = march(board,y,x,dy,dx,length)
                # Nếu tọa độ lấy ra chưa set và chưa từng đi thì mới lấy
                if move not in taken and move not in cord:
                    cord[move]=False
    # Trả ra 1 object chứa nhiều object khác, mỗi object có 1 giá trị đi kèm là có đi được hay không
    return cord
    
def TF34score(score3,score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    # Duyệt mọi hướng trong score4
    for key4 in score4:
        # Nếu hướng đó có giá trị >=1 tức có >=1 ô có 4 điểm
        if score4[key4] >=1:
            # nếu score4[key4] >=1 VD cái key 4 ta đang xét ỏ đây là (1,1) tức là nó có {4: {(1,1): 1 or bất cứ giá trị nào >=1}}
            # Tức là trong cái mảng dài [0,0,4,3,2,1] có ít nhất 1 giá trị 4 tức trong 5 ô liên tiếp nào đó, khi đánh nước này 
            # sẽ tạo ra 4 ô liên tiếp. Ta k cần biết liệu có bị chặn 2 đầu hay k. 
            # Ta check thêm rằng trên 1 đường nào đó khác. có >=2 cái tạo nước 3. VD: [0,0,3,0,0,3] => ta cóc cần biết gì hết, chỉ cần hiểu là
            # trên 1 hướng mà tạo ra nước 4 thì ta ta bắt buộc phải chặn trên hướng đó. Và hướng còn lại sẽ tạo ra 2 nước 3 là được. 
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                    return True
    # Chú ý: 1 nước 4 liên tiếp cũng tương đương với có 2 nước 3 đều bắt buộc người kia phải chặn nhưng 2 nước 3 thì k chắn là có 1 nước 4.
    # tức 2 nước 3 là điều kiện tối thiểu chưa chắc thắng đâu nếu người ta chặn ngay. 
    # Ở đây khi đã có score4 là 1 nước liên tiếp và buộc người kia phải chặn thì chỉ cần tạo 2 nước 3 ở 1 đường khác là đủ thắng r.
    # Thực chất có usecase 1 hướng là 1 nước 4, 1 hướng là 1 nước 3 cũng được nhưng nước 3 kia phải 0 bị chặn
    # Ta bỏ sot TH vì k check hết được VD 1 nước 4 sinh 1 nước 3 trống dài ở 2 đầu
    # Thực tế ở đây vẫn chưa chuẩn: 1 nước 4 trên 1 đường và 2 nước 3 trên đường khác vẫn chưa chắc thắng được. VD:
    '''
            1
    0 0 0 1 X 0 0 
            0
            0
            0
    => Khi đánh X thì k thắng được => thực chất là sai vì ta đang chỉ xét phạm vi xung quanh ô X thôi, mà 0001X00 thì blank + black k tạo ra
    2 ô 3 liên tiếp được nên k tính case này mà. Nhưng case dưới cũng k thắng được nên TH này k chắc là thắng được

            1
    0 0 A A X A A 0 0 
            0
            0
            0
    '''
    return False
    
# Hàm này nhận cả board, người chơi được quyền đi tiếp là col, người chơi đối thủ là
# anticol, chấm điểm cho tọa độ(x,y)
def stupid_score(board,col,anticol,y,x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''
    
    # Khởi tạo giá trị cơ bản
    global colors
    M = 1000
    res,adv, dis = 0, 0, 0
    
    #tấn công: nếu ô này là giá trị ta đánh để chủ động tăng điểm thì sao
    board[y][x]=col
    #draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board,col,y,x) 
    # Lấy được sumcol là object chứa các object điểm theo từng hướng rồi
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    #{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    # Tạo ra nhiều điểm hơn thì có trọng số cao hơn
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]
    
    #phòng thủ: nếu ô này phía bên kia đánh vào thì sao, nếu điểm quá cao thì ta phải đánh vào đó để chặn lại
    board[y][x]=anticol
    sumanticol = score_of_col_one(board,anticol,y,x)  
    d = winning_situation(sumanticol)
    dis += d * (M-100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis
    # Khi đánh thêm 1 nước thì tính điểm nếu ta đánh và nếu người kia đánh thì là bnh, rồi cộng tổng lại để lấy ra điểm tốt nhất
    # Ở đây nó cũng chưa xử lý nếu đi được 5 nước thì trọng số đáng lẽ phải lớn nhất chứ nhưng nó gom lại vì nếu 1 nước 5 sẽ tương tự có thêm
    # 1 nước 4 nữa và tương tự thôi
    
    board[y][x]=' '
    return res
    
def winning_situation(sumcol):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''
    # Hàm này trả ra điểm có mức độ từ 1 đến 5 để tính
    
    if 1 in sumcol[5].values():
        # Nếu là nước thắng thì trả ra điểm cao nhất luôn
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
        # Nếu nước này tạo ra >= 2 hướng cho 4 điểm hoặc chỉ có >=1 hướng cho 4 điểm nhưng
        # ta biết là hàm score_of_row trả ra kiểu [1,1,0,0,0,0,0,0] khi ghép hướng vào sẽ được (1,1): [1,1,0,0,0,0,0,0]
        # và khi đi qua score ready sẽ được {0: { (1,1): 6, }, 1: {(1,1): 2, }, } vì có 6 ô có điểm 0 ở trên hàng chéo (1,1)
        return 4
    elif TF34score(sumcol[3],sumcol[4]):
        # Nếu nước này tạo ra case chắc chắn thắng thì cũng gán 1 số điểm cao. Ta chưa bao được TH 1 nước 4 sinh 1 nước 3 trống dài ở 1 đầu
        return 4
    else:
        # Ta sort score3 theo value giảm dần và nếu ta đánh nước này làm cho 2 hướng khác nhau có >= 2 ô có điểm là 3 thì chơi
        # Cũng bao k hết. VD tạo nước 3 đôi thì nó vẫn k ưu tiên đánh
        # Điều này là k tốt, thực tế để tìm nước 3 đôi rất khó vì ta k thể check được có bị chặn 1 đầu hay không vì chặn 1 đầu thì nó chả có tác dụng
        # gì. Còn case bên dưới lại khó xảy ra khi đánh 1 nước mà tạo ra 2 hướng có 3 ô liên tiếp trong 5 ô liên tiếp trống
        score3 = sorted(sumcol[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0
    
def best_move(board,col):
    '''
    trả lại điểm số của mảng trong lợi thế của từng màu
    '''
    # Khởi tạo giá trị
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'
    
    movecol = (0,0)
    maxscorecol = ''

    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi 
    if is_empty(board):
        movecol = ( int((len(board))*random.random()),int((len(board[0]))*random.random()))
    else:
        # Lấy tất cả các bước đi possible, cách các nước đã đi xa tối đa 3 bước
        moves = possible_moves(board)

        # Duyệt mọi nước đi xét là possible trên bàn cờ và chỉ ra nước tốt nhất
        for move in moves:
            y,x = move
            if maxscorecol == '':
                # Lần đầu set giá trị max score
                scorecol=stupid_score(board,col,anticol,y,x)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol=stupid_score(board,col,anticol,y,x)
                # Update maxscore cho đến khi gặp giá trị ok nhất
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol

###################
## END AI Engine ##
###################

# def getindexposition(x,y):
#     '''
#     lấy index
#     '''
#     intx,inty = int(x),int(y)
#     dx,dy = x-intx,y-inty
#     if dx > 0.5:
#         x = intx +1
#     elif dx<-0.5:
#         x = intx -1
#     else:
#         x = intx
#     if dy > 0.5:
#         y = inty +1
#     elif dx<-0.5:
#         y = inty -1
#     else:
#         y = inty
#     return x,y

# Vẽ lên màn hình nút đen và trắng
def draw_stone(x,y,colturtle):
    colturtle.goto(x+0.5,y+0.2)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()
    initialize

def click(x,y):
    global board,colors,win, move_history
    
    # Mỗi khi click là lấy tọa đọ chuẩn nếu chưa thắng
    if win!=True:
        x=math.floor(x)
        y=math.floor(y)
    else:
        # Nếu đã thắng và click đúng vào tọa độ của button restart thì chạy lại
        if 5.5<=x<=8.5 and 7<=y<=8:
            x=-1
            y=-1
            gameOverTurtle.clear()
            colors['b'].clear()
            colors['w'].clear()
            board=make_empty_board(len(board))
            win=False
        x=-1
        y=-1
    
    # TH ngoại lệ
    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]
     
        del(move_history[-1])
        board[y][x] = " "
        x, y = move_history[-1]
       
        del(move_history[-1])
        board[y][x] = " "
        return
    
    # Click ra ngoài
    if not is_in(board, y, x):
        return
    
    # Ô này chưa có mới vẽ vào
    if board[y][x] == ' ':
        
        # Vẽ lên màn hình và lưu data lại để tính
        draw_stone(x,y,colors['b'])
        board[y][x]='b'
        
        # Lưu lại lịch sử nước đấu để xử lý về sau
        move_history.append((x, y))
        
        # Nếu win thì kết thúc
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            win = True
            endGame()
            return 
        
        # Máy sẽ tìm best move và đánh vào đó. Rồi làm tương tự là vẽ lên rồi check đúng sai
        ay,ax = best_move(board,'w')
        draw_stone(ax,ay,colors['w'])
        board[ay][ax]='w'    
            
        move_history.append((ax, ay))
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            win = True
            endGame()
            return

def initialize(size):
    # Khởi tạo bién
    global win,board,screen,colors, move_history
    
    move_history = []
    win = False
    board = make_empty_board(size)
    
    screen = turtle.Screen()
    
    # Handle click màn hình bắt sự kiện
    screen.onclick(click)

    # Style, vẽ khung hình setup
    # screen.setup(600, 600)
    screen.setup(screen.screensize()[1]*3,screen.screensize()[1]*3)
    screen.setworldcoordinates(-1,size,size,-1)
    screen.bgcolor('orange')
    screen.tracer(500)
    
    colors = {'w':turtle.Turtle(),'b':turtle.Turtle(), 'g':turtle.Turtle()}
    colors['w'].color('white')
    colors['b'].color('black')
  
    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)
    
    border = turtle.Turtle()
    border.speed(9)
    border.penup()
    
    side = (size-1)/2
    
    i=-1
    for start in range(size):
        border.goto(start,side + side *i)    
        border.pendown()
        i*=-1
        border.goto(start,side + side *i)     
        border.penup()
        
    i=1
    for start in range(size):
        border.goto(side + side *i,start)
        border.pendown()
        i *= -1
        border.goto(side + side *i,start)
        border.penup()
        
    border.ht()

    # Quay vòng để CT luôn hoạt động k bị tắt đi
    screen.listen()
    screen.mainloop()

if __name__ == '__main__':
    initialize(20)
# Hiểu cách check is_win và cách tìm best_move để vẽ là xong

'''
Khi đánh 1 nước: lấy ra tất cả các ô xung quanh các phạm vi đã đánh
Chấm điểm cho từng ô và láy ô điểm cao nhất. Điểm cao nếu điểm ta nhận được lớn hơn điểm đổi thủ trừ đi
Để chấm điểm cho 1 ô ta giả sử nếu đánh vào ô đó và tính. Ta sẽ chấm điểm cho riêng phạm vi ô đó. VD: hàng ngang khi đánh thử b vào ô đó
row_to_list: [' ', ' ', w, ' ', b, ' ', ' ', ' ', ' ', ]
=> score_of_row: [-1, -1, 0, 1, 1] trả về {(0, 1): [-1, -1, 0, 1, 1]} => đang chỉ xét 1 hướng (0,1)
=> score_of_col_one -> score_ready: 
{
    0: {
        (0,1): 1
    },
    1: {
        (0,1): 2
    },
    2: {},
    3: {},
    4: {},
    5: {},
    -1: {
        (0, 1): 2
    }
}
=> rồi từ cái này truyền vào winning_situation để tìm ra các case thắng luôn, với các case đó ta cộng 1 số điểm khá cao với trọng số rất lớn M =1000
cho nó. Còn general case, ta vẫn chấm điểm xem nước đi tiếp theo đó tạo ra nhiều hướng được nhiều điểm hơn thì ưu tiên bằng cách gộp điểm lại:
{
    0: 1,
    1: 2,
    2,3,4,5: 0,
    -1: 2
}

'''