import os
import time
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
from PIL import Image, ImageTk, ImageDraw

# =========================================================
# CAMINHO DA LOGO PERSONALIZADA (EDITAR AQUI!)
# Se o caminho abaixo não for válido ou estiver vazio, uma logo padrão será usada.
CAMINHO_LOGO_PERSONALIZADA = r"C:\Users\danie\OneDrive\Desktop\conversu_logo.png"
# =========================================================

# ==== Definição de Cores e Fontes (Cores Originais Revertidas) ====
COR_FUNDO = "#F25C3A"  # Laranja vibrante
COR_BOTAO = "#2C2CB3"  # Azul escuro
COR_HOVER = "#1E1EA3"  # Azul escuro um pouco mais claro para hover
COR_TEXTO = "white"    # Branco
FONTE_TEXTO = ("Segoe UI", 10)
FONTE_TITULO = ("Segoe UI", 12, "bold")
FONTE_RODAPE = ("Segoe UI", 8, "italic")
COR_CAIXA_TEXTO = "#FFF1E6" # Bege claro
# ==========================================================

# Variável global para armazenar o histórico da sessão
# Cada item será um dicionário: {'url': url, 'titulo': titulo, 'caminho_arquivo': caminho}
historico_extracoes = []

def limpar_url_imagem(src):
    parsed = urlparse(src)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def limpar_nome_arquivo(titulo):
    return re.sub(r'[\\/*?:"<>|]', "_", titulo.strip())

def extrair_com_selenium(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)

        html = driver.page_source
        titulo = driver.title
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(['header', 'footer', 'nav', 'script', 'style']):
            tag.decompose()

        body = soup.body or soup

        for img in body.find_all("img"):
            src = img.get("src", "")
            img["src"] = limpar_url_imagem(src)

        markdown = md(str(body), heading_style="atx")
        return titulo, markdown

    except Exception as e:
        return None, f"Erro: {str(e)}"

def salvar_markdown_auto(diretorio, titulo, markdown):
    nome = limpar_nome_arquivo(titulo or "pagina")
    caminho = os.path.join(diretorio, f"{nome}.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(markdown)
    return caminho

def carregar_logo_para_label(label_destino, caminho_logo):
    try:
        if caminho_logo and os.path.exists(caminho_logo):
            img = Image.open(caminho_logo)
        else:
            raise FileNotFoundError

        largura_max = 150
        altura_max = 80
        img.thumbnail((largura_max, altura_max), Image.Resampling.LANCZOS)
        
        img_tk = ImageTk.PhotoImage(img)
        label_destino.config(image=img_tk)
        label_destino.image = img_tk
        return True
    except Exception as e:
        # Logo padrão com as cores originais
        img_padrao = Image.new('RGB', (150, 80), color = '#CCCCCC')
        d = ImageDraw.Draw(img_padrao)
        d.text((20, 30), "Sem Logo", fill=(50,50,50))
        img_tk_padrao = ImageTk.PhotoImage(img_padrao)
        label_destino.config(image=img_tk_padrao)
        label_destino.image = img_tk_padrao
        return False

def centralizar_janela(janela_alvo, largura, altura):
    janela_alvo.update_idletasks()
    tela_largura = janela_alvo.winfo_screenwidth()
    tela_altura = janela_alvo.winfo_screenheight()

    pos_x = int((tela_largura - largura) / 2)
    pos_y = int((tela_altura - altura) / 2)

    janela_alvo.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def show_input_state():
    """Oculta widgets de resultado e exibe widgets de entrada."""
    label_titulo_resultado.grid_forget()
    caixa_texto_resultado.grid_forget()
    btn_voltar.grid_forget()
    btn_historico.grid_forget() # Oculta o botão histórico na tela de resultados

    label_entrada_url.grid(row=1, column=0, pady=(5, 8))
    entrada_url.grid(row=2, column=0, padx=24)
    botao_extrair.grid(row=3, column=0, pady=10)
    status_label.grid(row=4, column=0)
    
    # Exibe o botão de histórico na tela de entrada
    btn_historico.grid(row=0, column=0, sticky="ne", padx=10, pady=10) 
    
    status_label.config(text="") # Limpa o texto de status
    progress_bar.stop()
    progress_bar.grid_forget() # Garante que esteja oculto ao retornar

    entrada_url.config(state=tk.NORMAL) # Habilita para poder limpar
    entrada_url.delete("1.0", tk.END)  # Limpa todo o texto

    botao_extrair.config(state=tk.NORMAL) # Reabilita o botão "Extrair"


def show_result_state():
    """Oculta widgets de entrada e exibe widgets de resultado."""
    label_entrada_url.grid_forget()
    entrada_url.grid_forget()
    botao_extrair.grid_forget()
    status_label.grid_forget()
    progress_bar.stop()
    progress_bar.grid_forget()
    btn_historico.grid_forget() # Oculta o botão histórico na tela de entrada

    label_titulo_resultado.grid(row=1, column=0, pady=(5, 5))
    caixa_texto_resultado.grid(row=2, column=0, padx=24, pady=5)
    btn_voltar.grid(row=3, column=0, pady=10)
    btn_historico.grid(row=0, column=0, sticky="ne", padx=10, pady=10) # Exibe o botão histórico na tela de resultados


def iniciar_extracao():
    urls_raw = entrada_url.get("1.0", tk.END).strip()
    urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]
    
    if not urls:
        messagebox.showerror("Erro", "Insira pelo menos uma URL válida.")
        return

    diretorio = filedialog.askdirectory(title="Escolha a pasta para salvar os arquivos Markdown")
    if not diretorio:
        messagebox.showwarning("Cancelado", "Nenhuma pasta foi selecionada.")
        return

    botao_extrair.config(state=tk.DISABLED) # Desabilita o botão ao iniciar a extração
    btn_historico.config(state=tk.DISABLED) # Desabilita o botão histórico durante a extração
    
    # --- Gerencia a barra de progresso e status ---
    status_label.config(text="⏳ Preparando...")
    status_label.grid(row=4, column=0) 
    progress_bar.grid(row=5, column=0, pady=5) 
    progress_bar.start(10)
    
    if len(urls) > 1:
        progress_bar.config(mode="determinate", maximum=len(urls), value=0)
    else:
        progress_bar.config(mode="indeterminate")
        
    janela.update_idletasks()

    salvos = []
    erros = []

    for i, url in enumerate(urls):
        if not url.startswith("http"):
            erros.append(f"URL inválida: {url}")
            if len(urls) > 1:
                progress_bar["value"] = i + 1
            janela.update_idletasks()
            continue

        status_label.config(text=f"⏳ Extraindo ({i+1}/{len(urls)}): {url[:50]}...")
        janela.update_idletasks()

        time.sleep(1) # Simula um pequeno atraso para UX
        titulo, resultado = extrair_com_selenium(url)

        if isinstance(resultado, str) and resultado.startswith("Erro"):
            erros.append(f"❌ {url}\n   Erro: {resultado.replace('Erro: ', '')}")
        else:
            caminho = salvar_markdown_auto(diretorio, titulo, resultado)
            salvos.append(f"✅ {url}\n   Salvo em: {caminho}")
            # Adiciona ao histórico de extrações
            historico_extracoes.append({'url': url, 'titulo': titulo, 'caminho_arquivo': caminho})
        
        if len(urls) > 1:
            progress_bar["value"] = i + 1
        janela.update_idletasks()

    mensagem = ""
    if salvos:
        mensagem += "Páginas salvas com sucesso:\n\n" + "\n\n".join(salvos)
    if erros:
        if salvos:
            mensagem += "\n\n---\n\n"
        mensagem += "Erros encontrados:\n\n" + "\n\n".join(erros)

    caixa_texto_resultado.config(state=tk.NORMAL)
    caixa_texto_resultado.delete("1.0", tk.END)
    caixa_texto_resultado.insert(tk.END, mensagem.strip())
    caixa_texto_resultado.config(state=tk.DISABLED)
    
    progress_bar.stop()
    progress_bar.grid_forget() 
    status_label.config(text="✅ Finalizado.")
    
    btn_historico.config(state=tk.NORMAL) # Reabilita o botão histórico após a extração
    show_result_state() # Muda para a visualização de resultados após a extração

def verificar_e_adicionar_quebra_linha():
    """
    Verifica o conteúdo da entrada_url e adiciona uma quebra de linha
    se a última linha não estiver vazia e não terminar em quebra de linha.
    """
    conteudo = entrada_url.get("1.0", tk.END)
    linhas = conteudo.strip().split('\n')
    
    if linhas and linhas[-1].strip() and not conteudo.endswith('\n'):
        entrada_url.insert(tk.END, "\n")
    entrada_url.see(tk.END) 


def on_paste_event(event=None):
    """
    Chamado quando um evento de colar (Ctrl+V, Cmd+V, ou clique direito) é detectado.
    Agenda a verificação para adicionar a quebra de linha após a operação de colar.
    """
    janela.after(50, verificar_e_adicionar_quebra_linha)

def mostrar_historico():
    """Cria e exibe uma nova janela com o histórico de extrações da sessão."""
    historico_window = tk.Toplevel(janela)
    historico_window.title("Histórico de Extrações")
    historico_window.geometry("600x400")
    historico_window.configure(bg=COR_FUNDO)
    centralizar_janela(historico_window, 600, 400)

    label_titulo_historico = tk.Label(historico_window, text="Histórico de Extrações da Sessão:",
                                      bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_TITULO)
    label_titulo_historico.pack(pady=10)

    historico_texto_area = scrolledtext.ScrolledText(historico_window,
                                                      width=70,
                                                      height=15,
                                                      font=FONTE_TEXTO,
                                                      bd=0,
                                                      relief="flat",
                                                      bg=COR_CAIXA_TEXTO,
                                                      fg="black",
                                                      wrap=tk.WORD)
    historico_texto_area.pack(padx=20, pady=5, expand=True, fill="both")
    historico_texto_area.config(state=tk.DISABLED) # Desabilita edição

    if not historico_extracoes:
        historico_texto_area.config(state=tk.NORMAL)
        historico_texto_area.insert(tk.END, "Nenhuma extração realizada nesta sessão ainda.")
        historico_texto_area.config(state=tk.DISABLED)
    else:
        historico_texto_area.config(state=tk.NORMAL)
        for i, item in enumerate(historico_extracoes):
            historico_texto_area.insert(tk.END, f"{i+1}. URL: {item['url']}\n")
            historico_texto_area.insert(tk.END, f"   Título: {item['titulo']}\n")
            historico_texto_area.insert(tk.END, f"   Salvo em: {item['caminho_arquivo']}\n")
            if i < len(historico_extracoes) - 1:
                historico_texto_area.insert(tk.END, "----------------------------------------\n")
        historico_texto_area.config(state=tk.DISABLED)

    btn_fechar_historico = ttk.Button(historico_window, text="Fechar", command=historico_window.destroy)
    btn_fechar_historico.pack(pady=10)


# ==== Configuração da Interface Gráfica Principal ====

janela = tk.Tk()
janela.title("Extrator de Páginas para Markdown")

centralizar_janela(janela, 660, 550)

janela.configure(bg=COR_FUNDO)

style = ttk.Style()
# Usando o tema padrão para que as cores personalizadas se apliquem melhor
style.theme_use("default") 

style.configure("TButton", font=FONTE_TEXTO, background=COR_BOTAO,
                foreground=COR_TEXTO, padding=(8, 8), borderwidth=0)
style.map("TButton", background=[("active", COR_HOVER)])

style.configure("green.Horizontal.TProgressbar",
                troughcolor=COR_CAIXA_TEXTO,
                bordercolor=COR_BOTAO,
                background="green",
                lightcolor="lightgreen",
                darkcolor="darkgreen")

# --- Logo no topo ---
label_logo_principal = tk.Label(janela, bg=COR_FUNDO)
label_logo_principal.pack(pady=(15, 5))
carregar_logo_para_label(label_logo_principal, CAMINHO_LOGO_PERSONALIZADA)

# --- Frame para o conteúdo central usando grid ---
frame_conteudo_principal = tk.Frame(janela, bg=COR_FUNDO)
frame_conteudo_principal.pack(expand=True, fill="both")
frame_conteudo_principal.grid_columnconfigure(0, weight=1) # Coluna 0 se expande para centralizar

# Botão de histórico (posicionado no canto superior direito do frame de conteúdo)
btn_historico = ttk.Button(frame_conteudo_principal, text="Histórico de Extrações", command=mostrar_historico)
# Este botão será grid-ed dinamicamente em show_input_state e show_result_state

# Widgets de entrada
label_entrada_url = tk.Label(frame_conteudo_principal, text="Cole uma ou mais URLs (uma por linha):",
                             bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_TITULO)

entrada_url = scrolledtext.ScrolledText(frame_conteudo_principal,
                                        width=70,
                                        height=6,
                                        font=FONTE_TEXTO,
                                        bd=2, # Borda de volta para o visual original
                                        relief="flat", # Manter flat ou mudar para sunken/groove para borda visível
                                        bg=COR_CAIXA_TEXTO,
                                        fg="black",
                                        insertbackground="black")
# Vincular eventos de colagem
entrada_url.bind("<Control-v>", on_paste_event) 
entrada_url.bind("<Command-v>", on_paste_event) 
entrada_url.bind("<Button-3>", on_paste_event)  


botao_extrair = ttk.Button(frame_conteudo_principal, text="Extrair para Markdown", command=iniciar_extracao)

status_label = tk.Label(frame_conteudo_principal, text="", fg=COR_TEXTO, bg=COR_FUNDO, font=("Segoe UI", 9))

progress_bar = ttk.Progressbar(frame_conteudo_principal, orient="horizontal", length=300,
                               mode="indeterminate", style="green.Horizontal.TProgressbar")

# Área para exibição dos resultados
label_titulo_resultado = tk.Label(frame_conteudo_principal, text="Resultados da Extração:",
                                   bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_TITULO)

caixa_texto_resultado = scrolledtext.ScrolledText(frame_conteudo_principal,
                                                  width=70,
                                                  height=12,
                                                  font=FONTE_TEXTO,
                                                  bd=2, # Borda de volta para o visual original
                                                  relief="flat", # Manter flat
                                                  bg=COR_CAIXA_TEXTO,
                                                  fg="black",
                                                  wrap=tk.WORD)

btn_voltar = ttk.Button(frame_conteudo_principal, text="Voltar", command=show_input_state, style="TButton")

# --- Rodapé na parte inferior ---
tk.Label(janela, text="Criado por Dani_Dev",
          bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_RODAPE).pack(side="bottom", pady=(15, 8))

# Inicializa a interface no estado de entrada
show_input_state()

janela.mainloop()
