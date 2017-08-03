import io

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def getMark(x = 0, y = 0, text = "Hello world!"):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(x, y, text)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    mark_pdf = PdfFileReader(packet)
    return mark_pdf.getPage(0)

def markpdf(file_in, file_out):
    # open origin for read and destination for write
    original_pdf = PdfFileReader(file_in)
    result_pdf = PdfFileWriter()

    info = original_pdf.documentInfo
    info.update({'/Creator': 'markpdf by Tony G. Bolaño'})
    info.update({'/Author': 'Tony G. Bolaño'})
    info.update({'/Title': 'Testing markpdf'})
    info.update({'/Subject': 'Testing markpdf subject'})

    # this doesn't work, only can put one of this :(
    info.update({'/Keywords': 'hola'})

    result_pdf.addMetadata(info)

    the_mark = getMark()
    print(the_mark)

    # read ecery page of original file
    # and inserts into destination file
    for page in original_pdf.pages:
        #page = original_pdf.getPage(i)
        page.mergePage(the_mark)
        result_pdf.addPage(page)

    result_pdf.addPage(the_mark)

    # encrypt pdf
    result_pdf.encrypt('', 'vaya')

    # save destination pdf to disk
    output_stream = open(file_out, "wb")
    result_pdf.write(output_stream)
    output_stream.close()

if __name__ == '__main__':
    markpdf('test.pdf', 'result.pdf')