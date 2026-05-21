import tkinter as tk

root = tk.Tk()
root.title("Todo List")
root.geometry("300x400")

tasks = []

def add():
    text = entry.get()
    if text:
        tasks.append(text)
        listbox.delete(0, tk.END)
        for t in tasks:
            listbox.insert(tk.END, t)
        entry.delete(0, tk.END)
        counter.config(text=f"Tasks: {len(tasks)}")

def delete():
    if listbox.curselection():
        index = listbox.curselection()[0]
        tasks.pop(index)
        listbox.delete(0, tk.END)
        for t in tasks:
            listbox.insert(tk.END, t)
        counter.config(text=f"Tasks: {len(tasks)}")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add", command=add)
add_btn.pack()

listbox = tk.Listbox(root, width=30, height=15)
listbox.pack(pady=10)

delete_btn = tk.Button(root, text="Delete", command=delete)
delete_btn.pack()

counter = tk.Label(root, text="Tasks: 0")
counter.pack(pady=10)

root.mainloop()