### Este é um script Python que lê e traduz arquivos PDF para texto e áudio usando as bibliotecas PyPDF2, pdfplumber, ### pyttsx3 e googletrans. Ele contém a classe InfoPdf que tem dois métodos: SayThis e Translator.

### O método SayThis lê o conteúdo do arquivo PDF especificado e reproduz em áudio usando a biblioteca pyttsx3. Ele usa o pdfplumber para extrair o texto do arquivo PDF e adiciona o número da página em que o texto foi encontrado. Depois disso, usa a biblioteca pyttsx3 para converter o texto em voz.

### O metodo Translator traduz o conteúdo de uma página específica do arquivo PDF para lingua especifica e salva em um arquivo de texto. Ele usa a biblioteca PyPDF2 para abrir o arquivo PDF e extrair o texto da página especificada. Depois disso, usa a biblioteca googletrans para traduzir o texto para o inglês e salva o resultado em um arquivo de texto.

### Para usar este script, basta criar um objeto da classe InfoPdf e chamar os métodos SayThis e Translator com os parâmetros necessários. Certifique-se de instalar as bibliotecas necessárias antes de executar o script.

### Exemplo de uso:

from DataInfoPdf import arqPdf

pdf = arqPdf.infoPdf()

# Ler e reproduzir em audio o arquivo PDF

# 0 ou 1 indica o que fazer, onde 0 ler uma pagina especifica e 1 a leitura do arquivo todo

pdf.SayThis(nome_pdf (string), 0 ou 1 (int), numero da pagina (int))

# Traduzir a página 3 do arquivo PDF para inglês e salvar em um arquivo de texto

pdf.Translator(nome_pdf (string), pagina (int), lingua(string))
