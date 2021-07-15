import random
import numpy as np
import time

c=0
all = []
unit = 0
m = 0
# n = int(input("Nhap so ket qua muon tim:"))
n = int(input("Pls enter solution number you want:"))
print(n)
start_time = time.time()
# kiem tra vi tri quan hau tren ban co
def getHeuristic(chess):
    huristic = []
    for i in range(len(chess)):
        j = i - 1
        huristic.append(0)
        while j >= 0:
            if chess[i] == chess[j] or (abs(chess[i] - chess[j]) == abs(i - j)):#kiểm tra trùng hàng và trùng đường chéo
                huristic[i] += 1
            j -= 1
        j = i + 1
        while j < len(chess):
            if chess[i] == chess[j] or (abs(chess[i] - chess[j]) == abs(i - j)):#kiểm tra trùng hàng và trùng đường chéo
                huristic[i] += 1
            j += 1
    return huristic
# danh gia su thich nghi cua cac ca the trong quan the
# lưu ý chess ở đây là 1 mảng
def getFitness(chess): 
    clashes = 0
    for i in range(len(chess) - 1):#chạy hết chiều dài mảng - 1 
        for j in range(i + 1, len(chess)):#chạy từ i+1 đến phần tử cuối của mảng
            if chess[i] == chess[j]:#nếu phần tử i bằng j thì ...
                clashes += 1 #clashes tăng 1
    for i in range(len(chess) - 1):
        for j in range(i + 1, len(chess)):
            if abs(chess[j] - chess[i]) == abs(j - i):#phần tử trước và sau khác nhau thì điểm fitness càng lớn
                clashes += 1
    return 28 - clashes  # 8*7/2 = 28 số cặp hậu mà nó không tấn công nhau. Số lần các con hậu tấn công nhau càng cao thì
                        #chỉ số fitness càng thấp. Do đó, chỉ số fitness = 28 đồng nghĩa với việc số lần các con hậu tấn
                        #công nhau = 0 -> có được 1 giải pháp cho bài toán.

# tạo 2 cá thể ban đầu cho quần thể và tạo ra các cá thể tiếp theo
def buildKid(chess1, chess2, crossOver):
    new = []
    for i in range(crossOver):#chay tu 0 - 3 để lấy 1/2 gen của cá thể
        new.append(chess1[random.randint(0, 7)])#thêm 4 phần tử vào mảng -> được 1/2 bộ gen
    for i in range(crossOver, 8):#chạy từ 4 dến 8 lấy 1/2 số gen còn lại
        new.append(chess2[random.randint(0, 7)])#thêm 4 phần tử còn lại vào mảng để tạo thành mảng 8 phần tử = 1 bộ gen
    return new

# lai tạo các cá thể
def changeChilds(crossover):
    global father, mother, child1, child2
    child1 = buildKid(father,mother,crossover) 
    child2 = buildKid(mother, father, crossover)
# chọn lọc NST có fitness cao hơn để tạo đột biến
def changeChromosome(chess):
    global crossover, father, mother
    newchange = -1
    while newchange != 0:
        newchange = 0
        tmpchess = chess
        getHur = getHeuristic(tmpchess)#kiểm tra mảng có thỏa mãng điều kiện hay không, thỏa thì gắn vào getHur
        index = getHur.index(max(getHur))#giá trị fitness lớn nhất sẽ được lấy chỉ mục
        maxFitness = getFitness(tmpchess)#lấy fitness của mảng đó rồi gán vào maxFitness
        #chạy vòng lặp trong mãng 8 phần tử
        for i in range(1, 9):
            tmpchess[index] = i
            if getFitness(tmpchess) > maxFitness:#nếu mảng nào có fitness cao hơn thì gán làm maxfitness
                maxFitness = getFitness(tmpchess)#lấy fitness của mảng tmpchess rồi gắn làm maxfitness
                newchange = i#gán i = index mà vòng for đã duyệt đến, mục đích là để vòng while luôn chạy cho đến khi i=0
            tmpchess = chess
        if newchange == 0:
            for i in range(len(chess) - 1):#chạy từ 0 đến độ dài của mảng - 1
                for j in range(i + 1, len(chess)):#chạy từ i + 1 đến hết độ dài mảng, i phụ thuộc vào vòng for ngoài
                    if chess[i] == chess[j]:#nếu phần tử i bằng j thì ...
                        chess[j] = random.randint(1, 8)# thì tạo giá trị mới cho bộ gen đó
        else:
            chess[index] = newchange
# vòng lập để thuật toán hoạt động đến khi tìm đủ kết quả mà người dùng yêu cầu            
while c < n: 
    unit += 1 #giá trị tăng lên khi tìm được 1 kết quả, phục vụ cho việc in kết quả
    crossover = 4# giá trị đầu vào cho độ dài NST sẽ được lai tạo VD như gen có 8 giá trị thì giữ lại 4 và random thêm 4 giá trị mới để tạo đột biến
    father = []#bộ gen của cá thể cha, có cấu trúc là mãng 1 chiều
    mother = []# bộ gen của cá thể mẹ, có cấu trúc là mãng 1 chiều
    count = 0 # biến đến để phục vụ cho việc in kết quả
    for i in range(8):
        #khoi tao ca the cha va me ngau nhien
        father.append(random.randint(1, 8))
        mother.append(random.randint(1, 8))
    print("----------------------------------------------------------------Khởi tạo 2 cá thể nguyên thủy của quần thể : ")
    print("father: ",father," Fitness: {:.2f} %" .format((getFitness(father)/28)*100))
    print("mother: ",mother," Fitness: {:.2f} %" .format((getFitness(mother)/28)*100))
    while getFitness(father) != 28 and getFitness(mother) != 28:  # 8*7/2 = 28
        changeChilds(crossover)#tạo cá thể con
        changeChromosome(child1)#tạo đột biến 
        changeChromosome(child2)#tạo đột biến
        count += 1
        print("------------------------------------------------------------Sau khi lai tạo và đột biến cá thể F{:d} của cặp ba mẹ thứ {:d}: ".format(count,unit))
        print("child1: ",child1," Fitness: {:.2f} %" .format((getFitness(child1)/28)*100))
        print("child2: ",child2," Fitness: {:.2f} %" .format((getFitness(child2)/28)*100))
        #cá thể con ở đời này sẽ đc làm cá thể cha,mẹ ở đời kế tiếp, trai lớn lấy vợ gái lớn gã chồng thế thôi
        father = child1
        mother = child2

    if getFitness(father) == 28:  # 8*7/2 = 28 nếu cá thể cha = 28 điểm fitness thì nó đc chọn là kết quả
        if father not in all:# kiểm tra trùng kết quả, nếu như kết quả chưa có thì thêm vào 
            all.append(father)# thêm kết quả và mảng
            c += 1
            print("=============Individual Fitness = 100'%' is goal======================== \n")
            print("The row is the first index of array and colum is value of index this")
            for i in all:
                print(i,"\n")
    else:
        if mother not in all:
            all.append(mother)
            c += 1
            print("=============Individual Fitness = 100'%' is goal======================== \n")
            for i in all:
                print(i,"\n")
# khoi tao ban co 8x8
Goal_test = np.empty(shape=(8,8),dtype = 'int32')
#tạo modul để in kết quả thuật toán
def Modul_PrintTotalSolutions(m):
    print("===================Kqua qua bieu dien o dang ban co vua==============")
    for i in all: # duyet mang tat ca cac solution
    # print(i)
        m+=1
        # hien thi ket qua ra ban co 8x8
        for x in range(0,8):
            for y in range(0,8):
                if(y==(i[x]-1)):
                    Goal_test[x,y]="1"
                else:
                    Goal_test[x,y]="0"
        print("Ket qua thu ",m)             
        print(Goal_test,"\n\n")    
    print("=====================================================================")
    totalTime = end_time - start_time
    print("Total run-time: {:.2f}s for {:d} solutions".format(totalTime,c))
end_time=time.time()
Modul_PrintTotalSolutions(m)