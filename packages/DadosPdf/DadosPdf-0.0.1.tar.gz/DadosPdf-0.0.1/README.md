### Este é um script Python que lê e traduz arquivos PDF para texto e áudio usando as bibliotecas PyPDF2, pdfplumber, ### pyttsx3 e googletrans. Ele contém a classe InfoPdf que tem dois métodos: SayThis e Translator.

### O método SayThis lê o conteúdo do arquivo PDF especificado e reproduz em áudio usando a biblioteca pyttsx3. Ele usa o pdfplumber para extrair o texto do arquivo PDF e adiciona o número da página em que o texto foi encontrado. Depois disso, usa a biblioteca pyttsx3 para converter o texto em voz.

### O método Translator traduz o conteúdo de uma página específica do arquivo PDF para lingua especifica e salva em um arquivo de texto. Ele usa a biblioteca PyPDF2 para abrir o arquivo PDF e extrair o texto da página especificada. Depois disso, usa a biblioteca googletrans para traduzir o texto para o inglês e salva o resultado em um arquivo de texto.

### Para usar este script, basta criar um objeto da classe InfoPdf e chamar os métodos SayThis e Translator com os parâmetros necessários. Certifique-se de instalar as bibliotecas necessárias antes de executar o script.

### Exemplo de uso:

from docpdf import docpdf

pdf = docpdf.infoPdf()

# Ler e reproduzir em áudio o arquivo PDF

pdf.SayThis('meu_arquivo.pdf')

# Traduzir a página 3 do arquivo PDF para inglês e salvar em um arquivo de texto

pdf.Translator('meu_arquivo.pdf', 3)
