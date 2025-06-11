import tkinter as tk
from tkinter import ttk, messagebox

usuarios = []
contas = []
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 500.0

def buscar_conta(numero_conta):
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            return conta
    return None

def criar_usuario(nome, data_nascimento, bairro, cidade, logradouro, estado, cpf, sigla_estado):
    return {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "bairro": bairro,
        "cidade": cidade,
        "logradouro": logradouro,
        "estado": estado,
        "cpf": cpf,
        "sigla_estado": sigla_estado,
    }

def criar_conta_para_usuario(usuario, tipo_conta):
    numero_conta = len(contas) + 1
    conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "tipo": tipo_conta,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
    }
    contas.append(conta)
    return conta

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato, "Depósito realizado com sucesso!"
    else:
        return saldo, extrato, "Operacão falhou! Valor inválido."

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        return saldo, extrato, numero_saques, "Valor inválido."
    if valor > saldo:
        return saldo, extrato, numero_saques, "Saldo insuficiente."
    if valor > limite:
        return saldo, extrato, numero_saques, "Saque excede o limite."
    if numero_saques >= limite_saques:
        return saldo, extrato, numero_saques, "Limite de saques excedido."

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1
    return saldo, extrato, numero_saques, "Saque realizado com sucesso!"

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco de Bruno Silva - DIO")
        self.conta = None
        self.frame_inicial()

    def frame_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Bem-vindo ao Banco!").pack(pady=10)
        tk.Label(self.root, text="Informe o número da conta:").pack()
        self.entry_conta = tk.Entry(self.root)
        self.entry_conta.pack(pady=5)
        tk.Button(self.root, text="Entrar", command=self.entrar_conta).pack(pady=5)
        tk.Button(self.root, text="Criar Nova Conta", command=self.tela_criar_conta).pack(pady=5)
        tk.Button(self.root, text="Histórico de Contas", command=self.abrir_historico).pack(pady=5)

    def entrar_conta(self):
        if not contas:
            messagebox.showwarning("Sem contas", "Nenhuma conta cadastrada. Crie uma conta primeiro.")
            self.tela_criar_conta()
            return

        try:
            numero = int(self.entry_conta.get())
            conta = buscar_conta(numero)
            if conta:
                self.conta = conta
                self.tela_conta()
            else:
                messagebox.showerror("Erro", "Conta não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "Número de conta inválido.")

    def tela_conta(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        usuario = self.conta["usuario"]
        tk.Label(self.root, text=f"Conta: {self.conta['numero_conta']} ({self.conta['tipo']})").pack()
        tk.Label(self.root, text=f"Cliente: {usuario['nome']}").pack()
        self.lbl_saldo = tk.Label(self.root, text=f"Saldo: R$ {self.conta['saldo']:.2f}")
        self.lbl_saldo.pack()

        tk.Button(self.root, text="Depositar", command=self.tela_depositar).pack(pady=5)
        tk.Button(self.root, text="Sacar", command=self.tela_sacar).pack(pady=5)
        tk.Button(self.root, text="Ver Extrato", command=self.ver_extrato).pack(pady=5)
        tk.Button(self.root, text="Voltar", command=self.frame_inicial).pack(pady=10)

    def tela_criar_conta(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.campos_usuario = {}
        campos = ["nome", "data_nascimento", "bairro", "cidade", "logradouro", "estado", "cpf", "sigla_estado"]
        for campo in campos:
            tk.Label(self.root, text=campo.capitalize()).pack()
            self.campos_usuario[campo] = tk.Entry(self.root)
            self.campos_usuario[campo].pack()

        tk.Label(self.root, text="Tipo de Conta").pack()
        self.tipo_conta_var = tk.StringVar(value="Corrente")
        ttk.Combobox(self.root, textvariable=self.tipo_conta_var, values=["Corrente", "Poupança"]).pack()

        tk.Button(self.root, text="Criar Conta", command=self.criar_conta).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.frame_inicial).pack()

    def criar_conta(self):
        dados = {k: v.get() for k, v in self.campos_usuario.items()}
        if not all(dados.values()):
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
            return

        tipo = self.tipo_conta_var.get()
        usuario = criar_usuario(**dados)
        conta = criar_conta_para_usuario(usuario, tipo)
        messagebox.showinfo("Conta criada", f"{tipo} criada com sucesso!\nNúmero da conta: {conta['numero_conta']}")
        self.frame_inicial()

    def tela_depositar(self):
        valor = simpledialog.askfloat("Depósito", "Informe o valor:")
        if valor is not None:
            saldo, extrato, msg = depositar(self.conta['saldo'], valor, self.conta['extrato'])
            self.conta['saldo'] = saldo
            self.conta['extrato'] = extrato
            self.lbl_saldo.config(text=f"Saldo: R$ {saldo:.2f}")
            messagebox.showinfo("Resultado", msg)

    def tela_sacar(self):
        valor = simpledialog.askfloat("Saque", "Informe o valor:")
        if valor is not None:
            saldo, extrato, saques, msg = sacar(
                self.conta['saldo'], valor, self.conta['extrato'],
                LIMITE_SAQUE_VALOR, self.conta['numero_saques'], LIMITE_SAQUES)
            self.conta['saldo'] = saldo
            self.conta['extrato'] = extrato
            self.conta['numero_saques'] = saques
            self.lbl_saldo.config(text=f"Saldo: R$ {saldo:.2f}")
            messagebox.showinfo("Resultado", msg)

    def ver_extrato(self):
        extrato = self.conta['extrato'] if self.conta['extrato'] else "Não foram realizadas movimentações."
        messagebox.showinfo("Extrato", extrato)

    def abrir_historico(self):
        if not contas:
            messagebox.showinfo("Sem contas", "Nenhuma conta cadastrada. Crie uma conta primeiro.")
            self.tela_criar_conta()
            return

        janela = tk.Toplevel(self.root)
        janela.title("Histórico de Contas")

        tk.Label(janela, text="Selecione uma conta:").pack(pady=5)
        lista = ttk.Treeview(janela, columns=("Conta", "Nome", "Tipo"), show="headings")
        lista.heading("Conta", text="Conta")
        lista.heading("Nome", text="Nome")
        lista.heading("Tipo", text="Tipo")

        for conta in contas:
            lista.insert("", "end", values=(conta['numero_conta'], conta['usuario']['nome'], conta['tipo']))

        lista.pack(pady=5)

        def mostrar():
            item = lista.selection()
            if item:
                valores = lista.item(item[0], "values")
                numero = int(valores[0])
                conta = buscar_conta(numero)
                extrato = conta['extrato'] if conta['extrato'] else "Não foram realizadas movimentações."
                messagebox.showinfo(f"Extrato da Conta {numero}", extrato)

        tk.Button(janela, text="Ver Extrato da Conta Selecionada", command=mostrar).pack(pady=10)

# Execução principal
if __name__ == '__main__':
    from tkinter import simpledialog
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
