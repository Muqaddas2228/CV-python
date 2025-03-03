import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import tempfile

# Function to generate PDF
def generate_pdf(name, email, phone, summary, skills, experience, education, theme_color, profile_image):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Apply theme colors
    themes = {
        "Light": ((0, 0, 0), (255, 255, 255)),
        "Dark": ((255, 255, 255), (0, 0, 0)),
        "Blue": ((255, 255, 255), (0, 0, 128)),
        "Green": ((0, 0, 0), (0, 128, 0)),
        "Gray": ((0, 0, 0), (169, 169, 169)),
        "Purple": ((255, 255, 255), (75, 0, 130))
    }

    title_color, bg_color = themes.get(theme_color, ((0, 0, 0), (255, 255, 255)))
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, style='F')

    # Profile Image Handling
    if profile_image:
        image = Image.open(profile_image)
        temp_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        image.save(temp_image_path)  # Save the image temporarily
        pdf.image(temp_image_path, x=10, y=10, w=40, h=40)

    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(*title_color)
    pdf.cell(200, 10, name, ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, email, ln=True, align="C")
    pdf.cell(200, 10, phone, ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, summary)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Skills", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, skills)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Experience", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, experience)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Education", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, education)

    return pdf.output(dest="S").encode("latin1")

# Streamlit UI
st.title("📝 Professional Resume Generator")

name = st.text_input("👤 Full Name", placeholder="Enter your full name")
email = st.text_input("📧 Email", placeholder="Enter your email address")
phone = st.text_input("📞 Phone", placeholder="Enter your phone number")
summary = st.text_area("📌 Summary", placeholder="Write a brief summary about yourself")
skills = st.text_area("🛠 Skills (comma separated)", placeholder="e.g. Python, JavaScript, SQL")
experience = st.text_area("💼 Work Experience", placeholder="Describe your work experience")
education = st.text_area("🎓 Education", placeholder="Mention your education details")

# Profile Image Upload
profile_image = st.file_uploader("📸 Upload Profile Picture (Optional)", type=["jpg", "png", "jpeg"])

# Theme Selection
theme_color = st.selectbox("🎨 Select Theme Color", ["Light", "Dark", "Blue", "Green", "Gray", "Purple"])

# Live Preview
if name or email or phone or summary or skills or experience or education:
    st.subheader("📄 Resume Preview")
    if profile_image:
        image = Image.open(profile_image)
        st.image(image, width=100)

    st.markdown(f"**👤 Name:** {name}")
    st.markdown(f"**📧 Email:** {email}")
    st.markdown(f"**📞 Phone:** {phone}")
    st.markdown(f"### 📌 Summary\n{summary}")
    st.markdown(f"### 🛠 Skills\n{skills}")
    st.markdown(f"### 💼 Experience\n{experience}")
    st.markdown(f"### 🎓 Education\n{education}")
    st.markdown(f"**🎨 Selected Theme:** {theme_color}")

# Generate PDF
if st.button("📄 Generate PDF"):
    if name and email and phone:
        pdf_bytes = generate_pdf(name, email, phone, summary, skills, experience, education, theme_color, profile_image)
        st.download_button("📥 Download Resume", pdf_bytes, file_name="resume.pdf", mime="application/pdf")
    else:
        st.warning("⚠️ Please fill out Name, Email, and Phone fields!")