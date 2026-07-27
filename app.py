import streamlit as st
from ml_recommendation import recommend_by_input


st.set_page_config(
    page_title="Smart Laptop Finder",
    page_icon="💻",
    layout="centered"
)

# Sidebar Information

with st.sidebar:

    st.title("📌 Project Information")

    st.subheader("💻 Smart Laptop Finder")

    st.write(
        """
       An AI-powered laptop recommendation system
    that analyzes user preferences and finds
    the most suitable laptops based on similar
    features and specifications.
        """
    )

    st.markdown("---")

    st.subheader("📂 Dataset")

    st.write(
        """
        • Laptop specifications dataset  

        • Features include:
          - Processor
          - RAM
          - Storage
          - GPU
          - Operating System
          - Price
        """)
    
    st.markdown("---")
    
    st.subheader("🤖 ML Approach")

    st.write(
        """
        Techniques Used:

        ✅ One Hot Encoding  
        ✅ Feature Scaling  
        ✅ Cosine Similarity  
        """
    )

# Header
st.title("💻 Smart Laptop Finder")

st.markdown(
    """
    ### AI Powered Laptop Recommendation System

    Find your perfect laptop in seconds using Machine Learning.
    """
)

st.info("Choose your preferences below and click **Find My Laptop**.")


# User Inputs
left, right = st.columns(2)

with left:

    processor_brand = st.selectbox(
        "Processor Brand",
        ["intel", "amd"]
    )

    processor_tier = st.selectbox(
        "Processor Series",
        [
            "core i3",
            "core i5",
            "core i7",
            "ryzen 3",
            "ryzen 5",
            "ryzen 7"
        ]
    )

    ram = st.selectbox(
        "RAM (GB)",
        [4, 8, 16, 32]
    )


with right:

    storage = st.selectbox(
        "Storage (GB)",
        [256, 512, 1024]
    )

    gpu = st.selectbox(
        "Graphics",
        ["integrated", "dedicated"]
    )

    os = st.selectbox(
        "Operating System",
        ["windows", "mac"]
    )


budget = st.slider(
    "💰 Maximum Budget",
    20000,
    100000,
    60000,
    5000
)


sort_by = st.selectbox(
    "Sort Results",
    [
        "Best Match",
        "Lowest Price",
        "Highest Price"
    ]
)


# Buttons
col1, col2 = st.columns(2)

with col1:
    search = st.button(
        "🔍 Find My Laptop",
        use_container_width=True
    )

with col2:
    reset = st.button(
        "🔄 Reset",
        use_container_width=True
    )


if reset:
    st.rerun()


# Recommendation
if search:

    result = recommend_by_input(
        processor_brand,
        processor_tier,
        ram,
        storage,
        gpu,
        os
    )


    result = result[result["Price"] <= budget]


    if sort_by == "Lowest Price":
        result = result.sort_values("Price")


    elif sort_by == "Highest Price":
        result = result.sort_values(
            "Price",
            ascending=False
        )


    else:
        result = result.sort_values(
            "Similarity",
            ascending=False
        )


    if result.empty:

        st.warning(
            "No laptops found in this budget."
        )


    else:

        st.success(
            f"🎉 We found {len(result)} laptops matching your preferences!"
        )


        st.markdown(
    f"""
    **Your Selection:**  
    🧠 **{processor_brand.title()} {processor_tier.title()}** |
    💾 **{ram} GB RAM** |
    📦 **{storage} GB SSD** |
    💰 **₹{budget:,}**
    """
)

        st.divider()


        for index, row in result.iterrows():

            badge = (
                "🏆 Top Recommendation"
                if index == result.index[0]
                else "⭐ Recommended"
            )


            st.markdown(
                f"""
                <div class="card">

                <div class="badge">
                {badge}
                </div>


                <h3>
                {row['Brand'].title()}
                </h3>


                <p style="font-size:16px;">
                <b>{row['Model']}</b>
                </p>


                <div class="price">
                ₹ {row['Price']:,}
                </div>


                <table style="width:100%; margin-top:15px;">

                <tr>
                <td>🧠 <b>Processor</b></td>
                <td>{row['Processor']}</td>
                </tr>


                <tr>
                <td>💾 <b>RAM</b></td>
                <td>{row['RAM']} GB</td>
                </tr>


                <tr>
                <td>📦 <b>Storage</b></td>
                <td>{row['Storage']} GB</td>
                </tr>


                </table>


                <br>


                <div class="score">
                ⭐ Match Score :
                {row['Similarity']*100:.2f}%
                </div>


                </div>
                """,
                unsafe_allow_html=True
            )


            st.progress(
                float(row["Similarity"])
            )

            st.markdown("<br>", unsafe_allow_html=True)



# Footer
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px;">
        Developed by <b>Suhani Dhanotiya</b>
    </div>
    """,
    unsafe_allow_html=True
)