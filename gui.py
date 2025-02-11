import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import os
from tkinter import filedialog
from tkinter import messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize




nltk.download('stopwords')
nltk.download('punkt_tab')
imported_function = None
def main():
    global df, tree, columns, new_btn_created, values

    root = tk.Tk()
    root.geometry('1000x600')
    root.title('Patient Database')
    
    def bg():
        try:
            img_path = r'C:\Users\zwano\OneDrive\Desktop\patient_database\pngtree-ward-green-illustration-background-picture-image_2270017.jpg'
            if not os.path.exists(img_path):
                messagebox.showerror("File Not Found", f"The image file {img_path} was not found.")
                return
            
            bg_img = Image.open(img_path)
            bg_img = bg_img.resize((1000, 1000))
            bg_img = ImageTk.PhotoImage(bg_img)

            bg_lab = tk.Label(root, image=bg_img)
            bg_lab.place(relwidth=1, relheight=1)
            bg_lab.image = bg_img  # Keep a reference to prevent garbage collection
        except Exception as e:
            print("Error loading background image:", e)
        label = tk.Label(root, text="Patient Database", font=(48))
        label.pack()
    bg()
    
    def create_treeview():
        global tree
        if 'tree' in globals():
            tree.destroy()  

        tree = ttk.Treeview(root, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor='center', width=100)
        
        tree.pack(padx=100, pady=20)
        tree.bind("<<TreeviewSelect>>", on_select)
        tree.bind("<Key>", navigate)

    def load_data():
        tree.delete(*tree.get_children())
        for index, row in df.iterrows():
            tree.insert('', 'end', values=row.tolist())

    def refresh_table():
        create_treeview()
        load_data()
        
    def clear_entries():
        for entry in entry_fields:
            entry.delete(0, tk.END)

    def update_csv():
        try:
            if 'appointment_id' in df.columns:
                df.to_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\appointment_data.csv', index=False)
            else:
                df.to_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\patient_data.csv', index=False)
            print("CSV updated successfully.")
        except Exception as e:
            print("Error updating CSV:", e)

    def add_row():
        global df
        if 'appointment_id' in df.columns:
            new_data = [entry.get() for entry in entry_fields[:5]]
        else:
            new_data = [entry.get() for entry in entry_fields]

        if all(new_data):
            df.loc[len(df)] = new_data
            print("Added row:", new_data)
            update_csv()
            load_data()
            clear_entries()
        else:
            messagebox.showerror('error',"Error: All fields must be filled.")

    def edit_row():
        global df
        selected_item = tree.selection()
        if selected_item:
            if 'appointment_id' in df.columns:
                new_data = [entry.get() for entry in entry_fields[:5]]
            else:
                new_data = [entry.get() for entry in entry_fields]

            if all(new_data):
                index = tree.index(selected_item[0])
                df.iloc[index] = new_data
                print("Edited row:", new_data)
                update_csv()
                load_data()
                clear_entries()
            else:
                messagebox.showerror('error',"Error: All fields must be filled.")

    def delete_row():
        global df
        selected_item = tree.selection()
        if selected_item:
            index = tree.index(selected_item[0])
            df.drop(index, inplace=True)
            print("Deleted row at index:", index)
            update_csv()
            load_data()
        elif not selected_item:
            messagebox.showerror('error','error')
            
    

    def on_button_click():
        global imported_function,imported_function2
        
        # Conditional import inside the button click handler
        if imported_function is None:
            try:
                from video_recognition import recognize_faces,name  # Replace with your module and function
                imported_function =  recognize_faces
                imported_function2 = name
                print("Function imported successfully!")
            except ImportError:
                print("Failed to import function.")
        
        # Call the imported function if it's available
        if imported_function is not None:
            imported_function() 
    
    def on_select(event):
        global values
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0])['values']
            print("Selected values:", values)  # Debug statement
            clear_entries()
            for i, value in enumerate(values):
                if i < len(entry_fields):
                    entry_fields[i].insert(0, value)
        
    def navigate(event):
        current_selection = tree.selection()
        if current_selection:
            index = tree.index(current_selection[0])
            if event.keysym == 'Down':
                next_index = index + 1
                if next_index < len(tree.get_children()):
                    tree.selection_set(tree.get_children()[next_index])
                    tree.focus(tree.get_children()[next_index])
                    on_select(event)
            elif event.keysym == 'Up':
                previous_index = index - 1
                if previous_index >= 0:
                    tree.selection_set(tree.get_children()[previous_index])
                    tree.focus(tree.get_children()[previous_index])
                    on_select(event)

    def load_patients_data():
        global df, columns
        if os.path.exists(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\patient_data.csv'):
            df = pd.read_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\patient_data.csv')
        else:
            df = pd.DataFrame(columns=['id', 'name', 'age', 'gender', 'address', 'phone', 'aadhar'])
        columns = df.columns.tolist()
        refresh_table()

    def load_appointments_data():
        global df, columns
        if os.path.exists(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\appointment_data.csv'):
            df = pd.read_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\appointment_data.csv')
        else:
            df = pd.DataFrame(columns=['appointment_id', 'patient_name', 'doctor', 'date', 'status'])
        columns = df.columns.tolist()
        refresh_table()

    def load_records():
        global df, columns 
        if os.path.exists(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\medical_records_data.csv'):
            df = pd.read_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\medical_records_data.csv')
        else:
            df = pd.DataFrame(columns=['patient_id', 'patient_history_records', 'diagnosis', 'date', 'treatment', 'allergies'])

        columns = df.columns.tolist()
        refresh_table()
    
    def remove_stop_words(text):
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_words)
        return filtered_text
    
    def on_button_click():
        global imported_function, imported_function2
        if imported_function is None:
            try:
                # Import the functions and variables
                from video_recognition import recognize_faces, Name  # Name is a list, not a function
                imported_function = recognize_faces
                imported_function2 = Name  # This is the list of recognized names, not a callable function
                print("Function imported successfully!")
            except ImportError as e:
                print("Failed to import function:", e)
                messagebox.showerror("Import Error", "Failed to import face recognition functions.")
        
        if imported_function and imported_function2:
            # Call the function to recognize faces
            imported_function()  # Call recognize_faces, which will update the Name list with recognized names
            
            if imported_function2:  # If there are any recognized names in the Name list
                recognized_name = imported_function2[0]  # Get the first recognized name (or iterate through the list)
                print("Recognized name:", recognized_name)
                
                # Call filter_data_based_on_name with the recognized name
                filtered_data = filter_data_based_on_name(recognized_name)
                
                # Show filtered data in a popup window if data is found
                if filtered_data is not None:
                    gui_popup(recognized_name, filtered_data)
                else:
                    messagebox.showerror("No Data Found", f"No data found for patient name: {recognized_name}")
            else:
                messagebox.showerror("Recognition Error", "Failed to recognize a name.")

    
    def gui_popup(name, data):
        # Create a new top-level window to display filtered patient data
        popup = tk.Toplevel()
        popup.title(f"Patient Data for {name}")

        # Display the filtered data in a scrollable frame
        frame = tk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas with a scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to contain the table of data
        data_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=data_frame, anchor="nw")

        # Add the scrollbar to the frame
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add headers to the table
        headers = ["patient_id", "name", "age", "gender", "address", "number", "picture"]
        for col_num, header in enumerate(headers):
            label = tk.Label(data_frame, text=header, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col_num, padx=5, pady=5)

      
        for row_num, row_data in enumerate(data.values):
            for col_num, col_data in enumerate(row_data):
                label = tk.Label(data_frame, text=col_data, font=("Helvetica", 10))
                label.grid(row=row_num+1, column=col_num, padx=5, pady=5)

        data_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
    def filter_data_based_on_name(recognized_name):
        try:
            df = pd.read_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\patient_data.csv')
            filtered_data = df[df['name'].str.contains(recognized_name, case=False, na=False)]

            if not filtered_data.empty:
                print("Filtered Patient Data: ")
                print(filtered_data)
                return filtered_data
            else:
                print(f"No data found for patient name: {recognized_name}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred while filtering data: {e}")
            return None

   
    def upload_functionalities():
        global df, condition
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    file_content = remove_stop_words(file_content)
                    on_select(messagebox.showinfo('File Content', file_content))
                    condition = df['patient_id'] == values[0]
                    df.loc[condition, 'patient_history_records'] = f'yes {file_content}'
                    df.to_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\medical_records_data.csv', index=False)
            except Exception as e:
                messagebox.showerror('Error:', e)

    def med_history_popup():
        global condition
        patient_id = values[0]
        try:
            df = pd.read_csv(r'C:\Users\zwano\OneDrive\Desktop\patient_database\csv\medical_records_data.csv')
            patient_history = df.loc[df['patient_id'] == patient_id, 'patient_history_records'].values
            
            if patient_history and patient_history[0].startswith('yes'):
                medical_record = patient_history[0] 
                medical_record_content = medical_record.split('yes', 1)[1].strip() if 'yes' in medical_record else ''
                messagebox.showinfo('Medical History', medical_record_content) 
            else:
                messagebox.showinfo('Info', 'No medical history available for this patient.')
        except Exception as e:
            print('Error:', e)
            messagebox.showinfo('Error', 'Could not fetch medical history.')

    def create_btn():
        global new_btn_created
        if not new_btn_created:
            new_btn2 = tk.Button(root, text='Upload Files', command=upload_functionalities)
            new_btn = tk.Button(root, text='previous prescription', command=med_history_popup)
            new_btn2.pack(pady=10)
            new_btn.pack(pady=10)
            new_btn_created = True


    def create_btn():
        global new_btn_created
        if not new_btn_created:
            new_btn2 = tk.Button(root, text='Upload Files', command=upload_functionalities)
            new_btn = tk.Button(root, text='Medical History',command=med_history_popup)
            new_btn2.pack(pady=10) 
            new_btn2.pack(pady=10)
            new_btn.pack(pady=10)
            new_btn_created = True

    def load_records_and_create_button():
        load_records()  
        create_btn() 
    
        

    entry_fields = [tk.Entry(root) for _ in range(7)]
    for entry in entry_fields:
        entry.pack()

    btn_add = tk.Button(root, text="Add Row", command=add_row)
    btn_add.pack()
    btn_edit = tk.Button(root, text="Edit Row", command=edit_row)
    btn_edit.pack()
    btn_delete = tk.Button(root, text="Delete Row", command=delete_row)
    btn_delete.pack()
    med_btn = tk.Button(root, text='Load Patients', command=load_patients_data)
    med_btn.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
    appointment_btn = tk.Button(root, text='Load Appointments', command=load_appointments_data)
    appointment_btn.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
    records_btn = tk.Button(root, text='Load Medical Records', command=load_records_and_create_button)
    records_btn.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)
    face_det_btn = tk.Button(root, text='Face Detection', command=on_button_click)
    face_det_btn.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

    new_btn_created = False
    load_patients_data()  
    root.mainloop()

if __name__ == '__main__':
    main()