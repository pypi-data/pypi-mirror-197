import pyttsx3
import PyPDF2
import pdfplumber as pdftool
from googletrans import Translator

class infoPdf:
    

    def __init__(self):
        
        pass

    def SayThis(self, nome_pdf, opcao, numero):
        
        cont = 0
        txt = ''
        with pdftool.open(nome_pdf) as tool:

                for p_no, pagina in enumerate(tool.pages, 1):

                    cont += 1
        if opcao == 0:
            if (numero > cont) and (numero < cont):
                txt = 'Não foi possível encontrar a página. Tentar novamente.'
            else:
                pdf_file = open(nome_pdf, 'rb')

                pdf_reader = PyPDF2.PdfReader(pdf_file)

                page = pdf_reader.pages[numero-1]

                content = f'PAGE {numero}\n'
                content += page.extract_text()

                txt = content
        elif opcao == 1:
            with pdftool.open(nome_pdf) as tool:

                for p_no, pagina in enumerate(tool.pages, 1):

                    pag = f'\nPAGINA {p_no}\n'

                    data = pagina.extract_text()

                    txt += pag
                    txt += data
        
            
        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()

    def Translator(self, nome_pdf, pagina, lingua):
        """
        Traduz o conteúdo de uma página específica de um arquivo PDF para inglês e salva em um arquivo de texto.

        Parâmetros:
        ----------
        nome_pdf: str
            O nome do arquivo PDF a ser traduzido.
        pagina: int
            O número da página a ser traduzida.

        Retorno:
        -------
        Nenhum.
        """

        pdf_file = open(nome_pdf, 'rb')

        pdf_reader = PyPDF2.PdfReader(pdf_file)

        page = pdf_reader.pages[pagina-1]

        content = f'PAGE {pagina}\n'
        content += page.extract_text()

        pdf_file.close()

        arquivo = open('arquivo.txt', 'w', encoding='utf-8')
        translator = Translator()

        traducao = translator.translate(content, dest=lingua).text

        arquivo.write(traducao)


