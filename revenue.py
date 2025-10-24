import streamlit as st
import pandas as pd
import pickle
from datetime import date



        
model = st.sidebar.selectbox("Select the Regression MOdel",['Linear Regression','SVR','Polynomial Regression'])

if model == 'Linear Regression':
    
    with open("youtube_linear_model.pkl", "rb") as f:
        loaded_pipeline = pickle.load(f)
    
    st.title("🎬 YouTube Ad Revenue Prediction App")
    st.write("Enter video details below to predict estimated **Ad Revenue (USD)**") 


    views = st.number_input("Views", min_value=1, step=1, format="%d")
    likes = st.number_input("Likes", min_value=0, step=1, format="%d")
    comments = st.number_input("Comments", min_value=0, step=1, format="%d")
    watch_time_minutes = st.number_input("Watch Time (minutes)", min_value=0.0, step=0.1)
    video_length_minutes = st.number_input("Video Length (minutes)", min_value=1.0, step=0.1)
    subscribers = st.number_input("Subscribers", min_value=0, step=1, format="%d")

    category = st.selectbox(
        "Category",
        ['Lifestyle', 'Entertainment', 'Music', 'Education', 'Gaming', 'Tech']
    )

    device = st.selectbox(
        "Device",
        ['Desktop', 'TV', 'Tablet', 'Mobile']
    )

    country = st.selectbox(
        "Country",
        ['AU', 'IN', 'UK', 'DE', 'CA', 'US']
    )

    upload_date = st.date_input("Upload Date", value=date.today())


    year = upload_date.year
    month = upload_date.month
    day_of_week = upload_date.weekday()  # 0=Monday, 6=Sunday



    like_per_view = likes / views if views != 0 else 0
    comments_per_view = comments / views if views != 0 else 0
    watchtime_per_view = watch_time_minutes / views if views != 0 else 0
    watchtime_per_minute = watch_time_minutes / video_length_minutes if video_length_minutes != 0 else 0


    if st.button("Predict Ad Revenue"):
        
        st.balloons()
        
        input_data = pd.DataFrame([{
            "views": views,
            "likes": likes,
            "comments": comments,
            "watch_time_minutes": watch_time_minutes,
            "video_length_minutes": video_length_minutes,
            "subscribers": subscribers,
            "category": category,
            "device": device,
            "country": country,
            "year": year,
            "month": month,
            "day_of_week": day_of_week,
            "like_per_view": like_per_view,
            "comments_per_view": comments_per_view,
            "watchtime_per_view": watchtime_per_view,
            "watchtime_per_minute": watchtime_per_minute
        }])
    
        
        prediction = loaded_pipeline.predict(input_data)
        prediction = max(prediction[0], 0)
        st.success(f"💰 **Estimated Ad Revenue:** ${prediction:.2f}")
        
elif model == 'SVR':
    
    with open("youtube_svr_linear_model.pkl", "rb") as f:
        loaded_svr_pipeline = pickle.load(f)
    
    st.title("🎬 YouTube Ad Revenue Prediction App")
    st.write("Enter video details below to predict estimated **Ad Revenue (USD)**") 


    views = st.number_input("Views", min_value=1, step=1, format="%d")
    likes = st.number_input("Likes", min_value=0, step=1, format="%d")
    comments = st.number_input("Comments", min_value=0, step=1, format="%d")
    watch_time_minutes = st.number_input("Watch Time (minutes)", min_value=0.0, step=0.1)
    video_length_minutes = st.number_input("Video Length (minutes)", min_value=1.0, step=0.1)
    subscribers = st.number_input("Subscribers", min_value=0, step=1, format="%d")

    category = st.selectbox(
        "Category",
        ['Lifestyle', 'Entertainment', 'Music', 'Education', 'Gaming', 'Tech']
    )

    device = st.selectbox(
        "Device",
        ['Desktop', 'TV', 'Tablet', 'Mobile']
    )

    country = st.selectbox(
        "Country",
        ['AU', 'IN', 'UK', 'DE', 'CA', 'US']
    )

    upload_date = st.date_input("Upload Date", value=date.today())


    year = upload_date.year
    month = upload_date.month
    day_of_week = upload_date.weekday()  # 0=Monday, 6=Sunday



    like_per_view = likes / views if views != 0 else 0
    comments_per_view = comments / views if views != 0 else 0
    watchtime_per_view = watch_time_minutes / views if views != 0 else 0
    watchtime_per_minute = watch_time_minutes / video_length_minutes if video_length_minutes != 0 else 0


    if st.button("Predict Ad Revenue"):
        
        st.balloons()
        
        input_data = pd.DataFrame([{
            "views": views,
            "likes": likes,
            "comments": comments,
            "watch_time_minutes": watch_time_minutes,
            "video_length_minutes": video_length_minutes,
            "subscribers": subscribers,
            "category": category,
            "device": device,
            "country": country,
            "year": year,
            "month": month,
            "day_of_week": day_of_week,
            "like_per_view": like_per_view,
            "comments_per_view": comments_per_view,
            "watchtime_per_view": watchtime_per_view,
            "watchtime_per_minute": watchtime_per_minute
        }])
    
        
        prediction = loaded_svr_pipeline.predict(input_data)
        prediction = max(prediction[0], 0)
        st.success(f"💰 **Estimated Ad Revenue:** ${prediction:.2f}")
        
elif model == 'Polynomial Regression':
    
    with open("youtube_poly_model.pkl", "rb") as f:
        loaded_poly_pipeline = pickle.load(f)
    
    st.title("🎬 YouTube Ad Revenue Prediction App")
    st.write("Enter video details below to predict estimated **Ad Revenue (USD)**") 


    views = st.number_input("Views", min_value=1, step=1, format="%d")
    likes = st.number_input("Likes", min_value=0, step=1, format="%d")
    comments = st.number_input("Comments", min_value=0, step=1, format="%d")
    watch_time_minutes = st.number_input("Watch Time (minutes)", min_value=0.0, step=0.1)
    video_length_minutes = st.number_input("Video Length (minutes)", min_value=1.0, step=0.1)
    subscribers = st.number_input("Subscribers", min_value=0, step=1, format="%d")

    category = st.selectbox(
        "Category",
        ['Lifestyle', 'Entertainment', 'Music', 'Education', 'Gaming', 'Tech']
    )

    device = st.selectbox(
        "Device",
        ['Desktop', 'TV', 'Tablet', 'Mobile']
    )

    country = st.selectbox(
        "Country",
        ['AU', 'IN', 'UK', 'DE', 'CA', 'US']
    )

    upload_date = st.date_input("Upload Date", value=date.today())


    year = upload_date.year
    month = upload_date.month
    day_of_week = upload_date.weekday()  # 0=Monday, 6=Sunday



    like_per_view = likes / views if views != 0 else 0
    comments_per_view = comments / views if views != 0 else 0
    watchtime_per_view = watch_time_minutes / views if views != 0 else 0
    watchtime_per_minute = watch_time_minutes / video_length_minutes if video_length_minutes != 0 else 0


    if st.button("Predict Ad Revenue"):
        
        st.balloons()
        
        input_data = pd.DataFrame([{
            "views": views,
            "likes": likes,
            "comments": comments,
            "watch_time_minutes": watch_time_minutes,
            "video_length_minutes": video_length_minutes,
            "subscribers": subscribers,
            "category": category,
            "device": device,
            "country": country,
            "year": year,
            "month": month,
            "day_of_week": day_of_week,
            "like_per_view": like_per_view,
            "comments_per_view": comments_per_view,
            "watchtime_per_view": watchtime_per_view,
            "watchtime_per_minute": watchtime_per_minute
        }])
    
        
        prediction = loaded_poly_pipeline.predict(input_data)
        prediction = max(prediction[0], 0)
        st.success(f"💰 **Estimated Ad Revenue:** ${prediction:.2f}")
  
    
