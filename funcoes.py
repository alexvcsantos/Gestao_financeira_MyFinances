from tkinter import messagebox
import sqlite3


# classe com todas funções
class Funcs():

    ############################# Funções Banco de Dados ##############################
    # função conectar banco de dados
    def conecta_bd(self):
        self.con = sqlite3.connect("myfinances.bd")
        self.cursor = self.con.cursor()
        print("Conectando ao Banco de Dados")

    # função desconectar banco de dados
    def desconecta_bd(self):
        self.con.close()
        print("Desconectando do Banco de Dados")

    # Criar tabelas no banco de dados
    def criar_table(self):
        self.conecta_bd()
        # Criar tabela usuarios
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id_usuario INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                renda_mensal REAL NOT NULL
            );
        """)
        self.con.commit()

        # Criar tabela lancamentos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lancamentos(
                id_lancamento INTEGER PRIMARY KEY,
                data TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                id_usuario INTEGER,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
        self.con.commit()

        # Criar tabela Guia
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS guia_percent(
                id_guia_percent INTEGER PRIMARY KEY,
                aliquota_ir REAL,
                renda_bruta_anual REAL,
                dizimo_oferta REAL,
                impostos REAL,
                Renda_liquida REAL,
                moradia REAL,
                alimentacao REAL,
                transporte REAL,
                seguros REAL,
                dividas REAL,
                entretenimento_lazer REAL,
                vestuario REAL,
                poupanca REAL,
                saude REAL,
                diversos REAL,
                investimentos REAL,
                educacao REAL,
                id_usuario INTEGER,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
        self.con.commit()
        print("Banco de Dados criado")
        self.desconecta_bd()

    ############################# Funções converter moedas ##############################

    def real_br_money_mask(self, valor):    
        valor = "R$ {:,.2f}".format(valor).replace(',', '_').replace('.', ',').replace('_', '.')
        return valor

    def us_money_mask(self, valor):
        valor = float(str(format(valor).replace('R$ ', '').replace(',', '_').replace('.', '').replace('_', '.')))
        return valor

    ############################# Funções Info Janelas ##############################
    # função mudar da tela login para tela cadastro
    def janela_cadastro(self):
        self.usuario = self.ent_login.get()
        self.senha = self.ent_senha.get()
        if self.usuario != "" and self.senha != "":
            # chama função verificar_usuario
            if self.verificar_usuario(self.usuario, self.senha):
                self.janela_login.destroy()
                # chama o função cadastro
                self.cadastro()
            else:
                messagebox.showinfo(title='ERRO',
                                    message="Usuário ou Senha Inválido.")
        else:
            messagebox.showinfo(title='ERRO',
                                message="Usuário Inicial admin, Senha inicial admin. Clique no botão Cadastrar para alterar - Usuário e Senha.")

    # função mudar da tela login para tela home
    def janela_home(self):
        self.usuario = self.ent_login.get()
        self.senha = self.ent_senha.get()
        if self.usuario != "" and self.senha != "":
            # chama função verificar_usuario
            if self.verificar_usuario(self.usuario, self.senha):
                self.janela_login.destroy()
                self.home()
            else:
                messagebox.showinfo(title='ERRO',
                                    message="Usuário ou Senha Inválido.")
        else:
            messagebox.showinfo(title='ERRO',
                                message="Clique no botão Cadastrar para incluir - Usuário e Senha.")

    # função sai da tela cadastro entra na tela login
    def janela_home_cad(self):
        self.janela_cadastro.destroy()
        self.home()

    # função limpar campos de lançamentos
    def limpa_tela(self):
        self.ent_data.delete(0, 'end')
        self.cbb_categoria.delete(0, 'end')
        self.ent_valor.delete(0, 'end')

    ############################# Funções Info Usuário ##############################
    # carregar informações do usuário banco de dados
    def carrega_usuario(self):
        self.conecta_bd()
        dados_usuario = self.cursor.execute(""" SELECT * FROM usuarios """)
        # verificar se ja tem algum usuario no sistema
        if list(dados_usuario) == []:
            # Cria o usuário admin padrão
            self.cursor.execute(""" INSERT INTO usuarios (id_usuario, usuario, senha, nome_completo, renda_mensal)
                                VALUES ('1', 'admin', 'admin', 'Administrador', '10000')""")
            self.con.commit()

        dados_usuario = self.cursor.execute(""" SELECT * FROM usuarios """)
        for self.id, self.usuario, self.senha, self.nome, self.renda in dados_usuario:
            self.limpa_usuario()

            self.ent_user.insert(0, self.usuario)
            self.ent_senha.insert(0, self.senha)
            self.ent_nome.insert(0, self.nome)
            self.ent_renda.insert(0, self.renda)

        self.desconecta_bd()

    # função editar Usuario
    def editar_usuario(self, *args):
        self.usuario = self.ent_user.get()
        self.senha = self.ent_senha.get()
        self.nome = self.ent_nome.get()
        self.renda = self.ent_renda.get()

        self.conecta_bd()
        self.cursor.execute(""" UPDATE usuarios SET usuario = ?, senha = ?, nome_completo = ?, renda_mensal = ?
                                WHERE id_usuario = ? """, (self.usuario, self.senha, self.nome, self.renda, self.id))

        self.con.commit()
        self.desconecta_bd()

    # função verificar usuario e senha
    def verificar_usuario(self, usuario, senha):
        self.conecta_bd()
        login = self.cursor.execute(""" SELECT usuario, senha FROM usuarios""")

        for i in login:
            if usuario == i[0] and senha == i[1]:
                check = True
            else:
                check = False
        self.con.commit()
        self.desconecta_bd()
        return check

    # função limpar campos de usuário
    def limpa_usuario(self):
        self.ent_user.delete(0, 'end')
        self.ent_senha.delete(0, 'end')
        self.ent_nome.delete(0, 'end')
        self.ent_renda.delete(0, 'end')

    ########################### Funções Info % Gastos Orçado ############################
    # Método para definir valores em % por categoria gastável
    def guia_percentual(self):
        self.conecta_bd()
        consulta = list(self.cursor.execute(
            ''' SELECT renda_mensal FROM usuarios '''))
        for renda in consulta:
            self.renda = renda[0]
        self.desconecta_bd()

        self.renda_anual = self.renda * 12

        # calcular dizimo 10%
        self.dizimo = round(self.renda * 0.1, 2)
        '''
        Aliquotas imposto de renda:
        Renda até R$ 1.903,98: isento de imposto de renda;
        Renda entre R$ 1.903,99 e R$ 2.826,65: alíquota de 7,5%;
        Renda entre R$ 2.826,66 e R$ 3.751,05: alíquota de 15%;
        Renda entre R$ 3.751,06 e R$ 4.664,68: alíquota de 22,5%;
        Renda acima de R$ 4.664,68: alíquota máxima de 27,5%.
        '''
        # aliquotas de imposto de renda
        aliquotas_ir = [0, 0.075, 0.15, 0.225, 0.275]
        # salario limite por aliquotas de IR
        renda_ir = [1903.38, 2826.65, 3751.05, 4664.68, 1000000]
        # renda_anual_ir = list(map(lambda preco: round((preco * 12), 2), renda_ir))
        # tabela de percentual gastos, conforme renda, IR, calcula em cima da renda liquida
        guia_percent = {'Moradia': [0.38, 0.37, 0.35, 0.32, 0.3],
                        'Alimentação': [0.19, 0.15, 0.12, 0.12, 0.12],
                        'Transporte': [0.15, 0.15, 0.12, 0.12, 0.12],
                        'Seguros': [0.02, 0.04, 0.05, 0.05, 0.05],
                        'Dívidas': [0.05, 0.05, 0.05, 0.05, 0.05],
                        'Entretenimento/Lazer': [0.02, 0.03, 0.05, 0.05, 0.06],
                        'Vestuário': [0.04, 0.04, 0.05, 0.05, 0.05],
                        'Poupança': [0.02, 0.04, 0.04, 0.05, 0.05],
                        'Saúde': [0.04, 0.04, 0.05, 0.05, 0.05],
                        'Diversos': [0.03, 0.04, 0.04, 0.05, 0.06],
                        'Investimentos': [0, 0, 0.03, 0.04, 0.04],
                        'Educação': [0.06, 0.05, 0.05, 0.05, 0.05]}

        # Verificar a faixa do imposto de renda
        index_ir = 0
        for i, item in enumerate(renda_ir):
            if self.renda <= item:
                index_ir = i
        # calcular imposto, renda liquida
        self.aliquota = round(aliquotas_ir[index_ir] * 100, 2)
        self.imposto = round(self.renda * aliquotas_ir[index_ir], 2)
        self.renda_liquida_mensal = round(
            self.renda - self.dizimo - self.imposto, 2)

        # calcular gastos por categoria conforme renda
        self.moradia = self.renda_liquida_mensal * \
            guia_percent['Moradia'][index_ir]
        self.alimentacao = self.renda_liquida_mensal * \
            guia_percent['Alimentação'][index_ir]
        self.transporte = self.renda_liquida_mensal * \
            guia_percent['Transporte'][index_ir]
        self.seguro = self.renda_liquida_mensal * \
            guia_percent['Seguros'][index_ir]
        self.divida = self.renda_liquida_mensal * \
            guia_percent['Dívidas'][index_ir]
        self.lazer = self.renda_liquida_mensal * \
            guia_percent['Entretenimento/Lazer'][index_ir]
        self.vestuario = self.renda_liquida_mensal * \
            guia_percent['Vestuário'][index_ir]
        self.poupanca = self.renda_liquida_mensal * \
            guia_percent['Poupança'][index_ir]
        self.saude = self.renda_liquida_mensal * \
            guia_percent['Saúde'][index_ir]
        self.diversos = self.renda_liquida_mensal * \
            guia_percent['Diversos'][index_ir]
        self.investimento = self.renda_liquida_mensal * \
            guia_percent['Investimentos'][index_ir]
        self.educacao = self.renda_liquida_mensal * \
            guia_percent['Educação'][index_ir]

        self.conecta_bd()
        dados_guia = self.cursor.execute(""" SELECT * FROM guia_percent """)
        # verificar se ja tem guia percentual preenchida
        if list(dados_guia) == []:
            # criar tabela com os valores orçados
            self.cursor.execute(""" INSERT INTO guia_percent (id_guia_percent, aliquota_ir, renda_bruta_anual, 
                                dizimo_oferta, impostos, Renda_liquida, moradia, alimentacao, transporte, 
                                seguros, dividas, entretenimento_lazer, vestuario, poupanca, saude, diversos,
                                investimentos, educacao, id_usuario) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
                                (1, self.aliquota, self.renda_anual, self.dizimo, self.imposto, self.renda_liquida_mensal,
                                 self.moradia, self.alimentacao, self.transporte, self.seguro, self.divida, self.lazer,
                                 self.vestuario, self.poupanca, self.saude, self.diversos, self.investimento, self.educacao, 1))
        # atualiza os valores guia percentual
        self.cursor.execute(""" UPDATE guia_percent SET aliquota_ir = ?, renda_bruta_anual = ?, dizimo_oferta = ?, 
                                impostos = ?, Renda_liquida = ?, moradia = ?, alimentacao = ?, transporte = ?, 
                                seguros = ?, dividas = ?, entretenimento_lazer = ?, vestuario = ?, poupanca = ?, saude = ?, 
                                diversos = ?, investimentos = ?, educacao = ? WHERE id_guia_percent = ? """,
                            (self.aliquota, self.renda_anual, self.dizimo, self.imposto, self.renda_liquida_mensal,
                             self.moradia, self.alimentacao, self.transporte, self.seguro, self.divida, self.lazer,
                             self.vestuario, self.poupanca, self.saude, self.diversos, self.investimento, self.educacao, 1))
        self.con.commit()
        self.desconecta_bd()
        # self.select_lista()

    ############################# Funções Info Lançamentos ##############################
    # parametro event - é necessário pra usar Bind
    # função para selecionar o item com duplo clique
    def double_click(self, event):
        self.limpa_tela()
        # pega o indice selecionado
        item_selecionado = self.lst_lancamentos.selection()[0]
        # retorna uma tupla com valores do item selecionado
        valores = self.lst_lancamentos.item(item_selecionado, "values")
        self.codigo = valores[0]
        self.ent_data.insert('end', valores[1])
        self.cbb_categoria.insert('end', valores[2])
        self.ent_valor.insert('end', valores[3])

    # função adicionar lançamento
    def adicionar(self):
        self.codigo = ''
        self.data = self.ent_data.get_date()
        self.categoria = self.cbb_categoria.get()
        self.valor = self.ent_valor.get()
        self.valor = self.us_money_mask(self.valor)

        if self.data == "" or self.categoria == "" or self.valor == "":
            messagebox.showinfo(title='ERRO',
                                message="Digite todos os valores")
            return

        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO lancamentos (data, categoria, valor, id_usuario)
            VALUES (?, ?, ?, ?)""", (self.data, self.categoria, self.valor, 1))

        self.con.commit()
        self.desconecta_bd()
        self.select_lista()
        self.select_comparativo()
        self.limpa_tela()
        # self.ent_data.focus() # posiciona o cursor neste item

    # função deletar lançamentos
    def deletar(self):
        item_selecionado = self.lst_lancamentos.selection()[0]
        valores = self.lst_lancamentos.item(item_selecionado, "values")
        self.codigo = valores[0]

        self.conecta_bd()
        self.cursor.execute(" DELETE FROM lancamentos WHERE id_lancamento = ? ",
                            (self.codigo,))
        self.con.commit()
        self.desconecta_bd()

        self.limpa_tela()
        self.select_lista()
        self.select_comparativo()

    # função editar lançamentos
    def editar(self, *args):
        self.data = self.ent_data.get_date()
        self.categoria = self.cbb_categoria.get()
        self.valor = self.us_money_mask(self.ent_valor.get())

        self.conecta_bd()
        self.cursor.execute(""" UPDATE lancamentos SET data = ?, categoria = ?, valor = ?
                            WHERE id_lancamento = ? """, (self.data, self.categoria, self.valor, self.codigo))
        self.con.commit()
        self.desconecta_bd()

        self.select_lista()
        self.select_comparativo()
        self.limpa_tela()

    # função preencher a lista de lançamentos
    def select_lista(self):
        # apagar todos itens da lst_lancamentos
        self.lst_lancamentos.delete(*self.lst_lancamentos.get_children())
        self.conecta_bd()

        dt_inicial = self.ent_inicial.get_date()
        dt_final = self.ent_final.get_date()
        lista = self.cursor.execute(f""" SELECT id_lancamento, data, categoria, valor FROM lancamentos
                    WHERE data BETWEEN '{dt_inicial}' AND '{dt_final}' ORDER BY data """)

        for i in lista:
            i = (i[0], i[1], i[2], self.real_br_money_mask(i[3]))
            self.lst_lancamentos.insert("", "end", values=i)

        self.desconecta_bd()

        # atualiza total renda
        self.total_renda()
        # atualiza total despesa
        self.total_despesas()
        # Atualiza Superavit/Deficit
        self.ent_superavit.delete(0, 'end')
        total = self.us_money_mask(self.ent_renda.get()) - self.us_money_mask(self.ent_total.get())
        total = self.real_br_money_mask(total)
        self.ent_superavit.insert(1, total)

    # função calcular total Rendimentos
    def total_renda(self):
        self.ent_renda.delete(0, 'end')

        self.conecta_bd()
        dt_inicial = self.ent_inicial.get_date()
        dt_final = self.ent_final.get_date()
        rendas = self.cursor.execute(f""" SELECT valor FROM lancamentos 
                                    WHERE categoria = 'Sálario/Renda(Extra)' 
                                    AND data BETWEEN '{dt_inicial}' AND '{dt_final}' """)
        total = 0
        for renda in rendas:
            res = float(str(renda).replace(
                        ',', '').replace('(', '').replace(')', ''))
            total += res

        self.ent_renda.insert(1, self.real_br_money_mask(total))
        self.desconecta_bd()

    # função calcular total Despesas
    def total_despesas(self):
        self.ent_total.delete(0, 'end')

        self.conecta_bd()
        dt_inicial = self.ent_inicial.get_date()
        dt_final = self.ent_final.get_date()
        rendas = self.cursor.execute(f""" SELECT valor FROM lancamentos 
                                    WHERE categoria <> 'Sálario/Renda(Extra)' 
                                    AND data BETWEEN '{dt_inicial}' AND '{dt_final}' """)
        total = 0
        for renda in rendas:
            res = float(str(renda).replace(
                        ',', '').replace('(', '').replace(')', ''))
            total += res

        self.ent_total.insert(1, self.real_br_money_mask(total))
        self.desconecta_bd()

    # função preencher a lista de valores orçados x real
    def select_comparativo(self):
        # apagar todos itens da lst_comparativo
        self.lst_comparativo.delete(*self.lst_comparativo.get_children())
        self.conecta_bd()

        dt_inicial = self.ent_inicial.get_date()
        dt_final = self.ent_final.get_date()

        # pegar valores orçado
        valores_guia_percent = self.cursor.execute(f""" SELECT            
                                                        renda_bruta_anual/12,
                                                        dizimo_oferta,
                                                        impostos,
                                                        moradia,
                                                        alimentacao,
                                                        transporte,
                                                        seguros,
                                                        dividas,
                                                        entretenimento_lazer,
                                                        vestuario,
                                                        poupanca,
                                                        saude,
                                                        diversos,
                                                        investimentos,
                                                        educacao
                                                    FROM guia_percent """)
        valores_guia_percent = list(valores_guia_percent)

        # Criar dict comparando valores orçado, real, diferença
        tabela_comparativo = {'Sálario/Renda(Extra)': [], 'Dízimo/Oferta': [], 'Impostos': [],
                              'Moradia': [], 'Alimentação': [],
                              'Transporte': [], 'Seguros': [], 'Dívidas': [],
                              'Entretenimento/Lazer': [], 'Vestuário': [], 'Poupança': [],
                              'Saúde': [], 'Diversos': [], 'Investimentos': [], 'Educação': []}

        # gerar valores dict comparativo
        i = 0
        lista_valores = []
        for categoria in tabela_comparativo.keys():
            # pegar valor total lançamentos por categoria
            valor = self.cursor.execute(f""" SELECT sum(valor) FROM lancamentos
                                            WHERE data BETWEEN '{dt_inicial}' AND '{dt_final}' AND categoria = '{categoria}'
                                            GROUP BY categoria """)
            # pegar o valor da consulta sql
            valor = valor.fetchall()
            if not valor:
                valor = 0
                diferenca = float(valores_guia_percent[0][i]) - valor
                # preencher tabela_comparativo com valores - orçado, real, diferença
                valor_cat = (
                    categoria, valores_guia_percent[0][i], valor, diferenca)
            else:
                # calcular diferença valor orçado x real
                diferenca = float(
                    valores_guia_percent[0][i]) - float(valor[0][0])

                # preencher tabela_comparativo com valores - orçado, real, diferença
                valor_cat = (
                    categoria, valores_guia_percent[0][i], valor[0][0], diferenca)
            lista_valores.append(valor_cat)
            i += 1

        # Preencher a Lst_comparativo com os valores
        for i in lista_valores:
            i = (i[0], self.real_br_money_mask(i[1]), self.real_br_money_mask(i[2]), self.real_br_money_mask(i[3]))
            self.lst_comparativo.insert("", "end", values=i)

        self.desconecta_bd()

    def filtrar(self):
        self.select_lista()
        self.select_comparativo()
