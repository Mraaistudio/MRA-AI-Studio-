
import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(
    page_title="MRA AI Studio",
    page_icon="✨",
    layout="wide"
)

st.title("✨ MRA AI Studio")
st.caption("Your All-in-One AI Toolkit")

# Read API key securely from Streamlit Secrets
try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    api_key = ""

client = OpenAI(api_key=api_key) if api_key else None

tool = st.selectbox(
    "Choose your tool",
    [
        "CV Maker",
        "Social Media Poster Maker",
        "AI Chatbot",
        "AI Text Writer",
        "English-Urdu Translator",
        "AI Image Generator"
    ]
)

def ask_ai(prompt):
    if not client:
        st.error(
            "API key missing. Add OPENAI_API_KEY "
            "in your Streamlit app Secrets."
        )
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI error: {e}")
        return None


if tool == "CV Maker":
    st.header("📄 Create Your CV")

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


elif tool == "Social Media Poster Maker":
    st.header("📢 Create Social Media Post")

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
                    f"{business}\n\n{service} ab hasil karein!\n"
                    f"{offer}\n\nRabtay ke liye: {contact}"
                )
            else:
                post = (
                    f"{business}\n\nDiscover our {service}!\n"
                    f"{offer}\n\nContact: {contact}"
                )

            st.markdown("### Post Preview")
            st.text(post)
            st.download_button(
                "Download Post",
                post,
                file_name="social_post.txt"
            )
        else:
            st.warning("Enter business name and service.")


elif tool == "AI Chatbot":
    st.header("🤖 AI Chatbot")
    question = st.text_area("Ask your question")

    if st.button("Ask AI"):
        if question.strip():
            answer = ask_ai(question)
            if answer:
                st.markdown("### Answer")
                st.write(answer)
        else:
            st.warning("Please enter a question.")


elif tool == "AI Text Writer":
    st.header("✍️ AI Text Writer")
    topic = st.text_area("What should AI write?")
    style = st.selectbox(
        "Writing type",
        ["Social Media Caption", "Email", "Story",
         "Application", "Product Description", "General"]
    )
    write_language = st.selectbox(
        "Output language",
        ["English", "Urdu", "Roman Urdu"]
    )

    if st.button("Write Text"):
        if topic.strip():
            result = ask_ai(
                f"Write a {style} in {write_language}. "
                f"Topic and instructions: {topic}"
            )
            if result:
                st.text_area("Generated Text", result, height=250)
                st.download_button(
                    "Download Text", result,
                    file_name="ai_text.txt"
                )
        else:
            st.warning("Enter a topic first.")


elif tool == "English-Urdu Translator":
    st.header("🌐 English-Urdu Translator")
    source_text = st.text_area("Enter text to translate")
    direction = st.selectbox(
        "Translate into",
        ["Urdu", "English", "Roman Urdu"]
    )

    if st.button("Translate"):
        if source_text.strip():
            result = ask_ai(
                f"Translate the following text into {direction}. "
                f"Keep the meaning accurate:\n\n{source_text}"
            )
            if result:
                st.text_area("Translation", result, height=200)
                st.download_button(
                    "Download Translation", result,
                    file_name="translation.txt"
                )
        else:
            st.warning("Enter text to translate.")


elif tool == "AI Image Generator":
    st.header("🎨 AI Image Generator")
    description = st.text_area(
        "Describe the image you want",
        placeholder="A beautiful sunset over the sea..."
    )

    if st.button("Generate Image"):
        if not client:
            st.error(
                "Add OPENAI_API_KEY in Streamlit Secrets first."
            )
        elif not description.strip():
            st.warning("Describe your image first.")
        else:
            try:
                with st.spinner("Generating image..."):
                    result = client.images.generate(
                        model="gpt-image-1",
                        prompt=description,
                        size="1024x1024"
                    )
                    image_bytes = base64.b64decode(
                        result.data[0].b64_json
                    )

                st.image(image_bytes, caption="AI Generated Image")
                st.download_button(
                    "Download Image",
                    image_bytes,
                    file_name="mra_ai_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(
                    "Image generation failed. Check API access, "
                    f"billing and model availability. Details: {e}"
                )

st.divider()
st.caption("MRA AI Studio | Made with Streamlit")
