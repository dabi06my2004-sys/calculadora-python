import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática: Cálculo Diferencial", page_icon="📐", layout="wide")

# --- OCULTAR ELEMENTOS PARA QUE NO COPIEN ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} /* Oculta el menú de hamburguesa */
    footer {visibility: hidden;}    /* Oculta el pie de página "Made with Streamlit" */
    header {visibility: hidden;}    /* Oculta la barra de colores superior */
</style>
""", unsafe_allow_html=True)
# --- 2. ESTILOS VISUALES (CSS) ---
st.markdown("""
<style>
/* Botones grandes y bonitos */
div.stButton > button { 
    width: 100%; 
    padding: 12px; 
    font-size: 18px; 
    font-weight: bold; 
    border-radius: 10px;
    border: 1px solid #555;
    transition: 0.3s;
}
div.stButton > button:hover {
    border-color: #00FF00;
    color: #00FF00;
}
/* Cajas de texto de explicación */
.stExpander {
    border: 1px solid #2E7D32;
    border-radius: 8px;
    background-color: #1E1E1E;
}
</style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA DE LA CALCULADORA ---
if 'input_text' not in st.session_state: st.session_state.input_text = ""

def agregar(txt): st.session_state.input_text += txt
def borrar_uno(): st.session_state.input_text = st.session_state.input_text[:-1]
def limpiar(): st.session_state.input_text = ""

# --- 4. BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.markdown("## 🎛️ Panel de Control")
    
    # Pantalla de entrada
    func_input = st.text_input("Escribe la función aquí:", key="input_text", placeholder="Ej: (x^2 - 4)/(x - 2)")
    
    st.write("---")
    
    # --- TECLADO CIENTÍFICO ---
    # Fila 1: Variables y Potencias
    c1, c2, c3, c4 = st.columns(4)
    c1.button("x", on_click=agregar, args=("x",), help="Variable X")
    c2.button("x²", on_click=agregar, args=("^2",), help="Al cuadrado")
    c3.button("x³", on_click=agregar, args=("^3",), help="Al cubo")
    c4.button("^", on_click=agregar, args=("^",), help="Potencia personalizada")
    
    # Fila 2: Operaciones Básicas (Emojis para visibilidad)
    c1, c2, c3, c4 = st.columns(4)
    c1.button("➕", on_click=agregar, args=("+",))
    c2.button("➖", on_click=agregar, args=(" - ",))
    c3.button("✖️", on_click=agregar, args=("*",))
    c4.button("➗", on_click=agregar, args=("/",))
    
    # Fila 3: Funciones Avanzadas
    c1, c2, c3, c4 = st.columns(4)
    c1.button("sin", on_click=agregar, args=("sin(",))
    c2.button("cos", on_click=agregar, args=("cos(",))
    c3.button("ln", on_click=agregar, args=("log(",))
    c4.button("√", on_click=agregar, args=("sqrt(",))
    
    # Fila 4: Paréntesis y Borrado
    c1, c2, c3, c4 = st.columns(4)
    c1.button("(", on_click=agregar, args=("(",))
    c2.button(")", on_click=agregar, args=(")",))
    c3.button("🔙", on_click=borrar_uno)
    c4.button("🗑️", on_click=limpiar)

    st.info("💡 **Tip:** Usa paréntesis `( )` para agrupar divisiones. Ej: `(x+1)/(x-1)`")

# --- 5. LÓGICA MATEMÁTICA PRINCIPAL ---
# AQUÍ ESTÁ EL TÍTULO QUE PEDISTE
st.title("Matemática: Cálculo Diferencial")
st.markdown("Herramienta de análisis, resolución y graficación paso a paso.")

# Configuración SymPy
x = sp.symbols('x')
trans = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))

if func_input:
    try:
        # Limpieza de entrada (sen -> sin)
        clean_txt = func_input.replace('sen', 'sin')
        expr = parse_expr(clean_txt, transformations=trans)
        
        # Mostrar función bonita
        st.success(f"Función Activa:")
        st.latex(f"f(x) = {sp.latex(expr)}")
        
        # --- PESTAÑAS PRINCIPALES ---
        tab1, tab2, tab3, tab4 = st.tabs(["📏 Límites", "📉 Derivadas", "∫ Integrales", "📊 Gráfico Pro"])
        
      # === TAB 1: LÍMITES (VISUALIZACIÓN CORREGIDA) ===
        with tab1:
            col1, col2 = st.columns([1, 2])
            val_lim = col1.text_input("x tiende a:", "5")
            
            if col1.button("Calcular Límite"):
                try:
                    if val_lim == 'oo': target = sp.oo
                    else: target = sp.sympify(val_lim)
                    
                    res_final = sp.limit(expr, x, target)
                    try: sustitucion = expr.subs(x, target)
                    except: sustitucion = sp.nan
                    
                    # Resultado Principal
                    col2.markdown(f"### Resultado:")
                    col2.latex(fr"\lim_{{x \to {val_lim}}} f(x) = {sp.latex(res_final)}")
                    if not res_final.is_infinite and not res_final.has(sp.nan):
                        col2.write(f"Decimal: {res_final.evalf():.4f}")

                    # --- PASO A PASO ---
                    with st.expander("📝 Ver Procedimiento Algebraico Paso a Paso", expanded=True):
                        
                        # PASO 1
                        st.markdown("**Paso 1: Evaluar la indeterminación**")
                        st.latex(fr"f({val_lim}) = {sp.latex(expr).replace('x', '('+val_lim+')')}")
                        
                        if sustitucion.has(sp.nan) or (target != sp.oo and "0/0" in str(sustitucion)) or sustitucion == 0:
                            st.error("⚠️ Obtenemos una forma indeterminada **0/0**.")
                            
                            # PASO 2: FACTORIZACIÓN
                            st.markdown("---")
                            st.markdown("**Paso 2: Factorizar Numerador y Denominador**")
                            
                            num, den = sp.fraction(expr)
                            num_fact = sp.factor(num)
                            den_fact = sp.factor(den)

                            # Mostramos la factorización individual
                            c_f1, c_f2 = st.columns(2)
                            with c_f1: 
                                st.caption("Numerador:")
                                st.latex(fr"{sp.latex(num)} \rightarrow {sp.latex(num_fact)}")
                            with c_f2: 
                                st.caption("Denominador:")
                                st.latex(fr"{sp.latex(den)} \rightarrow {sp.latex(den_fact)}")
                            
                            # PASO 3: REESCRIBIR (AQUÍ ESTABA EL ERROR DEL "1")
                            st.markdown("---")
                            st.markdown("**Paso 3: Reescribir el límite factorizado**")
                            st.write("Juntamos las partes factorizadas en una sola fracción:")
                            
                            # CORRECCIÓN: Construimos la fracción LaTeX manualmente para que quede perfecta
                            fraccion_visual = fr"\frac{{{sp.latex(num_fact)}}}{{{sp.latex(den_fact)}}}"
                            st.latex(fr"\lim_{{x \to {val_lim}}} {fraccion_visual}")
                            
                            # PASO 4: SIMPLIFICAR (AQUÍ ESTABA EL OTRO ERROR)
                            st.markdown("**Paso 4: Cancelar términos semejantes**")
                            st.write("Eliminamos el término que causa el cero (el paréntesis repetido arriba y abajo):")
                            
                            # CORRECCIÓN: Usamos 'cancel' para forzar la simplificación visual
                            expr_simplificada = sp.cancel(expr)
                            st.latex(fr"\lim_{{x \to {val_lim}}} {sp.latex(expr_simplificada)}")
                            
                            # PASO 5: EVALUAR
                            st.markdown("---")
                            st.markdown("**Paso 5: Evaluación Final**")
                            st.write(f"Sustituimos $x={val_lim}$ en la función simplificada:")
                            st.latex(fr"= {sp.latex(expr_simplificada).replace('x', '('+val_lim+')')} = {sp.latex(res_final)}")
                            
                        else:
                            st.success("✅ La sustitución fue directa.")

                except Exception as e:
                    col2.error(f"Error: {e}")
        # === TAB 2: DERIVADAS ===
        with tab2:
            orden = st.slider("Orden de la derivada", 1, 3, 1)
            res_diff = sp.diff(expr, x, orden)
            
            st.markdown(f"### Derivada de Orden {orden}:")
            st.latex(fr"\frac{{d^{orden}}}{{dx^{orden}}} f(x) = {sp.latex(res_diff)}")
            
            with st.expander("📝 Ver Reglas de Derivación aplicables"):
                f_str = str(expr)
                st.write("Para resolver esto manualmente, recuerda:")
                if "/" in f_str and not "**" in f_str:
                    st.markdown("- **Regla del Cociente:** $\\frac{u'v - uv'}{v^2}$")
                if "*" in f_str:
                    st.markdown("- **Regla del Producto:** $u'v + uv'$")
                if "sin" in f_str or "cos" in f_str or "exp" in f_str:
                    st.markdown("- **Regla de la Cadena:** $f'(g(x)) \cdot g'(x)$")
                st.markdown("- **Regla de la Potencia:** $nx^{n-1}$")

        # === TAB 3: INTEGRALES ===
        with tab3:
            tipo = st.radio("Método:", ["Indefinida (+C)", "Definida (Área)"], horizontal=True)
            
            if tipo == "Indefinida (+C)":
                res_int = sp.integrate(expr, x)
                st.latex(fr"\int ({sp.latex(expr)}) dx = {sp.latex(res_int)} + C")
            else:
                c1, c2 = st.columns(2)
                a = c1.number_input("Límite inferior (a)", value=-5.0)
                b = c2.number_input("Límite superior (b)", value=5.0)
                
                if st.button("Calcular Área"):
                    res_def = sp.integrate(expr, (x, a, b))
                    st.latex(fr"\int_{{{a}}}^{{{b}}} f(x) dx = {sp.latex(res_def)}")
                    st.info(f"Valor numérico aproximado: {res_def.evalf():.4f} u²")

        # === TAB 4: GRÁFICO PRO ===
        with tab4:
            st.markdown("### Plano Cartesiano Interactivo")
            rango = st.slider("🔍 Zoom (Escala de visualización)", 5, 50, 10)
            
            try:
                # Crear datos para gráfica
                f_num = sp.lambdify(x, expr, modules=['numpy'])
                x_vals = np.linspace(-rango, rango, 1000)
                y_vals = f_num(x_vals)
                
                # Filtrar valores infinitos para que no rompan la gráfica (asíntotas)
                y_vals[y_vals > 100] = np.nan 
                y_vals[y_vals < -100] = np.nan
                
                # Configurar Plotly
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='#00FF00', width=3)))
                
                fig.update_layout(
                    template="plotly_dark",
                    height=600,
                    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='white', showgrid=True, range=[-rango, rango]),
                    yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='white', showgrid=True, scaleanchor="x", scaleratio=1, range=[-rango, rango]),
                    title="Arrastra el mouse para moverte • Rueda para Zoom"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.warning("No se puede graficar en este rango (posibles números imaginarios).")

    except Exception as e:
        st.error(f"Error de sintaxis: Revisa los paréntesis. ({e})")
else:
    st.info("👈 Comienza ingresando una función en el panel izquierdo.")

# --- PIE DE PÁGINA PERSONALIZADO ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-style: italic;">
    by: David My 👀
</div>
""", unsafe_allow_html=True)







