#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Abono para Invernaderos - App Móvil Android
Convertida de Streamlit a Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from datetime import datetime

# Configurar ventana para móvil
Window.size = (360, 640)

class CalculadoraAbonoApp(App):
    def build(self):
        self.title = "🌱 Calculadora de Abono"
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Título
        title = Label(
            text='🌱 Calculadora de Abono\nInvernaderos',
            font_size='20sp',
            size_hint_y=None,
            height=dp(80),
            text_size=(None, None),
            halign='center',
            color=(0.1, 0.6, 0.2, 1)
        )
        main_layout.add_widget(title)
        
        # ScrollView para formulario
        scroll = ScrollView()
        form_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=(0, dp(10))
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Crear campos de entrada
        self.inputs = {}
        
        # Número de invernadero
        form_layout.add_widget(self.create_input_field(
            "Número de invernadero:", "numero_invernadero", ""
        ))
        
        # Superficie
        form_layout.add_widget(self.create_input_field(
            "Superficie del invernadero (m²):", "superficie", "0"
        ))
        
        # Goteros totales
        form_layout.add_widget(self.create_input_field(
            "Goteros totales:", "goteros_totales", "0"
        ))
        
        # Caudal por gotero
        form_layout.add_widget(self.create_input_field(
            "Caudal de cada gotero (L×H⁻¹):", "caudal_gotero", "0"
        ))
        
        # CE del abono
        form_layout.add_widget(self.create_input_field(
            "CE del abono:", "ce_abono", "0"
        ))
        
        # Tiempo de riego
        form_layout.add_widget(self.create_input_field(
            "Tiempo de riego (minutos):", "tiempo_riego", "0"
        ))
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        # Botón calcular
        calc_button = Button(
            text='🧮 CALCULAR',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.7, 0.3, 1),
            font_size='18sp'
        )
        calc_button.bind(on_press=self.calcular)
        main_layout.add_widget(calc_button)
        
        # Área de resultados
        self.resultado_label = Label(
            text='Introduce los datos y presiona CALCULAR',
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='top',
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.resultado_label)
        
        # Botones de acción
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        share_button = Button(
            text='📤 Compartir',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        share_button.bind(on_press=self.compartir)
        
        reset_button = Button(
            text='🔄 Reiniciar',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        reset_button.bind(on_press=self.reiniciar)
        
        button_layout.add_widget(share_button)
        button_layout.add_widget(reset_button)
        main_layout.add_widget(button_layout)
        
        return main_layout
    
    def create_input_field(self, label_text, key, default_value):
        """Crear campo de entrada con etiqueta"""
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5)
        )
        
        # Etiqueta
        label = Label(
            text=label_text,
            size_hint_y=None,
            height=dp(30),
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1),
            text_size=(Window.width - dp(40), None),
            halign='left',
            valign='bottom'
        )
        
        # Campo de entrada
        text_input = TextInput(
            text=default_value,
            size_hint_y=None,
            height=dp(40),
            font_size='16sp',
            multiline=False,
            input_filter='float' if key != 'numero_invernadero' else None
        )
        
        self.inputs[key] = text_input
        
        container.add_widget(label)
        container.add_widget(text_input)
        
        return container
    
    def get_float_value(self, key, default=0.0):
        """Obtener valor float de un input"""
        try:
            value = self.inputs[key].text.strip()
            return float(value) if value else default
        except ValueError:
            return default
    
    def calcular(self, instance):
        """Realizar cálculos"""
        try:
            # Obtener valores
            numero_invernadero = self.inputs['numero_invernadero'].text.strip()
            superficie = self.get_float_value('superficie')
            goteros_totales = int(self.get_float_value('goteros_totales'))
            caudal_gotero = self.get_float_value('caudal_gotero')
            ce_abono = self.get_float_value('ce_abono')
            tiempo_riego = self.get_float_value('tiempo_riego')
            
            # Validaciones
            if superficie <= 0 or goteros_totales <= 0 or caudal_gotero <= 0:
                self.mostrar_error("Introduce valores válidos para superficie, goteros y caudal.")
                return
            
            # Cálculos principales
            goteros_por_metro = goteros_totales / superficie
            litros_agua_hora = superficie * goteros_por_metro * caudal_gotero
            caudal_1000m2_hora = litros_agua_hora / (superficie / 1000)
            
            # Agua gastada en el riego
            agua_gastada_riego = 0
            if tiempo_riego > 0:
                agua_gastada_riego = ((superficie * goteros_por_metro * caudal_gotero) / 60) * tiempo_riego
            
            # Abono gastado
            abono_gastado = 0
            if ce_abono > 0 and tiempo_riego > 0:
                abono_gastado = (caudal_1000m2_hora / 100000) * ce_abono * tiempo_riego * (superficie / 1000)
            
            # Guardar resultados
            self.ultimo_calculo = {
                'numero_invernadero': numero_invernadero,
                'superficie': superficie,
                'goteros_totales': goteros_totales,
                'caudal_gotero': caudal_gotero,
                'ce_abono': ce_abono,
                'tiempo_riego': tiempo_riego,
                'goteros_por_metro': goteros_por_metro,
                'litros_agua_hora': litros_agua_hora,
                'caudal_1000m2_hora': caudal_1000m2_hora,
                'agua_gastada_riego': agua_gastada_riego,
                'abono_gastado': abono_gastado
            }
            
            # Mostrar resultados
            resultado_texto = f"""📊 RESULTADOS DEL CÁLCULO

🏠 Invernadero: {numero_invernadero if numero_invernadero else 'No especificado'}

📈 Cálculos intermedios:
• Goteros por m²: {goteros_por_metro:.4f}
• Litros agua/hora: {litros_agua_hora:.2f} L
• Caudal 1000m²/hora: {caudal_1000m2_hora:.2f} L"""

            if tiempo_riego > 0:
                resultado_texto += f"\n• Agua gastada riego: {agua_gastada_riego:.2f} L"
            
            if abono_gastado > 0:
                resultado_texto += f"""

🎯 RESULTADO FINAL:
• ABONO GASTADO: {abono_gastado:.2f} Kg"""
            else:
                resultado_texto += f"""

⚠️ Para calcular el abono gastado,
introduce CE del abono y tiempo de riego."""
            
            self.resultado_label.text = resultado_texto
            
        except Exception as e:
            self.mostrar_error(f"Error en el cálculo: {str(e)}")
    
    def mostrar_error(self, mensaje):
        """Mostrar popup de error"""
        popup = Popup(
            title='❌ Error',
            content=Label(text=mensaje, text_size=(dp(250), None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def compartir(self, instance):
        """Compartir resultados"""
        if not hasattr(self, 'ultimo_calculo'):
            self.mostrar_error("Primero debes hacer un cálculo")
            return
        
        # Crear texto para compartir
        data = self.ultimo_calculo
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        texto_compartir = f"""🌱 CALCULADORA DE ABONO - RESULTADOS

📅 Fecha: {fecha}
🏠 Invernadero: {data.get('numero_invernadero', 'No especificado')}

📊 DATOS:
• Superficie: {data['superficie']:.2f} m²
• Goteros: {data['goteros_totales']}
• Caudal: {data['caudal_gotero']:.2f} L×H⁻¹
• CE abono: {data['ce_abono']}
• Tiempo riego: {data['tiempo_riego']:.1f} min

📈 RESULTADOS:
• Goteros/m²: {data['goteros_por_metro']:.4f}
• Agua/hora: {data['litros_agua_hora']:.2f} L
• Agua gastada: {data['agua_gastada_riego']:.2f} L

🎯 ABONO GASTADO: {data['abono_gastado']:.2f} Kg

Calculado con la app móvil"""
        
        # Mostrar popup con texto
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        text_label = Label(
            text=texto_compartir,
            text_size=(dp(280), None),
            halign='left',
            valign='top'
        )
        
        scroll_view = ScrollView(size_hint=(1, 0.9), do_scroll_x=False)
        scroll_view.add_widget(text_label)
        content.add_widget(scroll_view)
        
        popup = Popup(
            title='📤 Compartir Resultados',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def reiniciar(self, instance):
        """Reiniciar campos"""
        for key, input_field in self.inputs.items():
            if key == 'numero_invernadero':
                input_field.text = ''
            else:
                input_field.text = '0'
        
        self.resultado_label.text = 'Introduce los datos y presiona CALCULAR'
        
        if hasattr(self, 'ultimo_calculo'):
            delattr(self, 'ultimo_calculo')

if __name__ == '__main__':
    CalculadoraAbonoApp().run()
