#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:09:24 2021

@author: hemanth
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 18:59:34 2021

@author: hemanth
"""
from sensor_comm_v3 import SensorComm 
import serial.tools.list_ports
import matplotlib.pyplot as plt
import serial
import time
import numpy
import numpy as np
import tkinter as tk
from file_read import read_raw
from tkinter import ttk   
from tkinter import Tk,Button,Label,HORIZONTAL,DoubleVar,Scale,Text,Toplevel,NORMAL,DISABLED,Checkbutton,messagebox,IntVar
# from tkinter import *
# from tkinter.ttk import Progressbar
# from PIL import ImageTk,Image
# import cmd_gen_new as cg
# from cmd_cls_new_calib import CMD
global newWindow
global read_para
global COM_PORT
global global_offset
global cmd_gen
global REG
global channel,slot,mode,slot_val,gain,param_selected,DETECTOR_BIAS,HC,values,param_val_sel
gain=1
param_selected=0
DETECTOR_BIAS=0
HC=0
path_store = './'

def serial_ports():    
    comlist= list(serial.tools.list_ports.comports())
    connected =[]
    for element in comlist:
        connected.append(element.device)
    return connected  

def mouseclick_brightness(event):
   COM_PORT=cb.get() 
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   sel =" B = "+str(brightness.get()) 
   blabel.config(text = sel)
   br=int(str(brightness.get())  )
 
   cmd_gen.fpga_write(0xd0,br)
   # cmd_gen.set_brightness(br)
   ser.close()
def default_brightness():
   COM_PORT=cb.get()  
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   # blabel.config(text = sel)
   default_br=cmd_gen.fpga_read(0xd0)
   br_get=default_br['data'][0]<<24|default_br['data'][1]<<16|default_br['data'][2]<<8|default_br['data'][3]
   # print(type(br_get))
   brightness.set(br_get)
   dval=str(br_get)
   sel =" B = "+dval 
   blabel.config(text = sel)
   ser.close()
def mouseclick_contrast(event):
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
   sel1 = " C = " + str(contrast.get())  
   clabel.config(text = sel1)
   ct=int(str(contrast.get())  )
   cmd_gen.set_contrast(ct)
   ser.close()
def default_contrast():
   COM_PORT=cb.get()  
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   # blabel.config(text = sel)
   default_ct=cmd_gen.fpga_read(0xd4)
   ct_get=default_ct['data'][0]<<24|default_ct['data'][1]<<16|default_ct['data'][2]<<8|default_ct['data'][3]
   # print(type(br_get))
   contrast.set(ct_get)
   cval=str(ct_get)
   sel1 =" C = "+cval 
   clabel.config(text = sel1)
   ser.close()
    

def mouseclick_dphe(event):
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.select_agc_mode(0)
   sel2 = " DPHE = " + str(dphe.get())  
   dphelabel.config(text = sel2)
   dphe_val=int(str(dphe.get())  )
   # print(dphe_val)
   cmd_gen.fpga_write(0xa5,dphe_val)
   ser.close()
def default_dphe():
   COM_PORT=cb.get()  
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   # blabel.config(text = sel)
   default_dphe=cmd_gen.fpga_read(0xa5)
   dphe_get=default_dphe['data'][0]<<24|default_dphe['data'][1]<<16|default_dphe['data'][2]<<8|default_dphe['data'][3]
   # print(type(br_get))
   dphe.set(dphe_get)
   dpheval=str(dphe_get)
   sel2 =" DPHE = "+dpheval 
   dphelabel.config(text = sel2)
   ser.close()

   
def mouseclick_contrast_gain(event):
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
   cmd_gen.select_agc_mode(1)  
   sel3 = " CG = " + str(contrast_gain.get())  
   cglabel.config(text = sel3)
   contrast_gain_val=int(str(contrast_gain.get())  )
   cmd_gen.fpga_write(0xa9,contrast_gain_val)
   ser.close()
def default_csg():
   COM_PORT=cb.get()  
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   # blabel.config(text = sel)
   default_csg=cmd_gen.fpga_read(0xa9)
   csg_get=default_csg['data'][0]<<24|default_csg['data'][1]<<16|default_csg['data'][2]<<8|default_csg['data'][3]
   # print(type(br_get))
   contrast_gain.set(csg_get)
   csgval=str(csg_get)
   sel3 =" CS = "+csgval 
   cglabel.config(text = sel3)
   ser.close()
      
def mouseclick_contrast_offset(event):
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
   sel4 = " CO = " + str(contrast_offset.get())  
   colabel.config(text = sel4)
   contrast_gain_val=int(str(contrast_offset.get())  )
   cmd_gen.fpga_write(0xaa,contrast_gain_val)  
   ser.close()
def default_cog():
   COM_PORT=cb.get()  
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   # blabel.config(text = sel)
   default_cog=cmd_gen.fpga_read(0xaa)
   cog_get=default_cog['data'][0]<<24|default_cog['data'][1]<<16|default_cog['data'][2]<<8|default_cog['data'][3]
   # print(type(br_get))
   contrast_offset.set(cog_get)
   cogval=str(cog_get)
   sel4 =" CO = "+cogval 
   colabel.config(text = sel4) 
   ser.close()
            
def on_device(event):
    COM_PORT=cb.get() 
    # cb.current(0)
    print(COM_PORT)   
    return
def shutterless():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x54,gain)
   cmd_gen.fpga_write(0x91,0)
   
   ser.close()
def shuttered():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x54,gain)
   # cmd_gen.fpga_write(0x81,2)
   # cmd_gen.fpga_write(0x80,0)
   # cmd_gen.shutter_open()
   cmd_gen.fpga_write(0x91,0x3)
   # time.sleep(0.9)
   # cmd_gen.shutter_close()
   ser.close()
def seminuc():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x54,gain)
   # cmd_gen.fpga_write(0x81,1)
   # cmd_gen.fpga_write(0x80,0)
   # cmd_gen.shutter_open()
   cmd_gen.fpga_write(0x91,0x18)
   # time.sleep(2)
   # cmd_gen.shutter_close()    
   ser.close()     
def ugain():
   global gain 
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   if var1.get()==1:
        cmd_gen.fpga_write(0x54,0x3)
        gain=3        
   else:
        cmd_gen.fpga_write(0x54,0x1)
        gain=1

def whitehot():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x52,0)
   bh_polarity.configure(text="")
   wh_polarity.configure(text='WH ON')
   ser.close() 
def blackhot():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x52,1)
   wh_polarity.configure(text="")
   bh_polarity.configure(text='BH ON')
   ser.close() 
def agc_mode1():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')  
   cmd_gen.select_agc_mode(0)
   ser.close() 
def smoothening_disable():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')  
   cmd_gen.fpga_write(0x64,0)
   ser.close()
def smoothening_enable():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')  
   cmd_gen.fpga_write(0x64,1)
   ser.close()     
   
def agc_mode2():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.select_agc_mode(1)     
   ser.close()
def soft_nuc_enable():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x55,1)  
   ser.close() 
   
def soft_nuc_disable():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.fpga_write(0x55,0)  
   ser.close() 

def dzoom_1x():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.set_digital_zoom('1x') 
   ser.close() 
def dzoom_2x():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.set_digital_zoom('2x') 
   ser.close() 
def dzoom_4x():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   cmd_gen.set_digital_zoom('4x')  
   ser.close() 
def mouseclick_area_select(event):
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
   area_selected= cbarea.get()
   sel_area_lbl.config(text = "AREA = "+area_selected)
   cmd_gen.switch_athena_temp_area(int(area_selected))
   ser.close()   
def channel_sel(event):
   # COM_PORT=cb.get()
   # ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   # cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   channel_selected=cbchannel.get()
   if(channel_selected=='agc'):
       channel=2
       slot_val=[int(x) for x in range(1,65)]
       cbslot['values']=slot_val 
   else:
       slot_val=[int(x) for x in range(1,33)]
       cbslot['values']=slot_val 
   if(channel_selected=='nuc'):
       channel=1 
   if(channel_selected=='raw'):
       channel=0 
   # print(type(channel))       
   return channel
def mode_sel(event):
   # COM_PORT=cb.get()
   # ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   # cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
   mode_selected=cbmode.get()
   if(mode_selected=='continuous'):
       mode=0
   if(mode_selected=='single'):
       mode=4
   # print(type(mode))    
   return mode
def slot_sel(event):
   # COM_PORT=cb.get()
   # ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   # cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    slot=int(cbslot.get())
  
   
   

def default_area():
   COM_PORT=cb.get()
   ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
   cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
   default_area=cmd_gen.get_temp_area()
   cbarea.set(default_area)
   ser.close()
   
def enable_co_correction(cmd_gen,mode='div1024', slot=1):
    
    #Mode definition
    # COM_PORT=cb.get()
    # ser = serial.Serial(COM_PORT, 115200 , timeout=5)  #921600
    # cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
    mode_dict = {'fine':1,
                 'div1024':2,
                 'div600':3, 
                 'div800':4, 
                 'div1000':5, 
                 'div1200':6, 
                 'div1400':7
                 }
    
    if(mode not in mode_dict):
        print('Illegal Mode value:',mode)
        print('Mode needs to be one of the following')
        print('[\'fine\', \'div1024\', \'div600\', \'div800\', \'div1000\', \'div1200\', \'div1400\']')
        return
        
    co_address_base = 0x006CC000
    co_address_offset = 0x00052800
    co_address = co_address_base+(slot-1)*co_address_offset
    
    cmd_gen.set_CO_addr(co_address)
    
    cmd_gen.disable_nuc()
    cmd_gen.disable_blind_pix_subtraction()
    cmd_gen.lock_global_offset()
    cmd_gen.take_snapshot(channel=0, mode=12, number_frames=1)
    cmd_gen.switch_CO_bus_mode(1)
    cmd_gen.set_CO_mode(mode_dict[mode])
    cmd_gen.trigger_wait_CO_calc()
    cmd_gen.switch_CO_bus_mode(0)
    cmd_gen.enable_blind_pix_subtraction()
    cmd_gen.auto_global_offset()
    cmd_gen.enable_nuc()
    # ser.close()

def coarse_update():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
    AREA = int(cmd_gen.get_temp_area())
    print(AREA)    
    slot=AREA-1
    MsgBox = tk.messagebox.askquestion ('COARSE UPDATE','Are you sure you want update CO',icon = 'warning')
    if MsgBox == 'yes':
        enable_co_correction(cmd_gen,mode='fine', slot=slot)
        # window.destroy()
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')
    
    ser.close()
def reg_data(event):
    # COM_PORT=cb.get()
    # ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    # cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    REG=int(cbreg.get(),16)
    print(type(REG))
    print(REG)
    return
def reg_data_enter(event):
    REG=int(cbreg.get(),16)
    print(type(REG))
    print(REG)
    
    
    
def data_dec():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    REG=int(cbreg.get(),16)
    
    DATA=int(reg_val.get(1.0, "end-1c"),10)
    # print(type(DATA)  ) 
    # print(DATA)
    cmd_gen.fpga_write(REG,DATA)
    ser.close()
def data_hex():  
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    REG=int(cbreg.get(),16)
    # print(type(REG))
    DATA1=int(reg_val_hex.get(1.0, "end-1c"),16)
    # print(type(DATA1)  ) 
    # print(DATA1)
    cmd_gen.fpga_write(REG,DATA1)
    ser.close()
def read():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    REG=int(cbreg.get(),16)
    read_val=cmd_gen.fpga_read(REG)
    # print(read_val['data'])
    # print(read_val['data'][2])
    out=read_val['data'][0]<<24|read_val['data'][1]<<16|read_val['data'][2]<<8|read_val['data'][3]
    # print(out)   
    reg_val_hex.delete("1.0", "end")
    reg_val_hex.insert(tk.END,hex(out))
    reg_val.delete("1.0", "end")
    reg_val.insert(tk.END,out)
        # print(hex(out))
    ser.close()    
def fw_version():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    fw_version= cmd_gen.fpga_read(0x10)
    # print(fw_version['data'][3])
    fw_ver_out=fw_version['data'][0]<<24|fw_version['data'][1]<<16|fw_version['data'][2]<<8|fw_version['data'][3]
    print(fw_ver_out)
    fw_ver.delete("1.0","end")
    fw_ver.insert(tk.END,fw_ver_out)
    ser.close()
def int_time():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    inte_time=int(int_time.get(1.0, "end-1c"),10)
    cmd_gen.set_intergration_time_start(inte_time) 
    # print(type(inte_time) ) 
    ser.close()
def get_int_time():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new') 
    int_time_val=cmd_gen.get_intergration_time_start()
    int_time.delete("1.0", "end")
    int_time.insert(tk.END,int(int_time_val)  )  
    ser.close()
def sensor_gain():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    sensorgain=int(sensor_gain.get(1.0, "end-1c"),10)
    cmd_gen.set_sensor_gain(sensorgain)
    # print(sensorgain)
    ser.close()
def get_sensor_gain():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    get_sensorgain=cmd_gen.get_sensor_gain()
    sensor_gain.delete("1.0", "end")
    sensor_gain.insert(tk.END,int(get_sensorgain)  )  
    # print(sensorgain)
    ser.close()     
def save_settings():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    MsgBox = tk.messagebox.askquestion ('SAVE USER SETTINGS','Are you sure you want to save',icon = 'warning')
    if MsgBox == 'yes':
        cmd_gen.save_user_settings()
        # window.destroy()
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')

    ser.close()
def ret_0():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,0)
    ser.close()
def ret_1():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,1)  
    cmd_gen.fpga_write(0x76,1) 
    ser.close()
def ret_2():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,2)  
    cmd_gen.fpga_write(0x76,1) 
    ser.close()    
def ret_3():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,3)  
    cmd_gen.fpga_write(0x76,1)  
    ser.close()
def ret_4():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,4)  
    cmd_gen.fpga_write(0x76,1) 
    ser.close()
def ret_5():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0x66,5)  
    cmd_gen.fpga_write(0x76,1)
    ser.close()
def destroy():
    global newWindow
    read_param_button.configure(state=NORMAL)
    newWindow.destroy()

    # read_param_button.configure(state=NORMAL)
         
def openNewWindow():
    global newWindow
    global read_para
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    read_param_button.configure(state=DISABLED)
    newWindow = Toplevel(top)
    newWindow.title("parameters")
    newWindow.geometry("400x400") 
    read_para = Text(newWindow,height=23,width = 53,font='Arial 10 bold')
    read_para.place(x=10,y=5)
    # exit_button= Button(newWindow,text='EXIT',font='Arial 10 bold',height = 1, width = 8)
    # exit_button.place(x=200,y=350)
    readpara_button= Button(newWindow,text='READ',font='Arial 10 bold',height = 1, width = 8,command=update)
    readpara_button.place(x=150,y=350)
    serial_num = cmd_gen.get_device_serial_num_new()
    meta1 = cmd_gen.get_meta1_avg()
    global_offset = cmd_gen.get_global_offset()    
    blind_pix_avg_frame = cmd_gen.get_blind_pix_avg_frame()   
    img_avg = cmd_gen.get_img_avg()  
    dark_pixel_count = cmd_gen.get_dark_pixel_count()
    saturated_pixel_count = cmd_gen.get_saturated_pixel_count()
    raw_img_avg = cmd_gen.get_image_average_raw()   
    d_bias = cmd_gen.get_detector_bias()
    hc = cmd_gen.get_heating_compensation()
    temp_offset = cmd_gen.get_temp_sense_offset()
    
    area = cmd_gen.get_temp_area()
    read_para.delete("1.0", "end")
    read_para.insert(tk.END," serial no ="+ str(serial_num)+"\n"+"\n"  ) 
    read_para.insert(tk.END," meta avg ="+ str(meta1)+"\n"+"\n"  ) 
    read_para.insert(tk.END," global offset ="+ str(global_offset)+"\n"+"\n"  ) 
    read_para.insert(tk.END," img_avg ="+ str(img_avg)+"\n"+"\n" ) 
    read_para.insert(tk.END," dark_pixel_count ="+ str(dark_pixel_count)+"\n"+"\n" ) 
    read_para.insert(tk.END," blind_pix_avg_frame ="+ str(blind_pix_avg_frame)+"\n"+"\n" ) 
    read_para.insert(tk.END," saturated_pixel_count ="+ str(saturated_pixel_count)+"\n"+"\n" ) 
    read_para.insert(tk.END," raw_img_avg ="+ str(raw_img_avg)+"\n"+"\n" )
    read_para.insert(tk.END," d_bias ="+ str(hex(d_bias))+"\n"+"\n" )
    read_para.insert(tk.END," hc ="+ str(hex(hc))+"\n"+"\n" )
    read_para.insert(tk.END," temp_offset ="+ str(hex(temp_offset))+"\n"+"\n" )
    read_para.insert(tk.END," area ="+ str(area)+"\n"+"\n" )
    newWindow.protocol("WM_DELETE_WINDOW", destroy)
    ser.close()
def update():
    global read_para    
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    serial_num = cmd_gen.get_device_serial_num_new()
    global_offset = cmd_gen.get_global_offset()    
    blind_pix_avg_frame = cmd_gen.get_blind_pix_avg_frame()   
    img_avg = cmd_gen.get_img_avg()  
    dark_pixel_count = cmd_gen.get_dark_pixel_count()
    saturated_pixel_count = cmd_gen.get_saturated_pixel_count()
    raw_img_avg = cmd_gen.get_image_average_raw()   
    d_bias = cmd_gen.get_detector_bias()
    hc = cmd_gen.get_heating_compensation()
    temp_offset = cmd_gen.get_temp_sense_offset()
    meta1 = cmd_gen.get_meta1_avg()
    area = cmd_gen.get_temp_area()
    read_para.delete("1.0", "end")
    read_para.insert(tk.END," serial no ="+ str(serial_num)+"\n"+"\n"  )
    read_para.insert(tk.END," meta avg ="+ str(meta1)+"\n"+"\n"  ) 
    read_para.insert(tk.END," global offset ="+ str(global_offset)+"\n"+"\n"  ) 
    read_para.insert(tk.END," img_avg ="+ str(img_avg)+"\n"+"\n" ) 
    read_para.insert(tk.END," dark_pixel_count ="+ str(dark_pixel_count)+"\n"+"\n" ) 
    read_para.insert(tk.END," blind_pix_avg_frame ="+ str(blind_pix_avg_frame)+"\n"+"\n" ) 
    read_para.insert(tk.END," saturated_pixel_count ="+ str(saturated_pixel_count)+"\n"+"\n" ) 
    read_para.insert(tk.END," raw_img_avg ="+ str(raw_img_avg)+"\n"+"\n" )
    read_para.insert(tk.END," d_bias ="+ str(hex(d_bias))+"\n"+"\n" )
    read_para.insert(tk.END," hc ="+ str(hex(hc))+"\n"+"\n" )
    read_para.insert(tk.END," temp_offset ="+ str(hex(temp_offset))+"\n"+"\n" )
    read_para.insert(tk.END," area ="+ str(area)+"\n"+"\n" )
    ser.close()
def erase():
  
    MsgBox = tk.messagebox.askquestion ('erase qspi','Are you sure you want to erase qspi',icon = 'warning')
    if MsgBox == 'yes':
        erase_command()
        # window.destroy()
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')
    
def erase_command():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.erase_qspi_4KB(0x0, 1)
    messagebox.showinfo("erases qspi", "enabled")
    ser.close()
def snap_shot():
    global channel,slot,mode
    slot=int(cbslot.get())
    mode_selected=cbmode.get()
    if(mode_selected=='continuous'):
       mode=0
    if(mode_selected=='single'):
       mode=4
    channel_selected=cbchannel.get()
    if(channel_selected=='agc'):
       channel=2
    if(channel_selected=='nuc'):
       channel=1
    if(channel_selected=='raw'):
       channel=0 
       
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.take_snapshot(channel=channel, mode=mode, number_frames=slot)  
    ser.close()    

def image_readback_single(slot, mode='agc'):
    
    #############################################
    # slot can go from 1 to 32 for raw and
    # 1 to 64 for processed
    # mode can be either 'raw', 'nuc' or 'agc'
    #############################################
    
    #addresses are defined in VHDL file
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    snapshot_qspi_base_address = 0x284E000
    snapshot_sdram_base_address = 0x3794000
    # bar1()
    width=0
    height=0
    if(mode=='raw'):
        width = 664
        height = 519
        snapshot_offset = 0xAA000
        snapshot_size = width*height*2 # since images are 16bits
    elif(mode=='nuc'):
        width = 640
        height = 480
        snapshot_offset = 0xAA000
        snapshot_size = width*height*2 # since images are 16bits
    elif(mode=='agc'):
        width = 640
        height = 480
        snapshot_offset = 0x55000
        snapshot_size = width*height # since images are 8bits
    # bar2()    
    cmd_gen.disable_nuc()
    cmd_gen.transfer_data_to_sdram(snapshot_sdram_base_address,snapshot_qspi_base_address+(slot-1)*snapshot_offset,snapshot_offset)
    ret=cmd_gen.qspi_success_status(sleeptime_max=50)
    if(ret==-1):
        print('QSPI Problem, exiting')
        return
    # bar3()
    data=cmd_gen.read_data_sdram(snapshot_sdram_base_address, snapshot_size)
    data=np.asarray(data, dtype=np.uint8) 
    data_swap = np.zeros(data.shape, dtype=data.dtype)
    # bar4()
    for i in range(len(data)//4):
        data_swap[i*4+0:i*4+4] = np.flip(data[i*4+0:i*4+4])
            
    data_swap.tofile(path_store+mode+'snapshot_readback_serial_slot_'+str(slot)+'.bin')
    # img1=data_swap.reshape(height,width)
    # plt.figure(figsize=(15,15))
    # # plt.plot(data_swap)
    # plt.imshow(img1,'gray')
    # plt.savefig(path_store+mode+'_snapshot_readback_serial_slot_'+str(slot)+".jpg")
    # plt.pause(0.1)
    # cmd_gen.enable_nuc()
    file_name=path_store+mode+'snapshot_readback_serial_slot_'+str(slot)+'.bin'
    if(mode=='agc'):
        img1=read_raw(file_name,640,480,8)
        plt.figure(figsize=(15,15))
        plt.imshow(img1,'gray')
        plt.savefig(path_store+mode+'_snapshot_readback_serial_slot_'+str(slot)+".jpg")
        plt.pause(0.1)
    elif(mode=='nuc'):
        img1=read_raw(file_name,640,480,16)
        plt.figure(figsize=(15,15))
        plt.imshow(img1,'gray')
        plt.savefig(path_store+mode+'_snapshot_readback_serial_slot_'+str(slot)+".jpg")
        plt.pause(0.1)
    else:
        img1=read_raw(file_name,664,519,16)
        plt.figure(figsize=(15,15))
        plt.imshow(img1,'gray')
        plt.savefig(path_store+mode+'_snapshot_readback_serial_slot_'+str(slot)+".jpg")
        plt.pause(0.1)
    ser.close()
   
def read_snap_shot():
    slot_num = 0
    global channel,slot,mode
    slot=int(cbslot.get())
    mode_selected=cbmode.get()

    channel_selected=cbchannel.get()
    if(channel_selected=='agc'):
       channel=2
    if(channel_selected=='nuc'):
       channel=1
    if(channel_selected=='raw'):
       channel=0   

    if(mode_selected=='continuous'):
        for slot_num in range(1,(slot+1)):
            image_readback_single(slot_num,mode=channel_selected) 

    if(mode_selected=='single'):

            image_readback_single(slot,mode=channel_selected)        

def shutter_open():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.shutter_close()
    ser.close() 
def shutter_close():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.shutter_open()
    ser.close()     
def set_threshold(event):
    TH=int(cbthreshold.get())
    print(type(TH))
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    cmd_gen.fpga_write(0xEE,TH)
    ser.close() 

def param_sel(event):
    global param_selected
    if cb_param.get()=='BIAS':
        param_selected=1
    if cb_param.get()=='HC' :
        param_selected=2
    if cb_param.get()=='TSO':
        param_selected=3
    # return             
def param_value(event):
    values=int(cb_param_val.get(),16)
    
    return values   
def param_value_enter(event):
    values=int(cb_param_val.get(),16)

    return values   
def set_param():
    COM_PORT=cb.get()
    ser = serial.Serial(COM_PORT , 115200 , timeout=5)  #921600
    cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
    values=int(cb_param_val.get(),16)
    # print(values)
    
    if param_selected==1:
        # print(values)
        cmd_gen.set_detector_bias(values)
    if param_selected==2:
        cmd_gen.set_heating_compensation(values)
        # print(type(values))
    if param_selected==3:
        cmd_gen.set_temp_sense_offset(values)
        # print(type(values))
        
    
############################################################## 
if __name__ == "__main__":  
    
    top = Tk()
    top.title(" 12u ATHENA ")  
    top.geometry("880x640")
    cb=IntVar()
    v = DoubleVar()    
    # print("a")
    brightness = Scale( top, variable = v, from_ = 0, to = 10,length=350,orient = HORIZONTAL,showvalue=0,label="BRIGHTNESS",font='Arial 10 bold')  
    brightness.place(x=10,y=90)
    # brightness.set(85) 
    brightness.bind('<ButtonRelease>',mouseclick_brightness) 
    
    contrast = Scale( top, from_ = 0, to = 10,length=350,orient = HORIZONTAL,showvalue=0,label="CONTRAST",font='Arial 10 bold') 
    # contrast.set(64) 
    contrast.place(x=10,y=140) 
    contrast.bind('<ButtonRelease>',mouseclick_contrast)
    
    dphe = Scale( top, from_ = 0, to = 100,length=350,orient = HORIZONTAL,showvalue=0,label="DPHE",font='Arial 10 bold') 
    # contrast.set(64) 
    dphe.place(x=10,y=195) 
    dphe.bind('<ButtonRelease>',mouseclick_dphe)
    
    contrast_gain = Scale( top, from_ = 0, to = 100,length=350,orient = HORIZONTAL,showvalue=0,label="CONTRAST STRETCH GAIN",font='Arial 10 bold') 
    # contrast.set(64) 
    contrast_gain.place(x=10,y=245) 
    contrast_gain.bind('<ButtonRelease>',mouseclick_contrast_gain)
    
    contrast_offset = Scale( top, from_ = 0, to = 100,length=350,orient = HORIZONTAL,showvalue=0,label="CONTRAST STRETCH OFFSET",font='Arial 10 bold') 
    # contrast.set(64) 
    contrast_offset.place(x=10,y=305) 
    contrast_offset.bind('<ButtonRelease>',mouseclick_contrast_offset)
    
    blabel = Label(top,font='Arial 10 bold')  
    blabel.place(x=430,y=108)  
    clabel = Label(top,font='Arial 10 bold')  
    clabel.place(x=430,y=155)
    dphelabel = Label(top,font='Arial 10 bold')  
    dphelabel.place(x=430,y=212)
    cglabel = Label(top,font='Arial 10 bold')  
    cglabel.place(x=430,y=264)
    colabel = Label(top,font='Arial 10 bold')  
    colabel.place(x=430,y=324)
    polarity=Label(top,text='POLARITY',font='Arial 10 bold')
    polarity.place(x=10,y=370)
    wh_polarity=Label(top)
    wh_polarity.place(x=95,y=400)
    bh_polarity=Label(top)
    bh_polarity.place(x=180,y=400)
    agc=Label(top,text='AGC MODE',font='Arial 10 bold')
    agc.place(x=10,y=413)
    smooth_lbl=Label(top,text='SMOOTH',font='Arial 10 bold')
    smooth_lbl.place(x=10,y=453)
    softnuc=Label(top,text='SOFT NUC',font='Arial 10 bold')
    softnuc.place(x=10,y=490)
    digital_zoom=Label(top,text='D ZOOM',font='Arial 10 bold')
    digital_zoom.place(x=10,y=550)
    reticle_lbl=Label(top,text='RETICLE',font='Arial 10 bold')
    reticle_lbl.place(x=10,y=600)
    reg_lbl=Label(top,text='REG',font='Arial 10 bold')
    reg_lbl.place(x=580,y=220)
    txt_lbl=Label(top,text='Dec value',font='Arial 10 bold')
    txt_lbl.place(x=650,y=220)
    txt1_lbl=Label(top,text='Hex value',font='Arial 10 bold')
    txt1_lbl.place(x=650,y=270)
    snapshot_lbl=Label(top,text='SNAP SHOT',font='Arial 10 bold')
    snapshot_lbl.place(x=580,y=500)
    mode_lbl=Label(top,text='mode',font='Arial 10 bold')
    mode_lbl.place(x=740,y=480)
    channel_lbl=Label(top,text='channel',font='Arial 10 bold')
    channel_lbl.place(x=660,y=480)
    slot_lbl=Label(top,text='slot',font='Arial 10 bold')
    slot_lbl.place(x=820,y=480)
    lbl_shutter= Label(top, text="SHUTTER",font='Arial 10 bold',fg=("black"))
    lbl_shutter.place(x=580, y=580)
    
    nuc_label=Label(top, text='NUC MODES',font='Arial 10 bold')
    nuc_label.place(x=10,y=45)
    shutterless_button= Button(top, text='SHUTTERLESS',font='Arial 10 bold',command=shutterless)
    shutterless_button.place(x=110,y=40)
    shuttered_button= Button(top, text='SHUTTERED',font='Arial 10 bold',command=shuttered)
    shuttered_button.place(x=230,y=40)
    seminuc_button= Button(top, text='SEMI NUC',font='Arial 10 bold',command=seminuc)
    seminuc_button.place(x=340,y=40)
    var1 = IntVar()
    t1 = Checkbutton(top, text="U-GAIN",font='Arial 10 bold', variable=var1, onvalue=1, offvalue=0, command=ugain)
    t1.place(x=430,y=40)
    whitehot_button= Button(top, text='WHITE HOT',font='Arial 10 bold',height = 1, width = 9,command=whitehot)
    whitehot_button.place(x=90,y=365)
    blackhot_button= Button(top, text='BLACKHOT',font='Arial 10 bold',height = 1, width = 8,command=blackhot)
    blackhot_button.place(x=172,y=365)
    mode1_button= Button(top, text='MODE 1',font='Arial 10 bold',height = 1, width = 9,command=agc_mode1)
    mode1_button.place(x=90,y=410)
    mode2_button= Button(top, text='MODE 2',font='Arial 10 bold',height = 1, width = 8,command=agc_mode2)
    mode2_button.place(x=172,y=410)
    smooth_button= Button(top, text='DISABLE',font='Arial 10 bold',height = 1, width = 8,command=smoothening_disable)
    smooth_button.place(x=172,y=450)
    smooth_button1= Button(top, text='ENABLE',font='Arial 10 bold',height = 1, width = 9,command=smoothening_enable)
    smooth_button1.place(x=90,y=450)
    disable_button= Button(top, text='DISABLE',font='Arial 10 bold',height = 1, width = 8,command=soft_nuc_disable)
    disable_button.place(x=172,y=485)
    enable_button= Button(top, text='ENABLE',font='Arial 10 bold',height = 1, width = 9,command=soft_nuc_enable)
    enable_button.place(x=90,y=485)
    one_button= Button(top, text='1X',font='Arial 10 bold',command=dzoom_1x)
    one_button.place(x=90,y=545)
    two_button= Button(top, text='2X',font='Arial 10 bold',command=dzoom_2x)
    two_button.place(x=145,y=545)
    four_button= Button(top, text='4X',font='Arial 10 bold',command=dzoom_4x)
    four_button.place(x=200,y=545)
    ret_zero_button= Button(top, text='0',font='Arial 10 bold',command=ret_0)
    ret_zero_button.place(x=90,y=595)
    ret_one_button= Button(top, text='1',font='Arial 10 bold',command=ret_1)
    ret_one_button.place(x=125,y=595)
    ret_two_button= Button(top, text='2',font='Arial 10 bold',command=ret_2)
    ret_two_button.place(x=160,y=595)
    ret_three_button= Button(top, text='3',font='Arial 10 bold',command=ret_3)
    ret_three_button.place(x=195,y=595)
    ret_four_button= Button(top, text='4',font='Arial 10 bold',command=ret_4)
    ret_four_button.place(x=225,y=595)
    ret_five_button= Button(top, text='5',font='Arial 10 bold',command=ret_5)
    ret_five_button.place(x=255,y=595)
    shutteropen_button= Button(top, text='OPEN',font='Arial 10 bold',command=shutter_open)
    shutteropen_button.place(x=670,y=575)
    shutterclose_button= Button(top, text='CLOSE',font='Arial 10 bold',command=shutter_close)
    shutterclose_button.place(x=730,y=575)
    fw_button= Button(top, text='FW VERSION',font='Arial 10 bold',command=fw_version)
    fw_button.place(x=580,y=610)
    co_update_button= Button(top, text='COARSE OFFSET UPDATE',font='Arial 10 bold',command=coarse_update)
    co_update_button.place(x=580,y=170)
    dec_button= Button(top, text='SEND DEC',font='Arial 10 bold',command=data_dec)
    dec_button.place(x=740,y=235)
    hex_button= Button(top, text='SEND HEX',font='Arial 10 bold',command=data_hex)
    hex_button.place(x=740,y=285)
    read_button= Button(top, text='READ',font='Arial 10 bold',command=read)
    read_button.place(x=580,y=285)
    int_button= Button(top, text='SET INTEGRATION TIME',font='Arial 10 bold',command=int_time)
    int_button.place(x=670,y=330)
    get_int_button= Button(top, text='GET',font='Arial 10 bold',command=get_int_time)
    get_int_button.place(x=840,y=330)
    set_sensor_gain_button= Button(top, text='SET SENSOR GAIN',font='Arial 10 bold',width=19,command=sensor_gain)
    set_sensor_gain_button.place(x=670,y=380)
    get_sensor_gain_button= Button(top, text='GET',font='Arial 10 bold',command=get_sensor_gain)
    get_sensor_gain_button.place(x=840,y=380)
    save_usersetting_button= Button(top, text='SAVE USER SETTINGS',font='Arial 10 bold',command=save_settings)
    save_usersetting_button.place(x=360,y=600)
    read_param_button= Button(top, text='READ PARAMETER',font='Arial 10 bold',state=NORMAL,command=openNewWindow)
    read_param_button.place(x=580,y=440)
    get_br_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_brightness)
    get_br_button.place(x=370,y=108)
    get_ct_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_contrast)
    get_ct_button.place(x=370,y=155)
    get_dphe_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_dphe)
    get_dphe_button.place(x=370,y=212)
    get_csg_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_csg)
    get_csg_button.place(x=370,y=264)
    get_cog_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_cog)
    get_cog_button.place(x=370,y=324)
    get_area_button= Checkbutton(top, text='GET',font='Arial 10 bold',command=default_area)
    get_area_button.place(x=740,y=77)
    erase_button= Button(top, text='ERASE QSPI',font='Arial 10 bold',state=NORMAL,command=erase)
    erase_button.place(x=750,y=440)
    snapshot_button= Button(top, text='TAKE SNAP SHOT',font='Arial 10 bold',state=NORMAL,command=snap_shot)
    snapshot_button.place(x=580,y=530)
    set_param_button= Button(top, text='SET',font='Arial 10 bold',state=NORMAL,command=set_param)
    set_param_button.place(x=815,y=118)
    read_snapshot_button= Button(top, text='READ SNAP SHOT',font='Arial 10 bold',state=NORMAL,command=read_snap_shot)
    read_snapshot_button.place(x=730,y=530)
    lbl_deviceport = Label(top, text="Device port",font='Arial 10 bold',fg=("black"),bg=("cyan"))
    lbl_deviceport.place(x=580, y=5)
    cb=ttk.Combobox(top,values=serial_ports())################comport
    try:
        cb.current(0)
        cb.place(x=580,y=30)
        cb.bind('<<ComboboxSelected>>', on_device)
    except:   
        cb.place(x=580,y=30)
        cb.bind('<<ComboboxSelected>>', on_device)
    sel_area_lbl=Label(top,text='SELECT AREA',font='Arial 10 bold') 
    sel_area_lbl.place(x=580,y=60)
    param_lbl=Label(top,text='SET PARAM',font='Arial 10 bold') 
    param_lbl.place(x=580,y=120)
    areavalue=[0,1,2,3,4,5,6]
    cbarea =ttk.Combobox(top)
    cbarea.place(x=580,y=80)
    cbarea['values']=areavalue
    cbarea['state'] = 'readonly'
    cbarea.bind('<<ComboboxSelected>>',mouseclick_area_select)
    
    set_th_lbl=Label(top,text='THD',font='Arial 10 bold') 
    set_th_lbl.place(x=770,y=175)
    th_value=[int(x) for x in range(100,1100,100)]
    cbthreshold =ttk.Combobox(top,width=5)
    cbthreshold.place(x=810,y=175)
    cbthreshold['values']=th_value
    cbthreshold['state'] = 'readonly'
    cbthreshold.bind('<<ComboboxSelected>>',set_threshold)
    
    # registers = [*range(hex(int(0x0)),int(255),1)]
    hexlist = [hex(x) for x in range(256)]
    cbreg =ttk.Combobox(top,width=5)
    cbreg.place(x=580,y=240)
    cbreg['values']=hexlist
    # cbreg['state'] = 'readonly'
    cbreg.bind('<<ComboboxSelected>>',reg_data)
    cbreg.bind('<Return>',reg_data_enter)
    reg_val = Text(top,height=1,width = 10)
    reg_val.place(x=650,y=240)
    reg_val_hex = Text(top,height=1,width = 10)
    reg_val_hex.place(x=650,y=290)
    channels=['agc','nuc','raw']
    cbchannel =ttk.Combobox(top,width=5)
    cbchannel.place(x=660,y=500)
    cbchannel['values']=channels
    cbchannel['state'] = 'readonly'
    cbchannel.bind('<<ComboboxSelected>>',channel_sel)
    channel_sel=cbchannel.get()
    modes=['continuous','single']
    cbmode =ttk.Combobox(top,width=10)
    cbmode.place(x=720,y=500)
    cbmode.bind('<<ComboboxSelected>>',mode_sel)
    cbmode['values']=modes
    cbmode['state'] = 'readonly'
    slot_val=[int(x) for x in range(1,65)]
    # # if(channel_sel=='nuc'):
    # #     slot_val=[int(x) for x in range(1,33)]
    cbslot =ttk.Combobox(top,width=3)
    cbslot.bind('<<ComboboxSelected>>',slot_sel)
    cbslot.place(x=820,y=500)
    cbslot['values']=slot_val
    cbslot['state'] = 'readonly'
    param_val=['BIAS','HC','TSO']
    cb_param =ttk.Combobox(top,width=6)
    cb_param.bind('<<ComboboxSelected>>',param_sel)
    cb_param.place(x=680,y=120)
    cb_param['values']=param_val
    cb_param['state'] = 'readonly'
    param_val_sel=[hex(x)for x in range(0x0,0xff)]
    cb_param_val =ttk.Combobox(top,width=6)
    cb_param_val.bind('<<ComboboxSelected>>',param_value)
    cb_param_val.bind('<Return>',param_value_enter)
    cb_param_val.place(x=750,y=120)
    
    cb_param_val['values']=param_val_sel
    
    int_time = Text(top,height=1,width = 10)
    int_time.place(x=580,y=335)
    # get_int_time = Text(top,height=1,width = 10)
    # get_int_time.place(x=580,y=455)
    sensor_gain = Text(top,height=1,width = 10)
    sensor_gain.place(x=580,y=385)
    fw_ver = Text(top,height=1,width = 10)
    fw_ver.place(x=690,y=614)
    top.mainloop()  
