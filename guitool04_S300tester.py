import socket

import threading
import time
from struct import *
from tkinter import *
import tkinter.ttk
# socket.setblocking
# socket.setblocking(0)
# socket.settimeout(1)
socket.setdefaulttimeout(3)
runcmd=14593
# Profile_run=0
# connections=[0]
# ReadSCANer=[0]
# WriteSCANer=[0]
def str_to_num(abc):
    num = 0
    a = [ord(i) for i in abc]
    for i in a:
        num = (num<<8)+i
    return num
def MB_Client_READ(sock,ind,_flag):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    timeoutCNT=0
    ReceiveCnt_READ=0
    ReceiveCnt_WRITE=0
    global runcmd
    while Kill_flag==0:
        if TI >= 65534:
            TI=0

        FD=3
        addr=5
        cnt=2
        packet1=pack(">HHBBBBHH",TI,0,0,6,1,FD,addr,cnt)
        # print("Request_READ :",packet)
        try:
            sock.send(packet1)
        except:
            print("send Byte error")
            return

        try:
            receivemesg = sock.recv(1024)
            ReceiveCnt_READ+=1
            connection_infoTABLE[ind][0]=ReceiveCnt_READ
            connection_infoTABLE[ind][2]=receivemesg[12:].hex()
        
        except socket.timeout:
            connection_infoTABLE[ind][3]+=1
            if ind<32:
                treeTable01.set(ind, column="four1", value=connection_infoTABLE[ind][3])
            else :
                treeTable02.set(ind-32, column="four2", value=connection_infoTABLE[ind][3])
            listBOX.insert(END, str(sock.getpeername()[0])+"READ timeout count:"+str(connection_infoTABLE[ind][3]))

        except ConnectionError:
            listBOX.insert(END,"ConnectionError"+str(sock.getpeername()[0]))
            return
        TI=TI+1
        time.sleep(0.05)
        
        packet2=pack(">HHHBBHHBHHHH",TI,0,15,1,16,startaddr,quantityaddr,bytecount, 5990,runcmd,50,50)
        # print("Request_WRITE :",packet)
        try:
            sock.send(packet2)
        except:
            print("send Byte error")
            return
        
        
        try:
            receivemesg = sock.recv(1024)
            ReceiveCnt_WRITE+=1
            connection_infoTABLE[ind][1]=ReceiveCnt_WRITE

        except socket.timeout:
            connection_infoTABLE[ind][3]+=1
            if ind<32:
                treeTable01.set(ind, column="four1", value=connection_infoTABLE[ind][3])
            else :
                treeTable02.set(ind-32, column="four2", value=connection_infoTABLE[ind][3])
            listBOX.insert(END, str(sock.getpeername()[0])+"WRITE timeout count:"+str(connection_infoTABLE[ind][3]))

        except ConnectionError:
            listBOX.insert(END,"ConnectionError"+str(sock.getpeername()[0]))
            # root.showinfo("Cuation!", str(sock.getpeername()[0])+"disconnected")
            return
        TI=TI+1
        time.sleep(0.05)
    
    return

def MB_Client_WRITE(sock,ind,_flag):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    timeoutCNT=0
    ReceiveCnt_WRITE=0
    global runcmd
    while Kill_flag==0:
        if TI > 65535:
            TI=0

       
        TI=TI+1
        time.sleep(0.2)
    
    return

def TRY_run():
    global runcmd
    runcmd=14594
    # print("Success to RUN")
    listBOX.insert(END,"Success to RUN:14594")
    return

def TRY_stop():
    global runcmd
    runcmd=14593
    # print("Success to STOP")
    listBOX.insert(END,"Success to STOP:14593")
    return

def TRY_connect():
    CLIENT_NUM=int(entry2bt1.get())
    entry2bt1.configure(state='disabled')
    btn1.configure(state='disabled')
    btn2.configure(state='normal')
    
    global connections
    connections=[x for x in range(CLIENT_NUM)]

    # for num in connections:
    index=0
    while index< CLIENT_NUM:
        connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connections[index].setblocking(True)
        connections[index].settimeout(1)

        HOST = entry2IPADDR1.get()+'.'+entry2IPADDR2.get()+'.'+entry2IPADDR3.get()+'.'+str(int(entry2IPADDR4.get())+index)
        try:
            connections[index].connect((HOST,PORT))
            listBOX.insert(END,"Success to establish connection:"+HOST)
            if index<32:
                try:
                    treeTable01.insert('', index, text=HOST,values=[0,0,"stop",0],iid=index)
                except:
                    treeTable01.delete(index)
                    treeTable01.insert('', index, text=HOST,values=[0,0,"stop",0],iid=index)
            else :
                try:
                    treeTable02.insert('', index-32, text=HOST,values=[0,0,"stop",0],iid=index-32)
                except:
                    treeTable02.delete(index)
                    treeTable02.insert('', index-32, text=HOST,values=[0,0,"stop",0],iid=index-32)

        except socket.timeout:
            listBOX.insert(END,"Failed to establish connection:"+HOST)
            if index<32:
                try:
                    treeTable01.insert('', index, text=HOST,values=[0,0,"unconnected",0],iid=index)
                except:
                    treeTable01.delete(index)
                    treeTable01.insert('', index, text=HOST,values=[0,0,"unconnected",0],iid=index)
            else :
                try:
                    treeTable02.insert('', index-32, text=HOST,values=[0,0,"unconnected",0],iid=index-32)
                except:
                    treeTable02.delete(index-32)
                    treeTable02.insert('', index-32, text=HOST,values=[0,0,"unconnected",0],iid=index-32)

        index=index+1

def TRY_Start_Reust():
    listBOX.insert(END," start request FD : 3 X1 ,FD:6 X4")
    CLIENT_NUM=int(entry2bt1.get())
    index=0
    global ReadSCANer
    global WriteSCANer
    global Kill_flag
    Kill_flag=0
    global connection_infoTABLE
    connection_infoTABLE=[[0,0,0,0] for x in range(CLIENT_NUM)]
    
    ReadSCANer=[x for x in range(CLIENT_NUM)]
    WriteSCANer=[x for x in range(CLIENT_NUM)]
    while index < CLIENT_NUM:
        # connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            ReadSCANer[index] = threading.Thread(target=MB_Client_READ,args=(connections[index],index,Kill_flag))
            # WriteSCANer[index]=threading.Thread(target=MB_Client_WRITE,args=(connections[index],index,Kill_flag))
            ReadSCANer[index].daemon = True
            # WriteSCANer[index].daemon = True
            ReadSCANer[index].start()
            # WriteSCANer[index].start()
            
            btn3_1.configure(state='normal')
            btn4_1.configure(state='normal')
        except:
            listBOX.insert(END,"No connection:"+str(connections[index].getpeername()[0]))

        index=index+1

    TRY_printer = threading.Thread(target=TRY_print,args=(index,Kill_flag))
            
    TRY_printer.daemon = True
    
    TRY_printer.start()


def TRY_print(indxx,_flag):
    # ind=0
    global Kill_flag
    running_stste = hex(10)
    while Kill_flag==0:
        ind=0
        while ind<indxx and Kill_flag==0:

            if ind<32:
                    treeTable01.set(ind, column="one1", value=connection_infoTABLE[ind][0:1] )
                    treeTable01.set(ind, column="two1", value=connection_infoTABLE[ind][1:2])

                    if int(connection_infoTABLE[ind][2])  & 2 == 0x02:
                        treeTable01.set(ind, column="three1", value="forword")
                    elif int(connection_infoTABLE[ind][2]) & 4 == 0x04:
                        treeTable01.set(ind, column="three1", value="reverse")
                    elif int(connection_infoTABLE[ind][2]) & 1 == 0x01:
                        treeTable01.set(ind, column="three1", value="stop")
                    
            else :
                    treeTable02.set(ind-32, column="one2", value=connection_infoTABLE[ind][0:1])
                    treeTable02.set(ind-32, column="two2", value=connection_infoTABLE[ind][1:2])

                    if int(connection_infoTABLE[ind][2])  & 2 == 0x02:
                        treeTable02.set(ind-32, column="three2", value="forword")
                    elif int(connection_infoTABLE[ind][2]) & 4 == 0x04:
                        treeTable02.set(ind-32, column="three2", value="reverse")
                    elif int(connection_infoTABLE[ind][2]) & 1 == 0x01:
                        treeTable02.set(ind-32, column="three2", value="stop")

            ind+=1
        time.sleep(1)

    return
        



def TRY_disconnect():
    index=0
    global Kill_Profile_flag
    Kill_Profile_flag=1
    global Kill_flag
    Kill_flag=1
    entry2bt1.configure(state='normal')
    btn1.configure(state='normal')
    btn2.configure(state='disabled')
    while index < int(entry2bt1.get()):
        try:
            ReadSCANer[index]._delete
            WriteSCANer[index].delete
            # if index<32:
            #     treeTable01.delete(index)
            # else:
            #     treeTable02.delete(index-32)
        except:
            print("No ReadSCANer, WriteSCANer Thread")
            # if index<32:
            #     treeTable01.delete(index)
            # else:
            #     treeTable02.delete(index-32)
        connections[index].close()
        index+=1
    
    listBOX.insert(END,"disconnect all connections")
    print("disconnect all connections")

def TRY_clearlog():
    listBOX.delete(0,END)
    # index=0
    # while index < int(entry2bt1.get()):

    #     if index<32:
    #         treeTable01.delete(index)
    #     else:
    #         treeTable02.delete(index-32)
    
def MAKE_Profile_run_thread():

        global Kill_Profile_flag
        Profile_run = threading.Thread(target=TRY_Profile_run,args=(Kill_Profile_flag,))
        Profile_run.daemon = True
        Profile_run.start()
            
def TRY_Profile_run(_flag):
    global runcmd
    global Kill_Profile_flag
    Kill_Profile_flag=0
    while Kill_Profile_flag==0:
        
        runcmd=14594
        # RUN FWD
        print("14594")
        internal_timer=20
        while internal_timer!=0 and Kill_Profile_flag==0:
            time.sleep(1)
            internal_timer-=1
            if Kill_Profile_flag==1:
                break

        runcmd=14593
        # STOP
        print("14593")
        internal_timer=2
        while internal_timer!=0 and Kill_Profile_flag==0 :
            time.sleep(1)
            if (int(connection_infoTABLE[0][2]) & 1 == 0x01):
                internal_timer-=1
                if Kill_Profile_flag==1:
                    break
                
        runcmd=14596
        # RUN REV
        print("14596")
        internal_timer=20
        while internal_timer!=0 and Kill_Profile_flag==0:
            time.sleep(1)
            internal_timer-=1
            if Kill_Profile_flag==1:
                break

        runcmd=14593
        # STOP
        print("14593")
        internal_timer=2
        while internal_timer!=0 and Kill_Profile_flag==0 :
            time.sleep(1)
            if (int(connection_infoTABLE[0][2]) & 1 == 0x01):
                internal_timer-=1
                if Kill_Profile_flag==1:
                    break

    return

def TRY_Profile_stop():
    global runcmd
    global Kill_Profile_flag
    runcmd=14593
    print("14593")
    Kill_Profile_flag=1

#thread issue
Kill_flag = 0
Kill_Profile_flag=1



# modbus multi-client window setting 
Button_X=575+430
BOX_X=475+440
HOST = '192.168.10.10'
PORT= 502
root= Tk()
root.title("Modbus Test tool for multi-64")

root.geometry("1080x690+300+50")
root.resizable(False, False)
# IP ADDRESS texture
label1 =Label(root, text ="Start IP address:")
label1.place(x=BOX_X-100,y=15)
entry2IPADDR1=Entry(root)
entry2IPADDR1.place(x=BOX_X+0,y=15,width=30,height=25)
entry2IPADDR1.insert(END,"192")
entry2IPADDR2=Entry(root)
entry2IPADDR2.place(x=BOX_X+32,y=15,width=30,height=25)
entry2IPADDR2.insert(END,"168")
entry2IPADDR3=Entry(root)
entry2IPADDR3.place(x=BOX_X+32*2,y=15,width=30,height=25)
entry2IPADDR3.insert(END,"10")
entry2IPADDR4=Entry(root)
entry2IPADDR4.place(x=BOX_X+32*3,y=15,width=30,height=25)
entry2IPADDR4.insert(END,"10")

#connect button textrue
label2 =Label(root, text ="num of node:")
label2.place(x=BOX_X-100,y=50)
btn1 = Button(root,text="connect",command =TRY_connect)
btn1.place(x=Button_X,y=50,width=65)
entry2bt1=Entry(root)
entry2bt1.place(x=BOX_X,y=50,width=80,height=25)
entry2bt1.insert(END,"1")
#Start Req button textrue
btn2 = Button(root,text="Start Req",command =TRY_Start_Reust,state='disabled')
btn2.place(x=Button_X,y=50+50-20,width=65,height=25)
#Profile_run button textrue
btn3_1 = Button(root,text="Profile run",command =MAKE_Profile_run_thread,state='disabled')
btn3_1.place(x=Button_X-100,y=50+50+50-40,width=80,height=25)
#run button textrue
btn3 = Button(root,text="run FWD",command =TRY_run)
btn3.place(x=Button_X,y=50+50+50-40,width=65,height=25)
#Profile_stop button textrue
btn4_1 = Button(root,text="Profile stop",command =TRY_Profile_stop,state='disabled')
btn4_1.place(x=Button_X-100,y=50+50+50+50-60,width=80,height=25)
#stop button textrue
btn3 = Button(root,text="stop",command =TRY_stop)
btn3.place(x=Button_X,y=50+50+50+50-60,width=65,height=25)
#disconnect button textrue
btn4 = Button(root,text="disconnect",command=TRY_disconnect,)
btn4.place(x=Button_X,y=50+50+50+100-80,width=65,height=25)
#clearlog button textrue
btn5 = Button(root,text="clear log",command=TRY_clearlog,)
btn5.place(x=Button_X,y=50+50+50+150-80,width=65,height=25)
#log text
frame=Frame(root)
frame.place(x=BOX_X-125,y=50+50+50+100+50,width=290,height=300-20)
# frame.pack(fill=X,anchor=N,pady=5)
scrollbar=Scrollbar(frame)
scrollbar.pack(side=RIGHT,fill=Y)
listBOX=Listbox(frame,yscrollcommand=scrollbar,bg="white",height=27,width=11)
listBOX.pack(side=LEFT,fill=X,expand=1)
scrollbar.config(command=listBOX.yview)
# txt4log=Text(root)
# txt4log.place(x=15,y=50,width=100,height=300)
# txt4log.insert(END,"")

# tree table
treeTable01=tkinter.ttk.Treeview(root, columns=["one1", "two1","three1","four1"], displaycolumns=["one1", "two1","three1","four1"])
treeTable01.place(x=10,y=10,width=390,height=670)
treeTable01.column("#0", width=80, anchor="w")
treeTable01.heading("#0", text="Node IP", anchor="center")
treeTable01.column("#1", width=50, anchor="center")
treeTable01.heading("one1", text="ReadRxCnt", anchor="center")
treeTable01.column("#2", width=50, anchor="center")
treeTable01.heading("two1", text="WriteRxCnt", anchor="center")
treeTable01.column("#3", width=50, anchor="center")
treeTable01.heading("three1", text="Status", anchor="center")
treeTable01.column("#4", width=30, anchor="center")
treeTable01.heading("four1", text="ErrorCnt", anchor="center")

treeTable02=tkinter.ttk.Treeview(root, columns=["one2", "two2","three2","four2"], displaycolumns=["one2", "two2","three2","four2"])
treeTable02.place(x=400,y=10,width=390,height=670)
treeTable02.column("#0", width=80, anchor="w")
treeTable02.heading("#0", text="Node IP", anchor="center")
treeTable02.column("#1", width=50, anchor="center")
treeTable02.heading("one2", text="ReadRxCnt", anchor="center")
treeTable02.column("#2", width=50, anchor="center")
treeTable02.heading("two2", text="WriteRxCnt", anchor="center")
treeTable02.column("#3", width=50, anchor="center")
treeTable02.heading("three2", text="Status", anchor="center")
treeTable02.column("#4", width=30, anchor="center")
treeTable02.heading("four2", text="ErrorCnt", anchor="center")



if __name__ == "__main__":

    root.mainloop()