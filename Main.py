import tkinter as tk
from tkinter import messagebox
import psycopg2

class PrincipalBD:
    def __init__(self, win):
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="1234", port="5433")
        self.comando = self.conn.cursor()

        self.lblNome = tk.Label(win, text='Seu Nome')
        self.lblCpf = tk.Label(win, text='CPF')
        self.lblNomeProd = tk.Label(win, text='Nome do Produto')
        self.lblPrecoAV = tk.Label(win, text='Preço do Produto À VISTA\n 10% de desconto')
        self.lblPrecoCC = tk.Label(win, text='Preço do Produto\nNO CREDITO\n(Atualizado Automaticamente)')

        self.txtNome = tk.Entry(win, bd=3)
        self.txtCpf = tk.Entry(win)
        self.txtNomeProd = tk.Entry(win)
        self.txtPrecoAV = tk.Entry(win)
        self.txtPrecoCC = tk.Entry(win)

        self.txtPrecoAV.bind('<FocusOut>', self.calcular_preco_cc)

        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)

        self.lblNome.grid(row=0, column=0)
        self.lblCpf.grid(row=1, column=0)
        self.lblNomeProd.grid(row=2, column=0)
        self.lblPrecoAV.grid(row=3, column=0)
        self.lblPrecoCC.grid(row=4, column=0)

        self.txtNome.grid(row=0, column=1)
        self.txtCpf.grid(row=1, column=1)
        self.txtNomeProd.grid(row=2, column=1)
        self.txtPrecoAV.grid(row=3, column=1)
        self.txtPrecoCC.grid(row=4, column=1)

        self.btnCadastrar.grid(row=5, column=0)
        self.btnAtualizar.grid(row=5, column=1)
        self.btnExcluir.grid(row=5, column=2)
        self.btnLimpar.grid(row=6, column=1)

        self.lblNome.place(x=100, y=50)
        self.txtNome.place(x=250, y=50)

        self.lblCpf.place(x=100, y=100)
        self.txtCpf.place(x=250, y=100)

        self.lblNomeProd.place(x=100, y=150)
        self.txtNomeProd.place(x=250, y=150)

        self.lblPrecoAV.place(x=100, y=200)
        self.txtPrecoAV.place(x=250, y=200)

        self.lblPrecoCC.place(x=100, y=250)
        self.txtPrecoCC.place(x=250, y=250)

        self.btnCadastrar.place(x=100, y=300)
        self.btnAtualizar.place(x=200, y=300)
        self.btnExcluir.place(x=300, y=300)
        self.btnLimpar.place(x=400, y=300)
        
        

    def fCadastrarProduto(self):
        nome = self.txtNome.get()
        cpf = self.txtCpf.get()
        nome_prod = self.txtNomeProd.get()
        preco_av = float(self.txtPrecoAV.get())
        preco_cc = float(self.txtPrecoCC.get())  

        try:
            self.conn.autocommit = False

            self.comando.execute("INSERT INTO Users (Nome, Cpf) VALUES (%s, %s)", (nome, cpf))
            self.conn.commit()

            self.comando.execute("INSERT INTO Products (NomeProd, PrecoAV, PrecoCC) VALUES (%s, %s, %s)", (nome_prod, preco_av, preco_cc))
            self.conn.commit()
        except Exception as e:
            print(f"Erro: {e}")
            self.conn.rollback()
        finally:
            self.conn.autocommit = True
            messagebox.showinfo("Seu Cadastro foi Realizado!")

    def fLimparTela(self):
        self.txtNome.delete(0, 'end')
        self.txtCpf.delete(0, 'end')
        self.txtNomeProd.delete(0, 'end')
        self.txtPrecoAV.delete(0, 'end')
        self.txtPrecoCC.delete(0, 'end')

    def calcular_preco_cc(self, event):
        try:
            preco_av = float(self.txtPrecoAV.get())
            preco_cc = preco_av * 1.1
            self.txtPrecoCC.delete(0, 'end')
            self.txtPrecoCC.insert(0, str(preco_cc))
        except ValueError:
            messagebox.showerror("ERRO", "Digite um valor válido para o Preço À Vista.")
            
    def fAtualizarProduto(self):
        try:
            nome_prod, preco_av, preco_cc = self.txtNomeProd.get(), float(self.txtPrecoAV.get()), float(self.txtPrecoCC.get())
            self.atualizarDados(nome_prod, preco_av, preco_cc)  # Chame o método atualizarDados com os argumentos corretos
            self.fLimparTela()
            print('Produto Atualizado com Sucesso!')
        except Exception as e:
            print(f'Erro ao atualizar o produto: {e}')

    def atualizarDados(self, nome_prod, preco_av, preco_cc):
        try:
            self.conn.autocommit = False
                
            self.comando.execute("UPDATE Products SET PrecoAV = %s, PrecoCC = %s WHERE NomeProd = %s", (preco_av, preco_cc, nome_prod))
            self.conn.commit()

            self.conn.autocommit = True
            messagebox.showinfo("Produto Atualizado com Sucesso!")
        except Exception as e:
            print(f"Erro: {e}")
            self.conn.rollback()
            messagebox.showerror("Erro", "Não foi possível atualizar o produto.")
            
        
    def fExcluirProduto(self):
        nome_prod = self.txtNomeProd.get()
        self.excluirDados(nome_prod)
        self.fLimparTela()
        print('Produto Excluído com Sucesso!')

    def excluirDados(self, nome_prod):
        try:
            self.conn.autocommit = False
            self.comando.execute("DELETE FROM Products WHERE NomeProd = %s", (nome_prod,))
            self.conn.commit()
            self.conn.autocommit = True
            messagebox.showinfo("Produto Excluído com Sucesso!")
        except Exception as e:
            print(f"Erro: {e}")
            self.conn.rollback()
            messagebox.showerror("Erro", "Não foi possível excluir o produto.")   

        
janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Bem Vindo ao PyProducts')
janela.geometry("800x400")
janela.mainloop()
