# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:38:03 2018

@author: atidem
"""
 
# veriler matrisi dosyadan çekildi //include data
veriler = []
with open("veriler.txt") as dosya:
    for satir in dosya:
        veriler.append(satir.strip().split(","))
dosya.close()
sutun = veriler[0]

# hangi sütunda ne kadar missing value var // missing value counter
def missingCountFinder():
    toplam=0
    missingValueList =[]
    for i in range(0,len(sutun)):
        for j in range(0,len(veriler)): 
            if(veriler[j][i]=="?"):
                toplam = toplam + 1
        missingValueList.append(toplam)
        toplam = 0
    return missingValueList

# bir sınıf içerisinde ortalama bulmak // find mean in a class
def findMean(c,totalVeri,sinif,d):
    toplam=0
    sayac=0
    for a in range (0,len(c)):
        if(c[a]!="?" and totalVeri[a][d]==sinif):
            toplam=toplam+int(c[a])
            sayac=sayac+1
    return int(toplam/sayac)

# farklı değerleri bulma // uniqe value finder 
def findDifferentValue(c):
    sayanList = []
    for a in range (0,len(c)):
        if(c[a] not in sayanList and c[a]!="unKnow" ):
            sayanList.append(c[a])
    return sayanList

# istenen sütunu ayrıştırmak boyut indirgemek
def divisionColumn(c,columnIndex):
    dividedCol=[]
    for a in range(1,len(c)):
            dividedCol.append(c[a][columnIndex])
    return dividedCol

#kutulama yardımcı bölücüsü // binding 
def bindingColumnsValue(c):
    sirali = []
    sirali = c
    bindingListValue = []
    sirali.sort(key=int)
    bol = int(len(sirali) / 5)
    for a in range(bol,len(sirali),bol):
        if(sirali[a]==sirali[a+1]):
            for b in (range(a,a+bol)):
                if(sirali[a]!=sirali[b]):
                    break
            bindingListValue.append(int(sirali[b]))
        else:
            bindingListValue.append(int(sirali[a]))
    return bindingListValue

##kutulama    //  binding
def bindingColumns(c,d):
    bindingListValue = bindingColumnsValue(c)
    for b in range(1,len(d)):
        if (int(d[b]) <= int(bindingListValue[0])):
            d[b] = " - "+str(bindingListValue[0])    
        elif(int(d[b]) > int(bindingListValue[0]) and int(d[b]) <= int(bindingListValue[1])):
            d[b] = str(bindingListValue[0])
            d[b] = d[b] + " - "
            d[b] = d[b]+str(bindingListValue[1])
        elif(int(d[b]) > int(bindingListValue[1]) and int(d[b]) <= int(bindingListValue[2])):
            d[b] = str(bindingListValue[1])
            d[b] = d[b] + " - "
            d[b] = d[b]+str(bindingListValue[2])
        elif(int(d[b]) > int(bindingListValue[2]) and int(d[b]) <= int(bindingListValue[3])):
            d[b] = str(bindingListValue[2])
            d[b] = d[b] + " - "
            d[b] = d[b]+str(bindingListValue[3])
        elif(int(d[b]) >= int(bindingListValue[3])):
            d[b] = " + "+str(bindingListValue[3])
    return d
    
# ön işlemeye çalışmak   // preprocess
def preProcessingData(matris):
    missingCount=missingCountFinder()
    ## ortalama alınacak kolon için numerik olmayan ve missing value barındırmayan kolon bulur
    c = 0
    for c in range(1,len(sutun)):
        if(missingCount[c]==0 and not(matris[1][c].isnumeric())):
            break

#boşluk doldurma sayılır // missing value process
    for a in range(0,len(matris[1])): #sutun
        if(missingCount[a]!=0):
            for b in range(1,len(veriler)): #satır
                if(matris[b][a]=="?" and matris[1][a].isnumeric()):
                    matris[b][a]=findMean(divisionColumn(matris,a),matris,matris[b][c],c)
                elif(matris[b][a]=="?" and not(matris[1][a].isnumeric())):
                    matris[b][a]="unKnow"  
                    
#kutulamasak mı // binding                  
    binded = []
    for a in range(1,len(matris[1])):
         if(matris[1][a].isnumeric() and len(findDifferentValue(divisionColumn(matris,a)))>4):
             binded = bindingColumns(divisionColumn(matris,a),divisionColumn(matris,a))
             for b in range(1,len(binded)):
                 matris[b][a] = binded[b]                  
    return matris

#kolonu frekansa dönüştürmek // convert to frequency from column
def convertToFrequency(matris):
    stunList = findDifferentValue(matris)
    temp = []
    frekans = []
    frekans.append(list(stunList)) 
    for a in range(0,len(matris)):
        for b in range(0,len(stunList)):
            if(matris[a] == stunList[b]):
                temp.append("1")
            else:
                temp.append("0")
        frekans.append(list(temp))
        temp.clear()   
    return frekans
    
def letsApriorio(df):
    support = 0,8
    confidence = 0.6
    lift = 3
    leverage =0.1
    relations = []
    print("minimum support değerini giriniz \n")
    support = input()
    if(int(support) > 1 and int(support) <= 100):
        support = int(support) / 100
    elif(float(support) > 100 ):
        print("geçersiz support değerini giriniz")
        return -1
    else:
        support = 0
    print("Confidence / Lift / Leverage ölçülerinden birini seçiniz..")
    secenek = input()
    secenek = secenek.lower()
    if(secenek=="lift" or secenek=="confidence" or secenek=="leverage" ):
        print("minimum ",secenek," değerini giriniz..")
        deger = 0
        deger = input()
        if(secenek=="lift"):
            if(float(deger) < 0.1):
                print("geçersiz değer")
                return -1
            lift = deger
        if(secenek=="confidence"):
            if(float(deger) < 0):
                print("geçersiz değer")
                return -1
            confidence = deger
        if(secenek=="leverage"):
            if(float(deger) < -0.25 or float(deger)>0.25):                
                print("geçersiz değer")
                return -1
            leverage = deger
    else:
        print("geçersiz seçim")
        return -1
		
    #seçilmişe support değeriyle karşılaştırılmış itemlerin frekans matrisini getiriyor 
    secilmisListe = []
    tempFreq = []
    for a in range(0,len(df[0])): # sutun       
        tempFreq = convertToFrequency(divisionColumn(df,a))
        for b in range(0,len(tempFreq[0])): # frekans sutunu
            supportCount = 0
            for c in range(0,len(tempFreq)):# frekans satırı
                if(tempFreq[c][b]=="1"):
                    supportCount = supportCount+1
            if(support < supportCount / len(tempFreq)):
                temp=[]
                temp.append(sutun[a])
                temp.append(tempFreq[0][b])
                temp.append(supportCount)
                for x in range(1,len(tempFreq)):
                    temp.append(tempFreq[x][b])
        if(len(temp)!=0):secilmisListe.append(list(temp))
        temp.clear()
    
    #ikililer için // rule combine (2)
    pxy=0
    total=len(secilmisListe[0])-3
    for a in range(0,len(secilmisListe)): 
        for b in range(0,len(secilmisListe)):
            if(a!=b):
                pxy=0
                for c in range(3,len(secilmisListe[0])):
                    if(secilmisListe[a][c]=="1" and secilmisListe[b][c]=="1"):
                        pxy=pxy+1
                if(pxy!=0):
                    relations.append(list([secilmisListe[a][0]," ",secilmisListe[a][1]," ise ",secilmisListe[b][0]," ",secilmisListe[b][1]," dir "," support :",pxy/total," lift :",(pxy/total)/((secilmisListe[a][2]/total)*(secilmisListe[b][2]/total)),pxy/secilmisListe[a][2],(pxy/total)-((secilmisListe[a][2]/total)*(secilmisListe[b][2]/total))]))
     #üçlüler için    rule combine (3)      
    for a in range(0,len(secilmisListe)):
        for b in range(0,len(secilmisListe)):
            for c in range(0,len(secilmisListe)):
                if(a!=b and b!=c and c!=a):
                    pxyz=0
                    pxy=0
                    for k in range(0,len(secilmisListe[0])): 
                        if(secilmisListe[a][k]=="1" and secilmisListe[b][k]=="1" and secilmisListe[c][k]=="1"):
                            pxyz=pxyz+1
                            pxy=pxy+1
                        elif(secilmisListe[a][k]=="1" and secilmisListe[b][k]=="1"):                            
                            pxy=pxy+1
                    if(pxy!=0):    
                        relations.append(list([secilmisListe[a][0]," ",secilmisListe[a][1]," ve ",secilmisListe[b][0]," ",secilmisListe[b][1]," ise ",secilmisListe[c][0]," ",secilmisListe[c][1]," dir "," support :",pxyz/total," lift :",(pxyz/total)/((secilmisListe[c][2]/total)*(secilmisListe[a][2]/total)*(secilmisListe[b][2]/total)),pxyz/pxy,(pxyz/total)-((secilmisListe[c][2]/total)*(secilmisListe[a][2]/total)*(secilmisListe[b][2]/total))]))
    
    ##dosyaya yazma bolümü    // write to file 
    dosya = open("aprioria.txt", "w")          
    for a in range(0,len(relations)):
        if(secenek=="lift"):
            if(float(relations[a][len(relations[a])-3])>float(lift)):
                for b in range(0,len(relations[a])-2):
                    dosya.write(str(relations[a][b]))
                dosya.write("\n")
        if(secenek=="confidence"):
            if(float(relations[a][len(relations[a])-2])>float(confidence)):
                for b in range(0,len(relations[a])-2):
                    dosya.write(str(relations[a][b]))
                dosya.write("\n")
        if(secenek=="leverage"):
            if(float(relations[a][len(relations[a])-1])>float(leverage)):
                for b in range(0,len(relations[a])-2):
                    dosya.write(str(relations[a][b]))
                dosya.write("\n")      
    dosya.close()            
letsApriorio(preProcessingData(veriler))
    
           
             
    