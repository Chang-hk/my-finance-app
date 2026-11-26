import streamlit as st

st.set_page_config(page_title="個人理財與生活計算機", page_icon="💰")
st.title("💰 個人專屬：理財與生活計算機")

tab1, tab2 = st.tabs(("📈 複利資產模擬器", "🛍️ 滿額折扣計算機"))

with tab1:
    st.subheader("複利與資產成長模擬")
    money = st.slider("每年年底存入金額（元）", min_value=10000, max_value=500000, value=120000, step=10000)
    years = st.slider("持續投資年數（年）", min_value=1, max_value=30, value=15)
    rate = st.slider("預期年化報酬率（%）", min_value=1.0, max_value=15.0, value=5.0, step=0.5)

    total = 0
    history = ()
    history_list = list(history)
    for year in range(1, years + 1):
        total = (total + money) * (1 + rate / 100)
        history_list.append(round(total, 1))

    st.success(f"🎉 經過 {years} 年後，預估累積總資產為：{round(total, 1):,} 元")
    st.line_chart(history_list)

with tab2:
    st.subheader("網購滿千打 8 折計算機")
    price = st.number_input("請輸入消費總金額（元）：", min_value=0, value=1500, step=100)

    if price >= 1000:
        final_price = price * 0.8
        st.success(f"🥳 恭喜達到滿千優惠！打 8 折後應付：{final_price:,} 元（現省 {price - final_price:,} 元）")
    else:
        st.info(f"💡 未滿 1,000 元無折扣，應付原價：{price:,} 元（再買 {1000 - price:,} 元即可享 8 折！）")
