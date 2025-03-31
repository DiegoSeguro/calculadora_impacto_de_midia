import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

class CalculadoraImpactoMidia:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Impacto de Mídia Digital")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Definir cores e estilo
        self.cor_fundo = "#1E1E2E"  # Preto escuro
        self.cor_destaque = "#6A5ACD"  # Roxo claro (SlateBlue)
        self.cor_botao = "#4B0082"  # Índigo
        self.cor_texto = "#FFFFFF"  # Branco
        self.cor_input_bg = "#2C2C3E"  # Fundo dos inputs
        self.cor_input_texto = "#FFFFFF"  # Texto dos inputs
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.cor_fundo)
        self.style.configure('TLabel', background=self.cor_fundo, foreground=self.cor_texto, font=('Arial', 10))
        self.style.configure('TButton', background=self.cor_botao, foreground='black', font=('Arial', 10, 'bold'))
        self.style.configure('Titulo.TLabel', font=('Arial', 16, 'bold'), foreground=self.cor_destaque)
        self.style.configure('Subtitulo.TLabel', font=('Arial', 12, 'bold'), foreground=self.cor_destaque)
        
        # Definir variáveis
        self.cpm_values = []
        self.publico_value = tk.StringVar()
        self.investimento_value = tk.StringVar()
        
        # Criar layout principal
        self.criar_interface()
        
    def criar_interface(self):
        """Cria a interface gráfica do aplicativo"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Calculadora de Impacto de Mídia Digital", style='Titulo.TLabel')
        titulo.pack(pady=10)
        
        # Frame para entrada de dados
        input_frame = ttk.Frame(main_frame, style='TFrame')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Frame para CPM
        cpm_frame = ttk.Frame(input_frame, style='TFrame')
        cpm_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(cpm_frame, text="CPM (R$):", style='Subtitulo.TLabel').pack(anchor='w')
        
        # Frame para entrada dinâmica de CPM
        self.cpm_entries_frame = ttk.Frame(cpm_frame, style='TFrame')
        self.cpm_entries_frame.pack(fill=tk.X, pady=5)
        
        # Adicionar primeira entrada de CPM
        self.adicionar_campo_cpm()
        
        # Botão para adicionar mais campos CPM
        add_button = ttk.Button(cpm_frame, text="+ Adicionar CPM", command=self.adicionar_campo_cpm)
        add_button.pack(anchor='w', pady=5)
        
        # Frame para tamanho do público
        publico_frame = ttk.Frame(input_frame, style='TFrame')
        publico_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(publico_frame, text="Tamanho do Público:", style='Subtitulo.TLabel').pack(anchor='w')
        publico_entry = ttk.Entry(publico_frame, textvariable=self.publico_value, width=30)
        publico_entry.pack(anchor='w', pady=5)
        
        # Frame para investimento
        investimento_frame = ttk.Frame(input_frame, style='TFrame')
        investimento_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(investimento_frame, text="Investimento (R$):", style='Subtitulo.TLabel').pack(anchor='w')
        investimento_entry = ttk.Entry(investimento_frame, textvariable=self.investimento_value, width=30)
        investimento_entry.pack(anchor='w', pady=5)
        
        # Botão para calcular
        calcular_button = ttk.Button(input_frame, text="Calcular Impacto", command=self.calcular_impacto)
        calcular_button.pack(pady=15)
        
        # Frame para resultados
        self.resultado_frame = ttk.Frame(main_frame, style='TFrame')
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Inicialmente, mostra uma mensagem
        self.msg_inicial = ttk.Label(self.resultado_frame, 
                                     text="Preencha os dados acima e clique em 'Calcular Impacto' para visualizar os resultados",
                                     style='TLabel')
        self.msg_inicial.pack(pady=50)
    
    def adicionar_campo_cpm(self):
        """Adiciona um novo campo de entrada para CPM"""
        cpm_entry_frame = ttk.Frame(self.cpm_entries_frame, style='TFrame')
        cpm_entry_frame.pack(fill=tk.X, pady=2)
        
        # Criar uma variável para armazenar o valor
        cpm_var = tk.StringVar()
        self.cpm_values.append(cpm_var)
        
        # Criar campo de entrada
        cpm_entry = ttk.Entry(cpm_entry_frame, textvariable=cpm_var, width=20)
        cpm_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Se não for o primeiro campo, adicionar botão de remover
        if len(self.cpm_values) > 1:
            remove_button = ttk.Button(cpm_entry_frame, text="✕", 
                                       command=lambda frame=cpm_entry_frame, var=cpm_var: self.remover_campo_cpm(frame, var),
                                       width=3)
            remove_button.pack(side=tk.LEFT)
    
    def remover_campo_cpm(self, frame, var):
        """Remove um campo de entrada CPM"""
        # Remover a variável da lista
        if var in self.cpm_values:
            self.cpm_values.remove(var)
        
        # Destruir o frame
        frame.destroy()
    
    def validar_entradas(self):
        """Valida as entradas do usuário e retorna uma tupla (valido, mensagem)"""
        # Validar CPMs
        cpm_list = []
        for cpm_var in self.cpm_values:
            cpm_str = cpm_var.get().strip().replace(',', '.')
            if not cpm_str:
                return False, "Todos os campos CPM devem ser preenchidos."
            try:
                cpm = float(cpm_str)
                if cpm <= 0:
                    return False, "Os valores de CPM devem ser positivos."
                cpm_list.append(cpm)
            except ValueError:
                return False, "Os valores de CPM devem ser números decimais válidos."
        
        # Validar tamanho do público
        publico_str = self.publico_value.get().strip()
        if not publico_str:
            return False, "O campo Tamanho do Público deve ser preenchido."
        try:
            publico = int(publico_str)
            if publico <= 0:
                return False, "O tamanho do público deve ser um número inteiro positivo."
        except ValueError:
            return False, "O tamanho do público deve ser um número inteiro válido."
        
        # Validar investimento
        investimento_str = self.investimento_value.get().strip().replace(',', '.')
        if not investimento_str:
            return False, "O campo Investimento deve ser preenchido."
        try:
            investimento = float(investimento_str)
            if investimento <= 0:
                return False, "O valor do investimento deve ser positivo."
        except ValueError:
            return False, "O valor do investimento deve ser um número decimal válido."
        
        return True, "Dados válidos."
    
    def calcular_impacto(self):
        """Calcula o impacto com base nos dados inseridos e exibe os resultados"""
        # Validar as entradas
        valido, mensagem = self.validar_entradas()
        if not valido:
            messagebox.showerror("Erro de Validação", mensagem)
            return
        
        # Limpar o frame de resultados
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        
        # Obter os valores válidos
        cpm_list = [float(cpm_var.get().strip().replace(',', '.')) for cpm_var in self.cpm_values]
        publico = int(self.publico_value.get().strip())
        investimento = float(self.investimento_value.get().strip().replace(',', '.'))
        
        # Criar um notebook (abas) para os resultados
        notebook = ttk.Notebook(self.resultado_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Calcular o impacto para cada CPM e criar uma aba para cada cenário
        resultados = []
        
        for i, cpm in enumerate(cpm_list):
            # Calcular o impacto
            impacto_pessoas = (investimento * 1000) / cpm
            percentual_impacto = (impacto_pessoas / publico) * 100
            
            resultados.append({
                'cpm': cpm,
                'impacto_pessoas': impacto_pessoas,
                'percentual_impacto': percentual_impacto,
                'frequencia': impacto_pessoas / publico  # Novo campo de frequência
            })
            
            # Criar aba para o cenário
            tab = ttk.Frame(notebook, style='TFrame')
            notebook.add(tab, text=f"Cenário {i+1}")
            
            # Frame para informações
            info_frame = ttk.Frame(tab, style='TFrame')
            info_frame.pack(fill=tk.X, pady=10, padx=10)
            
            # Exibir informações do cenário
            ttk.Label(info_frame, text=f"CPM: R$ {cpm:.2f}", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
            ttk.Label(info_frame, text=f"Tamanho do Público: {publico:,}".replace(',', '.'), font=('Arial', 12)).pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Investimento: R$ {investimento:.2f}", font=('Arial', 12)).pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Impacto (Pessoas): {int(impacto_pessoas):,}".replace(',', '.'), font=('Arial', 12)).pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Percentual de Impacto: {percentual_impacto:.2f}%", font=('Arial', 12, 'bold'), foreground='#007bff').pack(anchor='w', pady=5)
            ttk.Label(info_frame, text=f"Frequência: {(impacto_pessoas / publico):.2f} impactos/pessoa", font=('Arial', 12)).pack(anchor='w', pady=2)
            
            # Frame para o gráfico
            graph_frame = ttk.Frame(tab, style='TFrame')
            graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Criar gráfico
            self.criar_grafico(graph_frame, publico, impacto_pessoas)
        
        # Aba de comparação (se houver mais de um CPM)
        if len(cpm_list) > 1:
            self.criar_aba_comparacao(notebook, resultados, publico)
    
    def criar_grafico(self, frame, publico, impacto):
        """Cria um gráfico para visualizar o impacto"""
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Dados para o gráfico
        labels = ['Público Total', 'Impacto']
        valores = [publico, impacto]
        cores = ['#e0e0e0', '#4a6fa5']
        
        # Criar gráfico de barras
        bars = ax.bar(labels, valores, color=cores, width=0.5)
        
        # Adicionar valores no topo das barras
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height):,}'.replace(',', '.'),
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=10)
        
        # Configurar gráfico
        ax.set_title('Comparação entre Público Total e Impacto', fontsize=12)
        ax.set_ylabel('Número de Pessoas', fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adicionar à interface
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_comparacao(self, notebook, resultados, publico):
        """Cria uma aba de comparação entre diferentes cenários"""
        tab = ttk.Frame(notebook, style='TFrame')
        notebook.add(tab, text="Comparação")
        
        # Frame para o gráfico
        graph_frame = ttk.Frame(tab, style='TFrame')
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criar gráfico de comparação
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Preparar dados
        cpms = [r['cpm'] for r in resultados]
        impactos = [r['impacto_pessoas'] for r in resultados]
        percentuais = [r['percentual_impacto'] for r in resultados]
        frequencias = [r['frequencia'] for r in resultados]
        cenarios = [f"C{i+1}" for i in range(len(resultados))]
        
        # Gráfico de impacto
        bars1 = ax1.bar(cenarios, impactos, color='#4a6fa5')
        ax1.set_title('Comparação de Impacto por Cenário')
        ax1.set_xlabel('Cenários')
        ax1.set_ylabel('Impacto (Pessoas)')
        
        # Adicionar valores
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{int(height):,}'.replace(',', '.'),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
        
        # Gráfico de percentual
        bars2 = ax2.bar(cenarios, percentuais, color='#3d5a80')
        ax2.set_title('Comparação de Percentual de Impacto')
        ax2.set_xlabel('Cenários')
        ax2.set_ylabel('Percentual (%)')
        
        # Adicionar valores
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height:.2f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
        
        # Gráfico de frequência
        bars3 = ax3.bar(cenarios, frequencias, color='#2a9d8f')
        ax3.set_title('Comparação de Frequência')
        ax3.set_xlabel('Cenários')
        ax3.set_ylabel('Frequência (impactos/pessoa)')
        
        # Adicionar valores
        for bar in bars3:
            height = bar.get_height()
            ax3.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Adicionar legenda de CPMs
        fig.text(0.5, 0.01, f"Legenda: " + ", ".join([f"C{i+1} = R$ {cpms[i]:.2f}" for i in range(len(cpms))]), 
                ha='center', fontsize=9)
        
        # Adicionar à interface
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Tabela comparativa
        ttk.Label(tab, text="Tabela Comparativa:", style='Subtitulo.TLabel').pack(anchor='w', padx=10, pady=(10, 5))
        
        # Criar frame para tabela
        table_frame = ttk.Frame(tab, style='TFrame')
        table_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Cabeçalhos
        headers = ["Cenário", "CPM (R$)", "Impacto (Pessoas)", "% de Impacto", "Frequência"]
        for i, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=('Arial', 10, 'bold')).grid(row=0, column=i, padx=10, pady=5, sticky='w')
        
        # Dados
        for i, r in enumerate(resultados):
            ttk.Label(table_frame, text=f"Cenário {i+1}").grid(row=i+1, column=0, padx=10, pady=3, sticky='w')
            ttk.Label(table_frame, text=f"R$ {r['cpm']:.2f}").grid(row=i+1, column=1, padx=10, pady=3, sticky='w')
            ttk.Label(table_frame, text=f"{int(r['impacto_pessoas']):,}".replace(',', '.')).grid(row=i+1, column=2, padx=10, pady=3, sticky='w')
            ttk.Label(table_frame, text=f"{r['percentual_impacto']:.2f}%").grid(row=i+1, column=3, padx=10, pady=3, sticky='w')
            ttk.Label(table_frame, text=f"{r['frequencia']:.2f}").grid(row=i+1, column=4, padx=10, pady=3, sticky='w')



# Função para criar ícone do programa
def resource_path(relative_path):
    """Obtém o caminho do recurso para funcionar com PyInstaller"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Função principal
def main():
    root = tk.Tk()
    app = CalculadoraImpactoMidia(root)
    
    # Definir ícone se disponível
    try:
        # Substitua 'icon.ico' pelo caminho do seu ícone
        # Ao converter para executável, você precisará incluir o ícone
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()
    

# ATIVAR


    # conda activate calculadora_midia (ativar o ambiente virtual)
    # calculadora_impacto_midia.py (ativar o script)