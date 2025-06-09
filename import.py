import os
import time
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

def limpar_url_imagem(src):
    parsed = urlparse(src)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def limpar_nome_arquivo(titulo):
    return re.sub(r'[\\/*?:"<>|]', "_", titulo.strip())

def extrair_com_selenium(url):
    try:
        options = Options()
        # options.add_argument("--headless")  # opcional
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
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

def iniciar_extracao():
    urls_raw = entrada_url.get("1.0", tk.END).strip()
    urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]
    
    if not urls:
        messagebox.showerror("Erro", "Insira pelo menos uma URL válida.")
        return

    # Perguntar onde salvar
    diretorio = filedialog.askdirectory(title="Escolha a pasta para salvar os arquivos Markdown")
    if not diretorio:
        messagebox.showwarning("Cancelado", "Nenhuma pasta foi selecionada.")
        return

    botao_extrair.config(state=tk.DISABLED)
    status_label.config(text="⏳ Extraindo páginas...")
    janela.update_idletasks()

    salvos = []
    erros = []

    for url in urls:
        if not url.startswith("http"):
            erros.append(f"URL inválida: {url}")
            continue

        titulo, resultado = extrair_com_selenium(url)

        if isinstance(resultado, str) and resultado.startswith("Erro"):
            erros.append(f"{url} → {resultado}")
        else:
            caminho = salvar_markdown_auto(diretorio, titulo, resultado)
            salvos.append(f"{url} → {caminho}")

    mensagem = ""
    if salvos:
        mensagem += "✅ Arquivos salvos:\n" + "\n".join(salvos) + "\n\n"
    if erros:
        mensagem += "❌ Erros:\n" + "\n".join(erros)

    messagebox.showinfo("Resultado", mensagem.strip())
    status_label.config(text="✅ Finalizado.")
    botao_extrair.config(state=tk.NORMAL)

# Interface Gráfica
janela = tk.Tk()
janela.title("Extrator de Páginas para Markdown")
janela.geometry("600x300")

tk.Label(janela, text="Cole uma ou mais URLs (uma por linha):").pack(pady=10)
entrada_url = scrolledtext.ScrolledText(janela, width=70, height=8)
entrada_url.pack()

botao_extrair = tk.Button(janela, text="Extrair para Markdown", command=iniciar_extracao)
botao_extrair.pack(pady=10)

status_label = tk.Label(janela, text="", fg="blue")
status_label.pack()

janela.mainloop()
