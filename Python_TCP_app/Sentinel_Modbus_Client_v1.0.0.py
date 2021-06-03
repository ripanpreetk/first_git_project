from tkinter import *
from pyModbusTCP.client import ModbusClient
from time import sleep
from datetime import datetime
from tkinter import ttk
from ttkthemes import themed_tk as tk
import struct

#selecting the theme for modbus client
top=tk.ThemedTk()
top.get_themes()
top.set_theme("yaru")
top.title("Sentinel Modbus Client Application")
top.configure(background='white smoke')

var = IntVar()
var.set(1)
c = ModbusClient()
good_count_num=0
bad_count_num=0

#defining the number of rows and columns for app
top.columnconfigure([0,1,2,3,4, 5], weight=1)
top.rowconfigure([0,1,2,3,4,5,6,7,8,9, 10, 11, 12, 13, 14, 15], weight=1)

#function for assigning the "var" value associated with Radio buttons
def sel():
   selection = "You selected the option " + str(var.get())
   blank_label.config(text = selection)

#function for displaying wrong address when IP is incorrect
def wrong_address():
    data_textbox.delete("1.0", END)
    data_textbox.insert("1.0", "Something went wrong!")

#function for good counts of reading or writing
def good_count():
    global good_count_num
    good_count_num=good_count_num+1
    print( f"Good pack count: {good_count_num}")
    good_count_entry.delete(0,END)
    good_count_entry.insert(0,f"{good_count_num}")

#function for bad counts of reading or writing
def bad_count():
    global bad_count_num
    bad_count_num=bad_count_num+1
    print(f"Bad pack count: {bad_count_num}")
    bad_count_entry.delete(0,END)
    bad_count_entry.insert(0,f"{bad_count_num}")

#function for clearing text in data output/textbox
def clear_text():
    data_textbox.delete("1.0", END)

#function to connect to Modbus application
def connect():
    try:
        global c
        c.host(ip_entry.get())
        c.port(502)
        c.timeout(10.0)
        if c.open():
            conn_status_text.delete(0, END)
            conn_status_text.insert(0,"Connected!")
        else:
            conn_status_text.delete(0, END)
            conn_status_text.insert(0, "Not Connected!")
    except:
        conn_status_text.delete(0, END)
        conn_status_text.insert(0, "Not Connected!")

#function to disconnect to Modbus application
def disconnect():
    global c
    conn_status_text.delete(0, END)
    conn_status_text.insert(0, "Disconnected!")

#function to read registers
def read_register():
    global c
    input_value=int(register_address_entry.get())
    try:
        register_number=int(register_count_entry.get())
    except:
        bad_count()
        data_textbox.delete("1.0", END)
        data_textbox.insert("1.0", "Register count is not correct!")

    #checking if address starts from "4"
    if int(input_value/10000)==4:
        global good_count_num
        reading=input_value-40001
        read=c.read_holding_registers(reading, register_number)

        if read:
            print(f"read: {read}")

        elif read==None or register_number=="" :
            bad_count()
            wrong_address()

    # checking if address starts from "3"
    elif int(input_value/10000)==3:
        reading = input_value - 30001
        read = c.read_input_registers(reading, register_number)
        if read:
            print(f"read: {read}")
        else:
            bad_count()
            wrong_address()

    # checking if address starts from "1"
    elif int(input_value/10000)==1:
        reading = input_value - 10001
        read = c.read_discrete_inputs(reading, register_number)
        if read:
            print(f"read: {read}")
        else:
            bad_count()
            wrong_address()
    else:
        print("Not a valid address!")
        bad_count()
        wrong_address()
        # Will increase its scope in FUTURE

    #Special call to read inspection time
    if var.get()==4 and (reading==302 or reading==604) and register_number==4:
        l = c.read_input_registers(302, 4)
        if l:
            print(l)
        num = l[0] << 48 | l[1] << 32 | l[2] << 16 | l[3]
        num = int(num / 1000)
        day = int(num / (24 * 60 * 60))
        hr = int(num / (3600))
        minutes = (num / 60)
        int_min = int(num / 60)
        seconds = int((minutes - int_min) * 60)
        data_textbox.delete("1.0", END)
        data_textbox.insert("1.0", f"{day}: {hr}: {int_min}: {seconds}")

    # To read int datatype
    elif var.get()==1  and read:
        try:
            num = read[0] << 16 | read[1]
            data_textbox.delete("1.0", END)
            data_textbox.insert("1.0", f"{num}")
            good_count()
        except:
            bad_count()
            wrong_address()

    # To read short/bool/enum
    elif (var.get()==5 or var.get()==6 or var.get()==7) and read:
        try:
            data_textbox.delete("1.0", END)
            data_textbox.insert("1.0", f"{read}")
            good_count()
        except:
            bad_count()
            wrong_address()

    # To read float
    elif var.get()==2 and read:
        try:
            num = read[0] << 16 | read[1]
            if num:
                hex_num = hex(num)
                hex_numm = hex_num[2:]
                final = struct.unpack('!f', bytes.fromhex(hex_numm))[0]
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{final}")
                good_count()
            else:
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", "0")
        except:
                bad_count()
                wrong_address()

    # To read string
    elif var.get()==3 and read:
        data_textbox.delete("1.0", END)
        b = []
        try:
            [b.append(chr(x)) for x in read]
            listToStr = ''.join([str(elem) for elem in b])
            final = listToStr
            data_textbox.delete("1.0", END)
            data_textbox.insert("1.0", f"{final}")
            good_count()
        except:
            bad_count()
            wrong_address()

    # TO read Long
    elif var.get()==4 and read:
        try:
            num = read[0] << 48 | read[1] << 32 | read[2] << 16 | read[3]
            num = int(num / 1000)
            if (ip_entry.get()=="127.0.0.1") or (ip_entry.get()=="localhost"):
                final = datetime.fromtimestamp(num)
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{final.time()}")
            else:
                final1=datetime.utcfromtimestamp(num)
                data_textbox.delete("1.0", END)
                data_textbox.insert("2.0", f"{final1.time()}")
            good_count()
        except:
            bad_count()
            wrong_address()

    # To read Timestamp
    elif var.get()==8 and read:
        try:
            num = read[0] << 48 | read[1] << 32 | read[2] << 16 | read[3]
            print(num)
            num = int(num / 1000)
            print(num)

            if (ip_entry.get()=="127.0.0.1") or (ip_entry.get()=="localhost"):
                final = datetime.fromtimestamp(num)
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{final}")
            else:
                utc=datetime.utcfromtimestamp(num)
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{utc}")
            good_count()
        except:
            bad_count()
            wrong_address()

    #TO read double
    elif var.get()==9 and read:
        try:
            num=read[0] << 48 | read[1] << 32 | read[2] << 16 | read[3]
            if num:
                hex_num=hex(num)
                hex_numm=hex_num[2:]
                final=struct.unpack("<d", struct.pack("Q", int("0x" + hex_numm, 16)))[0]
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{final}")
            else:
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", "0")
        except:
            bad_count()
            wrong_address()

    #TO read bitstream
    elif var.get()==10 and read:
        try:
            if int(input_value/10000)==1:
                stream=[1 if x==True else 0 for x in read]
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{stream}")
                good_count()
            else:
                data_textbox.delete("1.0", END)
                data_textbox.insert("1.0", f"{read}")
                good_count()

        except:
            bad_count()
            wrong_address()

    #to read raw data
    elif var.get()==11 and read:
        try:
            data_textbox.delete("1.0", END)
            data_textbox.insert("1.0", f"{read}")
            good_count()
        except:
            bad_count()
            wrong_address()

    else:
        data_textbox.delete("1.0", END)
        data_textbox.insert("1.0", "Something went wrong!")

#function to write registers
def write_register():
    global c
    insert_value=int(register_address_entry.get())

    if int(insert_value/10000)==4:
        writing=insert_value-40001
        value=data_textbox.get("1.0", END)

        # int
        if var.get()==1:
            try:
                final_value=int(value)
                write = c.write_single_register(writing, final_value)
                good_count()
            except:
                bad_count()
                wrong_address()

        # short/bool/enum
        elif (var.get()==5 or var.get()==6 or var.get()==7):
            try:
                final_value=int(value)
                write = c.write_single_register(writing, final_value)
                good_count()
            except:
                bad_count()
                wrong_address()

        #string
        elif var.get()==3:
            try:
                listi = list(value)
                final_value = [ord(x) for x in listi]
                final_value.pop()
                final_value.append(0)
                write = c.write_multiple_registers(writing, final_value)
                good_count()
            except:
                bad_count()
                wrong_address()

        # float
        elif var.get()==2:
            try:
                final_value=float(value); print(value)
                hexoo = hex(struct.unpack('<I', struct.pack('<f', final_value))[0]); print(hexoo)
                inti_hexoo = int(hexoo, 16); print(f"{inti_hexoo} : new int")
                x0 = inti_hexoo >> 16; x1 = inti_hexoo & 0xFF; print(x0, x1)
                float_num = c.write_multiple_registers(writing, [x0, x1])
                good_count()
            except:
                bad_count()
                wrong_address()

        # double
        elif var.get()==9:
            try:
                final_value=float(value)
                hex_conversion = hex(struct.unpack("<Q", struct.pack("d", final_value))[0]); print(f"Hex con:{hex_conversion}")
                inti_hexxi = int(hex_conversion, 16); print(f"Inti_hexi:{int(hex_conversion, 16)}")
                x0 = inti_hexxi >> 48; x1 = (inti_hexxi >> 32) & 0xFFFF; x2 = (inti_hexxi >> 16) & 0xFFFF; x3 = (inti_hexxi >> 0) & 0xFFFF
                float_num = c.write_multiple_registers(writing, [x0, x1, x2, x3])
                good_count()
            except:
                bad_count()
                wrong_address()

        # timestamp/raw data/
        elif (var.get() == 11 or var.get() == 8):
            bad_count()
            wrong_address()

        else:
            data_textbox.delete("1.0", END)
            data_textbox.insert("1.0", "Wrong input!")
            bad_count()
            wrong_address()
    else:
        bad_count()
        wrong_address()

s = ttk.Style()
s.configure('TButton',font=(12), bg='white smoke')

read_button=ttk.Button(top, text= "Read", command = read_register,style='my.TButton')
write_button=ttk.Button(top, text= "Write", command = write_register,style='my.TButton')
connect_button=ttk.Button(top, text= "Connect", command = connect,style='my.TButton', width=7)
clear_button=ttk.Button(top, text= "Clear", command = clear_text,style='my.TButton', width=6)
disconnect_button=ttk.Button(top, text= "Disconnect", command = disconnect,style='my.TButton', width=9)

connect_button.grid(row=0, column= 1, padx=5, pady=5, rowspan=2, sticky=SW)
read_button.grid(row=5, column= 1, padx=5, pady=5)
write_button.grid(row=5, column= 2,  padx=5, pady=5,  columnspan=2)
clear_button.grid(row=15, column=3,padx=5, pady=5)
disconnect_button.grid(row=0, column= 1, padx=5, pady=5, sticky=SE, rowspan=2)

s.configure('TLabel',background='white smoke',font=(12))

ip_label=ttk.Label(text="IP Address")
conn_status_label=ttk.Label(text="Connection Status")
register_address_label=ttk.Label(text="Register Address")
register_count_label=ttk.Label(text="No. of Regsiters",  justify="center")
data_label=ttk.Label(text="Data")
blank_label=ttk.Label("")
version_label=Label(text="Version:1.0.0",background='white smoke' )
good_count_label=ttk.Label(text="Good")
bad_count_label=ttk.Label(text="Error")

ip_label.grid(row=0, column= 0, padx=5, pady=5, sticky="s")
conn_status_label.grid(row=0, column= 2, padx=5, pady=5, sticky="e")
register_address_label.grid(row=3, column= 1, padx=5, pady=5, sticky="s")
register_count_label.grid(row=3, column= 2, padx=5, pady=5, sticky="s",  columnspan=2)
data_label.grid(row=7, column= 1,  padx=5, pady=5, sticky=W)
version_label.grid(row=15, column= 0,  padx=5, pady=5, sticky=SW)
good_count_label.grid(row=7, column= 3,  padx=5, sticky=S)
bad_count_label.grid(row=9, column= 3,  padx=5, sticky=S)

ip_entry=ttk.Entry(top, width =25 , justify="center")
register_address_entry=ttk.Entry(top, width =25, justify="center")
register_count_entry=ttk.Entry(top, width=25, justify="center")
conn_status_text=ttk.Entry(top, width=20, justify="center")
data_textbox=Text(top, height=15, width=50)
good_count_entry=ttk.Entry(top, width =10, justify="center")
bad_count_entry=ttk.Entry(top, width =10, justify="center")

ip_entry.grid(row=1, column= 0, padx=5, pady=5, sticky = "n")
register_address_entry.grid(row=4, column= 1, padx=5, pady=5, sticky = "n" )
register_count_entry.grid(row=4, column= 2, padx=5, pady=5,  columnspan=2)
data_textbox.grid(row=8, column=1,  padx=5, pady=5, columnspan=2, rowspan=8,sticky = NW )
conn_status_text.grid(row=1, column= 2, padx=5, pady=5, sticky=E)
good_count_entry.grid(row=8, column= 3, padx=5,sticky = N)
bad_count_entry.grid(row=10, column= 3, padx=5,sticky = N)

s.configure('TRadiobutton',font=(12), background='white smoke')

R1_int = ttk.Radiobutton(top, text="Int", variable=var, value=1,command=sel)
R2_float = ttk.Radiobutton(top, text="Float", variable=var, value=2,command=sel)
R3_string = ttk.Radiobutton(top, text="String", variable=var, value=3,command=sel)
R4_long = ttk.Radiobutton(top, text="Long", variable=var, value=4,command=sel)
R5_short = ttk.Radiobutton(top, text="Short", variable=var, value=5,command=sel)
R6_bool = ttk.Radiobutton(top, text="bool", variable=var, value=6,command=sel)
R7_enum = ttk.Radiobutton(top, text="enum", variable=var, value=7,command=sel)
R8_timestamp = ttk.Radiobutton(top, text="Timestamp", variable=var, value=8,command=sel)
R9_double = ttk.Radiobutton(top, text="Double", variable=var, value=9,command=sel)
R10_bitstream= ttk.Radiobutton(top, text="Bitstream", variable=var, value=10,command=sel)
R11_raw_data= ttk.Radiobutton(top, text="Raw data", variable=var, value=11,command=sel)

R1_int.grid(row =3 , column = 0, padx=3, pady=3,sticky=NW )
R2_float.grid(row =4 , column = 0, padx=3, pady=3, sticky=NW)
R3_string.grid(row =5, column = 0,  padx=3, pady=3, sticky=NW)
R4_long.grid(row =6 , column = 0,  padx=3, pady=3, sticky=NW)
R5_short.grid(row =7 , column = 0,  padx=3, pady=3, sticky=NW)
R6_bool.grid(row =8, column = 0,  padx=3, pady=3, sticky=NW)
R7_enum.grid(row =9 , column = 0,  padx=3, pady=3, sticky=NW)
R8_timestamp.grid(row =10 , column = 0,  padx=3, pady=3, sticky=NW)
R9_double.grid(row =11 , column = 0,  padx=3, pady=3, sticky=NW)
R10_bitstream.grid(row =12 , column = 0,  padx=3, pady=3, sticky=NW)
R11_raw_data.grid(row =13 , column = 0,  padx=3, pady=3, sticky=NW)

seprator=ttk.Separator(top,orient="horizontal")
seprator.grid(row=2, column = 0, columnspan=5, sticky="ew",  padx=3, pady=10)

ip_entry.insert(1, "127.0.0.1")
register_count_entry.insert(1,f"{1}")
top.mainloop()

