import cv2

def helper_DIT(image,thresh,hashMap):
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
                        obj = str(a) + '_' + str(b)
                        # print(type(obj))
                        if obj in hashMap:
                            hashMap[obj]+=1
                        else:
                            hashMap[obj]=1
                        b=b+1
                    a=a+1
            i=i+1
        j=j+1
    
def Enhanced_DigitalImageTampering(path):
    thresh_values = [i for i in range(5,20)]

    image=cv2.imread(path)

    hashMap = {}

    for thresh in thresh_values:
        helper_DIT(image,thresh,hashMap)

    for key, value in hashMap.items():
        if value > 7 :
            x = key.split("_")
            image[int(x[0])][int(x[1])]=255

    return image