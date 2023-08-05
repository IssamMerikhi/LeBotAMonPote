import tkinter as tk
import tkinter.filedialog as filedialog
import subprocess
from tkinter import ttk
from ttkbootstrap import Style

class ClickgramApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Le Bot à mon Pote")
        self.geometry("400x400")

        # Créer une variable pour stocker le chemin du fichier sélectionné
        self.followers_file = ""

        # Créer le style ttkbootstrap
        style = Style(theme="flatly")  # Choisir le thème "flatly" (light mode green theme)

        # Afficher le titre
        title_label = ttk.Label(self, text="Le Bot à mon Pote", font=("Agency FB", 20), padding=10)
        title_label.pack()

        # Afficher les étapes
        steps_label = ttk.Label(self, text="Étapes :", font=("Agency FB", 14), padding=10)
        steps_label.pack(anchor=tk.W)

        # Créer le bouton "Parcourir" pour sélectionner le fichier avec le style personnalisé
        style.configure("Custom.TButton", background="#007bff", foreground="white", padding=10)

        file_frame = ttk.Frame(self)
        file_frame.pack(pady=10)

        step1_label = ttk.Label(file_frame, text="1. Choisir son fichier", font=("Agency FB", 12))
        step1_label.grid(row=0, column=0, padx=5)

        browse_button = ttk.Button(file_frame, text="Parcourir", command=self.browse_file, style="Custom.TButton")
        browse_button.grid(row=0, column=1, padx=5)

        # Créer les boutons pour les scripts avec le style personnalisé
        style.configure("Custom.TButton", background="#28a745", foreground="white", padding=10)

        step2_label = ttk.Label(self, text="2. Liker les stories ou Liker les posts", font=("Agency FB", 12), padding=10)
        step2_label.pack(anchor=tk.W)

        post_story_frame = ttk.Frame(self)
        post_story_frame.pack(pady=5)

        post_button = ttk.Button(post_story_frame, text="Liker les posts", command=self.like_posts, style="Custom.TButton")
        post_button.grid(row=0, column=0, padx=5)

        story_button = ttk.Button(post_story_frame, text="Liker les stories", command=self.like_stories, style="Custom.TButton")
        story_button.grid(row=0, column=1, padx=5)

        # Afficher le chemin du fichier sélectionné avec le style personnalisé
        self.file_label = ttk.Label(self, text="Fichier sélectionné : ", foreground="black", padding=10)
        self.file_label.pack()

    def browse_file(self):
        # Ouvrir une boîte de dialogue pour sélectionner le fichier
        self.followers_file = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        
        # Mettre à jour le texte du label avec le chemin du fichier sélectionné
        self.file_label.config(text="Fichier sélectionné : " + self.followers_file)

    def like_posts(self):
        # Exécuter le script like_post.py en tant que processus séparé en lui transmettant le chemin du fichier
        if self.followers_file:
            subprocess.run(["python", "like_post.py", self.followers_file])
        else:
            print("Veuillez sélectionner un fichier d'utilisateurs avant de continuer.")

    def like_stories(self):
        # Exécuter le script like_story.py en tant que processus séparé en lui transmettant le chemin du fichier
        if self.followers_file:
            subprocess.run(["python", "like_story.py", self.followers_file])
        else:
            print("Veuillez sélectionner un fichier d'utilisateurs avant de continuer.")

if __name__ == "__main__":
    app = ClickgramApp()
    app.mainloop()
