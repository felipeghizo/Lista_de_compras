import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk

class ShoppingListApp:
    def __init__(self, root):
        # Inicializa a janela principal
        self.root = root
        self.root.title("Lista de Compras")

        # Carrega a imagem e cria um objeto PhotoImage
        self.image = Image.open("Template_3.jpg")  # Substitua pelo caminho da sua imagem
        self.photo = ImageTk.PhotoImage(self.image)

        # Cria o widget Listbox para exibir a lista de itens
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(pady=20, padx=10)

        # Cria o widget Entry para entrada de novos itens com placeholder
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5, padx=10)

        # Adiciona o placeholder ao widget Entry
        self.placeholder = "Produto"
        self.entry.insert(0, self.placeholder)  # Insere o texto do placeholder
        self.entry.bind("<FocusIn>", self.remove_placeholder)  # Remove o placeholder ao focar
        self.entry.bind("<FocusOut>", self.add_placeholder)  # Adiciona o placeholder ao desfocar

        # Cria e posiciona os botões
        self.add_button = tk.Button(root, text="Adicionar", command=self.adicionar_item, width=20)
        self.add_button.pack(pady=5, padx=50)

        self.edit_button = tk.Button(root, text="Editar", command=self.editar_item, width=20)
        self.edit_button.pack(pady=5, padx=50)

        self.delete_button = tk.Button(root, text="Excluir", command=self.excluir_item, width=20)
        self.delete_button.pack(pady=5, padx=50)

        self.mark_button = tk.Button(root, text="Marcar como Comprado", command=self.marcar_item, width=20)
        self.mark_button.pack(pady=5, padx=50)

        # Atualiza o Listbox para mostrar "Lista vazia!" se estiver vazio
        self.update_listbox()

        # Configura a função para exibir a imagem em um popup ao fechar o programa
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_listbox(self):
        """Atualiza o Listbox para mostrar 'Lista vazia!' se estiver vazio."""
        if self.listbox.size() == 0:
            self.listbox.insert(tk.END, "Lista vazia!")

    def remove_placeholder(self, event):
        """Remove o texto do placeholder quando o campo ganha foco."""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)

    def add_placeholder(self, event):
        """Adiciona o texto do placeholder se o campo estiver vazio."""
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder)

    def adicionar_item(self):
        """Adiciona um item à lista, se não estiver vazio e não for um placeholder."""
        item = self.entry.get()
        if item and item != self.placeholder:
            # Verifica se o item já está na lista
            for i in range(self.listbox.size()):
                if self.listbox.get(i) == item:
                    messagebox.showwarning("Item já existe", "Este item já está na lista!")
                    return

            # Remove "Lista vazia!" se houver itens
            if self.listbox.size() == 1 and self.listbox.get(0) == "Lista vazia!":
                self.listbox.delete(0)

            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END)  # Limpa o campo de entrada

    def editar_item(self):
        """Edita o item selecionado na lista."""
        selected_item_index = self.listbox.curselection()
        if selected_item_index:
            item = self.listbox.get(selected_item_index)
            if item == "Lista vazia!":
                messagebox.showwarning("Não pode editar", "Não é possível editar o item 'Lista vazia!'")
                return

            # Solicita o novo valor do item
            new_item = simpledialog.askstring("Editar Item", "Novo valor:")
            if new_item:
                # Verifica se o novo item já está na lista
                for i in range(self.listbox.size()):
                    if self.listbox.get(i) == new_item:
                        messagebox.showwarning("Item já existe", "Este item já está na lista!")
                        return

                self.listbox.delete(selected_item_index)
                self.listbox.insert(selected_item_index, new_item)

    def excluir_item(self):
        """Exclui o item selecionado da lista."""
        selected_item_index = self.listbox.curselection()
        if selected_item_index:
            if self.listbox.get(selected_item_index) == "Lista vazia!":
                messagebox.showwarning("Não pode excluir", "Não é possível excluir o item 'Lista vazia!'")
                return

            self.listbox.delete(selected_item_index)
            # Verifica se a lista está vazia para adicionar "Lista vazia!"
            if self.listbox.size() == 0:
                self.update_listbox()

    def marcar_item(self):
        """Marca o item selecionado como 'Comprado'."""
        selected_item_index = self.listbox.curselection()
        if selected_item_index:
            item = self.listbox.get(selected_item_index)
            if item == "Lista vazia!":
                messagebox.showwarning("Não pode marcar", "Não é possível marcar o item 'Lista vazia!'")
                return

            # Adiciona a tag "(Comprado)" ao item selecionado
            if "(Comprado)" not in item:
                self.listbox.delete(selected_item_index)
                self.listbox.insert(selected_item_index, item + " (Comprado)")

    def on_closing(self):
        """Função chamada quando a janela principal está prestes a ser fechada."""
        # Cria uma nova janela para exibir a imagem
        popup = tk.Toplevel(self.root)
        popup.title("Imagem")
        
        # Adiciona a imagem ao popup
        img_label = tk.Label(popup, image=self.photo)
        img_label.pack(pady=10)

        # Adiciona um botão para fechar o popup
        close_button = tk.Button(popup, text="Fechar", command=self.root.destroy)
        close_button.pack(pady=10)
        
        # Impede que o popup seja fechado sem clicar no botão "Fechar"
        popup.grab_set()

if __name__ == "__main__":
    # Inicializa a aplicação
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()
