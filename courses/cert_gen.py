from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import os

# Constantes y variables
MESES = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}

def generate_certf(name, dni, commission, mat_str, course):
    # variables
    idntify = f'{name} D.N.I.: {dni}'
    matricula = mat_str
    institute_part1 = 'El instituto de formación digital orientado a la administración'
    institute_part2 = 'y gestión empresarial www.instituto-digitaltech.com certifica que'
    text_course = 'aprobó la capacitación'
    fecha_hoy = datetime.now()
    nombre_mes = MESES[fecha_hoy.strftime('%B')]
    fecha_formateada = fecha_hoy.strftime(f'%d de {nombre_mes} de %Y')
    date = f'Se extiende el presente el día {fecha_formateada}'
    auth = 'ZENKLUSEN, Juan Ignacio'
    auth_ = 'Director Instituto DigitalTech'
    name_file = f'{matricula}-{course}-{name}-{fecha_hoy}.png'

    # Colores
    black_color = (0, 0, 0, 255)
    primary_font_color = (12, 0, 56, 255)
    secondary_font_color = (43, 89, 147, 255)

    url = f'media/{commission}'
    generate_cert = Image.open(url) # Guardo en la variable la imagen base
    size = generate_cert.size # En una tupla obtengo el tamaño del certificado A4

    # Lienzo
    draw = ImageDraw.Draw(generate_cert)

    # Fuentes
    primarty_font = ImageFont.truetype('courses/fonts/Josefin_Sans/static/JosefinSans-Bold.ttf', 40)
    secondary_font = ImageFont.truetype('courses/fonts/Josefin_Sans/static/JosefinSans-Bold.ttf', 80)
    name_font = ImageFont.truetype('courses/fonts/Josefin_Sans/static/JosefinSans-Bold.ttf', 60)
    auth_font = ImageFont.truetype('courses/fonts/Josefin_Sans/static/JosefinSans-Medium.ttf', 35)

    # Texto: instituto1
    bbox = draw.textbbox((0, 0), institute_part1, font = primarty_font)
    width_institute1 = bbox[2] - bbox[0]  # ancho
    height_institute1 = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_institute1 // 2, 430), # coordenadas en x, y
        institute_part1, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = primarty_font # por ultimo la fuente
    )

    # Texto: instituto2
    bbox = draw.textbbox((0, 0), institute_part2, font = primarty_font)
    width_institute2 = bbox[2] - bbox[0]  # ancho
    height_institute2 = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_institute2 // 2, 480), # coordenadas en x, y
        institute_part2, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = primarty_font # por ultimo la fuente
    )

    # Texto: Nombre
    bbox = draw.textbbox((0, 0), idntify, font = name_font)
    width_idntify = bbox[2] - bbox[0]  # ancho
    height_idntify = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_idntify // 2, 565), # coordenadas en x, y
        idntify, # texto a imprimir
        secondary_font_color, # tupla para el color de texto, RGBA
        font = name_font # por ultimo la fuente
    )

    # Texto: text_course
    bbox = draw.textbbox((0, 0), text_course, font = primarty_font)
    width_text_course = bbox[2] - bbox[0]  # ancho
    height_text_course = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_text_course // 2, 650), # coordenadas en x, y
        text_course, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = primarty_font # por ultimo la fuente
    )

    # Texto: Curso
    bbox = draw.textbbox((0, 0), course, font = name_font)
    width_course = bbox[2] - bbox[0]  # ancho
    height_course = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_course // 2, 725), # coordenadas en x, y
        course, # texto a imprimir
        primary_font_color, # tupla para el color de texto, RGBA
        font = name_font # por ultimo la fuente
    )

    # Texto: fecha
    bbox = draw.textbbox((0, 0), date, font = primarty_font)
    width_date = bbox[2] - bbox[0]  # ancho
    height_date = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_date // 2, 830), # coordenadas en x, y
        date, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = primarty_font # por ultimo la fuente
    )

    # Texto: auth
    bbox = draw.textbbox((0, 0), auth, font = auth_font)
    width_auth = bbox[2] - bbox[0]  # ancho
    height_auth = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_auth // 2, 1105), # coordenadas en x, y
        auth, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = auth_font # por ultimo la fuente
    )

    # Texto: auth
    bbox = draw.textbbox((0, 0), auth_, font = auth_font)
    width_auth_ = bbox[2] - bbox[0]  # ancho
    height_auth_ = bbox[3] - bbox[1]  # alto

    draw.text(
        (size[0] // 2 - width_auth_ // 2, 1140), # coordenadas en x, y
        auth_, # texto a imprimir
        black_color, # tupla para el color de texto, RGBA
        font = auth_font # por ultimo la fuente
    )

    # Genero el certificado
    save_path = "media/all_certificates/"  # Reemplaza con la ruta deseada
    generate_cert.save(os.path.join(save_path, name_file))

    return name_file
