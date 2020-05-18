import pickle
import os
import time

def sort(dic,slist):
  for i in range (0,len(slist)):
    ele=slist[i]
    minval=dic[ele]
    m_pos=i
    for j in range(i,len(slist)):
      
      if(dic[slist[j]]<minval):
        minval=dic[slist[j]]
        m_pos=j
    slist[i]=slist[m_pos]
    slist[m_pos]=ele
    


  return (slist)
def compute_dis(dist1,dist2):
    summation=0
    cnt=0
    for i in range (0,len(dist1)):
        for j  in range (0,len(dist1[i])):

            diff=dist1[i][j]-dist2[i][j]
            if((dist1[i][j]==dist2[i][j] and dist1[i][j]==[0.0])==False):
                cnt=cnt+1
            if(diff<0):
                diff=diff*-1
            val=diff/(1+dist1[i][j]+dist2[i][j])
            summation =summation +val
    dis=(summation)/cnt
        
    return(dis)
file = open('feature.dms', 'rb')
features=(pickle.load( file))
path="./train/query"

queries=os.listdir(path)
start = time.time()
s=0
ts=0.04245967463293287
prec=[]
recall=[]
okl=[]
goodl=[]
junkl=[]
fscore=[]

for query in queries:
    file = open(path+ "/" + query, 'r')
    q_image=(file.read()).split(" ")[0][5:]+".jpg"
   
    var1=query.split("_")
    var1=var1[0:len(var1)-1]
    var2=""
    for i in var1:
        var2=var2+i+"_"

    junk=var2+"junk.txt"
    good=var2+"good.txt"
    ok=var2+"ok.txt"
    junk="./train/ground_truth" + "/"+junk
    good="./train/ground_truth" + "/"+good
    ok="./train/ground_truth" + "/"+ok
    jfile = open(junk, 'r')
    gfile = open(good, 'r')
    ofile = open(ok, 'r')
    junklist=[]
    oklist=[]
    goodlist=[]
    qcarr=features[q_image]
    ground_truth_dict={}
    ground_truth_list=[]
    goodlist=gfile.read().split("\n")[:-1]
    junklist=jfile.read().split("\n")[:-1]
    oklist=ofile.read().split("\n")[:-1]
    ground_truth_list=goodlist+oklist+junklist
    ground_truth_dict={}
  
    for ele in ground_truth_list:
      carr=features[ele+".jpg"]
      distance=compute_dis(qcarr[0],carr[0])
      ground_truth_dict[ele]=distance
    top=5
    sortedd=sort(ground_truth_dict,ground_truth_list)
    output=[]
    for i in sortedd:
      if ground_truth_dict[i] <ts:
        output.append(i)
      else:
        break

    s=s+(ground_truth_dict[output[-1]])
    q_output=[0,0,0]
    for i in output:
      if i in goodlist:
        q_output[0]=q_output[0]+1
      elif i in oklist:
         q_output[1]=q_output[1]+1
      elif i in junklist:
         q_output[2]=q_output[2]+1
    precesion=(q_output[0]+q_output[1])/(q_output[0]+q_output[1]+q_output[2])
    recalll=(q_output[0]+q_output[1])/(len(goodlist)+len(oklist))
    prec.append(precesion)
    recall.append(recalll)
    fscore.append((2*(precesion )* (recalll))/(precesion+recalll))
    okl.append( q_output[1]/(q_output[1]+q_output[2]+q_output[0]))
    goodl.append( q_output[0]/(q_output[1]+q_output[2]+q_output[0]))
    junkl.append( q_output[2]/(q_output[1]+q_output[2]+q_output[0]))
    # types.append(q_output)

end=time.time()
avtime=(end-start)/(len(queries))
prec=(sorted(prec))
recall=(sorted(recall))
fscore=sorted(fscore)
avprec=sum(prec)/len(queries)
avrecall=sum(recall)/len(queries)
avfscore=sum(fscore)/len(queries)

okav=sum(okl)/len(okl)
goodav=sum(goodl)/len(goodl)
junkav=sum(junkl)/len(junkl)

print ("Number of queries :"+str(len(prec)))

print ("MAX precision: "+str((prec[-1]*100)) +"%")

print ("MIN precision: "+str((prec[0]*100)) +"%")

print ("AVERAGE precision: "+ str(avprec*100)+" %")
print ("MAX recall: "+str((recall[-1]*100)) +"%")

print ("MIN recall: "+str((recall[0]*100)) +"%")

print ("AVERAGE recall: "+ str(avrecall*100)+" %")



print ("average Time: "+ str(avtime)+"  seconds")

print ("MAX fscore: "+str((fscore[-1]*100)) +"%")

print ("MIN fscore: "+str((fscore[0]*100)) +"%")

print ("AVERAGE fscore: "+ str(avfscore*100)+" %")

print ("average OK: "+ str(okav*100)+"  %")
print ("average GOOD: "+ str(goodav*100)+"  %")
print ("average JUNK: "+ str(junkav*100)+"  %")


print ("average Time: "+ str(avtime)+"  seconds")


print ("Threshhold Distance  "+ str(s/33))


# print ("average GOOD: "+ str((good/len(prec))*100)+" %")

# print ("average OK: "+ str((ok/len(prec))*100)+" %")
# print ("average JUNK: "+ str((junk/len(prec))*100)+" %")




  
  
   
    
    
    



