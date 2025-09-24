# restaurant_billing_south_nonveg.py
# South-Indian Non-Veg Restaurant — Colorful Billing App 🍗🍛
# Run: streamlit run restaurant_billing_south_nonveg.py

import io
from datetime import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Optional PDF
PDF_AVAILABLE = True
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
except Exception:
    PDF_AVAILABLE = False

st.set_page_config(page_title="South-Indian Non-Veg Billing", page_icon="🍗", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.header{background:linear-gradient(90deg,#fb7185,#f59e0b,#facc15,#34d399,#60a5fa,#a78bfa);
padding:16px 18px;border-radius:16px;color:#0f172a;font-weight:700;box-shadow:0 6px 18px rgba(0,0,0,.08)}
.kpi{padding:16px;border-radius:16px;color:#0b1020;font-weight:700;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.kpi .value{font-size:28px;font-weight:800;margin-top:6px}
.kpi .label{font-size:13px;opacity:.8}
.block{background:#fff;border-radius:16px;padding:14px;box-shadow:0 6px 20px rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.04)}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🍗 South-Indian Non-Veg Restaurant — Order & Billing</div>', unsafe_allow_html=True)
st.caption("Select dishes & quantities → Generate bill → Charts → Download CSV/PDF invoice.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    tax_rate = st.number_input("Tax Rate (%)", 0.0, 50.0, 5.0, 0.5)
    currency = st.text_input("Currency Symbol", value="₹")

    st.subheader("🏪 Restaurant Info")
    biz_name = st.text_input("Name", value="RI Chettinad Non-Veg")
    biz_addr = st.text_area("Address", value="No.3, 100 Feet Road, Vadapalani, Chennai - 600026")
    biz_phone = st.text_input("Phone", value="9841814405")

    st.subheader("👤 Customer (optional)")
    customer_name = st.text_input("Customer Name", value="")
    customer_phone = st.text_input("Customer Phone", value="")

# --- South-Indian Non-Veg Menu ---
MENU = {
    "Biryanis": [
        {"item": "Chicken Biryani (Seeraga Samba)", "price": 219.0},
        {"item": "Mutton Biryani (Seeraga Samba)", "price": 289.0},
        {"item": "Egg Biryani", "price": 169.0},
        {"item": "Chicken 65 Biryani", "price": 259.0},
    ],
    "Starters": [
        {"item": "Chicken 65 (Boneless)", "price": 199.0},
        {"item": "Pepper Chicken Fry", "price": 219.0},
        {"item": "Mutton Chukka", "price": 269.0},
        {"item": "Nethili Fish Fry", "price": 229.0},
    ],
    "Curries & Gravies": [
        {"item": "Chettinad Chicken Curry", "price": 229.0},
        {"item": "Chettinad Mutton Curry", "price": 299.0},
        {"item": "Chicken Pepper Masala", "price": 239.0},
        {"item": "Mutton Keema Masala", "price": 279.0},
    ],
    "Bread & Rice": [
        {"item": "Parotta (2 pcs)", "price": 79.0},
        {"item": "Kothu Parotta (Chicken)", "price": 199.0},
        {"item": "Ghee Rice", "price": 149.0},
        {"item": "Idiyappam (Set of 4)", "price": 99.0},
    ],
    "Seafood Specials": [
        {"item": "Vanjaram Fish Fry", "price": 289.0},
        {"item": "Prawn Thokku", "price": 299.0},
        {"item": "Fish Curry (Tamil Nadu Style)", "price": 249.0},
    ],
    "Egg & Others": [
        {"item": "Egg Masala", "price": 139.0},
        {"item": "Omelette (2 eggs)", "price": 69.0},
        {"item": "Chicken Soup (Pepper)", "price": 119.0},
    ],
    "Beverages / Dessert": [
        {"item": "Rose Milk", "price": 69.0},
        {"item": "Lime Soda", "price": 59.0},
        {"item": "Gulab Jamun (2 pcs)", "price": 69.0},
    ],
}

# --- Session ---
if "quantities" not in st.session_state:
    st.session_state.quantities = {}
if "last_invoice" not in st.session_state:
    st.session_state.last_invoice = None

# --- Order Form ---
st.subheader("🧾 Menu & Order")
with st.form("order_form"):
    for category, items in MENU.items():
        st.markdown(f"#### 🌶️ {category}")
        for row in items:
            key = f"qty::{row['item']}"
            c1, c2, c3 = st.columns([5, 2, 3])
            with c1:
                st.write(f"**{row['item']}**")
            with c2:
                st.write(f"{currency}{row['price']:.2f}")
            with c3:
                qty = st.number_input(
                    f"Qty — {row['item']}",
                    min_value=0, max_value=50,
                    value=st.session_state.quantities.get(row['item'], 0),
                    step=1, key=key
                )
                st.session_state.quantities[row['item']] = qty
        st.divider()
    submitted = st.form_submit_button("🛒 Generate Bill")

# --- Helpers ---
def build_order_items():
    items = []
    for category, rows in MENU.items():
        for r in rows:
            name, price = r["item"], r["price"]
            qty = st.session_state.quantities.get(name, 0)
            if qty and qty > 0:
                items.append({
                    "Category": category,
                    "Item": name,
                    "Unit Price": float(price),
                    "Quantity": int(qty),
                    "Line Total": float(price) * int(qty),
                })
    return items

def make_invoice_number():
    return "INV-" + datetime.now().strftime("%Y%m%d-%H%M%S")

def compute_totals(items, tax_percent):
    subtotal = sum(x["Line Total"] for x in items)
    tax = subtotal * (tax_percent / 100.0)
    total = subtotal + tax
    return subtotal, tax, total

def money(x, cur="₹"):
    return f"{cur}{x:,.2f}"

def make_csv_bytes(df, meta):
    buf = io.StringIO()
    buf.write(f"{meta['biz_name']}\n{meta['biz_addr']}\nPhone: {meta['biz_phone']}\n")
    buf.write(f"Invoice: {meta['invoice_no']}, Date: {meta['date_str']}\n")
    if meta["customer_name"]: buf.write(f"Customer: {meta['customer_name']}\n")
    if meta["customer_phone"]: buf.write(f"Customer Phone: {meta['customer_phone']}\n")
    buf.write("\n")
    df.to_csv(buf, index=False)
    buf.write("\n")
    buf.write(f"Subtotal,{meta['currency']}{meta['subtotal']:.2f}\n")
    buf.write(f"Tax ({meta['tax_rate']}%),{meta['currency']}{meta['tax']:.2f}\n")
    buf.write(f"Total,{meta['currency']}{meta['total']:.2f}\n")
    return buf.getvalue().encode("utf-8")

def make_pdf_bytes(df, meta):
    if not PDF_AVAILABLE:
        return None
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=24, bottomMargin=24, leftMargin=24, rightMargin=24)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(meta['biz_name'], styles["Title"]))
    story.append(Paragraph(meta["biz_addr"], styles["Normal"]))
    story.append(Paragraph(f"Phone: {meta['biz_phone']}", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(f"<b>Invoice:</b> {meta['invoice_no']} &nbsp;&nbsp; <b>Date:</b> {meta['date_str']}", styles["Normal"]))
    if meta["customer_name"] or meta["customer_phone"]:
        s = "<b>Bill To:</b> " + (meta["customer_name"] or "")
        if meta["customer_phone"]:
            s += f" &nbsp;&nbsp; <b>Phone:</b> {meta['customer_phone']}"
        story.append(Paragraph(s, styles["Normal"]))
    story.append(Spacer(1, 12))

    table_data = [["Item", "Unit Price", "Qty", "Line Total"]]
    for _, r in df.iterrows():
        table_data.append([
            r["Item"],
            f"{meta['currency']}{float(r['Unit Price']):.2f}",
            str(int(r["Quantity"])),
            f"{meta['currency']}{float(r['Line Total']):.2f}",
        ])
    tbl = Table(table_data, colWidths=[230, 90, 60, 100])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#eeeeee")),
        ("GRID", (0,0), (-1,-1), 0.25, colors.gray),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 12))

    totals = [
        ["Subtotal", f"{meta['currency']}{meta['subtotal']:.2f}"],
        [f"Tax ({meta['tax_rate']}%)", f"{meta['currency']}{meta['tax']:.2f}"],
        ["Total", f"{meta['currency']}{meta['total']:.2f}"],
    ]
    t2 = Table(totals, colWidths=[230+90+60, 100])
    t2.setStyle(TableStyle([
        ("ALIGN", (1,0), (1,-1), "RIGHT"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.gray),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#f5f5f5")),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Nandri! Thanks for dining with us. 🍽️", styles["Italic"]))
    doc.build(story)
    buffer.seek(0)
    return buffer.read()

# --- Generate Bill ---
if submitted:
    items = build_order_items()
    if not items:
        st.warning("Please select at least one item (quantity > 0) to generate the bill.")
    else:
        df = pd.DataFrame(items)
        invoice_no = "INV-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        date_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        subtotal, tax, total = compute_totals(items, tax_rate)
        st.session_state.last_invoice = {
            "df": df,
            "meta": {
                "biz_name": biz_name.strip() or "Restaurant",
                "biz_addr": biz_addr.strip(),
                "biz_phone": biz_phone.strip(),
                "customer_name": customer_name.strip(),
                "customer_phone": customer_phone.strip(),
                "invoice_no": invoice_no,
                "date_str": date_str,
                "tax_rate": tax_rate,
                "subtotal": float(subtotal),
                "tax": float(tax),
                "total": float(total),
                "currency": currency,
            }
        }

# --- Show Bill + Dashboard ---
data = st.session_state.last_invoice
if data:
    df = data["df"].copy()
    meta = data["meta"]

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi" style="background:#ffe4e6;">
          <div class="label">🧾 Invoice</div><div class="value">{meta['invoice_no']}</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi" style="background:#fef3c7;">
          <div class="label">📅 Date</div><div class="value">{meta['date_str']}</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi" style="background:#dcfce7;">
          <div class="label">Subtotal</div><div class="value">{money(meta['subtotal'], currency)}</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi" style="background:#e0e7ff;">
          <div class="label">Grand Total</div><div class="value">{money(meta['total'], currency)}</div></div>""", unsafe_allow_html=True)

    st.markdown("### 🧾 Bill Summary")
    df_display = df.copy()
    df_display["Unit Price"] = df_display["Unit Price"].map(lambda x: f"{currency}{float(x):.2f}")
    df_display["Line Total"] = df_display["Line Total"].map(lambda x: f"{currency}{float(x):.2f}")
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.dataframe(df_display[["Category","Item","Unit Price","Quantity","Line Total"]],
                 use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(f"""<div class="kpi" style="background:#cffafe;">
          <div class="label">Subtotal</div><div class="value">{money(meta['subtotal'], currency)}</div></div>""", unsafe_allow_html=True)
    with t2:
        st.markdown(f"""<div class="kpi" style="background:#fde68a;">
          <div class="label">Tax ({meta['tax_rate']}%)</div><div class="value">{money(meta['tax'], currency)}</div></div>""", unsafe_allow_html=True)
    with t3:
        st.markdown(f"""<div class="kpi" style="background:#bbf7d0;">
          <div class="label">Grand Total</div><div class="value">{money(meta['total'], currency)}</div></div>""", unsafe_allow_html=True)

    st.markdown("### 📊 Dashboard")
    # Pie: category contribution
    cat_sum = df.groupby("Category")["Line Total"].sum().sort_values(ascending=False)
    fig1 = plt.figure()
    plt.pie(cat_sum.values, labels=cat_sum.index, autopct="%1.1f%%", startangle=140)
    plt.title("Category Contribution to Revenue")
    st.pyplot(fig1, use_container_width=True)

    # Bar: top dishes
    item_sum = df.groupby("Item")["Line Total"].sum().sort_values(ascending=False).head(8)
    fig2 = plt.figure()
    plt.bar(item_sum.index, item_sum.values)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Revenue")
    plt.title("Top Dishes by Revenue")
    st.pyplot(fig2, use_container_width=True)

    # Downloads
    st.markdown("### ⬇️ Download Invoice")
    csv_bytes = make_csv_bytes(df, meta)
    cA, cB = st.columns(2)
    with cA:
        st.download_button("Download CSV", data=csv_bytes,
                           file_name=f"{meta['invoice_no']}.csv", mime="text/csv",
                           use_container_width=True)
    with cB:
        if PDF_AVAILABLE:
            pdf_bytes = make_pdf_bytes(df, meta)
            st.download_button("Download PDF", data=pdf_bytes,
                               file_name=f"{meta['invoice_no']}.pdf", mime="application/pdf",
                               use_container_width=True)
        else:
            st.info("To enable PDF export, install **reportlab**: `pip install reportlab`")
else:
    st.info("Choose quantities and click **Generate Bill** to view the dashboard & invoice.")
