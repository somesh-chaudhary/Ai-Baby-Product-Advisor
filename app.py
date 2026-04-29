import streamlit as st
import os
from urllib.parse import quote_plus
from groq import Groq

# ─────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Baby Product Advisor",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — pastel, card-style, premium UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap');

  /* ── Root variables ── */
  :root {
    --bg:         #EAF7F0;
    --surface:    #FFFFFF;
    --border:     #F0E6E0;
    --accent:     #FF8FAB;
    --accent2:    #7EC8C8;
    --accent3:    #FFD166;
    --text:       #3B3347;
    --muted:      #8A7B90;
    --shadow:     0 4px 24px rgba(255,143,171,0.10);
    --shadow-lg:  0 8px 40px rgba(255,143,171,0.18);
    --radius:     18px;
  }

  /* ── Global reset ── */
  body {
    background-color: var(--bg) !important;
    color: var(--text);
  }

  /* ── Streamlit app container overrides ── */
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem !important; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #FFE4EE 0%, #E8F7F7 50%, #FFF3CC 100%);
    border-radius: var(--radius);
    padding: 2.4rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1.5px solid var(--border);
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '✨';
    position: absolute;
    font-size: 6rem;
    opacity: 0.07;
    top: -10px;
    right: -10px;
  }
  .hero h1 {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    font-size: 2.1rem;
    color: var(--text);
    margin: 0 0 0.4rem;
    letter-spacing: -0.5px;
  }
  .hero p {
    color: var(--muted);
    font-size: 1.05rem;
    margin: 0;
    font-weight: 500;
  }

  /* ── Input section card ── */
  .input-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow);
    border: 1.5px solid var(--border);
    margin-bottom: 1.8rem;
  }

  /* ── Streamlit widget labels ── */
  .stTextInput label, .stSelectbox label {
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    color: var(--text) !important;
    margin-bottom: 4px !important;
  }

  /* ── Inputs ── */
  .stTextInput input, .stSelectbox > div > div {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    background: #FFFBF9 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
    color: var(--text) !important;
    padding: 0.55rem 0.9rem !important;
    box-shadow: none !important;
    transition: border-color 0.2s;
  }
  .stTextInput input:focus, .stSelectbox > div > div:focus {
    border-color: var(--accent) !important;
    outline: none !important;
  }
  .stTextInput input::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
  }

  /* Only fix radio text */
  div[role="radiogroup"] label,
  div[role="radiogroup"] label span,
  div[role="radiogroup"] [data-baseweb="radio"] div,
  div[role="radiogroup"] [data-baseweb="radio"] span,
  [data-testid="stRadio"] label,
  [data-testid="stRadio"] label span,
  [data-testid="stRadio"] p,
  .stRadio label,
  .stRadio label span,
  .stRadio p {
    color: #000000 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
  }

  /* Button text visible */
  button {
    color: white !important;
  }

  /* ── Primary button ── */
  .stButton > button {
    background: linear-gradient(135deg, #FF8FAB 0%, #FF6B9D 100%) !important;
    color: white !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.75rem 2.4rem !important;
    box-shadow: 0 4px 20px rgba(255,107,157,0.35) !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.3px !important;
    width: 100%;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,107,157,0.45) !important;
    background: linear-gradient(135deg, #FF6B9D 0%, #FF4F8B 100%) !important;
  }
  .stButton > button:active {
    transform: translateY(0px) !important;
  }

  /* ── Section heading ── */
  .section-title {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: var(--text);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
  }

  /* ── Product card ── */
  .product-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.5rem 1.7rem;
    box-shadow: var(--shadow);
    border: 1.5px solid var(--border);
    margin-bottom: 1.2rem;
    transition: box-shadow 0.25s;
    position: relative;
    overflow: hidden;
  }
  .product-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    border-radius: 18px 0 0 18px;
  }
  .product-card:nth-child(1)::before { background: var(--accent); }
  .product-card:nth-child(2)::before { background: var(--accent2); }
  .product-card:nth-child(3)::before { background: var(--accent3); }
  .product-card:hover { box-shadow: var(--shadow-lg); }

  .product-num {
    display: inline-block;
    background: linear-gradient(135deg, #FFE4EE, #FFCCD8);
    color: var(--accent);
    font-weight: 800;
    font-size: 0.8rem;
    padding: 3px 10px;
    border-radius: 50px;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
  }
  .product-name {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--text);
    margin: 0.2rem 0 0.5rem;
  }
  .product-desc {
    color: var(--muted);
    font-size: 0.95rem;
    margin: 0 0 0.8rem;
    line-height: 1.55;
  }
  .age-badge {
    display: inline-block;
    background: #E8F7F7;
    color: #3A9D9D;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 50px;
    margin-bottom: 0.9rem;
    border: 1px solid #C4E8E8;
  }
  .benefit-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .benefit-list li {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.93rem;
    color: var(--text);
    margin-bottom: 0.45rem;
    line-height: 1.5;
  }
  .benefit-list li::before {
    content: '✦';
    color: var(--accent);
    font-size: 0.75rem;
    margin-top: 3px;
    flex-shrink: 0;
  }
  .buy-links {
    margin-top: 0.7rem;
    font-size: 0.92rem;
  }
  .buy-links a {
    color: var(--accent);
    font-weight: 700;
    text-decoration: none;
  }
  .buy-links a:hover {
    text-decoration: underline;
  }
  .buy-sep {
    margin: 0 0.4rem;
    color: var(--muted);
  }

  /* ── Safety card ── */
  .safety-card {
    background: linear-gradient(135deg, #FFF3E8 0%, #FFF8F0 100%);
    border-radius: var(--radius);
    padding: 1.5rem 1.7rem;
    border: 1.5px solid #FFE0C2;
    margin-bottom: 1.5rem;
  }
  .safety-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .safety-list li {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    font-size: 0.95rem;
    color: var(--text);
    margin-bottom: 0.6rem;
    line-height: 1.55;
  }
  .safety-list li::before {
    content: '🔶';
    font-size: 0.8rem;
    margin-top: 2px;
    flex-shrink: 0;
  }

  /* ── Arabic card ── */
  .arabic-card {
    background: linear-gradient(135deg, #EEF4FF 0%, #F5F0FF 100%);
    border-radius: var(--radius);
    padding: 1.7rem;
    border: 1.5px solid #D8E6FF;
    direction: rtl;
    text-align: right;
    font-size: 1.02rem;
    line-height: 1.9;
    color: var(--text);
    white-space: pre-wrap;
    font-family: 'Nunito', 'Arial', sans-serif;
  }

  /* ── Warning ── */
  .warn-box {
    background: #FFF3E0;
    border: 1.5px solid #FFB74D;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    color: #E65100;
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* ── Divider ── */
  .fancy-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
  }

  /* ── Footer ── */
  .footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 2.5rem;
    padding-bottom: 1.5rem;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AI GENERATION FUNCTION
# ─────────────────────────────────────────────
def generate_recommendations(age: str, category: str) -> dict:
    """
    Calls Groq LLM to produce structured baby product recommendations.
    Returns a dict with keys: products (list), safety_tips (list), arabic (str)
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY environment variable is not set.")
        st.stop()

    client = Groq(api_key=api_key)

    # Structured prompt that enforces clean, parseable output
    prompt = f"""You are an expert pediatric product advisor. A parent needs help choosing {category} products for a baby aged {age}.

Return EXACTLY this structure — no extra text, no markdown code blocks, follow this EXACT template:

PRODUCT 1
Name: [product name]
Description: [1–2 sentence description]
Age Suitability: [1 sentence explaining why it suits {age}]
Benefits:
- [benefit 1]
- [benefit 2]
- [benefit 3]

PRODUCT 2
Name: [product name]
Description: [1–2 sentence description]
Age Suitability: [1 sentence explaining why it suits {age}]
Benefits:
- [benefit 1]
- [benefit 2]
- [benefit 3]

PRODUCT 3
Name: [product name]
Description: [1–2 sentence description]
Age Suitability: [1 sentence explaining why it suits {age}]
Benefits:
- [benefit 1]
- [benefit 2]
- [benefit 3]

SAFETY TIPS
- [safety tip 1]
- [safety tip 2]
- [safety tip 3]
- [safety tip 4]

ARABIC TRANSLATION
[Full Arabic translation of all 3 products and safety tips above — keep the same structure, translate everything]

Rules:
- Products must be real, well-known brands or widely available products.
- Recommendations must be age-appropriate and safe for {age} old babies.
- Category is: {category}
- Be specific, warm, and reassuring in tone.
- Do NOT add any extra commentary outside the template."""

    model_name = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

    response = client.chat.completions.create(
      model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a warm, knowledgeable pediatric product specialist. "
                    "You always follow output templates exactly with no deviation. "
                    "You write clearly and helpfully for new parents."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.65,
        max_tokens=2200,
    )

    raw = response.choices[0].message.content.strip()
    return parse_response(raw)


# ─────────────────────────────────────────────
# RESPONSE PARSER
# ─────────────────────────────────────────────
def parse_response(raw: str) -> dict:
    """
    Parses the structured LLM output into a Python dict:
      { products: [...], safety_tips: [...], arabic: str }
    """
    products = []
    safety_tips = []
    arabic_text = ""

    # Split on "ARABIC TRANSLATION" first so we don't confuse Arabic dashes with tips
    arabic_split = raw.split("ARABIC TRANSLATION", 1)
    main_body = arabic_split[0]
    if len(arabic_split) > 1:
        arabic_text = arabic_split[1].strip()

    # Split on "SAFETY TIPS" to isolate tips
    safety_split = main_body.split("SAFETY TIPS", 1)
    products_body = safety_split[0]
    if len(safety_split) > 1:
        tips_raw = safety_split[1].strip()
        for line in tips_raw.splitlines():
            line = line.strip().lstrip("-•*").strip()
            if line:
                safety_tips.append(line)

    # Parse the three products
    for i in range(1, 4):
        marker = f"PRODUCT {i}"
        next_marker = f"PRODUCT {i + 1}" if i < 3 else "SAFETY TIPS"
        start = products_body.find(marker)
        end = products_body.find(next_marker) if next_marker in products_body else len(products_body)
        block = products_body[start:end].strip()

        product = parse_product_block(block, i)
        if product:
            products.append(product)

    return {
        "products": products,
        "safety_tips": safety_tips,
        "arabic": arabic_text,
    }


def parse_product_block(block: str, num: int) -> dict:
    """Extract fields from a single PRODUCT block."""
    lines = block.splitlines()
    name, description, age_suit, benefits = "", "", "", []
    in_benefits = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith(f"PRODUCT {num}"):
            continue
        if line.startswith("Name:"):
            name = line.replace("Name:", "").strip()
            in_benefits = False
        elif line.startswith("Description:"):
            description = line.replace("Description:", "").strip()
            in_benefits = False
        elif line.startswith("Age Suitability:"):
            age_suit = line.replace("Age Suitability:", "").strip()
            in_benefits = False
        elif line == "Benefits:":
            in_benefits = True
        elif in_benefits and line.startswith("-"):
            b = line.lstrip("-•*").strip()
            if b:
                benefits.append(b)

    if not name:
        return None
    return {
        "name": name,
        "description": description,
        "age_suitability": age_suit,
        "benefits": benefits,
    }


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────
def render_product_card(product: dict, index: int):
    badge_colors = [
        ("PRODUCT 1", "#FF8FAB"),
        ("PRODUCT 2", "#7EC8C8"),
        ("PRODUCT 3", "#FFB830"),
    ]
    label, color = badge_colors[index]

    benefits_html = "".join(
      f"<li>{b}</li>" for b in product.get("benefits", [])
    )

    product_name = product.get("name", "")
    encoded_name = quote_plus(product_name)
    amazon_url = f"https://www.amazon.in/s?k={encoded_name}"
    flipkart_url = f"https://www.flipkart.com/search?q={encoded_name}"

    st.markdown(f"""
    <div class="product-card">
        <span class="product-num" style="background:linear-gradient(135deg,{color}22,{color}44);color:{color};">
            {label}
        </span>
        <div class="product-name">{product.get('name','')}</div>
        <div class="product-desc">{product.get('description','')}</div>
        <div class="age-badge">✅ {product.get('age_suitability','')}</div>
        <ul class="benefit-list">{benefits_html}</ul>
        <div class="buy-links">
          <a href="{amazon_url}" target="_blank" rel="noopener">Buy on Amazon</a>
          <span class="buy-sep">•</span>
          <a href="{flipkart_url}" target="_blank" rel="noopener">Buy on Flipkart</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_safety_tips(tips: list):
    items_html = "".join(f"<li>{t}</li>" for t in tips)
    st.markdown(f"""
    <div class="safety-card">
      <ul class="safety-list">{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)


def render_arabic(text: str):
    st.markdown(f"""
    <div class="arabic-card">{text}</div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def main():
    # ── Hero banner ──
    st.markdown("""
    <div class="hero">
        <h1>👶 AI Baby Product Advisor</h1>
        <p>Safe, age-appropriate product picks — powered by AI, trusted by parents.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        age = st.text_input(
            "🍼 Baby's Age",
            placeholder="e.g. 3 months, 6 months, 1 year",
            help="Enter your baby's age in months or years"
        )
    with col2:
        category = st.radio(
          "📦 Product Category",
          ["Toys", "Feeding", "Skincare"],
          horizontal=True
        )

    submitted = st.button("✨  Find Perfect Products")

    # ── Validation ──
    if submitted:
        if not age.strip():
            st.markdown("""
            <div class="warn-box">⚠️ Please enter your baby's age to continue.</div>
            """, unsafe_allow_html=True)
            return

        # ── Loading spinner ──
        with st.spinner("🔍 Finding the best products for your little one…"):
            result = generate_recommendations(age.strip(), category)

        products = result.get("products", [])
        safety_tips = result.get("safety_tips", [])
        arabic = result.get("arabic", "")

        if not products:
            st.error("Something went wrong parsing the recommendations. Please try again.")
            return

        # ── Recommendations section ──
        st.markdown('<div class="section-title">👶 Recommendations</div>', unsafe_allow_html=True)
        for i, product in enumerate(products[:3]):
            render_product_card(product, i)

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── Safety Tips section ──
        st.markdown('<div class="section-title">🛡️ Safety Tips</div>', unsafe_allow_html=True)
        render_safety_tips(safety_tips)

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── Arabic translation section ──
        st.markdown('<div class="section-title">🌍 Arabic Version · النسخة العربية</div>', unsafe_allow_html=True)
        render_arabic(arabic)

    # ── Footer ──
    st.markdown("""
    <div class="footer">
        Made with ❤️ for parents everywhere · AI Baby Product Advisor
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
