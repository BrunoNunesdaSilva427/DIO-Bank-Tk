import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Dados globais
usuarios = []
contas = []
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 500.0

# Funções principais
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

def criar_conta_para_usuario(usuario):
    numero_conta = len(contas) + 1
    conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario,
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
        return saldo, extrato, "Valor de depósito inválido."

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        return saldo, extrato, numero_saques, "Valor inválido para saque."
    if valor > saldo:
        return saldo, extrato, numero_saques, "Saldo insuficiente."
    if valor > limite:
        return saldo, extrato, numero_saques, "Valor excede o limite de saque."
    if numero_saques >= limite_saques:
        return saldo, extrato, numero_saques, "Limite de saques atingido."

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1
    return saldo, extrato, numero_saques, "Saque realizado com sucesso."

# Interface Gráfica
class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco Digital")

        self.frame_inicial()

    def frame_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Número da Conta:").pack()
        self.entry_conta = tk.Entry(self.root)
        self.entry_conta.pack()

        tk.Button(self.root, text="Entrar", command=self.entrar_conta).pack(pady=5)
        tk.Button(self.root, text="Criar Nova Conta", command=self.tela_criar_conta).pack()

    def tela_criar_conta(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.campos_usuario = {}
        campos = ["nome", "data_nascimento", "bairro", "cidade", "logradouro", "estado", "cpf", "sigla_estado"]
        for campo in campos:
            tk.Label(self.root, text=campo.capitalize()).pack()
            self.campos_usuario[campo] = tk.Entry(self.root)
            self.campos_usuario[campo].pack()

        tk.Button(self.root, text="Criar Conta", command=self.criar_conta).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.frame_inicial).pack()

    def criar_conta(self):
        dados = {k: v.get() for k, v in self.campos_usuario.items()}
        if not all(dados.values()):
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
            return

        usuario = criar_usuario(**dados)
        conta = criar_conta_para_usuario(usuario)
        messagebox.showinfo("Conta criada", f"Conta criada com sucesso!\nNúmero da conta: {conta['numero_conta']}")
        self.frame_inicial()

    def entrar_conta(self):
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
        tk.Label(self.root, text=f"Bem-vindo, {usuario['nome']}").pack()
        self.label_saldo = tk.Label(self.root, text=f"Saldo: R$ {self.conta['saldo']:.2f}")
        self.label_saldo.pack()

        tk.Button(self.root, text="Depositar", command=self.depositar_gui).pack(pady=5)
        tk.Button(self.root, text="Sacar", command=self.sacar_gui).pack(pady=5)
        tk.Button(self.root, text="Ver Extrato", command=self.mostrar_extrato).pack(pady=5)
        tk.Button(self.root, text="Sair", command=self.frame_inicial).pack(pady=5)

    def depositar_gui(self):
        valor = simpledialog.askfloat("Depósito", "Valor do depósito:")
        if valor is not None:
            saldo, extrato, msg = depositar(self.conta["saldo"], valor, self.conta["extrato"])
            self.conta["saldo"] = saldo
            self.conta["extrato"] = extrato
            self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")
            messagebox.showinfo("Depósito", msg)

    def sacar_gui(self):
        valor = simpledialog.askfloat("Saque", "Valor do saque:")
        if valor is not None:
            saldo, extrato, num_saques, msg = sacar(
                self.conta["saldo"], valor, self.conta["extrato"],
                LIMITE_SAQUE_VALOR, self.conta["numero_saques"], LIMITE_SAQUES
            )
            self.conta["saldo"] = saldo
            self.conta["extrato"] = extrato
            self.conta["numero_saques"] = num_saques
            self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")
            messagebox.showinfo("Saque", msg)

    def mostrar_extrato(self):
        extrato = self.conta["extrato"] if self.conta["extrato"] else "Não foram realizadas movimentações."
        messagebox.showinfo("Extrato", extrato)


# Iniciar a aplicação
if __name__ == '__main__':
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
