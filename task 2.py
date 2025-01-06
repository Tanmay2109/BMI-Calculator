#Project by Tanmay Manish Patil
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_file = "bmi_data.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Name", "Weight", "Height", "BMI", "Date"])
    df.to_csv(csv_file, index=False)

def calculate_bmi():
    try:
        name = entry_name.get()
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        
        if height <= 0 or weight <= 0:
            messagebox.showerror("Input Error", "Please enter positive values for weight and height.")
            return
        
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        
        label_result.config(text=f"BMI: {bmi}")
        
        date = pd.to_datetime('today').strftime('%Y-%m-%d')
        data = pd.DataFrame([[name, weight, height, bmi, date]], columns=["Name", "Weight", "Height", "BMI", "Date"])
        data.to_csv(csv_file, mode='a', header=False, index=False)
        
        messagebox.showinfo("Success", f"Data saved for {name}")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

def show_history():
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        history_window = tk.Toplevel(window)
        history_window.title("BMI History")
        
        text = tk.Text(history_window, width=60, height=15)
        text.pack(pady=10)
        
        history = df.to_string(index=False)
        text.insert(tk.END, history)
    else:
        messagebox.showerror("Error", "No data available.")

def show_trend():
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        
        if df.empty:
            messagebox.showwarning("No Data", "No data available for trend analysis.")
            return
        
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['BMI'], marker='o', color='b', linestyle='-', markersize=6)
        plt.title("BMI Trend Over Time", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("BMI", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "No data available.")

window = tk.Tk()
window.title("BMI Calculator")

label_name = tk.Label(window, text="Enter your Name:")
label_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1, padx=10, pady=10)


label_weight = tk.Label(window, text="Enter your Weight (kg):")
label_weight.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry_weight = tk.Entry(window)
entry_weight.grid(row=1, column=1, padx=10, pady=10)

label_height = tk.Label(window, text="Enter your Height (m):")
label_height.grid(row=2, column=0, padx=10, pady=10, sticky="w")

entry_height = tk.Entry(window)
entry_height.grid(row=2, column=1, padx=10, pady=10)

label_result = tk.Label(window, text="BMI: ", font=("Arial", 14))
label_result.grid(row=3, column=0, columnspan=2, pady=10)

btn_calculate = tk.Button(window, text="Calculate BMI", command=calculate_bmi, bg="lightblue")
btn_calculate.grid(row=4, column=0, columnspan=2, pady=10)

btn_history = tk.Button(window, text="View History", command=show_history, bg="lightgreen")
btn_history.grid(row=5, column=0, columnspan=2, pady=10)

btn_trend = tk.Button(window, text="BMI Trend", command=show_trend, bg="lightyellow")
btn_trend.grid(row=6, column=0, columnspan=2, pady=10)

window.mainloop()
