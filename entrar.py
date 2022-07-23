import ast
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import sqlite3


root = Tk()
root.title('Entrar')
root.geometry('400x400+750+250')
root.configure(bg="#fff")
root.resizable(False, False)


def entrar():
    username = usuario.get()
    password = senha.get()

    file = open('dados.txt', 'r')
    d = file.read()
    r = ast.literal_eval(d)
    file.close()
    
    
    if username in r.keys() and password == r[username]:
        root.iconify()

        menu = Toplevel(root)
        menu.title('Menu')
        menu.geometry('500x350+700+300')
        menu.configure(bg="#fff")
        menu.resizable(False, False)


        # ------------- CADASTRO PRODUTO ---------------------------------------------------------- #

        def chama_cadastro():
            db_name = 'cadastrados.db'

            wind = Tk()
            wind.geometry('410x380+750+290')
            wind.title('Cadastrar novo Produto')
            wind.configure(bg="#fff")
            wind.resizable(False, False)


            def run_query(query, parameters=()):
                with sqlite3.connect(db_name) as conn:
                    cursor = conn.cursor()
                    query_result = cursor.execute(query, parameters)
                    conn.commit()
                    return query_result

            def viewing_records():
                records = tree.get_children()
                for element in records:
                    tree.delete(element)
                query = 'SELECT * FROM product ORDER BY name DESC'
                db_rows = run_query(query)
                for row in db_rows:
                    tree.insert('', 0, text=row[1], values=row[2])

            def validar():
                return len(name.get()) != 0 and len(price.get()) != 0
                
            def adicionar():
                if validar():
                    query = 'INSERT INTO product VALUES(NULL,?,?)'
                    parameters = (name.get(), price.get())
                    run_query(query, parameters)
                    message['text'] = messagebox.showinfo('Registrar', '{} cadastrado com sucesso!'.format(name.get()))
                    name.delete(0, END)
                    price.delete(0, END)
                else:
                    message['text'] = messagebox.showerror('Error', 'Preecha todos os campos!')
                viewing_records()


            def deletar():
                try:
                    tree.item(tree.selection())['values'][0]
                except:
                    messagebox.showerror('Error', 'Por favor selecione um item para continuar')
                    return
                name = tree.item(tree.selection())['text']
                query = 'DELETE FROM product WHERE name=?'
                run_query(query, (name,))
                messagebox.showinfo('Deletado', '{} deletado com sucesso!'.format(name))
                viewing_records()

            frame = LabelFrame(wind, text='', border=0, background='white')
            frame.grid(row=0, column=0, columnspan=2, padx=100, pady=30)

            Label(frame, text='Nome: ', background='white').grid(row=1, column=0)
            name = Entry(frame)
            name.grid(row=1, column=1)

            Label(frame, text='Preço: ', background='white').grid(row=2, column=0)
            price = Entry(frame, width=20)
            price.grid(row=2, column=1)

            Button(frame, text='Cadastrar Produto', width=15, bg='blue', fg='white', border=0, command=adicionar).grid(row=3, column=1, pady=10)
            Button(wind, text='Deletar Produto', width=13, bg='blue', fg='white', border=0, command=deletar).place(x=160, y=110)

            message = Label(text='')
            message.grid(row=3, column=0)

            tree = ttk.Treeview(wind, height=10, column=2)
            tree.place(x=3, y=150)
            tree.heading('#0', text='Nome Produto', anchor=CENTER)
            tree.heading('#1', text='Preço Produto', anchor=CENTER)

            tree.column('#0', anchor=CENTER)
            tree.column('#1', anchor=CENTER)
            
            viewing_records()
            wind.mainloop()
        
        # ------------------------------------------------------------------------- #

        # ----------- CADASTRO VENDA ----------------------------------------------- #

        def chama_vendas():
            db_name = 'cadastrados.db'

            vendas = Tk()
            vendas.geometry('420x400+750+270')
            vendas.title('Vendas')
            vendas.configure(bg='#fff')
            vendas.resizable(False, False)

            def run_query(query, parameters=()):
                with sqlite3.connect(db_name) as conn:
                    cursor = conn.cursor()
                    query_result = cursor.execute(query, parameters)
                    conn.commit()
                    return query_result
            
            tree_frame = Frame(vendas)
            tree_frame.pack(pady=20)

            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=10, column=2)
            tree.heading('#0', text='Nome Produto', anchor=CENTER)
            tree.heading('#1', text='Preço Produto', anchor=CENTER)

            tree.column('#0', anchor=CENTER)
            tree.column('#1', anchor=CENTER)

            records = tree.get_children()
            for element in records:
                tree.delete(element)
            query = 'SELECT * FROM product ORDER BY name DESC'
            db_rows = run_query(query)
            for row in db_rows:
                tree.insert('', 0, text=row[1], values=row[2])    
            
            
            tree.pack()
            tree_scroll.config(command=tree.yview)

            def procurar():
                global search_entry, search

                search = Toplevel(vendas)
                search.title('Procurar Produtos')
                search.configure(bg='#fff')
                search.geometry('350x200+780+350')
                search.resizable(False, False)
                
                search_frame = LabelFrame(search, background='white', border=0)
                search_frame.pack(padx=10, pady=10)

                search_entry = Entry(search_frame, font=('Helvetica', 18))
                search_entry.pack(padx=20, pady=20)

                search_button = Button(search, text='Procurar', command=procurar_produto)
                search_button.pack(padx=20, pady=20)

            def procurar_produto():
                procurar = search_entry.get()
                search.destroy()

                for record in tree.get_children():
                    tree.delete(record)

                conn = sqlite3.connect('cadastrados.db')
                c = conn.cursor()
                c.execute("SELECT * FROM product WHERE name like ?", (procurar,))
                records = c.fetchall()
                global count
                count = 0

                for row in records:
                    tree.insert('', 0, text=row[1], values=row[2])
                
                conn.commit()
                conn.close()


        # ------------------------------------------------------------------------- #

            # -------------- NOVA VENDA -------------------------------------------------#
            def nova_venda():
                try:
                    tree.item(tree.selection())['values'][0]
                except:
                    messagebox.showerror('Error', 'Por favor selecione um item para continuar')
                name = tree.item(tree.selection())['text']
                preco = tree.item(tree.selection())['values'][0]

                nova_venda = Toplevel(vendas)
                nova_venda.title('Nova Venda')
                nova_venda.geometry('616x410+700+260')
                nova_venda.configure(bg='#fff')
                nova_venda.resizable(False, False)

                Label(nova_venda, text='Produto:', background='white').place(x=190, y=30)
                produto = Entry(nova_venda, bg='white', textvariable=StringVar(nova_venda, value=name))
                produto.place(x=250, y=30)
                
                Label(nova_venda, text='Preço:', background='white').place(x=190, y=60)
                preco2 = Entry(nova_venda, bg='white', textvariable=IntVar(nova_venda, value=preco))
                preco2.place(x=250, y=60)

                Label(nova_venda, text='Cliente:', background='white').place(x=190, y=90)
                cliente = Entry(nova_venda, bg='white')
                cliente.place(x=250, y=90)

                Label(nova_venda, text='Quantidade:', background='white').place(x=175, y=120)
                quantidade = Entry(nova_venda, bg='white')
                quantidade.place(x=250, y=120)

                database = 'vendas.db'

                
                def teste():
                    Label(nova_venda, text='Total:', background='white').place(x=190, y=150)
                    global n1
                    global n2
                    global s
                    global final

                    n1 = float(preco2.get())
                    n2 = int(quantidade.get())
                    s = n1 * n2
                    final = Entry(nova_venda, bg='white', textvariable=DoubleVar(nova_venda, value=s))
                    final.place(x=250, y=150)

                def run_query(query, parameters=()):
                    with sqlite3.connect(database) as conn:
                        cursor = conn.cursor()
                        query_result = cursor.execute(query, parameters)
                        conn.commit()
                        return query_result
                
                

                tree_vendas = ttk.Treeview(nova_venda, columns = ('#1','#2','#3', '#4', '#5'))
                tree_vendas['show'] = 'headings'
                tree_vendas.heading('#1', text='Cliente', anchor=CENTER)
                tree_vendas.heading('#2', text='Produto', anchor=CENTER)
                tree_vendas.heading('#3', text='Preço', anchor=CENTER)
                tree_vendas.heading('#4', text='Quantidade', anchor=CENTER)
                tree_vendas.heading('#5', text='Total', anchor=CENTER)
                
                tree_vendas.column('#1', anchor=CENTER)
                tree_vendas.column('#2', anchor=CENTER)
                tree_vendas.column('#3', anchor=CENTER, width=70)
                tree_vendas.column('#4', anchor=CENTER, width=70)
                tree_vendas.column('#5', anchor=CENTER, width=70)
    

                def viewing_records():
                    records = tree_vendas.get_children()
                    for element in records:
                        tree_vendas.delete(element)
                    query = 'SELECT * FROM vendido'
                    db_rows = run_query(query)
                    for row in db_rows:
                        tree_vendas.insert('', 'end', values=row)
                
                tree_vendas.place(x=2, y=180)

                def validar():
                    return len(cliente.get()) != 0 and len(quantidade.get()) != 0

                def adicionar():
                    if validar():
                        query = 'INSERT INTO vendido VALUES(?,?,?,?,?)'
                        parameters = (cliente.get(), produto.get(), preco2.get(), quantidade.get(), final.get())
                        run_query(query, parameters)
                        cliente.delete(0, END)
                        produto.delete(0, END)
                        preco2.delete(0, END)
                        quantidade.delete(0, END)
                        final.delete(0, END)
                    else:
                        messagebox.showerror('Error', 'Preecha todos os campos!')
                    viewing_records()

                calcular_compra = Button(nova_venda, text='Calcular Compra', command=teste)
                calcular_compra.place(x=400, y=80)
                
                registrar_venda_button = Button(nova_venda, text='Registrar Venda', command=adicionar)
                registrar_venda_button.place(x=403, y=110)


                viewing_records()
                nova_venda.mainloop() 

            Button(vendas, text='Nova Venda', command=nova_venda, border=0, width=10, height=2, background='black', fg='white').place(x=165, y=270)
            Button(vendas, text='Pesquisar Produto', command=procurar, border=0, width=15, height=2, background='black', fg='white').place(x=150, y=330)

            vendas.mainloop()
            # ----------------------------------------------------------------------------------------------------------- #

        def sair():
            root.destroy()
            menu.destroy()

        button_cadastrar = PhotoImage(file='imagens/button_cadastrar-produto.png')
        Button(menu, image=button_cadastrar, bg='white', border=0, command=chama_cadastro).place(x=10, y=70)

        button_vendas = PhotoImage(file='imagens/button_sistema-de-vendas.png')
        Button(menu, image=button_vendas, bg='white', border=0, command=chama_vendas).place(x=10, y=140)

        button_sair = PhotoImage(file='imagens/button_sair-do-sistema.png')
        Button(menu, image=button_sair, bg='white', border=0, command=sair).place(x=10, y=210)

        imagem = PhotoImage(file='imagens/mercado.png')
        Label(menu, image=imagem, bg='white').place(x=180, y=25)

        menu.mainloop()
    
    else:
        messagebox.showerror('Error', 'Usuário ou senha incorretos')

#############################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def comando_registrar():

    janela = Toplevel(root)
    janela.title('Registrar')
    janela.geometry('400x400+750+250')
    janela.configure(bg="#fff")
    janela.resizable(False, False)

    def registrar():
        username = usuario.get()
        password = senha.get()
        confirm_password = confirmar_senha.get()

        if password == confirm_password:
            try:
                file = open('dados.txt', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2={username:password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file = open('dados.txt', 'w')
                w = file.write(str(r))

                messagebox.showinfo('Registrar', 'Usuário registrado com sucesso!')
                janela.destroy()

            except:
                file = open('dados.txt', 'w')
                pp = str({'Usuario':'senha'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Error', 'A senhas não conferem')


    def entrar():
        janela.destroy()



    frame = Frame(janela, width=350, height=350, bg='white')
    frame.place(x=25, y=50)

    heading = Label(frame, text='Sistema de Registro', fg='#000000', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=30, y=5)

    # --------------------------------------------- Registrar User --------------------------------------------------------- #

    def on_enter(e):
        usuario.delete(0, 'end')


    def on_leave(e):
        if usuario.get() == '':
            usuario.insert(0, 'Usuário')

    entry_user = PhotoImage(file='imagens/imagem.png')
    entry_image = Label(frame,image=entry_user,border=20,bg='white')
    entry_image.place(x=35,y=70)

    usuario = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 10))
    usuario.place(x=67, y=92)
    usuario.insert(0, 'Usuário')
    usuario.bind("<FocusIn>", on_enter)
    usuario.bind("<FocusOut>", on_leave)


    # ----------------------------------------------------------------------------------------------------------------------- #
    # --------------------------------------------- Registrar Senha --------------------------------------------------------- #

    def on_enter(e):
        senha.delete(0, 'end')


    def on_leave(e):
        if senha.get() == '':
            senha.insert(0, 'Senha')

    entry_senha = PhotoImage(file='imagens/imagem.png')
    entry_image = Label(frame,image=entry_senha,border=20,bg='white')
    entry_image.place(x=35,y=120)

    senha = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 10))
    senha.place(x=67, y=142)
    senha.insert(0, 'Senha')
    senha.bind("<FocusIn>", on_enter)
    senha.bind("<FocusOut>", on_leave)


    # ----------------------------------------------------------------------------------------------------------------------- #
    # --------------------------------------------- Registrar Confirmar_Senha --------------------------------------------------------- #

    def on_enter(e):
        confirmar_senha.delete(0, 'end')


    def on_leave(e):
        if confirmar_senha.get() == '':
            confirmar_senha.insert(0, 'Confirmar senha')

    entry_confsenha = PhotoImage(file='imagens/imagem.png')
    entry_image = Label(frame,image=entry_confsenha,border=20,bg='white')
    entry_image.place(x=35,y=170)

    confirmar_senha = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 10))
    confirmar_senha.place(x=67, y=192)
    confirmar_senha.insert(0, 'Confirmar senha')
    confirmar_senha.bind("<FocusIn>", on_enter)
    confirmar_senha.bind("<FocusOut>", on_leave)


# ----------------------------------------------------------------------------------------------------------------------- #

    button_registro = PhotoImage(file='imagens/button_registrar.png')
    Button(frame, image=button_registro, bg='white', border=0, command=registrar).place(x=120, y=230)

    entrar = Button(frame, width=20, text="Entrar", border=0, bg='white', cursor='hand2', fg='blue', command=entrar)
    entrar.place(x=100, y=280)



    janela.mainloop()
  


############################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=25, y=55)

heading = Label(frame, text='Sistema de Login', fg='#000000', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=40, y=2)

#--------------------------------------- Logar Username --------------------------------------------#


def on_enter(e):
    usuario.delete(0, 'end')


def on_leave(e):
    name = usuario.get()
    if name == '':
        usuario.insert(0, 'Usuário')


entry_name = PhotoImage(file='imagens/imagem.png')
entry_image = Label(frame,image=entry_name,border=20,bg='white')
entry_image.place(x=35,y=70)

usuario = Entry(frame, width=27, border=0, font=('Microsoft YaHei UI Light', 10),)
usuario.place(x=65,y=92)
usuario.insert(0, 'Usuário ')
usuario.bind('<FocusIn>', on_enter)
usuario.bind('<FocusOut>', on_leave)


#-------------------------------------------------------------------------------------------------------#
#--------------------------------------- Logar Senha -------------------------------------------------#

def on_enter(e):
    senha.delete(0, 'end')


def on_leave(e):
    name = senha.get()
    if name == '':
        senha.insert(0, 'Senha')

entry_senha = PhotoImage(file='imagens/imagem.png')
entry_image2 = Label(frame,image=entry_senha,border=20,bg='white')
entry_image2.place(x=35,y=130)

senha = Entry(frame, show='*', width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 10))
senha.place(x=65, y=152)
senha.insert(0, 'Senha ')
senha.bind('<FocusIn>', on_enter)
senha.bind('<FocusOut>', on_leave)

#-------------------------------------------------------------------------------------------------------#

round = PhotoImage(file='imagens/button_login (1).png')
Button(frame, image=round, bg='white', border=0, command=entrar).place(x=120, y=190)

cadastrar = Button(frame, width=20, text='Cadastrar Usuario', border=0, bg='white', cursor='hand2', fg='blue', command=comando_registrar)
cadastrar.place(x=100, y=250)

root.mainloop()