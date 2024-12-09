import streamlit as st
from datetime import datetime
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuración de correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"

# Inicializar estado de sesión
if "nombre_completo" not in st.session_state:
    st.session_state.nombre_completo = None
if "correo" not in st.session_state:
    st.session_state.correo = None
if "clave_verificacion" not in st.session_state:
    st.session_state.clave_verificacion = None
if "clave_validada" not in st.session_state:
    st.session_state.clave_validada = False

# Función para generar clave aleatoria
def generar_clave():
    return random.randint(100000, 999999)

# Función para enviar correo con clave y consentimiento informado
def enviar_clave_correo(destinatario, clave, nombre_completo):
    try:
        consentimiento_con_nombre = f"""
        Yo, {nombre_completo}, he leído y entendido los términos del siguiente consentimiento informado:

        Bienvenido a nuestra plataforma de captura y transmisión de datos fisiológicos. Este servicio está diseñado para facilitar la comunicación de mis datos de salud directamente a mi médico de manera eficiente y segura. Y que es independiente a la instancia de salud donde me atiendo.

        **Datos Fisiológicos Admitidos**
        - Temperatura Corporal
        - Presión Arterial (sistólica y diastólica)
        - Oxigenación en Sangre (oximetría)
        - Electrocardiograma (ECG), el cual debo subir en formato PDF.

        **Recomendación de Equipos Médicos**
        - La recomendación de dispositivos es exclusivamente de carácter informativo.
        - Tengo la libertad de adquirir los dispositivos que considere adecuados.
        - El uso, desempeño y costo de los equipos recomendados no generan ninguna responsabilidad para esta plataforma ni para mi médico tratante.

        **Aviso Legal**
        Este servicio es una herramienta de apoyo para mejorar la calidad de la atención médica. Sin embargo, entiendo que no sustituye la consulta médica presencial ni la valoración clínica directa por parte de mi médico tratante.

        **Declaración de Aceptación**
        Al enviar la clave de verificación que he recibido, confirmo que acepto los términos descritos en este consentimiento informado.
        """

        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Clave de Verificación y Consentimiento Informado"
        cuerpo = f"""
        Estimado/a {nombre_completo}:

        Su clave de verificación es: {clave}

        {consentimiento_con_nombre}

        Instrucciones importantes:
        - Ingrese la clave de verificación proporcionada en la plataforma para continuar con el registro.
        - Al ingresar esta clave, usted confirma haber leído, entendido y aceptado los términos del consentimiento informado.

        Gracias por confiar en nuestra plataforma para la gestión de su salud.
        """
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, destinatario, mensaje.as_string())
    except Exception as e:
        st.error(f"Error al enviar la clave: {e}")

# Función para enviar correo de confirmación con archivo adjunto
def enviar_confirmacion(destinatario, nombre_completo, datos_registrados, archivo_ecg):
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Confirmación de Registro de Datos Fisiológicos"
        cuerpo = f"""
        Estimado/a {nombre_completo}:

        Sus datos fisiológicos han sido registrados correctamente. A continuación, se presenta un resumen de la información enviada:

        {datos_registrados}

        Gracias por confiar en nuestra plataforma para la gestión de su salud.
        """
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Adjuntar archivo ECG
        if archivo_ecg:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(archivo_ecg.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={archivo_ecg.name}",
            )
            mensaje.attach(part)

        # Enviar correo
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, destinatario, mensaje.as_string())

        st.success("Correo de confirmación enviado correctamente.")
    except Exception as e:
        st.error(f"Error al enviar el correo de confirmación: {e}")

# Interfaz principal
st.title("Registro de Datos Fisiológicos")

# **Mostrar consentimiento informado directamente**
st.markdown("""
Bienvenido a nuestra plataforma de captura y transmisión de datos fisiológicos. Este servicio está diseñado para facilitar la comunicación de sus datos de salud directamente a su médico de manera eficiente y segura. Y que es independiente a la instancia de salud donde se atiende.

### Datos Fisiológicos Admitidos
En esta plataforma, puede registrar y transmitir los siguientes datos:
- Temperatura Corporal
- Presión Arterial (sistólica y diastólica)
- Oxigenación en Sangre (oximetría)
- Electrocardiograma (ECG), que debe subirse en formato PDF.

### Recomendación de Equipos Médicos
Para una correcta captura de estos signos vitales, le proporcionamos una lista de dispositivos médicos recomendados que cumplen con estándares de calidad. Es importante mencionar que:
- La recomendación de dispositivos es exclusivamente de carácter informativo.
- Usted tiene la libertad de adquirir los dispositivos que considere adecuados.
- El uso, desempeño y costo de los equipos recomendados no genera ninguna responsabilidad para esta plataforma ni para su médico.

### Aviso Legal
Este servicio es una herramienta de apoyo para mejorar la calidad de la atención médica. Sin embargo, no sustituye la consulta médica presencial ni la valoración clínica directa por parte de su médico tratante.

Si tiene alguna pregunta sobre el uso de la plataforma o los dispositivos recomendados, no dude en ponerse en contacto con nuestro equipo de soporte técnico.

**Gracias por confiar en nosotros para la gestión de su salud.**
""")

# **PASO 1: Consentimiento informado**
st.subheader("Consentimiento Informado")
nombre_completo = st.text_input("Ingrese su nombre completo para firmar el consentimiento")
consentimiento = st.checkbox(f"Declaro que he leído y acepto los términos del consentimiento informado, firmado por {nombre_completo}")

if not consentimiento or not nombre_completo:
    st.warning("Debe aceptar el consentimiento informado y proporcionar su nombre completo para continuar.")
else:
    st.success("Consentimiento informado aceptado. Continúe con la verificación de su correo electrónico.")
    st.session_state.nombre_completo = nombre_completo

# **PASO 2: Verificación de correo electrónico**
if consentimiento and nombre_completo:
    st.subheader("Verificación de Correo Electrónico")
    correo_1 = st.text_input("Ingrese su correo electrónico")
    correo_2 = st.text_input("Confirme su correo electrónico")

    if st.button("Enviar clave de verificación"):
        if correo_1 != correo_2 or not correo_1:
            st.error("Los correos no coinciden o están vacíos. Por favor, inténtelo de nuevo.")
        else:
            clave = generar_clave()
            st.session_state.clave_verificacion = clave
            st.session_state.correo = correo_1
            enviar_clave_correo(correo_1, clave, nombre_completo)
            st.success("Clave enviada a su correo electrónico junto con el consentimiento informado.")

# **PASO 3: Validación de clave de verificación**
if consentimiento and nombre_completo and st.session_state.clave_verificacion:
    st.subheader("Validación de Clave")
    clave_ingresada = st.text_input("Ingrese la clave de verificación enviada a su correo", type="password")

    if st.button("Validar clave"):
        if clave_ingresada == str(st.session_state.clave_verificacion):
            st.success("Clave validada correctamente. Puede proceder con el registro.")
            st.session_state.clave_validada = True
        else:
            st.error("Clave incorrecta. Por favor, intente nuevamente.")

# **PASO 4: Registro de datos fisiológicos**
if st.session_state.clave_validada:
    with st.form("registro_form"):
        st.subheader("Registro de Datos Fisiológicos")
        numero_economico = st.text_input("Número económico del INCICh")
        presion_sistolica = st.number_input("Presión arterial sistólica (mmHg)", min_value=70, max_value=200)
        presion_diastolica = st.number_input("Presión arterial diastólica (mmHg)", min_value=40, max_value=120)
        oxigenacion = st.slider("Oxigenación (%)", min_value=80, max_value=100)
        temperatura = st.number_input("Temperatura corporal (°C)", min_value=35.0, max_value=42.0)
        ecg = st.file_uploader("Suba su ECG (PDF)", type=["pdf"])

        submit_button = st.form_submit_button("Registrar")

        if submit_button:
            if not ecg:
                st.error("Por favor, suba su archivo de ECG en formato PDF.")
            else:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                datos_registrados = f"""
                - Nombre: {st.session_state.nombre_completo}
                - Número Económico: {numero_economico}
                - Presión Sistólica: {presion_sistolica}
                - Presión Diastólica: {presion_diastolica}
                - Oxigenación: {oxigenacion}%
                - Temperatura: {temperatura}°C
                - Fecha y Hora: {fecha_hora}
                """
                st.success("¡Registro exitoso!")
                st.write(f"**Datos Registrados:**\n{datos_registrados}")

                # Enviar correo de confirmación
                enviar_confirmacion(
                    st.session_state.correo,
                    st.session_state.nombre_completo,
                    datos_registrados,
                    ecg,
                )

