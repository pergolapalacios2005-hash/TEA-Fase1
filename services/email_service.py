import smtplib
from email.message import EmailMessage

def enviar_correo_bienvenida(destinatario):
    """Envía correo de bienvenida al usuario registrado en el sistema médico."""
    remitente = "pergolapalacios2005@gmail.com"
    password_app = "vfitvxuisqgdlbyw"

    msg = EmailMessage()
    msg['Subject'] = "🏥 ¡Bienvenido al Sistema Médico de Diagnóstico Previo!"
    msg['From'] = remitente
    msg['To'] = destinatario
    msg.set_content(f"""
¡Hola!

✅ ¡Tu cuenta ha sido creada exitosamente!

Ahora eres parte del Sistema Médico de Diagnóstico Previo, una herramienta 
basada en Inteligencia Artificial para análisis de síntomas preliminar.

📋 ¿CÓMO USAR EL SISTEMA?

1. Inicia sesión en la aplicación
2. Ve a "Nuevo Diagnóstico"
3. Describe detalladamente tus síntomas
4. El sistema IA analizará tus síntomas
5. Recibirás un diagnóstico preliminar

⚠️ IMPORTANTE - AVISO MÉDICO:

Este sistema proporciona DIAGNÓSTICO PRELIMINAR ÚNICAMENTE.
NO reemplaza:
• Consulta con un médico profesional
• Diagnóstico médico oficial
• Atención de emergencias

SIEMPRE CONSULTA CON UN PROFESIONAL DE SALUD PARA:
✓ Confirmar cualquier diagnóstico
✓ Recibir tratamiento
✓ Ante síntomas nuevos o inusuales
✓ Emergencias médicas (llama a emergencias)

🔐 PRIVACIDAD Y SEGURIDAD:

Tu información médica es:
• Almacenada de forma segura
• Encriptada en tránsito
• Protegida bajo políticas de privacidad
• Solo accesible por ti

📞 SOPORTE:

¿Problemas técnicos? Contacta: support@sistemamedicoia.com
¿Dudas? Revisa nuestro apartado de Ayuda en la aplicación.

Atentamente,
El equipo del Sistema Médico de Diagnóstico Previo

---
Este correo contiene información importante sobre tu cuenta médica.
Guárdalo para futuras referencias.
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password_app)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def enviar_diagnostico_realizado(destinatario, diagnostico_resumen):
    """Envía correo con resumen del diagnóstico realizado."""
    remitente = "pergolapalacios2005@gmail.com"
    password_app = "vfitvxuisqgdlbyw"

    msg = EmailMessage()
    msg['Subject'] = "📋 Tu Diagnóstico Preliminar - Sistema Médico"
    msg['From'] = remitente
    msg['To'] = destinatario
    msg.set_content(f"""
¡Hola!

Tu análisis de síntomas ha sido completado.

RESUMEN DEL DIAGNÓSTICO:
{diagnostico_resumen}

⚠️ RECUERDA:
Este es un diagnóstico PRELIMINAR basado en IA.
CONSULTA CON UN MÉDICO PROFESIONAL para confirmación.

Accede a tu historial en la aplicación para ver detalles completos.

---
Sistema Médico de Diagnóstico Previo
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password_app)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Error al enviar diagnóstico: {e}")
        return False