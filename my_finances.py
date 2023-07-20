from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from funcoes import Funcs

janela_login = Tk()


class Application(Funcs):

    def __init__(self):
        # Variaveis - cores
        self.cor_verde1 = '#014040'
        self.cor_laranja = '#F28C0F'
        self.cor_verde2 = '#02735E'

        self.janela_login = janela_login
        self.criar_table()
        self.login()
        self.janela_login.mainloop()

    # Login Page
    def login(self):
        self.janela_login.title("MyFinances - Gestor Financeiro")
        # ajustar linhas e colunas automaticamente a tela
        self.janela_login.rowconfigure(0, weight=1)
        self.janela_login.columnconfigure([0, 1,], weight=1)
        self.janela_login.geometry("800x600")
        self.janela_login.configure(bg="#ffffff")
        self.janela_login.resizable(False, False)

        self.canvas = Canvas(bg="#ffffff", height=600, width=800,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.background_img = PhotoImage(file=f"imagens/bg_login.png")
        self.canvas.create_image(400.0, 266.0, image=self.background_img)

        # Widgets
        self.ent_login = Entry(font=("ivy", 18, "bold"), bd=0, bg="white", fg='black',
                               highlightthickness=0)

        self.ent_login.place(x=200, y=363, width=400, height=46)

        self.ent_senha = Entry(font=("ivy", 18, "bold"), bd=0, bg="white", fg='black',
                               highlightthickness=0, show="*")

        self.ent_senha.place(x=200, y=454, width=400, height=46)

        # criando Botões
        self.btn_login = Button(text='Login', relief="ridge", bg=self.cor_verde1, fg='White',
                                font=("ivy", 16, "bold"), command=self.janela_home)

        self.btn_login.place(x=200, y=530, width=185, height=52)

        self.btn_cadastro = Button(text='Cadastrar', relief="ridge", bg=self.cor_verde1, fg='White',
                                   font=("ivy", 16, "bold"), command=self.janela_cadastro)

        self.btn_cadastro.place(x=415, y=530, width=185, height=52)

    # Cadastro Page
    def cadastro(self):
        self.janela_cadastro = Tk()
        self.janela_cadastro.title("MyFinances - Cadastro do Usuário")
        self.janela_cadastro.rowconfigure(0, weight=1)
        self.janela_cadastro.columnconfigure([0, 1,], weight=1)
        self.janela_cadastro.geometry("800x600")
        self.janela_cadastro.configure(bg="#ffffff")
        self.janela_cadastro.resizable(False, False)

        self.canvas = Canvas(bg="#ffffff", height=600,
                             width=800, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"imagens/bg_cadastro.png")
        self.background = self.canvas.create_image(400.0, 300.0,
                                                   image=self.background_img)

        # Widgets
        self.ent_user = Entry(font=("ivy", 18, "bold"), bd=0, bg='white',
                              fg='black', highlightthickness=0)
        self.ent_user.place(x=22, y=245, width=368, height=46)

        self.ent_senha = Entry(font=("ivy", 18, "bold"), bd=0, bg='white',
                               fg='black', highlightthickness=0)
        self.ent_senha.place(x=415, y=245, width=363, height=46)

        self.ent_nome = Entry(font=("ivy", 18, "bold"), bd=0, bg='white',
                              fg='black', highlightthickness=0)
        self.ent_nome.place(x=22, y=338, width=756, height=46)

        self.ent_renda = Entry(font=("ivy", 18, "bold"), bd=0, bg='white',
                               fg='black', highlightthickness=0)
        self.ent_renda.place(x=22, y=431, width=368, height=46)

        # carregar informações do banco dados
        self.carrega_usuario()

        # Botões
        self.btn_salvar = Button(text='Salvar', relief="raised", bg=self.cor_verde1, fg='White',
                                 font=("ivy", 16, "bold"), command=self.editar_usuario)

        self.btn_salvar.place(x=415, y=530, width=185, height=52)

        self.btn_OK = Button(text='OK', relief="raised", bg=self.cor_verde1, fg='White',
                             font=("ivy", 16, "bold"), command=self.janela_home_cad)

        self.btn_OK.place(x=200, y=530, width=185, height=52)

    # Home Page
    def home(self):
        self.janela_home = Tk()
        self.janela_home.title("MyFinances - Status")
        self.janela_home.rowconfigure(0, weight=1)
        self.janela_home.columnconfigure([0, 1,], weight=1)
        self.janela_home.geometry("800x600")
        self.janela_home.configure(bg="#ffffff")
        self.janela_home.resizable(False, False)

        self.canvas = Canvas(bg="#ffffff", height=600,
                             width=800, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background_img = PhotoImage(file=f"imagens/bg_home.png")
        self.canvas.create_image(383.0, 291.5, image=self.background_img)

        # Widgets
        self.ent_renda = Entry(bd=2, bg=self.cor_laranja, fg='black',
                               highlightthickness=0, font=("ivy", 14, "bold"), justify='right')
        self.ent_renda.place(x=377, y=36, width=165, height=24)

        self.ent_total = Entry(bd=2, bg=self.cor_laranja, fg='black',
                               highlightthickness=0, font=("ivy", 14, "bold"), justify='right')
        self.ent_total.place(x=377, y=70, width=165, height=24)

        self.ent_superavit = Entry(bd=2, bg=self.cor_laranja, fg='black',
                                   highlightthickness=0, font=("ivy", 14, "bold"), justify='right')
        self.ent_superavit.place(x=377, y=104, width=165, height=24)

        self.ent_inicial = DateEntry(day=1, locale='pt_br')
        self.ent_inicial.place(x=570, y=52, width=208, height=24)

        self.ent_final = DateEntry(locale='pt_br')
        self.ent_final.place(x=570, y=104, width=208, height=24)

        # Scroll - Treeview
        self.lst_lancamentos = ttk.Treeview(
                                columns=("id", "data", "categoria", "valor"), 
                                show='headings', selectmode='browse')
        # definir tamanho de cada coluna
        self.lst_lancamentos.column("id", width=15)
        self.lst_lancamentos.column("data", width=85)
        self.lst_lancamentos.column("categoria", width=180)
        self.lst_lancamentos.column("valor", width=95)
        # nomear o cabeçalho de cada coluna
        self.lst_lancamentos.heading("id", text="ID")
        self.lst_lancamentos.heading("data", text="DATA")
        self.lst_lancamentos.heading("categoria", text="CATEGORIA")
        self.lst_lancamentos.heading("valor", text="VALOR")
        # colocar lst_lançamentos na tela
        self.lst_lancamentos.place(x=17, y=175, width=383, height=410)
        # criar barras de rolagem
        self.scroll_vertical = Scrollbar(orient='vertical', command=self.lst_lancamentos.yview)
        self.lst_lancamentos.configure(yscroll=self.scroll_vertical.set)
        self.scroll_vertical.place(x=400, y=175, width=20, height=410)

        # inserir o Bind pra duplo clique
        self.lst_lancamentos.bind("<Double-1>", self.double_click)

        # entry novo lancamento
        self.lbl_data = Label(text='Data:', bg="#135725", fg="white",
                              font=("ivy", 14, "bold"))
        self.lbl_data.place(x=440, y=410)
        self.ent_data = DateEntry(year=2023, locale='pt_br')
        self.ent_data.place(x=440, y=440, width=276, height=24)

        self.lbl_categoria = Label(text='Categoria:', bg="#135725", fg="white",
                                   font=("ivy", 14, "bold"))
        self.lbl_categoria.place(x=440, y=470)
        self.lista_categorias = ['Sálario/Renda(Extra)', 'Dízimo/Oferta', 'Impostos',
                                 'Moradia', 'Alimentação', 'Transporte', 'Seguros', 'Dívidas',
                                 'Entretenimento/Lazer', 'Vestuário', 'Poupança', 'Saúde',
                                 'Diversos', 'Investimentos', 'Educação']
        self.cbb_categoria = ttk.Combobox(values=self.lista_categorias,
                                          font=("ivy", 14, "bold"))
        self.cbb_categoria.place(x=440, y=500, width=276, height=24)

        self.lbl_valor = Label(text='Valor:', bg="#135725", fg="white",
                               font=("ivy", 14, "bold"))
        self.lbl_valor.place(x=440, y=530)
        self.ent_valor = Entry(font=("ivy", 16, "bold"), bd=0, bg="#ffffff",
                               fg='#000000', highlightthickness=0)
        self.ent_valor.place(x=440, y=560, width=276, height=24)

        # Scroll Treview - comparativo orçado - real
        self.lst_comparativo = ttk.Treeview(
                                columns=("categoria", "orçado", "real", "diferença"), 
                                show='headings', selectmode='browse')
        # definir tamanho de cada coluna
        self.lst_comparativo.column("categoria", width=90)
        self.lst_comparativo.column("orçado", width=40)
        self.lst_comparativo.column("real", width=40)
        self.lst_comparativo.column("diferença", width=50)
        # nomear o cabeçalho de cada coluna
        self.lst_comparativo.heading("categoria", text="CATEGORIA")
        self.lst_comparativo.heading("orçado", text="ORÇADO")
        self.lst_comparativo.heading("real", text="REAL")
        self.lst_comparativo.heading("diferença", text="DIFERENÇA")
        # colocar lst_lançamentos na tela
        self.lst_comparativo.place(x=440, y=175, width=325, height=230)
        # criar barras de rolagem
        self.scroll_vertical = Scrollbar(orient='vertical', command=self.lst_comparativo.yview)
        self.lst_comparativo.configure(yscroll=self.scroll_vertical.set)
        self.scroll_vertical.place(x=765, y=175, width=20, height=230)

        # Botões
        self.img1 = PhotoImage(file=f"icones/botao_add_pq.png")
        self.btn_add = Button(image=self.img1, borderwidth=0,
                              highlightthickness=0, command=self.adicionar,
                              relief="flat")
        self.btn_add.place(x=730, y=410, width=55, height=55)

        self.img2 = PhotoImage(file=f"icones/botao_editar_pq.png")
        self.btn_editar = Button(image=self.img2, borderwidth=0,
                                 highlightthickness=0, command=self.editar,
                                 relief="flat")
        self.btn_editar.place(x=730, y=470, width=55, height=55)

        self.img0 = PhotoImage(file=f"icones/botao_excluir_pq.png")
        self.btn_deletar = Button(image=self.img0, borderwidth=0,
                                  highlightthickness=0, command=self.deletar,
                                  relief="flat")
        self.btn_deletar.place(x=730, y=530, width=55, height=55)

        self.btn_filtrar = Button(text='Filtrar', relief="raised", bg=self.cor_laranja, fg='black',
                                  font=("ivy", 10, "bold"), command=self.filtrar)
        self.btn_filtrar.place(x=570, y=130, width=80, height=20)

        # preenche a lista de lançamentos
        self.select_lista()
        # cria a lista dos valores orçados
        self.guia_percentual()
        # preenche a lista de comparativos
        self.select_comparativo()


Application()
