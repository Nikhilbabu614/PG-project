import cv2

def DigitalImageTampering(thresh,path):

    image=cv2.imread(path)


    [m,n,z] = image.shape
    
    if(z==3):
        image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  
    
    # Calculates differences at 8x8 block edges 
    j=1
    while((8*j)<m):  
        i=1
        while((8*i)<n):
            value = image[8*j][8*i] - image[8*j][(8*i) + 1] - image[(8*j) + 1][8*i] + image[(8*j) + 1][(8*i)+1]
            a=((8*(j-1))+1)
            while(a<=(8*j)):
                b=((8*(i-1))+1)
                while(b<=(8*i)):
                    image[a][b]=value
                    b=b+1
                a=a+1
            i=i+1
        j=j+1
                


    # Checks differences and thresholds them (left to right OR up and down) 
    j=1
    while((8*j)<m):
        i=1
        while((8*i) < n):
            difflr = abs(image[8*j][8*i] - image[8*j][(8*i)+1])
            diffud = abs(image[8*j][8*i] - image[(8*j)+1][8*i])
            if(difflr>=thresh or diffud>=thresh):
                a=((8*(j-1))+1)
                while(a<=(8*j)):
                    b=((8*(i-1))+1)
                    while(b<=(8*i)):
                        image[a][b]=255
                        b=b+1
                    a=a+1
            i=i+1
        j=j+1
    

    # Sets all nonwhite blocks equal to 0 
    j=1
    while((8*j)<m):
        i=1
        while((8*i)<n):
            if(image[8*j][8*i]!=255):
                a=((8*(j-1))+1)
                while(a<=(8*j)):
                    b=((8*(i-1))+1)
                    while(b<=(8*i)):
                        image[a][b]=0
                        b=b+1
                    a=a+1
            i=i+1
        j=j+1
    

    # # Cleans up right border 
    i=1
    while((8*i)<n):
        i=i+1
    a=1
    while(a<m):
        b=1
        while((8*(i-1)+b) < n):
            image[a][8*(i-1)+b] = 0
            b=b+1
        a=a+1

    # #Sets j to bottom pixel row for next loop 
    j=1
    while((8*j) < m):
        j=j+1

    #Cleans up next to last row   
    a=1
    while(a<n):
        b=1
        while((8*(j-2)+b) <m):
            image[8*(j-2)+b][a] = 255
            b=b+1
        a=a+1
    
    #Cleans up last row 
    a=1
    while(a<n):
        b=1
        while((8*(j-1)+b) < m):
            image[8*(j-1)+b][a] = 255
            b=b+1
        a=a+1; 

    return image