from streamlit.components.v1 import html
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io


# --------------------------------------------------------------------
# CLICK HELPER (unchanged)
# --------------------------------------------------------------------
def click_element(element):
    open_script = f"""
        <script type='text/javascript'>
            window.parent.document.querySelector('[id^=tabs-bui][id$=-{element}]').click();
        </script>
    """
    html(open_script, width=0, height=0)


# --------------------------------------------------------------------
# BREAKDOWN GENERATOR
# --------------------------------------------------------------------
def compute_breakdown(personal, travel, waste, energy, consumption):
    return {
        "Personal": personal["total_personal_kg_month"],
        "Travel": travel["total_travel_kg_month"],
        "Waste": waste["total_waste_kg_month"],
        "Energy": energy["total_energy_kg_month"],
        "Consumption": consumption["total_consumption_kg_month"]
    }


# --------------------------------------------------------------------
# FIXED PIE CHART (always correct)
# --------------------------------------------------------------------
def chart(breakdown, prediction):
    import matplotlib.pyplot as plt
    import io
    from PIL import Image, ImageDraw, ImageFont

    # Reset matplotlib state to avoid stale charts
    plt.clf()
    plt.close()

    labels = list(breakdown.keys())
    values = list(breakdown.values())

    colors = ["#2ecc71", "#1abc9c", "#16a085", "#48dbfb", "#74b9ff"]

    # --- create new figure properly ---
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="none")
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.8,
        colors=colors[:len(values)],
        textprops={"fontsize": 18, "weight": "bold", "color": "#000"},
    )

    ax.axis("equal")  # perfect circle

    # Convert to PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight")
    buf.seek(0)
    pie_img = Image.open(buf)

    # ---- background base ----
    background = Image.open("./media/default.png").convert("RGBA")
    background = background.resize((900, 900))
    draw = ImageDraw.Draw(background)

    # ---- center the pie ----
    bg_w, bg_h = background.size
    pie_w, pie_h = pie_img.size
    pos = ((bg_w - pie_w) // 2, (bg_h - pie_h) // 2 + 120)
    background.paste(pie_img, pos, pie_img)

    # ---- header text ----
    title_font = ImageFont.truetype("./style/ArchivoBlack-Regular.ttf", 75)
    value_font = ImageFont.truetype("./style/arialuni.ttf", 60)

    title_text = "Your Carbon Footprint"
    value_text = f"{prediction} kg CO₂ / month"

    title_w = draw.textbbox((0, 0), title_text, font=title_font)[2]
    value_w = draw.textbbox((0, 0), value_text, font=value_font)[2]

    cx = background.width // 2

    draw.text((cx - title_w / 2, 50), title_text, font=title_font, fill="#1B1C1C")
    draw.text((cx - value_w / 2, 160), value_text, font=value_font, fill="#1A1A1A")

    # ---- output ---
    final_buf = io.BytesIO()
    background.save(final_buf, format="PNG")
    final_buf.seek(0)

    return final_buf
