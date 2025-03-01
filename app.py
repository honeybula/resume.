import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyAmfGknEYmN6fNQJlk8TG1kWkEUKFH96e8")
model = genai.GenerativeModel("gemini-1.5-flash")



def generate_resume(name, skills, experience, education):
    """Generates a resume using the Gemini API."""
    prompt = f"""
    Generate a professional resume for:

    Name: {name}
    Skills: {skills}
    Experience: {experience}
    Education: {education}

    Format the resume in markdown. Include sections for Summary, Skills, Experience, and Education.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating resume: {e}"

def markdown_to_pdf(markdown_text, output_file):
    """Converts markdown text to PDF."""
    pdf = fPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    html = markdown.markdown(markdown_text)
    lines = html.splitlines()

    for line in lines:
        clean_line = line.replace('<p>', '').replace('</p>', '').replace('<strong>', "").replace('</strong>',"").replace("<li>"," - ").replace("</li>","").replace("<ul>","").replace("</ul>","").replace("<ol>","").replace("</ol>","").replace("<h1>","").replace("</h1>","").replace("<h2>","").replace("</h2>","").replace("<h3>","").replace("</h3>","").replace("<br>","\n")

        pdf.multi_cell(0, 10, txt=clean_line)

    pdf.output(output_file)

# Streamlit App
def main():
    st.title("AI-Powered Resume Generator")

    name = st.text_input("Name")
    skills = st.text_area("Skills (comma-separated)")
    experience = st.text_area("Experience (e.g., Job Title - Company - Dates - Responsibilities)")
    education = st.text_area("Education (e.g., Degree - University - Dates)")

    if st.button("Generate Resume"):
        if not name or not skills or not experience or not education:
            st.warning("Please fill in all fields.")
        else:
            with st.spinner("Generating resume..."):
                resume_markdown = generate_resume(name, skills, experience, education)
                st.markdown(resume_markdown)

            # Download options
            st.subheader("Download Options")
            col1, col2 = st.columns(2)

            with col1:
                if st.download_button("Download as Markdown", data=resume_markdown, file_name="resume.md", mime="text/markdown"):
                    st.success("Markdown file downloaded!")

            with col2:
                if st.button("Download as PDF"):
                    pdf_filename = "resume.pdf"
                    markdown_to_pdf(resume_markdown, pdf_filename)
                    with open(pdf_filename, "rb") as file:
                        st.download_button("Download PDF", data=file, file_name=pdf_filename, mime="application/pdf")
                    os.remove(pdf_filename) #Clean up the file afterwards.
                    st.success("PDF file downloaded!")

if __name__ == "__main__":
    main()
        