import streamlit as st
from datetime import date
from utils.auth import get_supabase


def _client():
    return get_supabase()


# =========================
# PRODUCTS
# =========================
def get_all_products(active_only=False):
    try:
        query = _client().table("products").select("*").order("id", desc=False)
        if active_only:
            query = query.eq("is_active", True)

        response = query.execute()
        return response.data if response and response.data else []
    except Exception as e:
        st.error(f"Error obteniendo productos: {e}")
        return []


def get_product_by_id(product_id):
    try:
        response = _client().table("products").select("*").eq("id", product_id).limit(1).execute()
        if response and response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error obteniendo producto: {e}")
        return None


def create_product(name, category, price, stock, min_stock, description, is_active=True):
    try:
        payload = {
            "name": name.strip(),
            "category": category.strip(),
            "price": float(price),
            "stock": int(stock),
            "min_stock": int(min_stock),
            "description": description.strip(),
            "is_active": bool(is_active),
        }

        response = _client().table("products").insert(payload).execute()

        if response and response.data:
            return response.data

        st.error("No se pudo guardar el producto.")
        return None

    except Exception as e:
        st.error(f"Error creando producto: {e}")
        return None


def update_product(product_id, name, category, price, stock, min_stock, description, is_active=True):
    try:
        payload = {
            "name": name.strip(),
            "category": category.strip(),
            "price": float(price),
            "stock": int(stock),
            "min_stock": int(min_stock),
            "description": description.strip(),
            "is_active": bool(is_active),
        }

        response = _client().table("products").update(payload).eq("id", product_id).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error actualizando producto: {e}")
        return None


def delete_product(product_id):
    try:
        response = _client().table("products").delete().eq("id", product_id).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error eliminando producto: {e}")
        return None


def update_stock(product_id, new_stock):
    try:
        response = _client().table("products").update({"stock": int(new_stock)}).eq("id", product_id).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error actualizando stock: {e}")
        return None


# =========================
# DAILY MENU
# =========================
def get_daily_menu(menu_date=None):
    try:
        if menu_date is None:
            menu_date = date.today().isoformat()

        response = (
            _client()
            .table("daily_menu")
            .select("id, menu_date, is_active, product_id, products(id, name, category, price, stock, is_active)")
            .eq("menu_date", menu_date)
            .order("id", desc=False)
            .execute()
        )
        return response.data if response and response.data else []
    except Exception as e:
        st.error(f"Error obteniendo menú diario: {e}")
        return []


def add_product_to_daily_menu(product_id, menu_date=None, is_active=True):
    try:
        if menu_date is None:
            menu_date = date.today().isoformat()

        payload = {
            "menu_date": menu_date,
            "product_id": int(product_id),
            "is_active": bool(is_active)
        }
        response = _client().table("daily_menu").insert(payload).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error agregando producto al menú: {e}")
        return None


def remove_product_from_daily_menu(menu_entry_id):
    try:
        response = _client().table("daily_menu").delete().eq("id", menu_entry_id).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error eliminando producto del menú: {e}")
        return None


# =========================
# ORDERS
# =========================
def create_order(customer_name, customer_phone, customer_address, payment_method, notes, items):
    try:
        if not items:
            raise ValueError("La orden debe tener al menos un producto.")

        products = {p["id"]: p for p in get_all_products()}
        total = 0.0
        order_items_payload = []

        for item in items:
            product_id = int(item["product_id"])
            quantity = int(item["quantity"])

            if product_id not in products:
                raise ValueError(f"Producto no encontrado: {product_id}")

            product = products[product_id]
            stock = int(product["stock"])
            price = float(product["price"])

            if quantity <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            if stock < quantity:
                raise ValueError(f"Stock insuficiente para {product['name']}.")

            subtotal = quantity * price
            total += subtotal

            order_items_payload.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": price,
                "subtotal": subtotal
            })

        order_payload = {
            "customer_name": customer_name.strip(),
            "customer_phone": customer_phone.strip(),
            "customer_address": customer_address.strip(),
            "payment_method": payment_method,
            "notes": notes.strip(),
            "status": "pendiente",
            "total": round(total, 2)
        }

        order_response = _client().table("orders").insert(order_payload).execute()
        if not order_response or not order_response.data:
            raise ValueError("No se pudo crear la orden.")

        order_id = order_response.data[0]["id"]

        for item in order_items_payload:
            item["order_id"] = order_id

        items_response = _client().table("order_items").insert(order_items_payload).execute()
        if not items_response:
            raise ValueError("No se pudieron registrar los items del pedido.")

        for item in order_items_payload:
            product = products[item["product_id"]]
            new_stock = int(product["stock"]) - int(item["quantity"])
            update_stock(item["product_id"], new_stock)

            _client().table("inventory_movements").insert({
                "product_id": item["product_id"],
                "movement_type": "salida",
                "quantity": int(item["quantity"]),
                "reason": f"Venta - pedido #{order_id}"
            }).execute()

        return order_id

    except Exception as e:
        st.error(f"Error creando pedido: {e}")
        return None


def get_all_orders():
    try:
        response = _client().table("orders").select("*").order("id", desc=True).execute()
        return response.data if response and response.data else []
    except Exception as e:
        st.error(f"Error obteniendo pedidos: {e}")
        return []


def get_order_items(order_id):
    try:
        response = (
            _client()
            .table("order_items")
            .select("id, quantity, unit_price, subtotal, product_id, products(name, category)")
            .eq("order_id", order_id)
            .execute()
        )
        return response.data if response and response.data else []
    except Exception as e:
        st.error(f"Error obteniendo items del pedido: {e}")
        return []


def update_order_status(order_id, new_status):
    try:
        response = _client().table("orders").update({"status": new_status}).eq("id", order_id).execute()
        return response.data if response else None
    except Exception as e:
        st.error(f"Error actualizando estado del pedido: {e}")
        return None


# =========================
# INVENTORY
# =========================
def register_inventory_movement(product_id, movement_type, quantity, reason):
    try:
        product = get_product_by_id(product_id)
        if not product:
            raise ValueError("Producto no encontrado.")

        quantity = int(quantity)
        current_stock = int(product["stock"])

        if movement_type == "entrada":
            new_stock = current_stock + quantity
        elif movement_type == "salida":
            if current_stock < quantity:
                raise ValueError("Stock insuficiente para registrar la salida.")
            new_stock = current_stock - quantity
        elif movement_type == "ajuste":
            new_stock = quantity
        else:
            raise ValueError("Tipo de movimiento inválido.")

        _client().table("inventory_movements").insert({
            "product_id": int(product_id),
            "movement_type": movement_type,
            "quantity": quantity,
            "reason": reason.strip()
        }).execute()

        update_stock(product_id, new_stock)
        return True

    except Exception as e:
        st.error(f"Error registrando movimiento de inventario: {e}")
        return False


def get_inventory_movements():
    try:
        response = (
            _client()
            .table("inventory_movements")
            .select("id, movement_type, quantity, reason, created_at, product_id, products(name, category)")
            .order("id", desc=True)
            .execute()
        )
        return response.data if response and response.data else []
    except Exception as e:
        st.error(f"Error obteniendo movimientos: {e}")
        return []


# =========================
# DASHBOARD + REPORTS
# =========================
def get_dashboard_stats():
    products = get_all_products()
    orders = get_all_orders()
    menu_today = get_daily_menu()

    total_products = len(products)
    low_stock = len([p for p in products if int(p.get("stock", 0)) <= int(p.get("min_stock", 3))])
    orders_today = len([
        o for o in orders
        if str(o.get("order_date", "")).startswith(date.today().isoformat())
    ])
    total_sales_today = sum(
        float(o.get("total", 0))
        for o in orders
        if str(o.get("order_date", "")).startswith(date.today().isoformat())
    )

    return {
        "total_products": total_products,
        "menu_today": len(menu_today),
        "orders_today": orders_today,
        "low_stock": low_stock,
        "sales_today": round(total_sales_today, 2),
    }


def get_sales_by_day():
    orders = get_all_orders()
    summary = {}

    for order in orders:
        raw_date = str(order.get("order_date", ""))[:10]
        total = float(order.get("total", 0))
        summary[raw_date] = summary.get(raw_date, 0) + total

    return [{"date": k, "sales": v} for k, v in sorted(summary.items())]


def get_top_selling_products():
    try:
        response = (
            _client()
            .table("order_items")
            .select("quantity, product_id, products(name, category)")
            .execute()
        )
        rows = response.data if response and response.data else []

        summary = {}
        for row in rows:
            product = row.get("products")
            if not product:
                continue
            name = product.get("name", "Sin nombre")
            qty = int(row.get("quantity", 0))
            summary[name] = summary.get(name, 0) + qty

        return [
            {"product": k, "quantity": v}
            for k, v in sorted(summary.items(), key=lambda x: x[1], reverse=True)
        ]
    except Exception as e:
        st.error(f"Error obteniendo productos más vendidos: {e}")
        return []