import qrcode
from io import BytesIO
from django.core.files import File

def Get_Qr_Code(data):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    file_name = 'qr_code.png'
    file_object = File(buffer, name=file_name)

    return file_object