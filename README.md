# 🌐 Extrator de Páginas para Markdown

## 📝 Descrição do Projeto
O Extrator de Páginas para Markdown é um aplicativo desktop robusto, construído em Python, projetado para simplificar a captura e organização de conteúdo web. Ele permite aos usuários extrair o conteúdo principal de páginas da web (HTML) e convertê-lo automaticamente para o formato Markdown (.md), pronto para ser salvo localmente em seu computador.

Com uma interface gráfica intuitiva, mesmo usuários sem conhecimento técnico podem navegar e utilizar a ferramenta com facilidade, tornando a transformação de páginas web em documentos Markdown uma tarefa rápida e eficiente.

## ✨ Funcionalidades Principais
Interface Gráfica (GUI) Intuitiva: Desenvolvida com Tkinter, oferece uma experiência de usuário simples e amigável.
Extração Múltipla de URLs: Aceita várias URLs simultaneamente, bastando inseri-las uma por linha no campo de entrada.
Limpeza Inteligente de Conteúdo: Remove automaticamente elementos irrelevantes de páginas web, como <header>, <footer>, <nav>, <script> e <style>, focando no conteúdo essencial.
Conversão para Markdown: Transforma o HTML extraído em arquivos Markdown bem formatados, prontos para uso.
Correção de Links de Imagens: Ajusta automaticamente os links de imagens para URLs absolutas, garantindo que as imagens sejam carregadas corretamente no Markdown.
Seleção de Pasta de Destino: Permite ao usuário escolher facilmente a pasta onde os arquivos Markdown gerados serão salvos.
Feedback de Processamento: Fornece indicações claras de sucesso ou erro ao final de cada extração, mantendo o usuário informado.
Histórico de Extrações da Sessão: Acompanha as extrações realizadas durante a sessão atual, permitindo revisitar URLs e caminhos de arquivo.

## 🚀 Tecnologias Utilizadas
Este projeto foi construído utilizando as seguintes tecnologias e bibliotecas Python:

Python 3.13: Linguagem de programação principal.
Selenium WebDriver: Utilizado para renderizar páginas web, incluindo aquelas que dependem de JavaScript para carregar o conteúdo dinamicamente.
BeautifulSoup4: Para parsear o HTML e facilitar a navegação e manipulação da estrutura da página.
markdownify: Biblioteca essencial para converter o HTML limpo em conteúdo Markdown.
Tkinter: Framework padrão do Python para criação de interfaces gráficas.
Pillow (PIL): Usada para manipulação de imagens, como carregar a logo do aplicativo.
Módulos Nativos: re (expressões regulares), urllib.parse (análise de URLs), os (interação com o sistema operacional) e time (controle de tempo).

## 🛠️ Como Instalar e Rodar
Siga os passos abaixo para configurar e executar o Extrator de Páginas para Markdown em sua máquina:

Pré-requisitos
Python 3.x (versão 3.13 ou superior recomendada).
ChromeDriver: O Selenium WebDriver exige que você tenha o ChromeDriver compatível com a sua versão do Google Chrome instalado e acessível no seu PATH do sistema, ou no mesmo diretório do script. Você pode baixá-lo aqui.
Instalação
Clone o Repositório (ou baixe o ZIP):
Bash

git clone [https://github.com/DanielHerique/Extrair_info_img](https://github.com/DanielHerique/Extrair_info_img)
cd Extrair_info_img
Crie e Ative um Ambiente Virtual (recomendado):
Bash

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
Instale as Dependências:
Bash

pip install -r requirements.txt
(Você precisará criar um arquivo requirements.txt com as dependências listadas abaixo)
Conteúdo para requirements.txt
selenium
beautifulsoup4
markdownify
Pillow
Executando o Aplicativo
Coloque a Logo (Opcional): Se você deseja usar sua logo personalizada, certifique-se de que o arquivo conversu_logo.png esteja na mesma pasta do script principal, e atualize a variável CAMINHO_LOGO_PERSONALIZADA no código, se necessário.
Execute o Script:
Bash

python seu_script_principal.py

## Só rodar este comando após verificar que o python está instalado

pip install beautifulsoup4 markdownify selenium Pillow requests

## 📸 Exemplo de Uso
O usuário inicia o aplicativo.
No campo de entrada, cola uma ou várias URLs (uma por linha).
Clica no botão "Extrair para Markdown".
![passo1](https://github.com/user-attachments/assets/b67de365-b65f-4cc1-a47e-6ebcd0e16edb)

É solicitada a escolha de uma pasta de destino para salvar os arquivos.
![passo2](https://github.com/user-attachments/assets/386a919c-4267-4a52-a59f-62919efb50b9)

O programa renderiza cada página, extrai o conteúdo principal, limpa os elementos irrelevantes e salva o resultado em arquivos .md na pasta escolhida.
Ao final, uma mensagem de sucesso ou erro é exibida, e o usuário pode acessar o histórico de extrações da sessão.
![falha](https://github.com/user-attachments/assets/49d30a32-8b7e-45c9-b46d-49c17da58b1a)
![sucesso](https://github.com/user-attachments/assets/879003da-7630-4396-b595-7d6d45af23ff)

