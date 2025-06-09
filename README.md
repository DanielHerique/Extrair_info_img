📝 Descrição do Projeto
Extrator de Páginas para Markdown é um aplicativo desktop com interface gráfica desenvolvido em Python que permite ao usuário extrair o conteúdo principal de páginas da web (HTML) e convertê-lo automaticamente para o formato Markdown (.md), pronto para ser salvo localmente.

O sistema utiliza Selenium WebDriver para renderizar páginas com JavaScript, processa o HTML com BeautifulSoup, e converte o conteúdo em Markdown com a biblioteca markdownify. A interface gráfica foi criada com Tkinter, permitindo fácil uso mesmo para usuários sem conhecimento técnico.

💡 Funcionalidades
Interface gráfica simples e intuitiva.

Aceita múltiplas URLs ao mesmo tempo (uma por linha).

Remove automaticamente elementos irrelevantes da página (como <header>, <footer>, <script>, etc.).

Converte o conteúdo extraído em arquivos Markdown formatados.

Corrige os links de imagens para URLs absolutas.

Permite escolher a pasta de destino dos arquivos gerados.

Indica erros e sucessos ao final da extração.

🚀 Tecnologias utilizadas
Python 3.13

Selenium

BeautifulSoup4

markdownify

Tkinter (GUI)

re, urllib, os, time

📸 Exemplo de uso
O usuário insere uma ou várias URLs no campo de entrada.

Escolhe uma pasta de destino para salvar os arquivos.

Clica no botão "Extrair para Markdown".

O programa renderiza a página, extrai o conteúdo principal e salva em arquivos .md.

