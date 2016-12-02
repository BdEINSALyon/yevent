import os
from time import time

from django.shortcuts import get_object_or_404
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.graphics.shapes import Drawing, rl_config
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

# Create your views here.
from invitation import security
from ticketing.models import Ticket, OptionSelection


def MyTicketsView(request):
    pass


def print(request, code):
    # Create the HttpResponse object with the appropriate PDF headers.

    ticket = get_object_or_404(Ticket, id=int(security.decrypt(code)['id']))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{}.pdf"'.format(ticket.gid())

    p = canvas.Canvas(response, pagesize=(595.27, 841.89),
                      bottomup=1,
                      pageCompression=0,
                      verbosity=0,
                      encrypt=None)

    logo = ImageReader('http://logos.bde-insa-lyon.fr/gala/gala_black_background_white.png')

    p.drawImage(logo, 10, 775, width=100, height=35, mask='auto')
    p.setFontSize(25)
    p.drawString(110, 750, ticket.first_name)
    p.drawString(110, 720, ticket.last_name)
    p.setFontSize(18)
    p.drawString(100, 680, ticket.email or '')

    qrw = QrCodeWidget(security.encrypt({'id': ticket.id, 'time': time()}))
    d = Drawing()
    d.add(qrw)

    renderPDF.draw(d, p, 20, 680)
    p.setFontSize(15)

    p.drawString(350, 750, ticket.price.name)
    i=-1
    for option in OptionSelection.objects.filter(ticket=ticket).all():
        if option.seats > 0:
            i += 1
            p.drawString(335, 720-50*i, "{}x ".format(option.seats))
            p.drawString(360, 720-50*i, option.option.name)

    p.setFontSize(11)
    p.drawCentredString(289, 50, "© 2016 Bureau des Elèves de l'INSA Lyon")

    p.showPage()
    p.save()
    return response
