def is_valid(i , j , m = 5 , n = 5):
    if (i >= 0 and i < m and j >= 0 and j < n ):
        return True
    return False

l = [ [ 0.0 for i in range (5) ] for i in range (5) ]
print(l)
n = float(input("Enter the temp. of the object in middle"))
l[2][2] = n;

time_step = 0

r = 0.2

while(time_step!=20):
    l_ = [row.copy() for row in l]
    for i in range (5):
        for j in range (5):
            change = 0.0
            if (is_valid(i+1,j)):
                change += (- l[i][j] + l[i+1][j]) 

            if (is_valid(i-1,j)):
                change += (-l[i][j] + l[i-1][j]) 

            if (is_valid(i,j+1)):
                change += (-l[i][j] + l[i][j+1]) 
            
            if (is_valid(i,j-1)):
                change += (-l[i][j] + l[i][j-1]) 

            l_[i][j] = l[i][j] + r * change
    l = l_

    print(f"\nTime step {time_step + 1}:")
    for row in l:
        print(["{:.2f}".format(x) for x in row])
        # for l_ in l:
        #     print(l_)
        # print("\n")
            
    # if(no_temp == 1):
    time_step += 1
    # print("\n")
