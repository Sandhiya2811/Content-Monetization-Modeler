import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="YouTube Ad Revenue Predictor",
    page_icon="📺",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    with open("youtube_linear_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

CATEGORY_OPTIONS = ['Lifestyle', 'Entertainment', 'Music', 'Education', 'Gaming', 'Tech']
DEVICE_OPTIONS = ['Desktop', 'TV', 'Tablet', 'Mobile']
COUNTRY_OPTIONS = ['AU', 'IN', 'UK', 'DE', 'CA', 'US']
DAY_OPTIONS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}

# ---------------------------------------------------------
# FEATURE ENGINEERING (must match training pipeline)
# ---------------------------------------------------------
def build_features(views, likes, comments, watch_time_minutes,
                    video_length_minutes, subscribers,
                    year, month, day_of_week,
                    category, device, country):

    like_per_view = likes / views if views != 0 else 0
    comments_per_view = comments / views if views != 0 else 0
    watchtime_per_view = watch_time_minutes / views if views != 0 else 0
    watchtime_per_minute = watch_time_minutes / video_length_minutes if video_length_minutes != 0 else 0

    row = {
        "views": views,
        "likes": likes,
        "comments": comments,
        "watch_time_minutes": watch_time_minutes,
        "video_length_minutes": video_length_minutes,
        "subscribers": subscribers,
        "like_per_view": like_per_view,
        "comments_per_view": comments_per_view,
        "watchtime_per_view": watchtime_per_view,
        "watchtime_per_minute": watchtime_per_minute,
        "year": year,
        "month": month,
        "day_of_week": day_of_week,
        "category": category,
        "device": device,
        "country": country,
    }

    # Column order must match training X.columns
    column_order = [
        "views", "likes", "comments", "watch_time_minutes",
        "video_length_minutes", "subscribers", "like_per_view",
        "comments_per_view", "watchtime_per_view", "watchtime_per_minute",
        "year", "month", "day_of_week", "category", "device", "country"
    ]

    return pd.DataFrame([row])[column_order]


# ---------------------------------------------------------
# SIDEBAR - NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("📺 Navigation")
page = st.sidebar.radio("Go to", ["🔮 Predict Revenue", "📊 Explore & Visualize", "ℹ️ About"])

# ---------------------------------------------------------
# PAGE 1: PREDICTION
# ---------------------------------------------------------
if page == "🔮 Predict Revenue":

    st.title("📺 YouTube Ad Revenue Predictor")
    st.markdown("Enter your video stats below to predict estimated **ad revenue (USD)**.")

    st.subheader("📈 Engagement Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        views = st.number_input("Views", min_value=1, value=10000, step=100)
        likes = st.number_input("Likes", min_value=0, value=1000, step=10)
    with col2:
        comments = st.number_input("Comments", min_value=0, value=200, step=5)
        watch_time_minutes = st.number_input("Total Watch Time (minutes)", min_value=0.0, value=25000.0, step=100.0)
    with col3:
        video_length_minutes = st.number_input("Video Length (minutes)", min_value=0.1, value=10.0, step=0.5)
        subscribers = st.number_input("Channel Subscribers", min_value=0, value=200000, step=1000)

    st.subheader("📅 Upload Details")
    col4, col5, col6 = st.columns(3)
    with col4:
        year = st.number_input("Year", min_value=2015, max_value=2030, value=2025)
    with col5:
        month = st.selectbox("Month", list(range(1, 13)), index=5)
    with col6:
        day_name = st.selectbox("Day of Week", list(DAY_OPTIONS.keys()))
        day_of_week = DAY_OPTIONS[day_name]

    st.subheader("🏷️ Video Attributes")
    col7, col8, col9 = st.columns(3)
    with col7:
        category = st.selectbox("Category", CATEGORY_OPTIONS)
    with col8:
        device = st.selectbox("Primary Device", DEVICE_OPTIONS)
    with col9:
        country = st.selectbox("Country", COUNTRY_OPTIONS)

    st.markdown("---")

    if st.button("🚀 Predict Ad Revenue", use_container_width=True, type="primary"):
        input_df = build_features(
            views, likes, comments, watch_time_minutes, video_length_minutes,
            subscribers, year, month, day_of_week, category, device, country
        )

        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)

        st.success(f"### 💰 Predicted Ad Revenue: **${prediction:,.2f} USD**")

        # ---------------- Derived metrics shown to user ----------------
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Like Rate", f"{(likes/views)*100:.2f}%")
        m2.metric("Comment Rate", f"{(comments/views)*100:.2f}%")
        m3.metric("Avg Watch Time / View", f"{(watch_time_minutes/views):.2f} min")
        m4.metric("Watchtime / Video Length", f"{(watch_time_minutes/video_length_minutes):.2f}x")

        st.markdown("---")

        # ---------------- INTERACTIVE: Sensitivity - Views vs Revenue ----------------
        st.subheader("📊 How Revenue Changes with Views")
        st.caption("Holding all other inputs constant, see how predicted revenue scales with views.")

        view_range = np.linspace(max(1, views * 0.2), views * 3, 25).astype(int)
        sim_rows = []
        for v in view_range:
            df_sim = build_features(
                v, likes, comments, watch_time_minutes, video_length_minutes,
                subscribers, year, month, day_of_week, category, device, country
            )
            sim_rows.append({"views": v, "predicted_revenue": max(model.predict(df_sim)[0], 0)})

        sim_df = pd.DataFrame(sim_rows)
        fig_views = px.line(sim_df, x="views", y="predicted_revenue", markers=True,
                             title="Predicted Revenue vs Views")
        fig_views.add_vline(x=views, line_dash="dash", line_color="red",
                             annotation_text="Your input")
        st.plotly_chart(fig_views, use_container_width=True)

        # ---------------- INTERACTIVE: Category comparison ----------------
        st.subheader("🏷️ Predicted Revenue Across Categories")
        st.caption("Same inputs, but compared across every video category.")

        cat_rows = []
        for cat in CATEGORY_OPTIONS:
            df_cat = build_features(
                views, likes, comments, watch_time_minutes, video_length_minutes,
                subscribers, year, month, day_of_week, cat, device, country
            )
            cat_rows.append({"category": cat, "predicted_revenue": max(model.predict(df_cat)[0], 0)})

        cat_df = pd.DataFrame(cat_rows).sort_values("predicted_revenue", ascending=False)
        fig_cat = px.bar(cat_df, x="category", y="predicted_revenue", color="category",
                          title="Predicted Revenue by Category (current inputs)")
        st.plotly_chart(fig_cat, use_container_width=True)

        # ---------------- INTERACTIVE: Device comparison ----------------
        st.subheader("📱 Predicted Revenue Across Devices")

        dev_rows = []
        for dev in DEVICE_OPTIONS:
            df_dev = build_features(
                views, likes, comments, watch_time_minutes, video_length_minutes,
                subscribers, year, month, day_of_week, category, dev, country
            )
            dev_rows.append({"device": dev, "predicted_revenue": max(model.predict(df_dev)[0], 0)})

        dev_df = pd.DataFrame(dev_rows).sort_values("predicted_revenue", ascending=False)
        fig_dev = px.bar(dev_df, x="device", y="predicted_revenue", color="device",
                          title="Predicted Revenue by Device (current inputs)")
        st.plotly_chart(fig_dev, use_container_width=True)

        # ---------------- INTERACTIVE: Day of Week comparison ----------------
        st.subheader("📅 Predicted Revenue Across Days of the Week")

        day_rows = []
        for dname, didx in DAY_OPTIONS.items():
            df_day = build_features(
                views, likes, comments, watch_time_minutes, video_length_minutes,
                subscribers, year, month, didx, category, device, country
            )
            day_rows.append({"day": dname, "predicted_revenue": max(model.predict(df_day)[0], 0)})

        day_df = pd.DataFrame(day_rows)
        fig_day = px.bar(day_df, x="day", y="predicted_revenue",
                          title="Predicted Revenue by Day of Week (current inputs)",
                          category_orders={"day": list(DAY_OPTIONS.keys())})
        st.plotly_chart(fig_day, use_container_width=True)


# ---------------------------------------------------------
# PAGE 2: EXPLORE & VISUALIZE (general interactive playground)
# ---------------------------------------------------------
elif page == "📊 Explore & Visualize":
    st.title("📊 Interactive What-If Explorer")
    st.markdown("Pick a feature to vary and see how the predicted revenue curve changes.")

    numeric_features = {
        "views": (1000, 50000, 10000),
        "likes": (0, 10000, 1000),
        "comments": (0, 2000, 200),
        "watch_time_minutes": (0, 100000, 25000),
        "video_length_minutes": (0.1, 60.0, 10.0),
        "subscribers": (0, 1000000, 200000),
    }

    base_inputs = {}
    st.subheader("⚙️ Base Inputs (held constant unless varied below)")
    cols = st.columns(3)
    keys = list(numeric_features.keys())
    for i, key in enumerate(keys):
        lo, hi, default = numeric_features[key]
        with cols[i % 3]:
            base_inputs[key] = st.number_input(key.replace("_", " ").title(), value=float(default))

    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", CATEGORY_OPTIONS, key="exp_cat")
    with col2:
        device = st.selectbox("Device", DEVICE_OPTIONS, key="exp_dev")
    with col3:
        country = st.selectbox("Country", COUNTRY_OPTIONS, key="exp_country")

    col4, col5, col6 = st.columns(3)
    with col4:
        year = st.number_input("Year", min_value=2015, max_value=2030, value=2025, key="exp_year")
    with col5:
        month = st.selectbox("Month", list(range(1, 13)), index=5, key="exp_month")
    with col6:
        day_name = st.selectbox("Day of Week", list(DAY_OPTIONS.keys()), key="exp_day")
        day_of_week = DAY_OPTIONS[day_name]

    st.markdown("---")
    st.subheader("🎛️ Choose a Feature to Sweep")
    sweep_feature = st.selectbox("Vary this feature across a range:", keys)
    lo, hi, default = numeric_features[sweep_feature]
    sweep_min, sweep_max = st.slider(
        f"Range for {sweep_feature}",
        min_value=float(lo), max_value=float(hi),
        value=(float(lo), float(hi))
    )

    n_points = st.slider("Number of points", 5, 50, 20)
    sweep_values = np.linspace(sweep_min, sweep_max, n_points)

    rows = []
    for val in sweep_values:
        inputs = dict(base_inputs)
        inputs[sweep_feature] = val
        df_row = build_features(
            inputs["views"], inputs["likes"], inputs["comments"],
            inputs["watch_time_minutes"], inputs["video_length_minutes"],
            inputs["subscribers"], year, month, day_of_week,
            category, device, country
        )
        pred = max(model.predict(df_row)[0], 0)
        rows.append({sweep_feature: val, "predicted_revenue": pred})

    result_df = pd.DataFrame(rows)

    fig = px.line(result_df, x=sweep_feature, y="predicted_revenue", markers=True,
                   title=f"Predicted Revenue vs {sweep_feature.replace('_',' ').title()}")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔍 View raw prediction table"):
        st.dataframe(result_df, use_container_width=True)


# ---------------------------------------------------------
# PAGE 3: ABOUT
# ---------------------------------------------------------
else:
    st.title("ℹ️ About this App")
    st.markdown("""
    This dashboard uses a **Linear Regression** model (`youtube_linear_model.pkl`)
    trained to predict **YouTube ad revenue (USD)** based on video performance metrics.

    **Features used by the model:**
    - Views, Likes, Comments
    - Watch Time (minutes), Video Length (minutes)
    - Subscribers
    - Derived ratios: Like/View, Comments/View, Watchtime/View, Watchtime/VideoLength
    - Year, Month, Day of Week
    - Category, Device, Country

    **Pages:**
    - 🔮 **Predict Revenue** – Enter your video stats and get an instant prediction,
      plus interactive charts showing how revenue changes with views, category,
      device, and day of week.
    - 📊 **Explore & Visualize** – A what-if playground to sweep any numeric
      feature across a range and see the predicted revenue curve.
    """)
