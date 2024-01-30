# import nezbytné nástroje
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from numpy import zeros, newaxis
import PIL
import tkinter.filedialog
import cv2
import numpy as np
import lxml.etree as ET
import matplotlib.pyplot as plt
import imutils
from tkinter import simpledialog
from tkinter import messagebox
import webbrowser
from pathlib import Path
import sys
import os

import modul_resize
import modul_togray
import modul_torgb
import modul_toycbcr
import modul_tohsv
import modul_rotate
import modul_scale
import modul_correction
import modul_negate
import modul_equalize
import modul_average
import modul_gaussian
import modul_sobel
import modul_median
import modul_laplace
import modul_canny
import modul_helpers
import modul_simple_thres
import modul_adaptive_thresh
import modul_otsu_thresh
import modul_erosion
import modul_dilation
import modul_opening
import modul_closing
import modul_top_hat
import modul_hough
import modul_coloring
import modul_searching
import modul_adaboost_haar
import modul_dlib
import modul_face_recognition

path=""
previous = None
list_of_actions = ""
path_to_file = ""
shown = False
percents_etalon = 0
angles_etalon = 0
correct_global = 0

angles_global = 0
percents_global = 0

A_global = 0
M_global = 0
G_global = 0
S_global = 0
C_global = 0
panel_size = 550
required_size = 580

#simple_thresholding-----------------------------------------
numb1 = 0
numb2 = 0

#adaptive_thresholding-----------------------------------------
maxValue = 0
C_constant = 0
blockSize = 0

#otsu--------------------------------------------------------
otsu_thresh = 0
otsu_maxValue = 0

#for adjust buttons to window---------------------------------
row_count = 0
column_count = 0
count_widgets = 0

#binary morphology-------------------------------------------
erosion_kernel = 0
erosion_iteration = 0

dilation_kernel = 0
dilation_iteration = 0

opening_kernel = 0

closing_kernel = 0

top_hat_kernel = 0

#hough transform--------------------------------------------
min_linelength = 0
max_linegap = 0
hough_threshold = 0

hough_param1 = 0
hough_param2 = 0

#global names ----------------------------------------------
#segmentation
thresh_bin = "Prahování-Bin"
count_of_thresh_bin = len(thresh_bin) #počet písmen ve slově
thresh_bin_inv = "Prahování-Bin,Inv"
count_of_thresh_bin_inv = len(thresh_bin_inv)
thresh_trunc = "Prahování-Zkr"
count_of_thresh_trunc = len(thresh_trunc)
thresh_tozero = "Prahování-Nul"
count_of_thresh_tozero = len(thresh_tozero)
thresh_tozero_inv = "Prahování-Nul,Inv"
count_of_thresh_tozero_inv = len(thresh_tozero_inv)

thresh_mean = "Prahování-Průměr"
count_of_thresh_mean = len(thresh_mean)
thresh_gauss = "Prahování-Gauss"
count_of_thresh_gauss = len(thresh_gauss)

otsu_bin = "Binarizace-Otsu"
count_of_otsu_bin = len(otsu_bin)

#binary morphology-------------------------------------------
erosion = "Eroze"
count_of_erosion = len(erosion)

dilation = "Dilatace"
count_of_dilation = len(dilation)

opening = "Otevření"
count_of_opening = len(opening)

closing = "Uzavření"
count_of_closing = len(closing)

top_hat = "Klobouk"
count_of_top_hat = len(top_hat)

#hough transform-----------------------------------------------
hought_line = "Hough-Přímka"
count_of_hough = len(hought_line)

hought_circle = "Hough-Kružnice"
count_of_houghc = len(hought_circle)

#detection and identification----------------------------------
coloring_areas = "Oblasti"
count_of_coloring_areas = len(coloring_areas)

searching = "Vzory"
count_of_searching = len(searching)

adaboost_haar = "Adaboost,Haar"
count_of_adaboost_haar = len(adaboost_haar)

dlib_temp = "Dlib"
count_of_dlib_temp = len(dlib_temp)

#detection sample/s---------------------------------------------
# ccoeff = "CCOEFf"
ccoeff_normed = "Vzor"
# ccorr = "CCORR"
# ccorr_normed = "CCORR_NORMED"
# sqdiff = "SQDIFF"
# sqdiff_normed = "SQDIFF_NORMED"
template = ""

# ccoeff_len = len(ccoeff)
ccoeff_normed_len = len(ccoeff_normed)
# ccorr_len = len(ccorr)
# ccorr_normed_len = len(ccorr_normed)
# sqdiff_len = len(sqdiff)
# sqdiff_normed_len = len(sqdiff_normed)

multi_ccoeff_normed = "Vzory"
multi_ccoeff_normed_len = len(multi_ccoeff_normed)

#face_recognition----------------------------------------------
face_r_cnn = "FaceR_CNN"
count_of_face_r_cnn = len(face_r_cnn)

face_r_hog = "FaceR_HOG"
count_of_face_r_hog = len(face_r_hog)

dataset = ""


class WrappingLabel(tkinter.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tkinter.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

def load_image_to_panelB(image):
    """
    Loads image into panelB. 
    PanelB is internally set on 400x400 px and color of background is black.
    Parameters
    ----------
    image : image
    """
    global panelB
    global panel_size
    size_width_height = panel_size
    color_of_background = "black"
    image = ImageTk.PhotoImage(image)
    if panelB is None:
        panelB = tkinter.Label(canvas, image=image)
        panelB.config(height = size_width_height, width = size_width_height, bg=color_of_background)
        panelB.image = image
        panelB.pack(side="right", padx=10, pady=10,fill=BOTH, expand=YES)
    else:
        panelB.configure(image=image)
        panelB.image = image
        
def load_image_to_panelB_for_next(image):
    """
    Loads image into panelB. 
    PanelB is internally set on 400x400 px and color of background is black.
    Parameters
    ----------
    image : image
    """
    global panelB
    global panel_size
    size_width_height = panel_size
    color_of_background = "black"
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def warning():
    """
    Messagebox with error for users with information about forgetting to upload a file (ex. user converts image before uploading, etc.).
    """
    messagebox.showerror('Info', 'Žádný soubor nebyl vybrán, prosím vyberte soubor.')

def error_equalization():
    messagebox.showerror('Info', 'Nepodařilo se provést ekvalizaci histogramu.')

def select_image():
    """
    The user can choose an image in .jpg, .png, .bmp. Loads selected image into panelA.
    PanelA is internally set on 400x400 px and color of background is black.
    In case of failure of uploading the image, function warning() is called.
    """
    global panelA, panelB
    global path
    global pathP
    global image_final
    global loaded_panelA, required_size, panel_size
    
    #global previous
    size_width_height = panel_size
    color_of_background = "black"
    try:
        path = tkinter.filedialog.askopenfilename(initialdir="", title="Vybrat obrázek", filetypes=(("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("BMP", "*.bmp"), ("PNG", "*.png")))
        if len(path) > 0:
            if(panelB != None):
                panelB.configure(image=None)
                panelB.image = None
            disable_menu()
            img = cv2.imread(path)
            image = modul_resize.resizing(img, required_size)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            pathP = path
            if panelA is None: 
                panelA = tkinter.Label(canvas, image=image)
                panelA.config(height = size_width_height, width = size_width_height, bg=color_of_background)
                panelA.image = image
                image_final = image
                panelA.pack(side="left", padx=10, pady=10)
                verify_selection_of_file()
            else:
                panelA.configure(image=image)
                panelA.image = image
                verify_selection_of_file()
    except:
        warning() 
        
def zero_parameters():
    global count_widgets, row_count, column_count
    count_widgets = 0
    row_count= 0
    column_count=0
        
def select_image_from_list(path_to_image):
    """
    The user can choose an image in .jpg, .png, .bmp. Loads selected image into panelA.
    PanelA is internally set on 400x400 px and color of background is black.
    In case of failure of uploading the image, function warning() is called.
    """
    global panelA, panelB
    global image_final
    global loaded_panelA
    global path, pathP, required_size, panel_size
    #global previous
    size_width_height = panel_size
    color_of_background = "black"
    if len(path_to_image) > 0:
        if(panelB != None):
            panelB.configure(image=None)
            panelB.image = None
        disable_menu()
        img = cv2.imread(path_to_image)
        image = modul_resize.resizing(img, required_size)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        pathP = path_to_image
        path = path_to_image
        if panelA is None: 
            panelA = tkinter.Label(canvas, image=image)
            panelA.config(height = size_width_height, width = size_width_height, bg=color_of_background)
            panelA.image = image
            image_final = image
            panelA.pack(side="left", padx=10, pady=10)

            verify_selection_of_file()
        else:
            panelA.configure(image=image)
            panelA.image = image
            verify_selection_of_file()

def save_image():
    global file_to_save
    if(panelB != None):
        cv2.imwrite("result.png", file_to_save)
        tkinter.messagebox.showinfo(title="Info", message="Obrázek byl úspěšně uložen do zdrojové složky.")
    else:
        tkinter.messagebox.showerror(title="Chyba", message="Obrázek se nepodařilo uložit. Musíte vybrat soubor a akci.")
        
def clear_last_step():
    global list_of_actions
    global path
    global row_count, column_count, count_widgets
    global panelB
    list = list_of_actions.split("; ")
    n = 0
    button_before = count_widgets - 1
    if len(path) != 0 and count_widgets > 2:
        
        if list[-1] == "":
            list = list[:-1]            
        for widget in bottomframe.winfo_children():
            n = n + 1
            if n == count_widgets or n == button_before:
                widget.destroy()
        list = list[:-1]
        count_widgets = count_widgets - 2
        
        control_rows_cols()
        control_environment() 
        
        list_of_actions = "; ".join(list)
        list_of_actions = list_of_actions + "; "
        text.config(text=list_of_actions)    
        
        if(panelB != None):
            panelB.configure(image=None)
            panelB.image = None

def control_rows_cols():
    global row_count, column_count, count_widgets
    if column_count == 2 or count_widgets % 10 == 0:
        column_count = 10
        if row_count > 0:
            row_count -= 1
    else:
        column_count -= 2

def open_list_of_methods():
    global list_of_actions
    global path
    global path_to_file
    global angles_global,percents_global,correct_global,A_global,M_global,G_global,S_global,C_global
    global numb1, numb2
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv
    global thres_gauss, thres_mean
    global otsu_thresh, otsu_maxValue
    global otsu_bin
    global maxValue, C_constant, blockSize
    global erosion, dilation, opening, closing, top_hat
    global erosin_kernel, erosin_iteration
    global dilation_kernel, dilation_iteration
    global opening_kernel
    global closing_kernel
    global top_hat_kernel
    global hought_line, min_linelength, max_linegap, hough_threshold
    global hought_circle, hough_param1, hough_param2
    global coloring_areas, searching, adaboost_haar, dlib_temp, face_recognition_temp
    global template, ccoeff_normed, multi_ccoeff_normed
    global adaboost_haar, count_of_adaboost_haar
    global dlib_temp, count_of_dlib_temp
    global face_r_cnn, count_of_face_r_cnn, face_r_hog, count_of_face_r_hog, dataset
    hide_all_buttons2()
    
    xml = "list_of_actions.xml"
    tree = ET.parse(xml)
    root = tree.getroot()
    
    methods = dict()
    numbers = dict()
    files = dict() 
    children = root.getchildren()
    loaded = False
    
    for child in children:
        if loaded == False:
            id_first = int(child.get("ID"))
            if id_first == 1:
                name = child.get("Name")
                path = name
                select_image_from_list(name)
                loaded = True
                clear_list_of_actions()
        else:
            word = child.get("Name")
            if word == "RGB2G":
                edit_list_of_actions("RGB2G")
                add_button(btnPrevodDoSede2)
                verify_choose_color_env()
            if word == "R-RGB":
                add_button(btnPrevodDoR2)
                edit_list_of_actions("R-RGB")
                verify_choose_color_env()
            if word == "G-RGB":
                add_button(btnPrevodDoG2)
                edit_list_of_actions("G-RGB")
                verify_choose_color_env()
            if word == "B-RGB":
                add_button(btnPrevodDoB2)
                edit_list_of_actions("B-RGB")
                verify_choose_color_env()
            if word == "Cb-YCbCr":
                add_button(btnPrevodDoCb2)
                edit_list_of_actions("Cb-YCbCr")
                verify_choose_color_env()
            if word == "Cr-YCbCr":
                add_button(btnPrevodDoCr2)
                edit_list_of_actions("Cr-YCbCr")
                verify_choose_color_env()
            if word == "H-HSV":
                 add_button(btnPrevodDoH2)
                 edit_list_of_actions("H-HSV")
                 verify_choose_color_env()
            if word == "S-HSV":
                 add_button(btnPrevodDoS2)
                 edit_list_of_actions("S-HSV")
                 verify_choose_color_env()
            if word == "Rotace":
                 angles_global = int(child.get("Number"))
                 edit_list_of_actions("Rotace " + str(angles_global) + " °")
                 add_button_for_parameters("Rotace")
            if word =="Měřítko":
                 percents_global = int(child.get("Number"))
                 edit_list_of_actions("Měřítko " + str(percents_global) + " %")
                 add_button_for_parameters("Měřítko")
            if word == "Korekce":
                 add_button_for_parameters("Korekce")
                 path_to_file = str(child.get("Temp"))
                 correct_global = int(child.get("Number"))
                 edit_list_of_actions("Korekce " + str(correct_global) + " " + path_to_file)
            if word == "Negativ":
                 add_button(btn_negativ2)
                 edit_list_of_actions("Negativ")
            if word == "Ekvalizace":
                 add_button(btn_equalization2)
                 edit_list_of_actions("Ekvalizace")
            if word == "Fprůměr":
                 A_global = int(child.get("Number"))
                 edit_list_of_actions("Fprůměr " + str(A_global))
                 add_button_for_parameters("Fprůměr")
            if word == "FGauss":
                 F_global = int(child.get("Number"))
                 add_button_for_parameters("FGauss")
                 edit_list_of_actions("FGauss " + str(F_global))
            if word == "Fmedián":
                 M_global=int(child.get("Number"))
                 add_button_for_parameters("Fmedián")
                 edit_list_of_actions("Fmedián " + str(M_global))
            if word == "LaplaceHD":
                 add_button(btn_laplace_edge_detector2)
                 edit_list_of_actions("LaplaceHD")
            if word == "SobelHD":
                 S_global=int(child.get("Number"))
                 add_button_for_parameters("SobelHD")
                 edit_list_of_actions("SobelHD " + str(S_global))
            if word == "CannyHD":
                 C_global=int(child.get("Number"))
                 add_button_for_parameters("CannyHD")
                 edit_list_of_actions("CannyHD " + str(C_global))
                 
            if word == thresh_bin:
                numb1 = int(child.get("Number"))
                numb2 = int(child.get("Temp"))
                xml_final_method(thresh_bin, numb1, numb2)
            if word == thresh_bin_inv:
                numb1 = int(child.get("Number"))
                numb2 = int(child.get("Temp"))
                xml_final_method(thresh_bin_inv, numb1, numb2)
            if word == thresh_trunc:
                numb1 = int(child.get("Number"))
                numb2 = int(child.get("Temp"))
                xml_final_method(thresh_trunc, numb1, numb2)
            if word == thresh_tozero:
                numb1 = int(child.get("Number"))
                numb2 = int(child.get("Temp"))
                xml_final_method(thresh_tozero, numb1, numb2)
            if word == thresh_tozero_inv:
                numb1 = int(child.get("Number"))
                numb2 = int(child.get("Temp"))
                xml_final_method(thresh_tozero_inv, numb1, numb2)
            if word == thresh_mean:
                maxValue = int(child.get("Number"))
                blockSize = int(child.get("Temp"))
                C_constant = int(child.get("Temp2"))
                xml_final_method3(thresh_mean, maxValue, blockSize, C_constant)
            if word == thresh_gauss:
                maxValue = int(child.get("Number"))
                blockSize = int(child.get("Temp"))
                C_constant = int(child.get("Temp2"))
                xml_final_method3(thresh_gauss, maxValue, blockSize, C_constant)
            if word == otsu_bin:
                otsu_thresh = int(child.get("Number"))
                otsu_maxValue = int(child.get("Temp"))
                xml_final_method(otsu_bin, otsu_thresh, otsu_maxValue)
            if word == erosion:
                erosion_kernel = int(child.get("Number"))
                erosion_iteration = int(child.get("Temp"))
                xml_final_method(erosion, erosion_kernel, erosion_iteration)
            if word == dilation:
                dilation_kernel = int(child.get("Number"))
                dilation_iteration = int(child.get("Temp"))
                xml_final_method(dilation, dilation_kernel, dilation_iteration)
            if word == opening:
                opening_kernel = int(child.get("Number"))
                xml_final_method1(opening, opening_kernel)
            if word == closing:
                closing_kernel = int(child.get("Number"))
                xml_final_method1(closing, closing_kernel)
            if word == top_hat:
                top_hat_kernel = int(child.get("Number"))
                xml_final_method1(top_hat, top_hat_kernel)
            if word == hought_line:
                min_linelength = int(child.get("Number"))
                max_linegap = int(child.get("Temp"))
                hough_threshold = int(child.get("Temp2"))
                xml_final_method3(hought_line, min_linelength, max_linegap, hough_threshold)
            if word == hought_circle:
                hough_param1 = int(child.get("Number"))
                hough_param2 = int(child.get("Temp"))
                xml_final_method(hought_circle, hough_param1, hough_param2)
            if word == coloring_areas:
                add_button(btnColoring)
                edit_list_of_actions(coloring_areas)
            if word == ccoeff_normed:
                 add_button(btnSearchingSample)
                 template = str(child.get("Number"))
                 edit_list_of_actions(ccoeff_normed + " " + template)
            if word == multi_ccoeff_normed:
                 add_button(btnSearchingSamples)
                 template = str(child.get("Number"))
                 edit_list_of_actions(multi_ccoeff_normed + " " + template)
            if word == adaboost_haar:
                add_button(btnAdaboostHaar)
                edit_list_of_actions(adaboost_haar)
            if word == dlib_temp:
                add_button(btnDlib)
                edit_list_of_actions(dlib_temp)
            if word == face_r_cnn:
                dataset = str(child.get("Number"))
                add_button(btnCNN)
                edit_list_of_actions(face_r_cnn)
            if word == face_r_hog:
                dataset = str(child.get("Number"))
                add_button(btnHOG)
                edit_list_of_actions(face_r_hog)
                
def xml_final_method3(name_method, n1, n2, n3):
    add_button_for_parameters(name_method)
    edit_list_of_actions(name_method + " " + str(n1) + " " + str(n2) + " " + str(n3))

def xml_final_method(name_method, n1, n2):
    add_button_for_parameters(name_method)
    edit_list_of_actions(name_method + " " + str(n1) + " " + str(n2))

def xml_final_method1(name_method, n1):
    add_button_for_parameters(name_method)
    edit_list_of_actions(name_method + " " + str(n1))

def save_list_of_methods():
    counter = 0
    global list_of_actions
    list_to_save = list_of_actions.split("; ")
    try:
        root = ET.Element("methods")
        for method in list_to_save:
            counter = counter + 1
            if " " in method:
                string = method.split(" ")
                method = string[0]
                number = string[1]
                if len(string) == 3:
                    temp = string[2]
                    method = ET.SubElement(root, "Method", ID=str(counter), Name=method, Number=number, Temp=temp)
                elif len(string) == 4:
                    temp = string[2]
                    temp2 = string[3]
                    method = ET.SubElement(root, "Method", ID=str(counter), Name=method, Number=number, Temp=temp, Temp2=temp2)
                else:
                    method = ET.SubElement(root, "Method", ID=str(counter), Name=method, Number=number)
            else:
                method = ET.SubElement(root, "Method", ID=str(counter), Name=method)
        tree = ET.ElementTree(root)
        tree.write("list_of_actions.xml", pretty_print=True, encoding = "utf-8", xml_declaration=True)
        tkinter.messagebox.showinfo(title="Info", message="Řetězec událostí byl uložen do zdrojové složky.")
    except:
        tkinter.messagebox.showerror(title="Chyba", message="Řetězec událostí se nepodařilo uložit!")
        
def select_file():
    global path_to_file
    path_to_file = tkinter.filedialog.askopenfilename(initialdir="", title="Vybrat obrázek", filetypes=(("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("PNG", "*.png")))

    
def select_template(info, count):
    global template
    template = tkinter.filedialog.askopenfilename(initialdir="", title="Vybrat vzor", filetypes=(("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("PNG", "*.png")))
    if template != "":
        add_init_template(count)
        info.destroy()

def select_dataset():
    global dataset
    dataset = tkinter.filedialog.askopenfilename(initialdir="", title="Vybrat dataset", filetypes=(("PICKLE", "*.pickle"),))


#----------------------------------------------------------GRAY---------------------------------------------        


def convert_to_gray():
    """
    Remembers the last path of image. Calls to_gray(path) - path is given in this function.
    """ 
    try:
        if len(path) > 0:
            to_gray(path)
        else:
            to_gray(pathP)
    except:
        warning()
        
def to_gray(path):
    global required_size
    gray = modul_togray.method_togray(required_size, path)
    last_section_of_methods_sec(gray)
    verify_choose_color_env()
#----------------------------------------------------------RGB----------------------------------------------

def convert_to_rrgb(number):
    """
    Remembers the last path of image. Calls to_rrgb(path, number) - path is given in this function and number
    from choice from user (buttons).
    Parameters
    ----------
    number : int
        Which type of RGB matrix 
    """
    try:
        if len(path) > 0:
            to_rrgb(path, number)
        else:
            to_rrgb(pathP, number)
    except:
        warning()
        

def to_rrgb(path, number): 
    """
    Converts the uploaded imate to rgb (R-RGB, G-RGB, B-RGB). Load_image_to_panelB(img) is called here.
    Parameters
    ----------
    path : string
        The path to file
    number : int
        Which type of RGB matrix
    """
    global required_size
    R = modul_torgb.method_torrgb(required_size, path, number)
    last_section_of_methods_sec(R)
    verify_choose_color_env()
    
#----------------------------------------------------------YCrCb---------------------------------------------

def convert_to_ycbcr(number):
    """
    Remembers the last path of image. Calls to_ycbcr(path, number) - path is given in this function and number
    from choice from user (buttons).
    Parameters
    ----------
    number : int
        Which type of YCrCb matrix
    """
    try:
        if len(path) > 0:
            to_ycbcr(path, number)
        else:
            to_ycbcr(pathP, number)
    except:
        warning()

def to_ycbcr(path, number):  
    """
    Converts the uploaded imate to YCrCb (Cr-YCrCb, Cb-YCrCb). Load_image_to_panelB(img) is called here.
    Parameters
    ----------
    path : string
        The path to file
    number : int
        Which type of YCrCb matrix
    """
    global required_size
    Y = modul_toycbcr.method_toycbcr(required_size, path, number)
    last_section_of_methods_sec(Y)
    verify_choose_color_env()
    
#----------------------------------------------------------HSV-----------------------------------------------

def convert_to_hsv(number):
    """
    Remembers the last path of image. Calls to_hsv(path, number) - path is given in this function and number
    from choice from user (buttons).
    Parameters
    ----------
    number : int
        Which type of HSV matrix
    """
    try:
        if len(path) > 0:
            to_hsv(path, number)
        else:
            to_hsv(pathP, number)
    except:
        warning()

def to_hsv(path, number):   
    """
    Converts the uploaded imate to HSV (H-HSV, S-HSV). Load_image_to_panelB(img) is called here.
    Parameters
    ----------
    path : string
        The path to file
    number : int
        Which type of HSV matrix
    """
    global required_size
    H = modul_tohsv.method_tohsv(required_size, path, number)
    last_section_of_methods_sec(H)
    verify_choose_color_env()

#----------------------------------------------------------ROTATION-------------------------------------------
def rotation():
    """
    Calls input_number() for user's input. Remembers the last path of image. Calls rotate(path, angles) - 
    path is given in this function and angles from input.
    """
    angles = input_number()
    rotate(angles)

def rotate(angles):
    """
    Rotates the uploaded image for required angles. Angles are given from user's input. Load_image_to_panelB(img)
    is called her.
    Parameters
    ----------
    path : string
        The path to file
    angles : int
        How many angles rotates the image
    """
    global previous
    global angles_global
    global angles_etalon
    angles_global = angles
    angles_etalon = angles
    
    rotated = modul_rotate.method_rotate(previous, angles)
    last_section_of_methods_sec(rotated)
    
def rotate_of_etalon(img):
    global angles_etalon
    rotated = modul_rotate.method_rotate(img, angles_etalon)
    angles_etalon = 0
    return rotated
    
#----------------------------------------------------------RESIZE---------------------------------------------

def change_scale():
    """
    Calls input_number() for user's input. Remembers the last path of image. Calls scale(path, percent) - 
    path is given in this function and percent from input.
    """
    global percent
    percent = input_number()
    scale(percent)

def scale(percent):
    """
    Resizes the uploaded image on required percent. Percent is given from user's input. Load_image_to_panelB(img)
    is called her.
    Parameters
    ----------
    path : string
        The path to file
    percent : int
        How many percent resizes the image
    """
    global percents_global
    global percents_etalon
    global previous

    percents_global = percent
    percents_etalon = percent
    res = modul_scale.method_scale(previous, percent)
    last_section_of_methods_sec(res)

def scale_of_etalon(img):
    global percents_etalon

    res = modul_scale.method_scale(img, percents_etalon)
    percents_etalon = 0
    return res
#----------------------------------------------------------CORRECTION-----------------------------------------
    
def correction():
    c = input_number()
    correct(c)

def correct(c):
    global correct_global
    global path_to_file
    global previous
    global file_to_save
    global percents_etalon, angles_etalon
    
    np.seterr(divide='ignore', invalid='ignore')
    correct_global = c
    etalon = cv2.imread(path_to_file)
    etalon = modul_resize.resizing(etalon, required_size)
    
    if percents_etalon != 0:
        etalon = scale_of_etalon(etalon)
    if angles_etalon!= 0:
        etalon = rotate_of_etalon(etalon)
        
    res = modul_correction.method_correct(previous, etalon, c)
   
    last_section_of_methods_sec(res)
    
#----------------------------------------------------------NEGATITON------------------------------------------

def negate():
    global previous
    negative = modul_negate.method_negate(previous)
    last_section_of_methods(negative)

#----------------------------------------------------------EQUALIZATION----------------------------------------
        
def equalize():
    global previous
    try:
        equ = modul_equalize.method_equalize(previous)
        last_section_of_methods(equ)
    except:
        error_equalization()
    
#----------------------------------------------------------FILTERS--------------------------------------------

def filtr(type_of_filter):
    number = input_number()
    
    if type_of_filter == 0:
        averaging(number)
    if type_of_filter == 1:
        gaussian(number)
    if type_of_filter == 2:
        median(number)
    if type_of_filter == 3:
        bilateral(number)
        
def averaging(number):
    global A_global
    global previous
    A_global = number
    blur = modul_average.method_average(previous, number)
    last_section_of_methods(blur)
    
def gaussian(number):
    global previous
    global G_global
    G_global = number
    blur = modul_gaussian.method_gaussian(previous, number)
    last_section_of_methods(blur)
    
def median(number):
    global previous
    global M_global
    M_global = number
    median = modul_median.method_median(previous,number)
    last_section_of_methods(median)
  
#----------------------------------------------------------DETECTOR-------------------------------------------
    
def laplace_edge_detector():
    laplace_detector()
    
def laplace_detector():
    global previous
    img = modul_laplace.method_laplace(previous)
    last_section_of_methods(img)

def sobel_edge_detector():
    number = input_number()
    sobel_detector(number)

def sobel_detector(number):
    global previous
    global S_global
    S_global = number
    origin_number = number
    number = modul_helpers.check_odd(number)
    if number > 31:
        return messagebox.showerror(title="Chyba", message="Číslo musí být menší než 32.")
    sobel = modul_sobel.method_sobel(previous, number)
    last_section_of_methods(sobel)
    
def canny_edge_detector():
    number = input_number()
    canny_detector(number)

def canny_detector(number):
    global C_global
    global previous
    C_global = number
    edges = modul_canny.method_canny(previous, number)
    last_section_of_methods(edges)

#----------------------------------------------------------SEGMENTATION---------------------------------------

def simple_thresholding(n1, n2, method):
    global previous, numb1, numb2
    numb1 = n1
    numb2 = n2
    thresh1 = modul_simple_thres.method_simple_thresh(previous, n1, n2, method)
    last_section_of_methods(thresh1)
    
def adaptive_thresholding(maxV, blockS, C_const, method):
    global maxValue, blockSize, C_constant, previous
    maxValue = maxV
    blockSize = blockS
    C_constant = C_const
    thresh1 = modul_adaptive_thresh.method_adaptive_thresh(previous,maxV, blockS, C_const, method)
    last_section_of_methods(thresh1)
    
def otsu_thresholding(thresh, o_maxValue):
    global otsu_thresh, otsu_maxValue
    otsu_thresh = thresh
    otsu_maxValue = o_maxValue
    thresh1 = modul_otsu_thresh.method_otsu_thresh(previous, thresh, o_maxValue)
    last_section_of_methods(thresh1)
    
#-----------------------------------------------------BINARY MORPHOLOGY---------------------------------------
    
def e_erosion(kernel, iteration):
    global erosion, erosion_kernel, erosion_iteration, previous
    erosion_kernel = kernel
    erosion_iteration = iteration
    erose = modul_erosion.method_erosion(previous, kernel, iteration)
    last_section_of_methods(erose)
    
def d_dilation(kernel, iteration):
    global dilation, dilation_kernel, dilation_iteration, previous
    dilation_kernel = kernel
    dilation_iteration = iteration
    dilate = modul_dilation.method_dilation(previous, kernel, iteration)
    last_section_of_methods(dilate)
    
def o_opening(kernel):
    global opening, opening_kernel, previous
    opening_kernel = kernel
    img = modul_opening.method_opening(previous, kernel)
    last_section_of_methods(img)

def c_closing(kernel):
    global closing, closing_kernel, previous
    closing_kernel = kernel
    img = modul_closing.method_closing(previous, kernel)
    last_section_of_methods(img)

def t_top_hat(kernel):
    global top_hat, top_hat_kernel, previous
    top_hat_kernel = kernel
    img = modul_top_hat.method_top_hat(previous, kernel)
    last_section_of_methods(img)

#----------------------------------------------------------Hough Transormation--------------------------------
    
def h_hought_line(linelength, linegap, threshold_h):
    global min_linelength, max_linegap, hough_threshold, previous
    min_linelength = linelength
    max_linegap = linegap
    hough_threshold = threshold_h
    hough = modul_hough.method_hough_transform(previous, linelength, linegap, hough_threshold)
    last_section_of_methods(hough)

def h_hought_circle(pam1, pam2):
    global hough_param1, hough_param2, previous
    hough_param1 = pam1
    hough_param2 = pam2
    hough = modul_hough.method_hought_circle(previous, pam1, pam2)
    last_section_of_methods(hough)

#----------------------------------------------------------Detection and Identification-----------------------
    
def c_coloring():
    global previous 
    color_img = modul_coloring.method_coloring(previous)
    last_section_of_methods(color_img)
    
def s_searching(method):
    global previous, template, percents_etalon, angles_etalon, required_size

    #np.seterr(divide='ignore', invalid='ignore')
    template_img = cv2.imread(template,0)
    if percents_etalon != 0:
        template_img = scale_of_etalon(template_img)
    if angles_etalon!= 0:
        template_img = rotate_of_etalon(template_img) 
    result_img = modul_searching.method_searching(previous, template_img, method)   
    last_section_of_methods_sec(result_img)
    
def a_adaboost_haar():
    global previous
    np.seterr(divide='ignore', invalid='ignore')
    result_img = modul_adaboost_haar.method_face_recognition(previous)   
    last_section_of_methods_sec(result_img)
    
def d_dlib():
    global previous
    np.seterr(divide='ignore', invalid='ignore')
    result_img = modul_dlib.method_dlib_face_recognition(previous)   
    last_section_of_methods_sec(result_img)
    
def f_face_recognition(method):
    global previous, dataset
    if method == 1:
        result = modul_face_recognition.method_face_recognition(previous, dataset, "cnn")
    if method == 2:
        result = modul_face_recognition.method_face_recognition(previous, dataset, "hog")
    last_section_of_methods_sec(result)
#----------------------------------------------------------Last_section_of_methods----------------------------

def last_section_of_methods(previous_content):
    global previous
    global file_to_save
    previous = previous_content
    result = cv2.cvtColor(previous, cv2.COLOR_RGB2BGR)
    file_to_save = result
    image_res = Image.fromarray(result)
    load_image_to_panelB(image_res)
    
def last_section_of_methods_sec(previous_content):
    global previous
    global file_to_save
    previous = previous_content
    file_to_save = previous_content
    image = Image.fromarray(previous_content)

    load_image_to_panelB(image)
#----------------------------------------------------------GUI------------------------------------------------
    
def hide_all_buttons2():
    for widget in bottomframe.winfo_children():
        widget.destroy()
    zero_parameters()

    
def verify_selection_of_file():
    menubar.entryconfigure("2", state=tkinter.NORMAL)
    
def verify_segmentation_for_detection():
    global list_of_actions
    global count_of_thresh_bin, count_of_thresh_bin_inv, count_of_thresh_trunc, count_of_thresh_tozero, count_of_thresh_tozero_inv, count_of_thresh_mean, count_of_thresh_gauss, count_of_otsu_bin 
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv, thresh_mean, thresh_gauss, otsu_bin 
    list = list_of_actions.split("; ")
    position = 0
    for word in list:
        if word[0:int(count_of_thresh_bin)] == thresh_bin or word[0:int(count_of_thresh_bin_inv)] == thresh_bin_inv:
            detection_env.entryconfigure("1", state=tkinter.NORMAL)
            break
        if word[0:int(count_of_thresh_trunc)] == thresh_trunc or word[0:int(count_of_thresh_tozero)] == thresh_tozero:
            detection_env.entryconfigure("1", state=tkinter.NORMAL)
            break
        if word[0:int(count_of_thresh_tozero_inv)] == thresh_tozero_inv or word[0:int(count_of_thresh_gauss)] == thresh_gauss:
            detection_env.entryconfigure("1", state=tkinter.NORMAL)
            break
        if word[0:int(count_of_thresh_mean)] == thresh_mean or word[0:int(count_of_otsu_bin)] == otsu_bin:
            detection_env.entryconfigure("1", state=tkinter.NORMAL)
            break
        else:
            detection_env.entryconfigure("1", state=tkinter.DISABLED)
    
    
def disable_menu():
    menubar.entryconfigure("2", state=tkinter.DISABLED)
    menubar.entryconfigure("3", state=tkinter.DISABLED)
    menubar.entryconfigure("4", state=tkinter.DISABLED)
    menubar.entryconfigure("5", state=tkinter.DISABLED)
    menubar.entryconfigure("6", state=tkinter.DISABLED)
    menubar.entryconfigure("7", state=tkinter.DISABLED)
    menubar.entryconfigure("8", state=tkinter.DISABLED)
    menubar.entryconfigure("9", state=tkinter.DISABLED)
    menubar.entryconfigure("10", state=tkinter.DISABLED)
    detection_env.entryconfigure("1", state=tkinter.DISABLED)

def verify_choose_color_env():
    menubar.entryconfigure("3", state=tkinter.NORMAL)
    menubar.entryconfigure("4", state=tkinter.NORMAL)
    menubar.entryconfigure("5", state=tkinter.NORMAL)
    menubar.entryconfigure("6", state=tkinter.NORMAL)
    menubar.entryconfigure("7", state=tkinter.NORMAL)
    menubar.entryconfigure("8", state=tkinter.NORMAL)
    menubar.entryconfigure("9", state=tkinter.NORMAL)
    menubar.entryconfigure("10", state=tkinter.NORMAL)
    
def control_environment():
    global count_widgets
    if count_widgets == 2:
        menubar.entryconfigure("3", state=tkinter.DISABLED)
        menubar.entryconfigure("4", state=tkinter.DISABLED)
        menubar.entryconfigure("5", state=tkinter.DISABLED)
        menubar.entryconfigure("6", state=tkinter.DISABLED)
        menubar.entryconfigure("7", state=tkinter.DISABLED)
        menubar.entryconfigure("8", state=tkinter.DISABLED)
        menubar.entryconfigure("9", state=tkinter.DISABLED)
        menubar.entryconfigure("10", state=tkinter.DISABLED)
    
def create_next_filemenu(menu, name, command):
    menu.add_separator()
    menu.add_cascade(label=name, command=command)
        
def edit_list_of_actions(action):
    global list_of_actions
    text.config(text=list_of_actions + action + "; ")
    list_of_actions = list_of_actions + action + "; "
    
def clear_list_of_actions():
    global list_of_actions
    if len(path) != 0:
        list_of_actions = ""
        text.config(text=list_of_actions)   
        hide_all_buttons2()
        add_button(btnVybratSoubor2) 
        edit_list_of_actions(path)
    
def clear_list_of_actions_with_path():
    global list_of_actions
    if len(path) != 0:
        list_of_actions = ""
        text.config(text=list_of_actions)   
        hide_all_buttons2()
        add_button(btnVybratSoubor2)
        edit_list_of_actions(path)
        
def edit_info_about_numbers(text):
    label_number.config(text=text)
    
def add_info_about_numbers():
    global shown
    if shown == False:
        label_number.pack(side="left", padx="0", pady="10")
        shown = True
    else:
        label_number.pack_forget()
        shown = False
        
def add_button(name_of_button):
    global count_widgets
    global column_count, row_count
    check_rows_cols()
    name_of_button().grid(row=row_count, column=column_count, sticky=N+S+E+W, padx = 1, pady = 1)
    column_count += 1
    count_widgets += 1
    add_arrow()

def check_rows_cols():
    global column_count, row_count, count_widgets
    if column_count == 10:
        column_count = 0
        row_count += 1

def add_button_for_parameters(name):
    global column_count
    global count_widgets
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv, thresh_mean, thresh_gauss, otsu_bin
    global erosion, dilation, opening, closing, top_hat
    global erosin_kernel, erosin_iteration
    global dilation_kernel, dilation_iteration
    global opening_kernel
    global closing_kernel
    global top_hat_kernel
    global hought_line, hought_circle
    
    check_rows_cols()
    if name == "Rotace":
        new_button = Button(bottomframe, text="Rotace", command=lambda:[action_for_button("Rotace")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_rotate)
    if name == "Měřítko":
        new_button = Button(bottomframe, text="Měřítko", command=lambda:[action_for_button("Měřítko")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_scale)
    if name == "Korekce":
        new_button = Button(bottomframe, text="Korekce", command=lambda:[action_for_button("Korekce")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_correct)
    if name == "Fprůměr":
        new_button = Button(bottomframe, text="Fprůměr", command= lambda:[action_for_button("Fprůměr")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_ffilter)
    if name == "FGauss":
        new_button = Button(bottomframe, text="FGauss", command= lambda:[action_for_button("FGauss")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_gfilter)
    if name == "Fmedián":
        new_button = Button(bottomframe, text="Fmedián", command= lambda:[action_for_button("Fmedián")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_mfilter)
    if name == "SobelHD":
        new_button = Button(bottomframe, text="SobelHD", command=lambda:[action_for_button("SobelHD")], height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_sdetector)
    if name == "CannyHD":
        new_button = Button(bottomframe, text="CannyHD", command=lambda:[action_for_button("CannyHD")],height = 1, width = 20)
        new_button.bind("<Button-3>",do_popup_cdetector)
    if name == thresh_bin:
        new_button = Button(bottomframe, text=thresh_bin, command=lambda:[action_for_button(thresh_bin)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_bin(event,"thres_bin"))
    if name == thresh_bin_inv:
        new_button = Button(bottomframe, text=thresh_bin_inv, command=lambda:[action_for_button(thresh_bin_inv)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_bin(event,"thres_bin_inv"))
    if name == thresh_trunc:
        new_button = Button(bottomframe, text=thresh_trunc, command=lambda:[action_for_button(thresh_trunc)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_bin(event,"thres_trunc"))
    if name == thresh_tozero:
        new_button = Button(bottomframe, text=thresh_tozero, command=lambda:[action_for_button(thresh_tozero)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_bin(event,"thres_tozero"))
    if name == thresh_tozero_inv:
        new_button = Button(bottomframe, text=thresh_tozero_inv, command=lambda:[action_for_button(thresh_tozero_inv)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_bin(event,"thres_tozero_inv"))
    if name == thresh_gauss:
        new_button = Button(bottomframe, text=thresh_gauss, command=lambda:[action_for_button(thresh_gauss)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_adap(event,"thres_gauss"))
    if name == thresh_mean:
        new_button = Button(bottomframe, text=thresh_mean, command=lambda:[action_for_button(thresh_mean)],height = 1, width = 20)
        new_button.bind("<Button-3>",lambda event: do_popup_thres_adap(event,"thres_mean"))
    if name == otsu_bin:
        new_button = Button(bottomframe, text=otsu_bin, command=lambda:[action_for_button(otsu_bin)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_otsu)
    if name == erosion:
        new_button = Button(bottomframe, text=erosion, command=lambda:[action_for_button(erosion)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_erosion)
    if name == dilation:
        new_button = Button(bottomframe, text=dilation, command=lambda:[action_for_button(dilation)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_dilation)
    if name == opening:
        new_button = Button(bottomframe, text=opening, command=lambda:[action_for_button(opening)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_opening)
    if name == closing:
        new_button = Button(bottomframe, text=closing, command=lambda:[action_for_button(closing)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_closing)
    if name == top_hat:
        new_button = Button(bottomframe, text=top_hat, command=lambda:[action_for_button(top_hat)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_top_hat)
    if name == hought_line:
        new_button = Button(bottomframe, text=hought_line, command=lambda:[action_for_button(hought_line)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_hough)
    if name == hought_circle:
        new_button = Button(bottomframe, text=hought_circle, command=lambda:[action_for_button(hought_circle)],height = 1, width = 20)
        new_button.bind("<Button-3>", do_popup_houghc)
    new_button.grid(row=row_count, column=column_count, sticky=N+S+E+W, padx = 1, pady = 1)

    count_widgets += 1
    column_count += 1
    add_arrow()
            
def add_arrow():
    global column_count
    global count_widgets
    check_rows_cols()

    arrow().grid(row=row_count, column=column_count, sticky=N+S+E+W)
    column_count += 1
    count_widgets += 1
    abst_env.entryconfigure("5", state=tkinter.NORMAL)
    
def action_for_button(name_of_final_method):
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv, thresh_gauss, thresh_mean
    global count_of_thresh_bin, count_of_thresh_bin_inv, count_of_thresh_trunc, count_of_thresh_tozero, count_of_thresh_tozero_inv
    global count_of_thresh_gauss, count_of_thresh_mean
    global maxValue, blockSize, C_constant
    global otsu_maxValue, otsu_thresh, otsu_bin, count_of_otsu_bin
    global list_of_actions
    global previous
    global path
    global path_to_file
    global angles_global,percents_global,correct_global,A_global,M_global,G_global,S_global,C_global
    global numb1, numb2
    global erosion, dilation, opening, closing, top_hat
    global erosin_kernel, erosin_iteration
    global dilation_kernel, dilation_iteration
    global opening_kernel
    global closing_kernel
    global top_hat_kernel
    global count_of_erotion, count_of_dilation, count_of_opening, count_of_closing, count_of_top_hat
    global hought_line, min_linelength, max_linegap, hough_threshold, count_of_hough
    global hought_circle, hough_param1, hough_param2
    global coloring_areas, searching, adaboost_haar, dlib_temp, face_recognition_temp
    global count_of_coloring_areas, count_of_searching, count_of_adaboost_haar, count_of_dlib_temp, count_of_face_recognition_temp
    global template, ccoeff_normed, ccoeff_normed_len, multi_ccoeff_normed, multi_ccoeff_normed_len 
    global adaboost_haar, count_of_adaboost_haar
    global dlib_temp, count_of_dlib_temp
    global face_r_cnn, count_of_face_r_cnn, face_r_hog, count_of_face_r_hog, dataset
    previous = None
    list = ""
    path = ""
    list = list_of_actions.split("; ")
    path = list[0]
    select_image_from_list(list[0])
     
    for word in list:
        if word == "RGB2G":
            convert_to_gray()
        if word == "R-RGB":
            convert_to_rrgb(0)
        if word == "G-RGB":
            convert_to_rrgb(1)
        if word == "B-RGB":
            convert_to_rrgb(2)
        if word == "Cb-YCbCr":
            convert_to_ycbcr(2)
        if word == "Cr-YCbCr":
            convert_to_ycbcr(1)
        if word == "H-HSV":
            convert_to_hsv(0)
        if word == "S-HSV":
            convert_to_hsv(1)
        if word[0:6] == "Rotace":
            rotate(angles_global)
        if word[0:7] =="Měřítko":
            scale(percents_global)
        if word[0:7] == "Korekce":
            correct(correct_global)
        if word == "Negativ":
            negate()
        if word == "Ekvalizace":
            equalize()
        if word[0:7] == "Fprůměr":
            averaging(A_global)
        if word[0:6] == "FGauss":
            gaussian(G_global)
        if word[0:7] == "Fmedián":
            median(M_global)
        if word == "LaplaceHD":
            laplace_detector()
        if word[0:7] == "SobelHD":
            sobel_detector(S_global)
        if word[0:7] == "CannyHD":
            canny_detector(C_global)
        if word[0:int(count_of_thresh_bin)] == thresh_bin:
            simple_thresholding(numb1, numb2, 1)
        if word[0:int(count_of_thresh_bin_inv)] == thresh_bin_inv:
            simple_thresholding(numb1, numb2, 2)
        if word[0:int(count_of_thresh_trunc)] == thresh_trunc:
            simple_thresholding(numb1, numb2, 3)
        if word[0:int(count_of_thresh_tozero)] == thresh_tozero:
            simple_thresholding(numb1, numb2, 4)
        if word[0:int(count_of_thresh_tozero_inv)] == thresh_tozero_inv:
            simple_thresholding(numb1, numb2, 5)
        if word[0:int(count_of_thresh_gauss)] == thresh_gauss:
            adaptive_thresholding(maxValue, blockSize, C_constant, 1)
        if word[0:int(count_of_thresh_mean)] == thresh_mean:
            adaptive_thresholding(maxValue, blockSize, C_constant, 2)
        if word[0:int(count_of_otsu_bin)] == otsu_bin:
            otsu_thresholding(otsu_thresh, otsu_maxValue)
        if word[0:int(count_of_erosion)] == erosion:
            e_erosion(erosion_kernel, erosion_iteration)
        if word[0:int(count_of_dilation)] == dilation:
            d_dilation(dilation_kernel, dilation_iteration)
        if word[0:int(count_of_opening)] == opening:
            o_opening(opening_kernel)
        if word[0:int(count_of_closing)] == closing:
            c_closing(closing_kernel)
        if word[0:int(count_of_top_hat)] == top_hat:
            t_top_hat(top_hat_kernel)
        if word[0:int(count_of_hough)] == hought_line:
            try:
                h_hought_line(min_linelength, max_linegap, hough_threshold)
            except:
                messagebox.showerror("Info", "Nepodařilo se provést HF pro přímky s těmito parametry.")
                clear_last_step()
        if word[0:int(count_of_houghc)] == hought_circle:
            try:
                h_hought_circle(hough_param1, hough_param2)
            except:
                messagebox.showerror("Info", "Nepodařilo se provést HF pro kružnice s těmito parametry.")
                clear_last_step()
        if word == coloring_areas:
            c_coloring()
        if word[0:int(ccoeff_normed_len)] == ccoeff_normed:
            s_searching(1)
        if word[0:int(multi_ccoeff_normed_len)] == multi_ccoeff_normed:
            s_searching(2)
        if word[0:int(count_of_adaboost_haar)] == adaboost_haar:
            try:
                a_adaboost_haar()
            except:
                messagebox.showerror("Info", "Nepodařilo se provést detekci obličeje.")
                clear_last_step()
        if word[0:int(count_of_dlib_temp)] == dlib_temp:
            try:
                d_dlib()
            except:
                messagebox.showerror("Info", "Nepodařilo se provést detekci obličeje.")
                clear_last_step()
        if word[0:int(count_of_face_r_cnn)] == face_r_cnn:
            try:
                f_face_recognition(1)
            except:
                messagebox.showerror("Info", "Nepodařilo se provést rozpoznání obličeje.")
                clear_last_step()
        if word[0:int(count_of_face_r_hog)] == face_r_hog:
            try:
                f_face_recognition(2)
            except:
                messagebox.showerror("Info", "Nepodařilo se provést rozpoznání obličeje.")
                clear_last_step()
        if word[0:3] == name_of_final_method[0:3]:
            return

def init_param(description):
    s = simpledialog.askinteger("Úprava parametrů", description)
    return s

def do_popup_rotate(event): 
    #vyskakovaci okno pro pravé tlačítko myši
    global angles_global
    s = init_param("Zadejte úhel otočení (ve stupních): ")
    if s == None:
        s = angles_global
    angles_global = s
    update_list_of_actions("rotate")
    
def do_popup_scale(event): 
    global percents_global
    s = init_param("Zadejte změnu měřítka (v procentech): ")
    if s == None:
        s = percents_global
    percents_global = s
    update_list_of_actions("scale")
    
def do_popup_correct(event): 
    global correct_global
    s = init_param("Zadejte velikost korekce: ")
    if s == None:
        s = correct_global
    correct_global = s
    update_list_of_actions("correct")

def do_popup_ffilter(event): 
    global A_global
    s = init_param("Zadejte velikost jádra: (Ideální rozsah: 1 - 100.)")
    if s == None:
        s = A_global
    A_global = s
    update_list_of_actions("ffilter")

def do_popup_gfilter(event): 
    global G_global
    s = init_param("Zadejte velikost jádra: ")
    if s == None:
        s = G_global
    G_global = s
    update_list_of_actions("gfilter")

def do_popup_mfilter(event): 
    global M_global
    s = init_param("Zadejte velikost jádra: (Zadávejte nejlépe lichá celá čísla (0 - 255).)")
    if s == None:
        s = M_global
    M_global = s
    update_list_of_actions("mfilter")
    
def do_popup_sdetector(event): 
    global S_global
    s = init_param("Zadejte velikost jádra: (Zadávejte nejlépe lichá celá čísla (0 - 31).)")
    if s == None:
        s = S_global
    S_global = s
    update_list_of_actions("sdetector")

def do_popup_cdetector(event): 
    global C_global
    s = init_param("Zadejte velikost jádra: ")
    if s == None:
        s = C_global
    C_global = s
    update_list_of_actions("cdetector")

def do_popup_thres_bin(event, method):
    global numb1, numb2
    info = Toplevel()  
    info.geometry("850x100")
    info.title('Zadejte prahy: ')
    
    label_numb1 = Label(info, text="Prah 1: ").pack(side="left", padx="10", pady="1")
    textbox_numb1 = Entry(info)
    textbox_numb1.pack(side="left", padx="10", pady="1")
    label_numb2 = Label(info, text="Prah 2: ").pack(side="left", padx="10", pady="1")
    textbox_numb2 = Entry(info)
    textbox_numb2.pack(side="left", padx="10", pady="1")
    textbox_numb1.insert(numb1, str(numb1)) 
    textbox_numb2.insert(numb2, str(numb2)) 
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs(textbox_numb1, textbox_numb2, method), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs(textbox_numb1, textbox_numb2, method):
    global numb1, numb2
    number1 = textbox_numb1.get()
    number2 = textbox_numb2.get()
    if number1 != None and number2 != None:
        numb1 = int(number1)
        numb2 = int(number2)
        update_list_of_actions(method)

def do_popup_thres_adap(event, method):
    global maxValue, blockSize, C_constant
    info = Toplevel()  
    info.geometry("950x100")
    info.title('Úprava parametrů: ')
    
    label_maxValue = Label(info, text="Max. velikost: ").pack(side="left", padx="10", pady="1")
    textbox_maxValue = Entry(info)
    textbox_maxValue.pack(side="left", padx="10", pady="1")
    label_blockSize = Label(info, text="Velikost bloku: ").pack(side="left", padx="10", pady="1")
    textbox_blockSize = Entry(info)
    textbox_blockSize.pack(side="left", padx="10", pady="1")
    label_C_constant = Label(info, text="Velikost konstanty: ").pack(side="left", padx="10", pady="1")
    textbox_C_constant = Entry(info)
    textbox_C_constant.pack(side="left", padx="10", pady="1")
    
    textbox_maxValue.insert(maxValue, str(maxValue)) 
    textbox_blockSize.insert(blockSize, str(blockSize)) 
    textbox_C_constant.insert(C_constant, str(C_constant)) 
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_adap(textbox_maxValue, textbox_blockSize, textbox_C_constant, method), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
  
def check_numbs_adap(textbox_n1, textbox_n2, textbox_n3, method):
    global maxValue, blockSize, C_constant
    number1 = textbox_n1.get()
    number2 = textbox_n2.get()
    number3 = textbox_n3.get()
    if number1 != None and number2 != None and number3 != None:
        maxValue = int(number1)
        blockSize = int(number2)
        C_constant = int(number3)
        update_list_of_actions(method)

def do_popup_otsu(event):
    global otsu_thresh, otsu_bin
    info = Toplevel()  
    info.geometry("850x100")
    info.title('Úprava parametrů: ')
    
    label_numb1 = Label(info, text="Prah: ").pack(side="left", padx="10", pady="1")
    textbox_numb1 = Entry(info)
    textbox_numb1.pack(side="left", padx="10", pady="1")
    label_numb2 = Label(info, text="Max. velikost: ").pack(side="left", padx="10", pady="1")
    textbox_numb2 = Entry(info)
    textbox_numb2.pack(side="left", padx="10", pady="1")
    textbox_numb1.insert(otsu_thresh, str(otsu_thresh)) 
    textbox_numb2.insert(otsu_maxValue, str(otsu_maxValue)) 
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_otsu(textbox_numb1, textbox_numb2), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
   
def check_numbs_otsu(textbox_numb1, textbox_numb2):
    global otsu_thresh, otsu_maxValue
    number1 = textbox_numb1.get()
    number2 = textbox_numb2.get()
    if number1 != None and number2 != None:
        otsu_thresh = int(number1)
        otsu_maxValue = int(number2)
        update_list_of_actions("otsu")

def do_popup_erosion(event):
    global erosion_kernel, erosion_iteration
    info = Toplevel()  
    info.geometry("800x100")
    info.title('Zadejte parametry: ')
    
    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    label_iteration = Label(info, text="Počet iterací: ").pack(side="left", padx="10", pady="1")
    textbox_iteration = Entry(info)
    textbox_iteration.pack(side="left", padx="10", pady="1")
    textbox_kernel.insert(erosion_kernel, str(erosion_kernel)) 
    textbox_iteration.insert(erosion_iteration, str(erosion_iteration)) 
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_erosion(textbox_kernel, textbox_iteration), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs_erosion(textbox_numb1, textbox_numb2):
    global erosion_kernel, erosion_iteration
    number1 = textbox_numb1.get()
    number2 = textbox_numb2.get()
    if number1 != None and number2 != None:
        erosion_kernel = int(number1)
        erosion_iteration = int(number2)
        update_list_of_actions("erosion")
        
def do_popup_dilation(event):
    global dilation_kernel, dilation_iteration
    info = Toplevel()  
    info.geometry("800x100")
    info.title('Zadejte parametry: ')
    
    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    label_iteration = Label(info, text="Počet iterací: ").pack(side="left", padx="10", pady="1")
    textbox_iteration = Entry(info)
    textbox_iteration.pack(side="left", padx="10", pady="1")
    textbox_kernel.insert(dilation_kernel, str(dilation_kernel)) 
    textbox_iteration.insert(dilation_iteration, str(dilation_iteration)) 
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_dilation(textbox_kernel, textbox_iteration), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs_dilation(textbox_numb1, textbox_numb2):
    global dilation_kernel, dilation_iteration
    number1 = textbox_numb1.get()
    number2 = textbox_numb2.get()
    if number1 != None and number2 != None:
        dilation_kernel = int(number1)
        dilation_iteration = int(number2)
        update_list_of_actions("dilation")
        
def do_popup_opening(event):
    global opening_kernel
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')
    
    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    
    textbox_kernel.insert(opening_kernel, str(opening_kernel))
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_opening(textbox_kernel), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs_opening(textbox_numb1):
    global opening_kernel
    number1 = textbox_numb1.get()
    if number1 != None:
        opening_kernel = int(number1)
        update_list_of_actions("opening")

def do_popup_closing(event):
    global closing_kernel
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')
    
    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    
    textbox_kernel.insert(closing_kernel, str(closing_kernel))
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_closing(textbox_kernel), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs_closing(textbox_numb1):
    global closing_kernel
    number1 = textbox_numb1.get()
    if number1 != None:
        closing_kernel = int(number1)
        update_list_of_actions("closing")

def do_popup_top_hat(event):
    global top_hat_kernel
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')
    
    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    
    textbox_kernel.insert(top_hat_kernel, str(top_hat_kernel))
    
    ok_button = Button(info, text = "OK", command= lambda: [check_numbs_top_hat(textbox_kernel), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command= lambda:[info.destroy(), clear_last_step()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numbs_top_hat(textbox_numb1):
    global top_hat_kernel
    number1 = textbox_numb1.get()
    if number1 != None:
        top_hat_kernel = int(number1)
        update_list_of_actions("tophat")

def do_popup_hough(event):
    info = Toplevel()  
    info.geometry("1100x100")
    info.title('Zadejte parametry: ')
    label_info = Label(info, text="Min. délka přímky:").pack(side="left", padx="10", pady="1")
    textbox1 = Entry(info)
    textbox1.pack(side="left", padx="10", pady="1")
    textbox1.insert(min_linelength, str(min_linelength)) 
    
    label_info2 = Label(info, text="Max. délka mezery:").pack(side="left", padx="10", pady="1")
    textbox2 = Entry(info)
    textbox2.pack(side="left", padx="10", pady="1")
    textbox2.insert(max_linegap, str(max_linegap))
    
    label_info3 = Label(info, text="Prahování:").pack(side="left", padx="10", pady="1")
    textbox3 = Entry(info)
    textbox3.pack(side="left", padx="10", pady="1")
    textbox3.insert(hough_threshold, str(hough_threshold))
    
    button_ok = Button(info, text='OK', command=lambda:[check_hough_line_pop(textbox1, textbox2, textbox3), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")

    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_hough_line_pop(t1, t2, t3):
    global min_linelength, max_linegap, hough_threshold
    number1 = t1.get()
    number2 = t2.get()
    number3 = t3.get()
    if number1 != None and number2 != None and number3 != None:
        min_linelength = int(number1)
        max_linegap = int(number2)
        hough_threshold = int(number3)
        update_list_of_actions("hough")
 
def do_popup_houghc(event):
    info = Toplevel()  
    info.geometry("900x100")
    info.title('Zadejte parametry: ')
    label_info = Label(info, text="Parametr 1:").pack(side="left", padx="10", pady="1")
    textbox1 = Entry(info)
    textbox1.pack(side="left", padx="10", pady="1")
    textbox1.insert(hough_param1, str(hough_param1)) 
    
    label_info2 = Label(info, text="Parametr 2:").pack(side="left", padx="10", pady="1")
    textbox2 = Entry(info)
    textbox2.pack(side="left", padx="10", pady="1")
    textbox2.insert(hough_param2, str(hough_param2))
    
    
    button_ok = Button(info, text='OK', command=lambda:[check_hough_circle_pop(textbox1, textbox2), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")

    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_hough_circle_pop(t1, t2):
    global hough_param1, hough_param2
    number1 = t1.get()
    number2 = t2.get()
    if number1 != None and number2 != None:
        hough_param1 = int(number1)
        hough_param2 = int(number2)
        update_list_of_actions("houghc")
    

def update_list_of_actions(apply):
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv, thresh_gauss, thresh_mean
    global count_of_thresh_bin, count_of_thresh_bin_inv, count_of_thresh_trunc, count_of_thresh_tozero, count_of_thresh_tozero_inv
    global count_of_thresh_gauss, count_of_thresh_mean
    global list_of_actions
    global angles_global
    global correct_global
    global percents_global
    global path_to_file #etalon - path to file
    global A_global, G_global, M_global, S_global, C_global
    global numb1, numb2
    global maxValue, blockSize, C_constant
    global otsu_bin, count_of_otsu_bin, otsu_thresh, otsu_maxValue
    global erosion, dilation, opening, closing, top_hat
    global erosin_kernel, erosin_iteration
    global dilation_kernel, dilation_iteration
    global opening_kernel
    global closing_kernel
    global top_hat_kernel
    global count_of_erotion, count_of_dilation, count_of_opening, count_of_closing, count_of_top_hat
    global hought_line, min_linelength, max_linegap, hough_threshold, count_of_hough
    global hought_circle, hough_param1, hough_param2

    list_of_actions = list_of_actions.split("; ")
    position = 0
    for word in list_of_actions:
        if apply == "rotate" and word[0:6] == "Rotace":
            word = "Rotace " + str(angles_global) + " °"
            list_of_actions[position] = word
        if apply == "scale" and word[0:7] =="Měřítko":
            word = "Měřítko " + str(percents_global) + " %"
            list_of_actions[position] = word
        if apply == "correct" and word[0:7] == "Korekce":
            word = "Korekce " + str(correct_global) + " " + path_to_file
            list_of_actions[position] = word
        if apply == "ffilter" and word[0:7] == "Fprůměr":
            word = "Fprůměr " + str(A_global)
            list_of_actions[position] = word
        if apply == "gfilter" and word[0:6] == "FGauss":
            word = "FGauss " + str(G_global)
            list_of_actions[position] = word
        if apply == "mfilter" and word[0:7] == "Fmedián":
            word = "Fmedián " + str(M_global)
            list_of_actions[position] = word
        if apply == "sdetector" and word[0:7] == "SobelHD":
            word = "SobelHD " + str(S_global)
            list_of_actions[position] = word
        if apply == "cdetector" and word[0:7] == "CannyHD":
            word = "CannyHD " + str(C_global)
            list_of_actions[position] = word  
        if apply == "thres_bin" and word[0:count_of_thresh_bin] == thresh_bin:
            word = thresh_bin + " " + str(numb1) + " " + str(numb2)
            list_of_actions[position] = word
        if apply == "thres_bin_inv" and word[0:count_of_thresh_bin_inv] == thresh_bin_inv:
            word = thresh_bin_inv + " " + str(numb1) + " " + str(numb2)
            list_of_actions[position] = word
        if apply == "thres_trunc" and word[0:count_of_thresh_trunc] == thresh_trunc:
            word = thresh_trunc + " " + str(numb1) + " " + str(numb2)
            list_of_actions[position] = word
        if apply == "thres_tozero" and word[0:count_of_thresh_tozero] == thresh_tozero:
            word = thresh_tozero + " " + str(numb1) + " " + str(numb2)
            list_of_actions[position] = word
        if apply == "thres_tozero_inv" and word[0:count_of_thresh_tozero_inv] == thresh_tozero_inv:
            word = thresh_tozero_inv + " " + str(numb1) + " " + str(numb2)
            list_of_actions[position] = word
        if apply == "thres_gauss" and word[0:count_of_thresh_gauss] == thresh_gauss:
            word = thresh_gauss + " " + str(maxValue) + " " + str(blockSize) + " " + str(C_constant)
            list_of_actions[position] = word
        if apply == "thres_mean" and word[0:count_of_thresh_mean] == thresh_mean:
            word = thresh_mean + " " + str(maxValue) + " " + str(blockSize) + " " + str(C_constant)
            list_of_actions[position] = word
        if apply == "otsu" and word[0:count_of_otsu_bin] == otsu_bin:
            word = otsu_bin + " " + str(otsu_thresh) + " " + str(otsu_maxValue)
            list_of_actions[position] = word
        if apply == "erosion" and word[0:count_of_erosion] == erosion:
            word = erosion + " " + str(erosion_kernel) + " " + str(erosion_iteration)
            list_of_actions[position] = word
        if apply == "dilation" and word[0:count_of_dilation] == dilation:
            word = dilation + " " + str(dilation_kernel) + " " + str(dilation_iteration)
            list_of_actions[position] = word
        if apply == "opening" and word[0:count_of_opening] == opening:
            word = opening + " " + str(opening_kernel)
            list_of_actions[position] = word
        if apply == "closing" and word[0:count_of_closing] == closing:
            word = closing + " " + str(closing_kernel)
            list_of_actions[position] = word
        if apply == "tophat" and word[0:count_of_top_hat] == top_hat:
            word = top_hat + " " + str(top_hat_kernel)
            list_of_actions[position] = word
        if apply == "hough" and word[0:count_of_hough] == hought_line:
            word = hought_line + " " + str(min_linelength) + " " + str(max_linegap) + " " + str(hough_threshold)
            list_of_actions[position] = word
        if apply == "houghc" and word[0:count_of_houghc] == hought_circle:
            word = hought_circle + " " + str(hough_param1) + " " + str(hough_param2)
            list_of_actions[position] = word

        position = position + 1
    list_of_actions = "; ".join(list_of_actions)
    text.config(text=list_of_actions)    

def init_choosing_hsv():
    info = Toplevel()
    info.title('Vyberte barevné prostředí')
    info.geometry("500x100")
    button_rrgb = Button(info, text="H-HSV", command=lambda:[add_button(btnPrevodDoH2),edit_list_of_actions("H-HSV"),verify_choose_color_env(), action_for_button("H-HSV"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    button_grgb = Button(info, text="S-HSV", command=lambda:[add_button(btnPrevodDoS2),edit_list_of_actions("S-HSV"),verify_choose_color_env(), action_for_button("S-HSV"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=clear_last_step, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    info.mainloop()

def init_choosing_ycbcr():
    info = Toplevel()
    info.title('Vyberte barevné prostředí')
    info.geometry("500x100")
    button_rrgb = Button(info, text='Cb-YCbCr', command=lambda:[add_button(btnPrevodDoCb2),edit_list_of_actions("Cb-YCbCr"),verify_choose_color_env(), action_for_button("Cb-YCbCr"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    button_grgb = Button(info, text='Cr-YCbCr', command=lambda:[add_button(btnPrevodDoCr2),edit_list_of_actions("Cr-YCbCr"),verify_choose_color_env(), action_for_button("Cr-YCbCr"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    info.mainloop()


def init_choosing_rgb():
    info = Toplevel()
    info.title('Vyberte barevné prostředí')
    info.geometry("680x100")
    button_rrgb = Button(info, text='R-RGB', command=lambda:[add_button(btnPrevodDoR2),edit_list_of_actions("R-RGB"),verify_choose_color_env(), action_for_button("R-RGB"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    button_grgb = Button(info, text='G-RGB', command=lambda:[add_button(btnPrevodDoG2),edit_list_of_actions("G-RGB"),verify_choose_color_env(), action_for_button("G-RGB"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    button_brgb = Button(info, text='B-RGB', command=lambda:[add_button(btnPrevodDoB2),edit_list_of_actions("B-RGB"),verify_choose_color_env(), action_for_button("B-RGB"), info.destroy()], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    info.mainloop()

def init_rotate(): 
    global angles_global
    s = simpledialog.askinteger("Rotace", "Zadejte úhel otočení (ve stupních): ")
    if s != None:
        angles_global = s    
        add_button_for_parameters("Rotace")
        edit_list_of_actions("Rotace " + str(s) + " °")
        action_for_button("Rotace")
        
def init_scale(): 
    global percents_global    
    s = simpledialog.askinteger("Měřítko", "Zadejte změnu měřítka (v procentech): ")
    if s != None:
        percents_global = s    
        add_button_for_parameters("Měřítko")
        edit_list_of_actions("Měřítko " + str(s) + " %")
        action_for_button("Měřítko")

def init_correction():
    global path_to_file, correct_global
    info = Toplevel()  
    info.geometry("850x100")
    textbox_input = Entry(info) 
    info.title('Vyberte etalon a korekci:')
    
    button_choose_file= Button(info, text="Vybrat etalon", command= lambda:[select_file(), check_select_file(info)], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    textbox_input.pack(side="left", padx="10", pady="1")
    
    ok_button = Button(info, text = "OK", command= lambda: [check_entry(info, textbox_input), add_init_correction(), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    textbox_input.insert(0, "0") 
    raise_above_all(info)
   
def check_select_file(info):
    global path_to_file
    if path_to_file != "":
        label_file_choose = Label(info, text="Etalon byl vybrán.", fg="green").pack(side="left", padx="10", pady="1")

def check_entry(info,textbox_input):
    global path_to_file, correct_global
    number = textbox_input.get()
    if number != None:
        correct_global = int(number)

def add_init_correction():
    global path_to_file, correct_global
    if correct_global != None and path_to_file != "":
        add_button_for_parameters("Korekce")
        edit_list_of_actions("Korekce " + str(correct_global) + " " + path_to_file)   
        action_for_button("Korekce")

def init_average_filter():
    global A_global
    s = simpledialog.askinteger("Fprůměr", "Zadejte velikost jádra: (Ideální rozsah: 1 - 100.)")
    if s != None:
        A_global = s    
        add_button_for_parameters("Fprůměr")
        edit_list_of_actions("Fprůměr " + str(s))
        action_for_button("Fprůměr")

def init_FGauss():
    global G_global
    s = simpledialog.askinteger("FGauss", "Zadejte velikost jádra: ")
    if s != None:
        G_global = s    
        add_button_for_parameters("FGauss")
        edit_list_of_actions("FGauss " + str(s))
        action_for_button("FGauss")

def init_Fmedian():
    global M_global
    s = simpledialog.askinteger("Fmedián", "Zadejte velikost jádra: (Zadávejte nejlépe lichá celá čísla (0 - 255).)")
    if s != None:
        M_global = s    
        add_button_for_parameters("Fmedián")
        edit_list_of_actions("Fmedián " + str(s))
        action_for_button("Fmedián")
    
def init_sobel():
    global S_global
    s = simpledialog.askinteger("SobelHD", "Zadejte velikost jádra: (Zadávejte nejlépe lichá celá čísla (0 - 31).)")
    if s != None:
        S_global = s    
        add_button_for_parameters("SobelHD")
        edit_list_of_actions("SobelHD " + str(s))
        action_for_button("SobelHD")
    
def init_canny():
    global C_global
    s = simpledialog.askinteger("CannyHD", "Zadejte velikost jádra: ")
    if s != None:   
        C_global = s    
        add_button_for_parameters("CannyHD")
        edit_list_of_actions("CannyHD " + str(s))
        action_for_button("CannyHD")

def init_simple_thresholding():
    global numb1, numb2
    info = Toplevel()  
    info.geometry("700x150")
    info.title('Zadejte prahy: ')

    label_numb1 = Label(info, text="Prah 1: ").pack(side="left", padx="10", pady="1")
    textbox_numb1 = Entry(info)
    textbox_numb1.pack(side="left", padx="10", pady="1")
    label_numb2 = Label(info, text="Prah 2: ").pack(side="left", padx="10", pady="1")
    textbox_numb2 = Entry(info)
    textbox_numb2.pack(side="left", padx="10", pady="1")

    textbox_numb1.insert(127, "127") 
    textbox_numb2.insert(255, "255") 
    
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="bottom", pady=3)
    button_tozero = Button(info, text='Nultý', command=lambda:[check_numb(textbox_numb1, textbox_numb2, 4), verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    button_trunc = Button(info, text='Zkrácený', command=lambda:[check_numb(textbox_numb1, textbox_numb2, 3), verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    button_bin_inv = Button(info, text='Binární inverzní', command=lambda:[check_numb(textbox_numb1, textbox_numb2, 2), verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    button_bin = Button(info, text='Binární', command=lambda:[check_numb(textbox_numb1, textbox_numb2, 1), verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    #button_tozero_inv = Button(info, text='Nultý inverzní', command=lambda:[check_numb(textbox_numb1, textbox_numb2, 5), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    #ok_button = Button(info, text = "OK", command= lambda: [check_numb(textbox_numb1, textbox_numb2), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="bottom")

def check_numb(textbox1, textbox2, method):
    global numb1, numb2
    global thresh_bin, thresh_bin_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv
    number = textbox1.get()
    number2 = textbox2.get()
    if number != None and number2 != None:
        numb1 = int(number)
        numb2 = int(number2)
        if method == 1:
            add_button_for_parameters(thresh_bin)
            edit_list_of_actions(thresh_bin + " " + str(number) + " " + str(number2))   
            action_for_button(thresh_bin)
        if method == 2:
           add_button_for_parameters(thresh_bin_inv)
           edit_list_of_actions(thresh_bin_inv + " " + str(number) + " " + str(number2))   
           action_for_button(thresh_bin_inv)
        if method == 3:
           add_button_for_parameters(thresh_trunc)
           edit_list_of_actions(thresh_trunc + " " + str(number) + " " + str(number2))   
           action_for_button(thresh_trunc) 
        if method == 4:
           add_button_for_parameters(thresh_tozero)
           edit_list_of_actions(thresh_tozero + " " + str(number) + " " + str(number2))   
           action_for_button(thresh_tozero) 
        if method == 5:
           add_button_for_parameters(thresh_tozero_inv)
           edit_list_of_actions(thresh_tozero_inv + " " + str(number) + " " + str(number2))   
           action_for_button(thresh_tozero_inv) 

def init_adaptive_thresholding():
    global maxValue, blockSize, C_constant
    info = Toplevel()  
    info.geometry("900x100")
    info.title('Zadejte parametry: ')

    label_maxValue = Label(info, text="Max. hodnota: ").pack(side="left", padx="10", pady="1")
    textbox_maxValue = Entry(info)
    textbox_maxValue.pack(side="left", padx="10", pady="1")
    label_blockSize = Label(info, text="Velikost bloku: ").pack(side="left", padx="10", pady="1")
    textbox_blockSize = Entry(info)
    textbox_blockSize.pack(side="left", padx="10", pady="1")
    label_C_constant = Label(info, text="Konstanta: ").pack(side="left", padx="10", pady="1")
    textbox_C_constant = Entry(info)
    textbox_C_constant.pack(side="left", padx="10", pady="1")

    textbox_maxValue.insert(255, "255") 
    textbox_blockSize.insert(11, "11") 
    textbox_C_constant.insert(2, "2")
    
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="bottom", pady=3)
    button_gauss = Button(info, text='Gaussovo', command=lambda:[check_numb_adaptive(textbox_maxValue, textbox_blockSize, textbox_C_constant, 1),verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")
    button_average = Button(info, text='Průměrné', command=lambda:[check_numb_adaptive(textbox_maxValue, textbox_blockSize, textbox_C_constant, 2), verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="bottom", pady="1")

def check_numb_adaptive(textbox_maxValue, textbox_blockSize, textbox_C_const, method):
    global maxValue, blockSize, C_constant
    global thresh_mean, thresh_gauss
   
    number = textbox_maxValue.get()
    number2 = textbox_blockSize.get()
    number3 = textbox_C_const.get()
    if number != None and number2 != None:
        maxValue = int(number)
        blockSize = int(number2)
        C_constant = int(number3)
        if method == 1:
            add_button_for_parameters(thresh_gauss)
            edit_list_of_actions(thresh_gauss + " " + str(number) + " " + str(number2) + " " + str(number3))   
            action_for_button(thresh_gauss)
        if method == 2:
           add_button_for_parameters(thresh_mean)
           edit_list_of_actions(thresh_mean + " " + str(number) + " " + str(number2) + " " + str(number3))   
           action_for_button(thresh_mean)
           
def init_otsu():
    global otsu_thresh, otsu_maxValue
    info = Toplevel()  
    info.geometry("850x100")
    info.title('Zadejte prahy: ')

    label_thresh = Label(info, text="Prah: ").pack(side="left", padx="10", pady="1")
    textbox_thresh = Entry(info)
    textbox_thresh.pack(side="left", padx="10", pady="1")
    label_maxValue = Label(info, text="Max. hodnota: ").pack(side="left", padx="10", pady="1")
    textbox_maxValue = Entry(info)
    textbox_maxValue.pack(side="left", padx="10", pady="1")

    textbox_thresh.insert(0, "0") 
    textbox_maxValue.insert(255, "255") 
    
    button_otsu = Button(info, text='OK', command=lambda:[check_numb_otsu(textbox_thresh, textbox_maxValue),verify_segmentation_for_detection(),info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numb_otsu(text1, text2):
    global otsu_thresh, otsu_maxValue
    global otsu_bin, count_of_otsu_bin
    number = text1.get()
    number2 = text2.get()
    if number != None and number2 != None:
        otsu_thresh = int(number)
        otsu_maxValue = int(number2)
        do_final_actions_from_init(otsu_bin, number, number2)

def init_erosion():
    global erosion_kernel, erosion_iteration
    info = Toplevel()  
    info.geometry("800x100")
    info.title('Zadejte parametry: ')

    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    label_iteration = Label(info, text="Iterace: ").pack(side="left", padx="10", pady="1")
    textbox_iteration = Entry(info)
    textbox_iteration.pack(side="left", padx="10", pady="1")

    textbox_kernel.insert(5, "5") 
    textbox_iteration.insert(5, "5") 
    
    button_ok = Button(info, text='OK', command=lambda:[check_numb_erosion(textbox_kernel, textbox_iteration), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
def check_numb_erosion(text1, text2):
    global erosion_kernel, erosion_iteration
    global erosion
    number = text1.get()
    number2 = text2.get()
    if number != None and number2 != None:
        erosion_kernel = int(number)
        erosion_iteration = int(number2)
        do_final_actions_from_init(erosion, number, number2)

def init_dilation():
    global dilation_kernel, dilation_iteration
    info = Toplevel()  
    info.geometry("800x100")
    info.title('Zadejte parametry: ')

    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    label_iteration = Label(info, text="Iterace: ").pack(side="left", padx="10", pady="1")
    textbox_iteration = Entry(info)
    textbox_iteration.pack(side="left", padx="10", pady="1")

    textbox_kernel.insert(5, "5") 
    textbox_iteration.insert(5, "5") 
    
    button_ok = Button(info, text='OK', command=lambda:[check_numb_dilation(textbox_kernel, textbox_iteration), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    
    
def check_numb_dilation(text1, text2):
    global dilation_kernel, dilation_iteration
    global dilation
    number = text1.get()
    number2 = text2.get()
    if number != None and number2 != None:
        dilation_kernel = int(number)
        dilation_iteration = int(number2)
        do_final_actions_from_init(dilation, number, number2)
        
def init_opening():
    global opening_kernel, opening
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')

    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    textbox_kernel.insert(5, "5") 
    
    button_ok = Button(info, text='OK', command=lambda:[check_numb_opening(textbox_kernel), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
    
def check_numb_opening(text1):
    global opening, opening_kernel
    number = text1.get()
    if number != None:
        opening_kernel = int(number)
        do_final_actions_from_init1(opening, number)
    
def init_closing():
    global closing_kernel, closing
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')

    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    textbox_kernel.insert(5, "5") 
    
    button_ok = Button(info, text='OK', command=lambda:[check_numb_closing(textbox_kernel), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")

    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
    
def check_numb_closing(text1):
    global closing, closing_kernel
    number = text1.get()
    if number != None:
        closing_kernel = int(number)
        do_final_actions_from_init1(closing, number)
    
def init_top_hat():
    global top_hat_kernel, top_hat
    info = Toplevel()  
    info.geometry("600x100")
    info.title('Zadejte parametry: ')

    label_kernel = Label(info, text="Velikost jádra: ").pack(side="left", padx="10", pady="1")
    textbox_kernel = Entry(info)
    textbox_kernel.pack(side="left", padx="10", pady="1")
    textbox_kernel.insert(5, "5") 
    
    button_ok = Button(info, text='OK', command=lambda:[check_numb_top_hat(textbox_kernel), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")

    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
    
def check_numb_top_hat(text1):
    global top_hat, top_hat_kernel
    number = text1.get()
    if number != None:
        top_hat_kernel = int(number)
        do_final_actions_from_init1(top_hat, number)
    
def init_hough_line():
    info = Toplevel()  
    info.geometry("1100x100")
    info.title('Zadejte parametry: ')
    label_info = Label(info, text="Min. délka přímky:").pack(side="left", padx="10", pady="1")
    textbox1 = Entry(info)
    textbox1.pack(side="left", padx="10", pady="1")
    textbox1.insert(10, "10") 
    
    label_info2 = Label(info, text="Max. délka mezery:").pack(side="left", padx="10", pady="1")
    textbox2 = Entry(info)
    textbox2.pack(side="left", padx="10", pady="1")
    textbox2.insert(200, "200")
    
    label_info3 = Label(info, text="Prahování:").pack(side="left", padx="10", pady="1")
    textbox3 = Entry(info)
    textbox3.pack(side="left", padx="10", pady="1")
    textbox3.insert(90, "90")
    
    button_ok = Button(info, text='OK', command=lambda:[check_hough_line(textbox1, textbox2, textbox3), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")

    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
    
def check_hough_line(t1, t2, t3):
    global hought_line, min_linelength, max_linegap, hough_threshold
    number1 = t1.get()
    number2 = t2.get()
    number3 = t3.get()
    if number1 != None and number2 != None and number3 != None:
        min_linelength = int(number1)
        max_linegap = int(number2)
        hough_threshold = int(number3)
        do_final_actions_from_init3(hought_line, min_linelength, max_linegap, hough_threshold)
    
def init_hough_circle():
    info = Toplevel()  
    info.geometry("900x100")
    info.title('Zadejte parametry: ')
    label_info = Label(info, text="Parametr 1:").pack(side="left", padx="10", pady="1")
    textbox1 = Entry(info)
    textbox1.pack(side="left", padx="10", pady="1")
    textbox1.insert(180, "180") 
    
    label_info2 = Label(info, text="Parametr 2:").pack(side="left", padx="10", pady="1")
    textbox2 = Entry(info)
    textbox2.pack(side="left", padx="10", pady="1")
    textbox2.insert(28, "28")

    button_ok = Button(info, text='OK', command=lambda:[check_hough_circle(textbox1, textbox2), info.destroy()], bg="gray88", height = 1, width = 20).pack(side="left", padx="10", pady="1")
    
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
    
def check_hough_circle(t1, t2):
    global hought_circle, hough_param1, hough_param2
    number1 = t1.get()
    number2 = t2.get()
    if number1 != None and number2 != None:
        hough_param1 = int(number1)
        hough_param2 = int(number2)
        do_final_actions_from_init(hought_circle, hough_param1, hough_param2)
        

def init_searching_sample(count):
    info = Toplevel()  
    info.geometry("500x100")
    info.title('Vyberte vzor:')
    button_choose_file= Button(info, text="Vybrat vzor", command= lambda:[select_template(info, count)], height = 1, width = 20).pack(side="left", padx="10", pady="1")
    ok_button = Button(info, text = "OK", command= lambda: [add_init_template(count), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)
   
def add_init_template(count):
    global template, ccoeff_normed, ccoeff_normed_len, multi_ccoeff_normed, multi_ccoeff_normed_len
    if template != "":
        if count == 1:
            temp = ccoeff_normed
            btn = btnSearchingSample
        else:
            temp = multi_ccoeff_normed
            btn = btnSearchingSamples
        add_button(btn)
        edit_list_of_actions(temp + " " + template)
        action_for_button(temp)

def raise_above_all(window):
    window.attributes('-topmost', 1)

def init_face_recognition():
    global face_r_cnn, face_r_hog, dataset
    info = Toplevel()  
    info.geometry("800x100")
    textbox_input = Entry(info) 
    info.title('Vyberte dataset a zvolte metodu rozpoznávání:')
    
    button_choose_file= Button(info, text="Vybrat dataset", command= lambda:[select_dataset(), check_select_dataset(info)], height = 1, width = 20).pack(side="left", padx="10", pady="1")

    hog = Button(info, text = face_r_hog, command= lambda: [check_dataset(info, 2), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    cnn = Button(info, text = face_r_cnn, command= lambda: [check_dataset(info, 1), info.destroy()], height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    clear_button = Button(info, text='Zrušit', command=info.destroy, height = 1, width = 20, bg="gray88").pack(side="left", padx="10", pady="1")
    raise_above_all(info)

def check_select_dataset(info):
    global dataset
    if dataset != "":
        label_file_choose = Label(info, text="Dataset vybrán.", fg="green").pack(side="left", padx="10", pady="1")
        
def check_dataset(info, method):
    global face_r_cnn, face_r_hog, dataset
    if dataset != "":
        if method == 1:
            temp = face_r_cnn
            btn = btnCNN
        else:
            temp = face_r_hog
            btn = btnHOG
        add_button(btn)
        edit_list_of_actions(temp + " " + dataset)
        action_for_button(temp)

def do_final_actions_from_init(text, number, number2):
    #add buttons, edil_list with 2 numbers
    add_button_for_parameters(text)
    edit_list_of_actions(text + " " + str(number) + " " + str(number2))   
    action_for_button(text)
    
def do_final_actions_from_init3(text, number, number2, number3):
    #add buttons, edil_list with 3 numbers
    add_button_for_parameters(text)
    edit_list_of_actions(text + " " + str(number) + " " + str(number2) + " " + str(number3))   
    action_for_button(text)
    
def do_final_actions_from_init1(text, number):
    #add buttons, edil_list with 1 number
    add_button_for_parameters(text)
    edit_list_of_actions(text + " " + str(number))   
    action_for_button(text)



def get_help():
    file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    path = os.path.join(file_location, "help\index.html")
    url = 'file:///' + path
    webbrowser.open(url, new=2)  # open in new tab
    
# inicializace hlavního okna toolkit s dvěma panely - panelA, panelB, canvas = dělá hlavní okno větší
root = tkinter.Tk()
# nastavení popisku hlavního okna
root.title('Modulární systém pro předzpracování a analýzu digitálních obrazových dat')

canvas = tkinter.Canvas(root)
root.geometry("1250x700")
root.minsize(width=1250, height=750)
root.maxsize(width=1250, height=850)
panelA = None
panelB = None  


canvas.pack()

panelA = None
panelB = None

frame_for_text = Frame(root)
frame_for_text.pack()

bottomframe = Frame(root, width=1250, height=500)
bottomframe.pack()

arrow = lambda:Label(bottomframe, text=">>")

text = WrappingLabel(frame_for_text, text=list_of_actions, width=900)

text.place(relx = 0.0,rely=1,anchor='sw')
text.pack(padx="10", pady="10",expand=YES, fill=tkinter.X)

#bottom buttons - for doing actions
# vytvoření tlačítka pro vybrání souboru - "file chooser", volá funkci select_image (zobrazení dialogu s možností výběru a následné načtení)
btnVybratSoubor2 = lambda:Button(bottomframe, text="OrigIm", command=lambda:[action_for_button(path)],height = 1, width = 20)
btnPrevodDoSede2 = lambda:Button(bottomframe, text="RGB2gray", command=lambda:[action_for_button("RGB2G")],height = 1, width = 20)

btnPrevodDoR2 = lambda:Button(bottomframe, text="R-RGB", command=lambda:[action_for_button("R-RGB")], height = 1, width = 20)
btnPrevodDoG2 = lambda:Button(bottomframe, text="G-RGB", command= lambda:[action_for_button("G-RGB")], height = 1, width = 20)
btnPrevodDoB2 = lambda:Button(bottomframe, text="B-RGB", command= lambda:[action_for_button("B-RGB")], height = 1, width = 20)

btnPrevodDoCb2 = lambda:Button(bottomframe, text="Cb-YCbCr", command= lambda:[action_for_button("Cb-YCbCr")], height = 1, width = 20)
btnPrevodDoCr2 = lambda:Button(bottomframe, text="Cr-YCbCr", command= lambda:[action_for_button("Cr-YCbCr")], height = 1, width = 20)

btnPrevodDoH2 = lambda:Button(bottomframe, text="H-HSV", command= lambda:[action_for_button("H-HSV")], height = 1, width = 20)
btnPrevodDoS2 = lambda:Button(bottomframe, text="S-HSV", command= lambda:[action_for_button("S-HSV")], height = 1, width = 20)

btn_negativ2 = lambda: Button(bottomframe, text="Negativ", command=lambda:[action_for_button("Negativ")], height = 1, width = 20)

btn_equalization2 = lambda: Button(bottomframe, text="Ekvalizace", command=lambda:[action_for_button("Ekvalizace")], height = 1, width = 20)

btn_laplace_edge_detector2 = lambda: Button(bottomframe, text="LaplaceHD", command=lambda:[action_for_button("LaplaceHD")], height = 1, width = 20)

btnColoring = lambda: Button(bottomframe, text=coloring_areas, command=lambda:[action_for_button(coloring_areas)], height = 1, width = 20)

btnSearchingSample = lambda: Button(bottomframe, text=ccoeff_normed, command=lambda:[action_for_button(ccoeff_normed)], height = 1, width = 20)

btnSearchingSamples = lambda: Button(bottomframe, text=multi_ccoeff_normed, command=lambda:[action_for_button(multi_ccoeff_normed)], height = 1, width = 20)

btnAdaboostHaar = lambda: Button(bottomframe, text=adaboost_haar, command=lambda:[action_for_button(adaboost_haar)], height = 1, width = 20)
btnDlib = lambda: Button(bottomframe, text=dlib_temp, command=lambda:[action_for_button(dlib_temp)], height = 1, width = 20)
btnHOG = lambda: Button(bottomframe, text=face_r_hog, command=lambda:[action_for_button(face_r_hog)], height = 1, width = 20)
btnCNN = lambda: Button(bottomframe, text=face_r_cnn, command=lambda:[action_for_button(face_r_cnn)], height = 1, width = 20)

menubar = Menu(root)
    
abst_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Soubor", menu=abst_env)
create_next_filemenu(abst_env, "Otevřít obrázek", lambda:[select_image(), clear_list_of_actions_with_path(),verify_segmentation_for_detection()])
create_next_filemenu(abst_env, "Uložit obrázek", save_image)
create_next_filemenu(abst_env, "Zpět", lambda:[clear_last_step(),abst_env.entryconfigure("5", state=tkinter.DISABLED),verify_segmentation_for_detection()])
create_next_filemenu(abst_env, "Otevřít řetězec metod", lambda:[clear_list_of_actions_with_path(), open_list_of_methods(), verify_segmentation_for_detection()]) #clear_list_of_actions(),hide_all_buttons2()
create_next_filemenu(abst_env, "Uložit řetězec metod", save_list_of_methods)

color_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Barevné prostory", menu=color_env, state=tkinter.DISABLED)
create_next_filemenu(color_env, "RGB2gray", lambda:[add_button(btnPrevodDoSede2),edit_list_of_actions("RGB2G"),verify_choose_color_env(),action_for_button("RGB2G"),verify_segmentation_for_detection()])
create_next_filemenu(color_env, "RGB", init_choosing_rgb)
create_next_filemenu(color_env, "YCbCr", init_choosing_ycbcr)
create_next_filemenu(color_env, "HSV", init_choosing_hsv)

geo_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Geometrické transformace", menu=geo_env, state=tkinter.DISABLED)
create_next_filemenu(geo_env, "Rotace", init_rotate)
create_next_filemenu(geo_env, "Měřítko", init_scale)

bright_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Jasové transformace", menu=bright_env, state=tkinter.DISABLED)
create_next_filemenu(bright_env, "Korekce", init_correction)
create_next_filemenu(bright_env, "Negativ", lambda:[add_button(btn_negativ2),edit_list_of_actions("Negativ"),action_for_button("Negativ")])
create_next_filemenu(bright_env, "Ekvalizace", lambda:[add_button(btn_equalization2), edit_list_of_actions("Ekvalizace"),action_for_button("Ekvalizace")])

filter_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Filtrace šumu", menu=filter_env, state=tkinter.DISABLED)
create_next_filemenu(filter_env, "Fprůměr", init_average_filter)
create_next_filemenu(filter_env, "FGauss", init_FGauss)
create_next_filemenu(filter_env, "Fmedián", init_Fmedian)

edge_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Hranové detektory", menu=edge_env, state=tkinter.DISABLED)
create_next_filemenu(edge_env, "LaplaceHD", lambda:[add_button(btn_laplace_edge_detector2),edit_list_of_actions("LaplaceHD"),action_for_button("LaplaceHD")])
create_next_filemenu(edge_env, "SobelHD", init_sobel)
create_next_filemenu(edge_env, "CannyHD", init_canny)

segment_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Segmentace obrazu", menu=segment_env, state=tkinter.DISABLED)
create_next_filemenu(segment_env, "Jednoduché prahování", init_simple_thresholding)
create_next_filemenu(segment_env, "Adaptivní prahování", init_adaptive_thresholding)
create_next_filemenu(segment_env, "Binarizace Otsu", init_otsu)

bin_morf_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Binární morfologie", menu=bin_morf_env, state=tkinter.DISABLED)
create_next_filemenu(bin_morf_env, "Eroze", init_erosion)
create_next_filemenu(bin_morf_env, "Dilatace", init_dilation)
create_next_filemenu(bin_morf_env, "Otevření", init_opening)
create_next_filemenu(bin_morf_env, "Uzavření", init_closing)
create_next_filemenu(bin_morf_env, "Vrchní část klobouku", init_top_hat)

hough_env = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Houghova transformace", menu=hough_env, state=tkinter.DISABLED)
create_next_filemenu(hough_env, "Pro přímky", init_hough_line)
create_next_filemenu(hough_env, "Pro kružnice", init_hough_circle)

detection_env = Menu(menubar, tearoff=0)
submenu = Menu(detection_env, tearoff=0)
menubar.add_cascade(label="Detekce a identifikace objektů", menu=detection_env, state=tkinter.DISABLED)
create_next_filemenu(detection_env, "Barvení oblastí", lambda:[add_button(btnColoring),edit_list_of_actions(coloring_areas),action_for_button(coloring_areas)])
detection_env.add_separator()
detection_env.add_cascade(label="Vyhledávání vzorů", menu=submenu)
submenu.add_command(label="Vzor", command=lambda:[init_searching_sample(1)])
submenu.add_separator()
submenu.add_command(label="Vzory", command=lambda:[init_searching_sample(2)])
create_next_filemenu(detection_env, "Detekce obličeje pomocí AdaBoost a Haar příznaků", lambda:[add_button(btnAdaboostHaar),edit_list_of_actions(adaboost_haar),action_for_button(adaboost_haar)])
create_next_filemenu(detection_env, "Detekce obličeje pomocí Dlib", lambda:[add_button(btnDlib),edit_list_of_actions(dlib_temp),action_for_button(dlib_temp)])
create_next_filemenu(detection_env, "Identifikace obličeje pomocí Face_recognition", init_face_recognition)

help_env = Menu(menubar, tearoff=0)
menubar.add_command(label="Nápověda", command=get_help)

root.config(menu=menubar)
root.mainloop()
