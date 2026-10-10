
import streamlit as st

st.set_page_config(
    page_title="MRA AI Studio",
    page_icon="✨"
)

st.title("✨ MRA AI Studio")
st.write("CV Maker & Social Media Post Maker")

tool = st.selectbox(
    "Choose your tool",
    ["CV Maker", "Social Media Post Maker"]
)

if tool == "CV Maker":
    st.header("Create Your CV")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    city = st.text_input("City")
    education = st.text_input("Education")
    skills = st.text_area("Skills")
    experience = st.text_area("Work Experience")
    job = st.text_input("Job You Want")

    if st.button("Generate CV"):
        if name and job:
            cv = f"""
{name.upper()}
Phone: {phone}
City: {city}

CAREER OBJECTIVE
Seeking a position as {job}.

EDUCATION
{education}

SKILLS
{skills}

WORK EXPERIENCE
{experience}
"""
            st.text_area("Your CV", cv, height=300)
            st.download_button(
                "Download CV",
                cv,
                file_name="my_cv.txt"
            )
        else:
            st.warning("Enter your name and target job.")

else:
    st.header("Create Social Media Post")

    business = st.text_input("Business Name")
    service = st.text_input("Product or Service")
    offer = st.text_input("Price or Offer")
    contact = st.text_input("Contact Details")

    language = st.selectbox(
        "Language", ["English", "Roman Urdu"]
    )

    if st.button("Generate Post"):
        if business and service:
            if language == "Roman Urdu":
                post = (
                    f"{business}\n\n"
                    f"{service} ab hasil karein!\n"
                    f"{offer}\n\n"
                    f"Rabtay ke liye: {contact}"
                )
            else:
                post = (
                    f"{business}\n\n"
                    f"Looking for {service}?\n"
                    f"{offer}\n\n"
                    f"Contact: {contact}"
                )

            st.markdown("### Post Preview")
            st.write(post)
            st.download_button(
                "Download Post",
                post,
                file_name="social_post.txt"
            )
        else:
            st.warning("Enter business name and service.")
