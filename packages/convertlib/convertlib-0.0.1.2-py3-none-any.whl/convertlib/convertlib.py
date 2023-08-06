import convertapi

class convertlib():
    """Realiza a conversão de diversas extensões de arquivos através da API Convertapi.

    Parameters
    ----------
    path: str
        Caminho onde o arquivo está localizado com sua devida extensão

    Methods
    -------
    docx2jpg():
    Converte arquivos docx para jpg

    docx2pdf():
    Converte arquivos docx para pdf

    docx2png():
    Converte arquivos docx para png

    gif2png():
    Converte arquivos gif para png

    html2docx():
    Converte arquivos html para docx

    jpg2svg():
    Converte arquivos jpg para svg

    pdf2csv():
    Converte arquivos pdf para csv

    pdf2jpg():
    Converte arquivos pdf para jpg

    pdf2png():
    Converte arquivos pdf para png

    pdf2txt():
    Converte arquivos pdf para txt
        
    png2pdf():
    Converte arquivos png para pdf

    pptx2pdf():
    Converte arquivos pptx para pdf
        
    txt2jpg():
    Converte arquivos txt para jpg

    txt2pdf():
    Converte arquivos txt para pdf

    txt2png():
    Converte arquivos txt para png

    """

    def __init__(self, path):
        self._path = path

    def docx2jpg(self):
        """
        Converte arquivos docx para jpg
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('jpg', { 'File': self._path }, from_format = 'docx').save_files('./')

    def docx2pdf(self):
        """
        Converte arquivos docx para pdf
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('pdf', { 'File': self._path }, from_format = 'docx').save_files('./')

    def docx2png(self):
        """
        Converte arquivos docx para png
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('png', { 'File': self._path }, from_format = 'docx').save_files('./')

    def gif2png(self):
        """
        Converte arquivos gif para png
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('png', { 'File': self._path }, from_format = 'gif').save_files('./')

    def html2docx(self):
        """
        Converte arquivos html para docx
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('docx', { 'File': self._path }, from_format = 'html').save_files('./')

    def jpg2svg(self):
        """
        Converte arquivos jpg para svg
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('svg', { 'File': self._path }, from_format = 'jpg').save_files('./')

    def pdf2csv(self):
        """
        Converte arquivos pdf para csv
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('csv', { 'File': self._path, 'Delimiter': ',' }, from_format = 'pdf').save_files('./')

    def pdf2jpg(self):
        """
        Converte arquivos pdf para jpg
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('jpg', { 'File': self._path }, from_format = 'pdf').save_files('./')

    def pdf2png(self):
        """
        Converte arquivos pdf para png
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('png', { 'File': self._path }, from_format = 'pdf').save_files('./')

    def pdf2txt(self):
        """
        Converte arquivos pdf para txt
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('txt', { 'File': self._path }, from_format = 'pdf').save_files('./')
        
    def png2pdf(self):
        """
        Converte arquivos png para pdf
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('pdf', { 'File': self._path }, from_format = 'png').save_files('./')

    def pptx2pdf(self):
        """
        Converte arquivos pptx para pdf
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('pdf', { 'File': self._path }, from_format = 'pptx').save_files('./')
        
    def txt2jpg(self):
        """
        Converte arquivos txt para jpg
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('jpg', { 'File': self._path }, from_format = 'txt').save_files('./')

    def txt2pdf(self):
        """
        Converte arquivos txt para pdf
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('pdf', { 'File': self._path }, from_format = 'txt').save_files('./')

    def txt2png(self):
        """
        Converte arquivos txt para png
        """
        convertapi.api_secret = 'wzxA1QPzyvAljkdK'
        convertapi.convert('png', { 'File': self._path }, from_format = 'txt').save_files('./')