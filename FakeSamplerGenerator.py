print("Initializing...")
from os import system
system("title Fake Sampler Generator v1.0")
from PIL import Image
from time import sleep
from os.path import isfile

def GetImageData(file=str):
    #Get Image
    try:
        image=Image.open(file,'r')
    except:
        print("Its not image!")
        sleep(1)
        exit(0)
    image=image.convert('RGBA')
    out=[]
    size=image.size
    #Reading data and optimizing pixels
    for y in range(0,size[1]):
        out.append([])
        for x in range(0,size[0]):
            out[y].append(image.getpixel((x,y)))
            pixel = list(out[y][x])
            for color in range(0,4):
                pixel[color]=(int(pixel[color]/255*100)/100)
            if pixel[0]==pixel[1] and pixel[0]==pixel[2] and pixel[0]==pixel[3]:
                out[y][x]=tuple([pixel[0]])
            else:
                out[y][x]=tuple(pixel)
    image.close()
    y=0
    #Optimize image data
    #Optimize Y
    while y<len(out)-1:
        if out[y]==out[y+1]:
            out.pop(y+1)
            if y==0 or type(out[y-1])==list:
                out.insert(y,1)
                y+=1
            else:
                out[y-1]+=1
        else:
            y+=1
    #Optimize X
    for y in range(0,len(out)):
        if type(out[y])==list:
            x=0
            while x<len(out[y])-1:
                if out[y][x]==out[y][x+1]:
                    out[y].pop(x+1)
                    if x==0 or type(out[y][x-1])==tuple:
                        out[y].insert(x,1)
                        x+=1
                    else:
                        out[y][x-1]+=1
                else:
                    x+=1
    y=0
    while y<len(out):
        if type(out[y])==list:
            if type(out[y-1])==list or y==0:
                out.insert(y,1)
                y+=1
            else:
                out[y-1]+=1
            x=0
            while x<len(out[y]):
                if type(out[y][x])==tuple:
                    if type(out[y][x-1])==tuple or x==0:
                        out[y].insert(x,1)
                        x+=1
                    else:
                        out[y][x-1]+=1
                x+=1
        y+=1
    return [out,size]

def CreateFile(file=str,name=str):
    print("Geting image data.")
    image,size=GetImageData(file)
    print("Generating function..")
    out="vec4 "+name.replace(' ','_')+"(vec2 Cord){vec2 size=vec2"+str(size).replace(' ','')+";float x=size.x*Cord.x;float y=size.y*Cord.y;"
    sy=0
    for y in range(0,len(image)):
        sx=0
        if type(image[y])==int:
            my=image[y]
        else:
            for x in range(0,len(image[y])):
                if type(image[y][x])==int:
                    mx=image[y][x]
                else:
                    if my==1:
                        out+="if(y=="+str(sy)
                    else:
                        out+="if(y>="+str(sy)+"&&y<"+str(sy+my)
                    if mx==1:
                        out+="&&x=="+str(sx)
                    else:
                        out+="&&x>="+str(sx)+"&&x<"+str(sx+mx)
                    out+=")return vec4"+str(image[y][x]).replace(' ','').replace('1.0','1').replace('0.0,','0,').replace('0.0)','0)').replace(',)',')')+";"
                    sx+=mx
            sy+=my
    out+="}"
    print("Creating file...")
    glsl=open(name+".glsl","w")
    glsl.write(out)
    glsl.close()
    print("Done!")

#Input
file=input("Input image file: ")

if not isfile(file):
    print("File not found!")
    sleep(1)
    exit(0)
name=input("Function name / output file name: ")

CreateFile(file,name)
sleep(1)