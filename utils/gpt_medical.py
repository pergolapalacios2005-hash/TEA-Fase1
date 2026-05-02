"""
Módulo de Integración GPT Médico
Maneja la comunicación con OpenAI GPT para diagnóstico médico previo.
"""

import os
from typing import Dict, List, Tuple

class GPTMedicalClient:
    """Cliente para procesar síntomas mediante GPT especializado en medicina."""
    
    def __init__(self, api_key=None):
        """
        Inicializa el cliente GPT médico.
        
        Args:
            api_key (str): Clave API de OpenAI. Si no se proporciona, busca en variables de entorno.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = 'gpt-4'  # O 'gpt-3.5-turbo' según disponibilidad
        self.initialized = False
        
        if self.api_key:
            self.initialized = True
            print("✓ GPT Medical Client inicializado con API key.")
        else:
            print("⚠ GPT Medical Client: API key no configurada. Modo offline.")

    def crear_prompt_diagnostico(self, sintomas: str, edad: str = "", genero: str = "", 
                                 antecedentes: str = "") -> str:
        """
        Crea un prompt especializado para GPT en análisis médico.
        
        Args:
            sintomas: Descripción de síntomas del usuario
            edad: Edad del paciente
            genero: Género del paciente
            antecedentes: Antecedentes médicos relevantes
            
        Returns:
            str: Prompt formateado para GPT
        """
        prompt = f"""
Eres un asistente médico de diagnóstico preliminar especializado. Tu tarea es analizar 
síntomas y proporcionar un diagnóstico PRELIMINAR.

IMPORTANTE: Siempre recuerda que esto NO reemplaza consulta médica profesional.

DATOS DEL PACIENTE:
- Síntomas: {sintomas}
- Edad: {edad if edad else 'No especificada'}
- Género: {genero if genero else 'No especificado'}
- Antecedentes: {antecedentes if antecedentes else 'Ninguno reportado'}

ANALIZA Y PROPORCIONA:
1. Diagnósticos posibles (máx 5), ordenados por probabilidad
2. Nivel de confianza para cada diagnóstico (0-100%)
3. Síntomas que apoyan cada diagnóstico
4. Diagnósticos descartados y por qué
5. Recomendaciones de acciones inmediatas (si aplica)
6. Cuándo buscar atención médica de emergencia

RESPONDE EN FORMATO ESTRUCTURADO Y CLARO.
"""
        return prompt

    def analizar_sintomas(self, sintomas: str, edad: str = "", genero: str = "", 
                         antecedentes: str = "") -> Dict:
        """
        Envía síntomas a GPT y obtiene análisis diagnóstico.
        
        Args:
            sintomas: Descripción de síntomas
            edad: Edad del paciente
            genero: Género del paciente
            antecedentes: Antecedentes médicos
            
        Returns:
            dict: Resultado del análisis con diagnósticos y recomendaciones
        """
        if not self.initialized:
            return self._respuesta_offline()
        
        try:
            # Aquí irá la integración real con OpenAI
            # import openai
            # response = openai.ChatCompletion.create(...)
            
            prompt = self.crear_prompt_diagnostico(sintomas, edad, genero, antecedentes)
            
            # Placeholder para respuesta real
            resultado = {
                'exito': True,
                'diagnosticos': [],
                'confianza_general': 0.0,
                'recomendaciones': [],
                'accion_urgente': False,
                'prompt_usado': prompt[:100] + "..."
            }
            
            return resultado
            
        except Exception as e:
            return {
                'exito': False,
                'error': f"Error al conectar con GPT: {str(e)}",
                'diagnosticos': [],
                'recomendaciones': []
            }

    def _respuesta_offline(self) -> Dict:
        """Retorna respuesta en modo offline cuando no hay API key."""
        return {
            'exito': False,
            'modo': 'offline',
            'mensaje': 'Sistema GPT no configurado. Por favor, añade OPENAI_API_KEY a variables de entorno.',
            'diagnosticos': [],
            'recomendaciones': ['Configura la clave API de OpenAI para usar diagnóstico con IA'],
            'accion_urgente': False
        }

    def generar_reporte_pdf(self, diagnostico_data: Dict, user_name: str = "Paciente") -> str:
        """
        Genera un reporte en PDF del diagnóstico (función futura).
        
        Args:
            diagnostico_data: Datos del diagnóstico
            user_name: Nombre del usuario
            
        Returns:
            str: Ruta del PDF generado
        """
        # Implementación futura con reportlab o similar
        return ""

    def validar_entrada_medica(self, texto: str) -> Tuple[bool, str]:
        """
        Valida que la entrada sea médicamente relevante.
        
        Args:
            texto: Texto a validar
            
        Returns:
            tuple: (es_valido, mensaje)
        """
        palabras_prohibidas = ['spam', 'publicidad', 'broma']
        
        if not texto or len(texto.strip()) < 10:
            return False, "Descripción muy corta"
        
        if len(texto) > 2000:
            return False, "Descripción muy larga (máx. 2000 caracteres)"
        
        if any(palabra in texto.lower() for palabra in palabras_prohibidas):
            return False, "Contenido no válido para análisis médico"
        
        return True, "Entrada válida"
