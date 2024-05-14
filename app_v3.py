
import os, requests
import tkinter as tk
from tkinter import filedialog
import webbrowser
from tkinter import font


def validate_selection():
    if not any(var.get() == "1" for var in option_vars_1) or not any(var.get() == "1" for var in option_vars_2) or not any(var.get() == "1" for var in option_vars_3):
        tk.messagebox.showerror("Error", "Please select one option in each column.")
        return False
    return True

def calculate():
    try:
        if not validate_selection():
            return
        value1 = float(entry1.get()) # Left
        value2 = float(entry2.get()) # Right
        value3 = float(entry3.get()) # Top
        value4 = float(entry4.get()) # Bottom
        if entry_folder_path.get().strip() == "":
            tk.messagebox.showerror("Error", "Please select a folder to save the file.")
            return
        
        result = value1 + value2 + value3 + value4 # You can perform any operation here
        
        selected_options_1 = [option for var, option in zip(option_vars_1, options_1) if var.get() == "1"]
        selected_options_2 = [option for var, option in zip(option_vars_2, options_2) if var.get() == "1"]
        selected_options_3 = [option for var, option in zip(option_vars_3, options_3) if var.get() == "1"]
        result_label.config(text="Result: " + str(result) + 
                            "\nSelected Soil Parameters: " + ", ".join(selected_options_1) +
                            "\nSelected Statistical values: " + ", ".join(selected_options_2) +
                            "\nSelected Layers: " + ", ".join(selected_options_3) +
                            #"\nProject Name: " + entry_project_name.get() +
                            "\nFolder Path: " + entry_folder_path.get(),  fg="blue")
        
        print(selected_options_1, selected_options_2, selected_options_3)
        print(value1, value2, value3, value4)
        
        parm_s = selected_options_1 #['alpha', 'silt'] #
        sta_v_s = selected_options_2 # ['mean', 'p5'] # 
        lyr_s = selected_options_3 # ['0_5', '5_15'] # 
        
        left_t  = int(abs(value1)+1)
        right_t = int(abs(value2))
        top_t   = int(abs(value3)+1)
        bottom_t = int(abs(value4))

        lat_list = list(range(bottom_t, top_t, 1))
        lon_list = list(range(right_t, left_t, 1))

        #print(lat_list)
        #print(lon_list)

        just_tif_name = []
        all_tifs = []
        custom_tif_names = []
        for p in parm_s:
            for s in sta_v_s:
                for ly in lyr_s:
                    target_url = "http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0"+"/"+ p +"/"+s+"/"+ly+"/"
                    for i in lat_list:
                        for j in lon_list:
                            tif_name = f'lat{i}{i+1}_lon-{j+1}-{j}.tif'
                            out_name = f'lat{i}{i+1}_lon-{j+1}-{j}-{p}-{s}-{ly}.tif'
                            custom_tif_names.append(out_name)
                            just_tif_name.append(tif_name)
                            print(tif_name)
                            print(out_name)
                            full_tif_name = target_url + tif_name
                            all_tifs.append(full_tif_name)
        
        '''
        all_tifs = ['http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/clay/mean/0_5/lat3738_lon-97-96.tif',
         'http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/clay/mean/0_5/lat3738_lon-98-97.tif',
         'http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/clay/mean/0_5/lat3839_lon-97-96.tif',
         'http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/clay/mean/0_5/lat3839_lon-98-97.tif']
        just_tif_name = ['lat3738_lon-97-96.tif', 'lat3738_lon-98-97.tif',
                         'lat3839_lon-97-96.tif', 'lat3839_lon-98-97.tif'] #'''
        # Folder path where you want to save the files
        folder_path = entry_folder_path.get()+"/" # "D:/work/research_t/swat/test/"

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)


        # Loop through the file names and download each file
        for t in range(len(all_tifs)):
            # Construct the full URL for each file
            #file_url = urljoin(base_url, file_name)
            
            # Send a GET request to download the file
            response = requests.get(all_tifs[t])
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Save the file to the specified folder
                #file_path = os.path.join(folder_path, just_tif_name[t])
                file_path = os.path.join(folder_path, custom_tif_names[t])
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {just_tif_name[t]}")
            else:
                print(f"Failed to download {just_tif_name[t]}. Status code: {response.status_code}")
        
        
    except ValueError:
        result_label.config(text="Please enter valid numbers",  fg="red")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_folder_path.delete(0, tk.END)
        entry_folder_path.insert(tk.END, folder_path)

# Create main window
window = tk.Tk()
window.title("POLARIS Soil Data Download Tool ")

# Set custom size for the window
window.geometry("600x680")

# Create label to describe the purpose of the window
#description_label = tk.Label(window, text="Enter two values below.\nFor more information, click here:", 
#                             justify=tk.LEFT, fg="blue", cursor="hand2")
#description_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
description_label = tk.Label(window, text="This interface helps POLARIS database download from Duke University repository \nFor more information about the data visit these links: ", 
                             justify=tk.LEFT)
description_label.grid(row=0, column=0, columnspan=3, sticky=tk.W)

# Create label to describe the purpose of the window
def open_link(event):
    webbrowser.open_new("http://hydrology.cee.duke.edu/POLARIS/")
    
ref1 = tk.Label(window, text="http://hydrology.cee.duke.edu/POLARIS/", justify=tk.LEFT, fg="blue", cursor="hand2")
ref1.grid(row=1, column=0, columnspan=2, sticky=tk.W)
ref1.bind("<Button-1>", open_link)   # Bind the label to open the link when clicked

# Create label to describe the purpose of the window
def open_link2(event):
    webbrowser.open_new("https://www.sciencedirect.com/science/article/pii/S0016706116301434")
    
ref2 = tk.Label(window, text="https://www.sciencedirect.com/science/article/pii/S0016706116301434", justify=tk.LEFT, fg="blue", cursor="hand2")
ref2.grid(row=2, column=0, columnspan=2, sticky=tk.W)
ref2.bind("<Button-1>", open_link2)   # Bind the label to open the link when clicked



'''
# Function to open the link
def open_link2():
    webbrowser.open_new("https://jakobzhao.github.io/slr/")

# Function to create the link button
def create_link_button():
    link_button = tk.Button(window, text="More Info", command=open_link2)
    link_button.grid(row=0, column=2)

# Create the link button
create_link_button() #'''


'''
# Create entry widget for inputting project name
label_project_name = tk.Label(window, text="Project Name:")
label_project_name.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
entry_project_name = tk.Entry(window, width=20)
entry_project_name.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W) #'''


# Create label to describe the purpose of the window
descrip_2 = tk.Label(window, text="Input the folder where to donload", justify=tk.LEFT)
descrip_2.grid(row=3, column=0, columnspan=2, sticky=tk.W)


# Create entry widget for inputting folder path
label_folder_path = tk.Label(window, text="Folder Path:")
label_folder_path.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
entry_folder_path = tk.Entry(window, width=50)  # Adjust width as needed
entry_folder_path.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)  # Span two columns
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)  # Place in column 3

################################## COL-1 ##################################
# Create a frame for the first column of options
frame_1 = tk.Frame(window, bd=2, relief=tk.RIDGE)
frame_1.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

# Create a label for the first column
label_1 = tk.Label(frame_1, text="Soil Parameters:")
label_1.grid(row=0, column=0, columnspan=2)

# Create Checkbutton widgets for each option in the first column
options_1 = ['alpha', 'bd', 'clay', 'hb', 'ksat', 'lambda', 'n','om','ph','sand','silt','theta-r','theta-s']
option_vars_1 = []
for i, option in enumerate(options_1):
    var = tk.StringVar(value="0")
    option_vars_1.append(var)
    check_button = tk.Checkbutton(frame_1, text=option, variable=var, onvalue="1", offvalue="0")
    check_button.grid(row=i%7+1, column=i//7, sticky=tk.W)

################################## COL-2 ##################################
# Create a frame for the second column of options
frame_2 = tk.Frame(window, bd=2, relief=tk.RIDGE)
frame_2.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

# Create Checkbutton widgets for each option in the second column
options_2 = ['mean', 'mode', 'p5', 'p50', 'p95']
option_vars_2 = []
for i, option in enumerate(options_2):
    var = tk.StringVar(value="0")
    option_vars_2.append(var)
    check_button = tk.Checkbutton(frame_2, text=option, variable=var, onvalue="1", offvalue="0")
    check_button.grid(row=i+1, column=0, sticky=tk.W)

# Create a label for the second column
label_2 = tk.Label(frame_2, text="Statistical values:")
label_2.grid(row=0, column=0, columnspan=2, sticky=tk.W)

################################## COL-3 ##################################
# Create a frame for the Third column of options
frame_3 = tk.Frame(window, bd=2, relief=tk.RIDGE)
frame_3.grid(row=5, column=2, padx=10, pady=10, sticky=tk.W)

# Create Checkbutton widgets for each option in the second column
options_3 = ['0_5', '5_15', '15_30', '30_60', '60_100', '100_200']
option_vars_3 = []
for i, option in enumerate(options_3):
    var = tk.StringVar(value="0")
    option_vars_3.append(var)
    check_button = tk.Checkbutton(frame_3, text=option, variable=var, onvalue="1", offvalue="0")
    check_button.grid(row=i+1, column=0, sticky=tk.W)

# Create a label for the second column
label_3 = tk.Label(frame_3, text="Layer:")
label_3.grid(row=0, column=0, columnspan=2, sticky=tk.W)
#############################################################################

# Create label to describe the purpose of the window
description_1 = tk.Label(window, text="Input coordinates for desired download area: left, right, top, bottom.\nClick the link to select coordinates using a map:", justify=tk.LEFT, fg="blue")
description_1.grid(row=6, column=0, columnspan=2)
# Bind the label to open the link when clicked
#description_1.bind("<Button-1>", open_link)

# Function to open the link
def open_link3():
    webbrowser.open_new("https://noayarae.github.io/POLARIS_Soil_Data_Download_Tool/index3.html")
def create_link_button():  # Function to create the link button
    link_button = tk.Button(window, text="Map", command=open_link3, cursor="hand2")
    link_button.grid(row=6, column=2)
# Create the link button
create_link_button()

#############################################################################
# Create entry widgets for input
label_entry1 = tk.Label(window, text="Left :")
label_entry1.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
entry1 = tk.Entry(window)
entry1.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

label_entry2 = tk.Label(window, text="Right :")
label_entry2.grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)
entry2 = tk.Entry(window)
entry2.grid(row=8, column=1, padx=10, pady=5, sticky=tk.W)

label_entry3 = tk.Label(window, text="Top :")
label_entry3.grid(row=9, column=0, sticky=tk.W, padx=10, pady=5)
entry3 = tk.Entry(window)
entry3.grid(row = 9, column=1, padx=10, pady=5, sticky=tk.W)

label_entry4 = tk.Label(window, text="Bottom :")
label_entry4.grid(row=10, column=0, sticky=tk.W, padx=10, pady=5)
entry4 = tk.Entry(window)
entry4.grid(row=10, column=1, padx=10, pady=5, sticky=tk.W)


# Create button to perform calculation
calculate_button = tk.Button(window, text="Calculate", command=calculate)
calculate_button.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Create label to display result
result_label = tk.Label(window, text="Result: ")
result_label.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Run the main event loop
window.mainloop()















