import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات
data = pd.read_csv("Jadarat_data.csv")

# تنظيف الأسماء العربية للأعمدة
data.columns = [
    "المسمى_الوظيفي", "تاريخ_الإعلان", "الوصف_الوظيفي", "المهام_الوظيفية",
    "اسم_الشركة", "رقم_المنشأة", "نوع_الشركة", "حجم_الشركة", "النشاط_الاقتصادي",
    "المؤهلات_المطلوبة", "المنطقة", "المدينة", "المزايا_الوظيفية",
    "نوع_العقد", "عدد_الوظائف", "رقم_الإعلان", "الخبرة_المطلوبة", "الجنس"
]

# عنوان الصفحة
st.title("📊 تحليل سوق الوظائف في السعودية")
st.markdown("""
### **هل فعلاً سوق العمل يعتمد على الخبرة؟ 🤔**
🔹 في هذا التحليل، سنلقي نظرة على متطلبات الوظائف في السعودية، ونرى كيف تختلف حسب الخبرة، والجنس، والمنطقة.
""")

# إضافة فلاتر تفاعلية
region_filter = st.sidebar.selectbox("🔍 اختر المنطقة", options=["الكل"] + list(data["المنطقة"].unique()))
gender_filter = st.sidebar.radio("👥 اختر الجنس", ["الكل", "ذكر", "أنثى", "كلا الجنسين"])
experience_filter = st.sidebar.slider("🎓 عدد سنوات الخبرة المطلوبة", 0, int(data["الخبرة_المطلوبة"].max()), (0, int(data["الخبرة_المطلوبة"].max())))

# تصفية البيانات بناءً على الفلاتر
filtered_data = data.copy()
if region_filter != "الكل":
    filtered_data = filtered_data[filtered_data["المنطقة"] == region_filter]
if gender_filter != "الكل":
    filtered_data = filtered_data[filtered_data["الجنس"] == gender_filter]
filtered_data = filtered_data[(filtered_data["الخبرة_المطلوبة"] >= experience_filter[0]) & (filtered_data["الخبرة_المطلوبة"] <= experience_filter[1])]

# عرض بعض المعلومات الإحصائية
st.markdown(f"#### 📌 عدد الوظائف المتاحة بعد التصفية: {filtered_data.shape[0]}")
st.write("👀 لمحة عن البيانات:", filtered_data[["المسمى_الوظيفي", "اسم_الشركة", "المنطقة", "الخبرة_المطلوبة", "الجنس"]].head())

# **رسم بياني: توزيع الوظائف حسب المناطق**
st.subheader("🌍 توزيع الوظائف حسب المناطق")
plt.figure(figsize=(10, 5))
sns.countplot(y=filtered_data["المنطقة"], order=filtered_data["المنطقة"].value_counts().index, palette="Blues_r")
plt.xlabel("عدد الوظائف")
plt.ylabel("المنطقة")
st.pyplot(plt)

# **رسم بياني: متطلبات الخبرة**
st.subheader("🎓 متطلبات الخبرة في الوظائف")
plt.figure(figsize=(8, 5))
sns.histplot(filtered_data["الخبرة_المطلوبة"], bins=10, kde=True, color="green")
plt.xlabel("عدد سنوات الخبرة المطلوبة")
plt.ylabel("عدد الوظائف")
st.pyplot(plt)

# **رسم بياني: توزيع الوظائف حسب الجنس**
st.subheader("👥 هل هناك تفضيل معين للجنس في الوظائف؟")
gender_counts = filtered_data["الجنس"].value_counts()
plt.figure(figsize=(6, 4))
plt.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", colors=["blue", "pink", "gray"])
st.pyplot(plt)

# **ملاحظة تحليلية للمستخدم**
st.markdown("""
📌 **أهم النتائج:**  
🔸 الوظائف في المدن الكبرى مثل **الرياض، جدة، والدمام** أعلى من بقية المناطق.  
🔸 **الخبرة مطلوبة بشدة** في بعض القطاعات، بينما هناك وظائف لا تتطلب خبرة.  
🔸 بعض الوظائف مخصصة للجنسين، لكن **هناك تباين واضح بين بعض المجالات.**
""")

st.success("✅ تحليلنا يوضح مدى أهمية الخبرة في سوق العمل السعودي، ولكن هناك أيضاً فرص للباحثين الجدد عن العمل! 🚀")
