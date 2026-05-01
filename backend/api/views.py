from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import datetime
import os

def is_reportlab_available():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        return True
    except ImportError:
        return False

def register_fonts():
    """Register fonts with Cyrillic support"""
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_dir = os.path.join(current_dir, '..', 'fonts')
        font_dir = os.path.abspath(font_dir)
        
        registered = False
        
        # Register regular font
        regular_font = os.path.join(font_dir, 'DejaVuSans.ttf')
        if os.path.exists(regular_font):
            pdfmetrics.registerFont(TTFont('DejaVuSans', regular_font))
            registered = True
        
        # Register bold font
        bold_font = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
        if os.path.exists(bold_font):
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_font))
        
        return registered
    except:
        return False


@method_decorator(login_required, name='dispatch')
class CertificatePDFView(APIView):
    """Generate PDF certificate for authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not is_reportlab_available():
            return HttpResponse("ReportLab not installed", status=500)
        
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        
        # Register fonts
        fonts_registered = register_fonts()
        font_name = "DejaVuSans" if fonts_registered else "Helvetica"
        font_bold = "DejaVuSans-Bold" if fonts_registered else "Helvetica-Bold"
        
        user = request.user
        profile = user.player_profile
        
        # Prepare data
        full_name = ""
        if user.first_name or user.last_name:
            full_name = f"{user.first_name} {user.last_name}".strip()
        else:
            full_name = user.username
        
        progress = profile.progress
        date_str = datetime.date.today().strftime('%d.%m.%Y')
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate_{}.pdf"'.format(user.username)
        
        # Setup canvas
        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        
        # Switch to landscape
        c.setPageSize((height, width))
        page_width, page_height = height, width
        
        # Background (light)
        c.setFillColor(HexColor('#F5F5F5'))
        c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
        
        # Border
        c.setStrokeColor(HexColor('#007ACC'))
        c.setLineWidth(8)
        c.rect(40, 40, page_width-80, page_height-80, fill=0, stroke=1)
        
        # Header - Logo
        c.setFillColor(HexColor('#007ACC'))
        c.setFont(font_bold, 28)
        c.drawString(100, page_height-80, "PC Workshop")
        
        # Title - CERTIFICATE
        c.setFillColor(HexColor('#007ACC'))
        c.setFont(font_bold, 48)
        title_width = c.stringWidth("CERTIFICATE", font_bold, 48)
        c.drawString((page_width-title_width)/2, page_height-160, "CERTIFICATE")
        
        # Subtitle
        c.setFillColor(HexColor('#555555'))
        c.setFont(font_name, 14)
        c.drawString((page_width-300)/2, page_height-190, "Confirmation of successful course completion")
        
        # Recipient name
        c.setFillColor(HexColor('#007ACC'))
        c.setFont(font_bold, 36)
        name_width = c.stringWidth(full_name, font_bold, 36)
        c.drawString((page_width-name_width)/2, page_height-280, full_name)
        
        # Line under name
        c.setStrokeColor(HexColor('#007ACC'))
        c.setLineWidth(2)
        line_start = (page_width-name_width-20)/2
        c.line(line_start, page_height-295, line_start+name_width+20, page_height-295)
        
        # Text under name
        c.setFillColor(HexColor('#555555'))
        c.setFont(font_name, 12)
        c.drawString((page_width-200)/2, page_height-320, "successfully completed PC assembly course")
        
        # Progress
        c.setFillColor(HexColor('#2E7D32'))
        c.setFont(font_bold, 24)
        progress_text = "Total progress: {}%".format(progress)
        progress_width = c.stringWidth(progress_text, font_bold, 24)
        c.drawString((page_width-progress_width)/2, page_height-380, progress_text)
        
        # Date and signature (bottom)
        c.setFillColor(HexColor('#555555'))
        c.setFont(font_name, 10)
        c.drawString(80, 60, "Issue date: {}".format(date_str))
        
        c.drawString(page_width-280, 60, "Course Administration")
        c.setStrokeColor(HexColor('#007ACC'))
        c.setLineWidth(1)
        c.line(page_width-280, 50, page_width-80, 50)
        
        c.showPage()
        c.save()
        
        return response


class CertificateInfoView(APIView):
    """Get certificate info (for preview)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = user.player_profile
        
        full_name = ""
        if user.first_name or user.last_name:
            full_name = f"{user.first_name} {user.last_name}".strip()
        else:
            full_name = user.username
        
        return Response({
            'full_name': full_name,
            'progress': profile.progress,
            'date': datetime.date.today().strftime('%d.%m.%Y'),
        })
