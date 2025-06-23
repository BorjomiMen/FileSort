# 🧹 File Sorter — Smart File Organizer  

A sleek and customizable **desktop file sorter** built with Python and `tkinter`. Automatically organizes files into categorized folders (Documents, Images, Music, etc.) based on file extensions. Perfect for decluttering your workspace with just one click!

---

## 🌟 Features  
- 📁 **Folder Selection**: Choose any directory to sort  
- 🔧 **Custom Rules**: Define file type → folder mappings (e.g., `.pdf → Documents`)  
- 📦 **Auto-Creation**: Automatically creates target folders if they don't exist  
- 📋 **Action Log**: Real-time log of all file movements  
- 📲 **System Notifications**: Alerts when sorting completes  
- 💾 **Persistent Settings**: Saves rules between sessions (`rules.json`)  
- ✂️ **Rule Management**: Add/remove sorting rules dynamically  

---

## 🛠️ Technologies Used  
- `tkinter` + `ttkthemes` for GUI  
- `plyer` for notifications  
- `shutil`/`os` for file ops  
- `json` for storage  

---

## 📦 Installation  
```bash
pip install plyer
```
# 🚀 How to Use
1) Clone the repo
2) Run python file_sorter.py
3) Select a folder to organize
4) Customize rules in the GUI
5) Click "Sort" and watch the magic happen!
