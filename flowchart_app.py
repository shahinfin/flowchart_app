import json
from datetime import date
from pydantic import BaseModel
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from typing import List
groq = Groq(api_key="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")

class FlowChartStep(BaseModel):
    title: str
    description: str

def generate_flow_chart_steps(explanation: str) -> List[FlowChartStep]:
    try:
        chat_completion = groq.chat.completions.create(
        messages=[
                {
                    "role": "system",
                    "content": "Please provide a in very detailed step-by-step guide with 6 to 10 steps. Each step should have a title and a description, description shall include some key points in and it shall have around 4-5 points for each title in description detailed line without new line. Make atleast 10 sentences.\n"
                            f"The JSON object must use the schema: {json.dumps(FlowChartStep.model_json_schema(), indent=2)}",
                },
                {
                    "role": "user",
                    "content": explanation,
                },
            ],
            model="llama3-8b-8192",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )
        steps = json.loads(chat_completion.choices[0].message.content)
        steps = steps['steps']
        return steps
    except Exception as e:
        st.error('No input given')

def render_html(name, flow_chart_steps, customer_cities, supplier_cities, arrow_chart):
    flow_chart_html = ""
    
    # Loop through steps in chunks of 4 to insert page breaks after every 4 steps
    for index, step in enumerate(flow_chart_steps):
        # Add a page break after every 4 steps
        if index % 4 == 0 and index != 0:
            flow_chart_html += "<div style='page-break-after: always;'></div>"
        if index != 0:
            flow_chart_html += """<div style="position: relative; text-align: center; font-size: 24px;">
                                    <div style="width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 10px solid #333; margin: 10px auto;"></div>
                                </div>"""
        flow_chart_html += f"""
            <div style="padding: 0px 0px 0px 50px;">
                <div style="max-width: 90%; padding: 10px 10px 10px 30px; background-color: #f0f0f0; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center; position: relative; page-break-inside: avoid;">
                    <h4 style="margin: 5px 0; color: #333;">{step['title']}</h4>
                    <div style="margin-top: 5px; font-size: 0.9em; color: #555; text-align: left;">
                        {step['description'].replace('*', '') if isinstance(step['description'],str) else str(step['description']).replace('*', '').replace('[', '').replace(']','')}
                    </div>
                </div>
            </div>
        """
    
    # Construct arrow chart
    blue_box_content = [arrow_chart['title1'], arrow_chart['title2'], arrow_chart['title3'], arrow_chart['title4']]
    grey_box_content = [arrow_chart['content1'], arrow_chart['content2'], arrow_chart['content3'], arrow_chart['content4']]
    category_chart_html = ""
    for i in range(4):
        category_chart_html += f"""
            <div style="display: flex; margin-bottom:20px; align-items: center;">
                <div style="background-color: #0C6C98; width: 190px; height: 80px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; padding-left: 5px;">
                    {blue_box_content[i]}
                </div>
                <div style="width: 230px; height: 130px; background-color: #D3D3D3; margin-left: 0px; display: flex; align-items: center; justify-content: flex-start; color: white; font-size: 10px; padding-left: 10px;">
                    {grey_box_content[i].replace(',', '<br>')}
                </div>
                <div style="width: 0; height: 0; border-top: 80px solid transparent; border-bottom: 80px solid transparent; border-left: 70px solid #D3D3D3;"></div>
            </div>
        """

    # Cities section
    cities_html = ""
    for city in customer_cities:
        cities_html += f"<li style='margin: 2px 0; font-size: 12px;'>{city}</li>"
    supplier_cities_html = ""
    if len(supplier_cities) > 0:
        for city in supplier_cities:
            supplier_cities_html += f"<li style='margin: 2px 0; font-size: 12px;'>{city}</li>" 

    # Full HTML content with page breaks
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>One Planet Travel and Events LLC - Business Flow Chart</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.2/html2pdf.bundle.min.js"></script>
        <script>
            function downloadPDF() {{
                const element = document.getElementById('pdf-content');
                html2pdf()
                    .from(element)
                    .set({{
                        margin: 1,  // Correctly defined margin
                        filename: 'business_flow_chart.pdf',
                        html2canvas: {{ scale: 2 }},
                        jsPDF: {{ format: 'a4', orientation: 'portrait' }} // Set PDF size to A4
                    }})
                    .save();
            }}
        </script>
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 210mm; margin: 0 auto;">
        <div id="pdf-content" style="padding: 50px;">
            <h3 style="margin-top: 20px; text-align: center;">{name}</h3>
            <h5 style="margin: 0;">Date: {date.today().strftime("%d/%m/%Y")}</h5>
            <h5 style="margin: 0;">To: Federal Tax Authority</h5>
            <h4 style="text-align:center;">Subject: Business Flow Chart</h4>
            <div style="font-size: 0.9em;">
                <p>The "{name}" a diversified business model centered around trading and consulting services. Primarily focused on heavy plant and equipment, the company sources machinery from Europe and oversees the logistics of installation and dismantling projects across Africa. This includes full-scale project management, ensuring smooth execution of industrial projects. Alongside these services, the company expands its reach by trading in textiles, foodstuffs, and beverages, providing a broad range of offerings that support business growth and diversified revenue streams.<p>
            </div>

            <!-- Page 1: Arrow Chart -->
            <div style="padding-left: 70px; justify-content: center; align-items: center; page-break-after: always;">
                {category_chart_html}
            </div>

            <!-- Flow Chart with page breaks every 4 steps -->
            <div id="flow-chart">
                <h3 style="color: #333;">Procurement Process:</h3>
                <div style="display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%;">
                    {flow_chart_html}
                </div>
            </div>

            <!-- Cities and Declaration -->
            <div style="page-break-inside: avoid;">
                <h4 style="color: #333; margin-top: 10px; margin-bottom: 10px;">Location of Customers: Outside UAE</h4>
                <ul style="margin: 0; font-size: 18px;"> 
                    {cities_html}
                </ul>

                {"<h4 style='color: #333; margin-top: 10px; margin-bottom: 10px;'>Location of Suppliers:</h4><ul style='margin: 0; font-size: 12px;'>" + supplier_cities_html + "</ul>" if supplier_cities else ""}

                <p style="margin-top: 80px; font-size: 0.9em;">I hereby declare that the information related to this disclosure is complete and best to my knowledge and none of above information is false or misrepresented.</p>

                <div style="margin-top: 30px; font-style: italic;">
                    <p style="font-size: 0.9em;">Authorized Signatory (Sign & Stamp)</p>
                </div>
            </div>
        </div>
        <button onclick="downloadPDF()" style="margin-top: 20px;">Download PDF</button>
    </body>
    </html>
    """
    return html_content




st.title("Business Flow Chart Renderer")
name_input = st.text_input("Enter the name of the company:", "One Planet Travel and Events LLC")
cities_input = st.text_input("Enter the names of cities (separated by commas):", "Serbia, Macedonia, Bosnia, Croatia")
supplier_input = st.text_input("Enter the names supplier of cities (separated by commas):", "Serbia, Macedonia, Bosnia, Croatia")

col1,col2=st.columns(2)
with col1:
    input_arrochart_title1=st.text_input('title',key="input_arrochart_title1")
    input_arrochart_title2=st.text_input('title',key="input_arrochart_title2")
    input_arrochart_title3=st.text_input('title',key="input_arrochart_title3")
    input_arrochart_title4=st.text_input('title',key="input_arrochart_title4")
with col2:
    input_arrochart_content1=st.text_input('content',key="input_arrochart_content1")
    input_arrochart_content2=st.text_input('content',key="input_arrochart_content2")
    input_arrochart_content3=st.text_input('content',key="input_arrochart_content3")
    input_arrochart_content4=st.text_input('content',key="input_arrochart_content4")    
arrow_chart={"title1":input_arrochart_title1,"title2":input_arrochart_title2,"title3":input_arrochart_title3,"title4":input_arrochart_title4,
            "content1":input_arrochart_content1,"content2":input_arrochart_content2,"content3":input_arrochart_content3,"content4":input_arrochart_content4}
st.subheader("Flow Chart Steps")
explaination = st.text_area(f"Step Explanation", f"Step Explanation")
if st.button("Generate Flow Chart"):
    flow_chart_steps = []
    col1, col2 = st.columns([1,2])
    flow_chart_steps = []
    flow_chart_step = generate_flow_chart_steps(explaination)
    if supplier_input:
        html_output = render_html(name_input, flow_chart_step, cities_input.split(','), supplier_input.split(','),arrow_chart)
        components.html(html_output, height=800, scrolling=True)
    else:
        supplier_input=""
        html_output = render_html(name_input, flow_chart_step.split(','), supplier_input.split(','),arrow_chart)
        components.html(html_output, height=800, scrolling=True)