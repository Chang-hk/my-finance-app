import streamlit as st
import yfinance as yf

st.set_page_config(page_title="個人理財與生活計算機", page_icon="💰")
st.title("💰 個人專屬：理財與生活計算機")

# 抓取即時匯率的小幫手（快取 10 分鐘，手機操作滑順快速）
@st.cache_data(ttl=600)
def get_fx_rate(pair):
    data = yf.Ticker(pair).history(period="5d")
    if not data.empty:
        return float(data["Close"].iloc[-1])
    return 0.0

# 建立三個分頁
tab1, tab2, tab3 = st.tabs(("📈 複利資產模擬器", "🛍️ 滿額折扣計算機", "💱 即時匯率換算機"))

# --- 第一分頁：複利資產模擬器 ---
with tab1:
    st.subheader("複利與資產成長模擬")
    money = st.slider("每年年底存入金額（元）", min_value=10000, max_value=500000, value=120000, step=10000)
    years = st.slider("持續投資年數（年）", min_value=1, max_value=30, value=15)
    rate = st.slider("預期年化報酬率（%）", min_value=1.0, max_value=15.0, value=5.0, step=0.5)

    total = 0
    history_list = []
    for year in range(1, years + 1):
        total = (total + money) * (1 + rate / 100)
        history_list.append(round(total, 1))

    st.success(f"🎉 經過 {years} 年後，預估累積總資產為：{round(total, 1):,} 元")
    st.line_chart(history_list)

# --- 第二分頁：滿額折扣計算機 ---
with tab2:
    st.subheader("網購滿千打 8 折計算機")
    price = st.number_input("請輸入消費總金額（元）：", min_value=0, value=1500, step=100)

    if price >= 1000:
        final_price = price * 0.8
        st.success(f"🥳 恭喜達到滿千優惠！打 8 折後應付：{final_price:,} 元（現省 {price - final_price:,} 元）")
    else:
        st.info(f"💡 未滿 1,000 元無折扣，應付原價：{price:,} 元（再買 {1000 - price:,} 元即可享 8 折！）")

# --- 第三分頁：港幣 ⇄ 台幣／美金 即時匯率換算機 ---
with tab3:
    st.subheader("✈️ 港幣 (HKD) ⇄ 台幣 / 美金 即時換算")
    
    target_currency = st.selectbox(
        "請選擇要換算的幣別：",
        ("🇹🇼 新台幣 (TWD)", "🇺🇸 美元 (USD)")
    )
    
    direction = st.radio("換算方向：", ("港幣 (HKD) ➔ 換成外幣", "外幣 ➔ 折合港幣 (HKD)"), horizontal=True)
    amount = st.number_input("請輸入金額：", min_value=0.0, value=1000.0, step=100.0)

    fx_map = {
        "🇹🇼 新台幣 (TWD)": ("HKDTWD=X", "TWD"),
        "🇺🇸 美元 (USD)": ("HKDUSD=X", "USD"),
    }
    ticker_code, unit_name = fx_map[target_currency]
    rate = get_fx_rate(ticker_code)

    if rate > 0:
        st.caption(f"📡 目前市場即時參考匯率：1 HKD ≈ {rate:.4f} {unit_name}")
        if direction == "港幣 (HKD) ➔ 換成外幣":
            converted = amount * rate
            st.success(f"💰 **{amount:,.2f} HKD** 約可兌換 **{converted:,.2f} {unit_name}**")
        else:
            converted = amount / rate
            st.success(f"💰 **{amount:,.2f} {unit_name}** 約折合 **{converted:,.2f} HKD**")
    else:
        st.warning("⚠️ 暫時無法取得匯率報價，請稍後再試。")
