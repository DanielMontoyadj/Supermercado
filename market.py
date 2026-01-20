import streamlit as st
import pandas as pd 

ISV_Alcohol=0.18
ISV=0.15
def calcular_subtotal(nombre_producto, precio_producto, cantidad_producto, tipo_impuesto):
    subtotal=float(precio_producto)*float(cantidad_producto)

    if tipo_impuesto == "Alcohol":
        tipo_impuesto= subtotal * ISV_Alcohol
    else:
        tipo_impuesto=subtotal * ISV
        
    nueva_fila={
        "Producto": nombre_producto,
        "precio": precio_producto,
        "cantidad": cantidad_producto,
        "Impuesto": tipo_impuesto,
        "SubTotal": subtotal,
        "Total": subtotal + tipo_impuesto
    }

    st.session_state.table_data=pd.concat(
        [st.session_state.table_data, 
        pd.DataFrame([nueva_fila,])],
        ignore_index=True
    )

if "table_data" not in st.session_state:
    st.session_state.table_data=pd.DataFrame(
        columns=["Producto", "precio", "cantidad", "SubTotal", "Impuesto"]
    )

if "producto_nombre" not in st.session_state:
    st.session_state.nombre_producto = ""
if "producto_precio" not in st.session_state:
    st.session_state.precio_producto = 0.0
if "producto_cantidad" not in st.session_state:
    st.session_state.cantidad_producto = 1
if "tipo" not in st.session_state:
    st.session_state.tipo = "Otros"

def limpiar_formulario():
    st.session_state.producto_nombre = ""
    st.session_state.producto_precio = 0.0
    st.session_state.producto_cantidad = 0

st.title("Supermercado El más Barato")

with st.form("producto_form"):
    producto_nombre=st.text_input("Ingrese el nombre del producto", key="producto_nombre")
    producto_precio=st.number_input("Ingrese el precio del producto",key="producto_precio")
    producto_cantidad=st.number_input("Ingrese la cantidad de productos", key="producto_cantidad")
    tipo_impuesto=st.selectbox("ISV", ["Alcohol", "Otros"], key="tipo")

    SubTotal_button=st.form_submit_button("Comprar producto")
    st.form_submit_button("Limpiar", on_click=limpiar_formulario)

if SubTotal_button:
    calcular_subtotal(producto_nombre, producto_precio, producto_cantidad, tipo_impuesto)

st.dataframe(st.session_state.table_data)

if st.button("calcular el total a pagar"):
    total = st.session_state.table_data["Total"].sum()
    st.subheader('El precio Total')
    st.write(f"L.{total:.2f}")

if st.button("Generar factura"):
    if st.session_state.table_data.empty:
        st.warning("No hay productos para generar factura")
    else:
        st.subheader("Factura de compra")
        df = st.session_state.table_data.copy()
        df_parcial = df[["Producto", "cantidad", "precio"]]
        st.dataframe(df_parcial)
        subtotal_total = df["SubTotal"].sum()
        impuestos_total = df["Impuesto"].sum()
        total_pagar = df["Total"].sum()
        st.write(f"**Subtotal:** L.{subtotal_total:.2f}")
        st.write(f"**Total Impuestos:** L.{impuestos_total:.2f}")
        st.write(f"**Total a Pagar:** L.{total_pagar:.2f}")


#quitar las tablas que se genera otra vez
#limpie el formulario
#calcule el impuesto
#deactivate