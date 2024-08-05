import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_mantine_components as dmc
from flask import request
import pandas as pd
import os
import uuid
from datetime import datetime

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Create a new Dash application instance
app = dash.Dash(__name__)
app.title = "NASA SkillBridge Application"
app._favicon = "/assets/nasa-logo.png"

# Function to create a label with a red asterisk to indicate a required field
def label_with_red_asterisk(title):
    return html.Div(
        children=[
            title,
            html.Span("*", style={"color": "red", "marginLeft": "5px"})
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "fontSize": "15px",
            "marginBottom": "2px",
            "fontWeight": "normal"
        }
    )

# Function to create a text input field with a label
def create_input(id_suffix, label, required=True, input_type="text"):
    return html.Div(
        children=[
            label_with_red_asterisk(label),  # Add the label
            dmc.TextInput(
                id=id_suffix,  # Set the ID for the input field
                type=input_type,  # Set the type of input (text, email, tel, etc.)
                required=required,
                sx={"boxShadow": "0px 4px 4px rgba(1, 1, 1, 0.1)", "borderRadius": "8px", "marginBottom": "15px"}
            )
        ]
    )

# Function to create a date input field with a label
def create_date_input(id_suffix, label):
    return html.Div(
        children=[
            label_with_red_asterisk(label),  # Add the label
            dmc.DatePicker(
                id=id_suffix,  # Set the ID for the date picker
                required=True,
                style={"marginBottom": "15px"}
            )
        ]
    )

# Function to create a text area input field with a label
def create_textarea(id_suffix, label, placeholder="Your explanation"):
    return html.Div(
        children=[
            label_with_red_asterisk(label),  # Add the label
            dmc.Textarea(
                id=id_suffix,  # Set the ID for the text area
                placeholder=placeholder,
                autosize=True,
                minRows=4,
                required=True,
                style={"marginBottom": "15px"}
            )
        ]
    )

# Function to create a dropdown (select) input field with a label and options
def create_dropdown(id_suffix, label, options):
    return html.Div(
        children=[
            label_with_red_asterisk(label),  # Add the label
            dmc.Select(
                id=id_suffix,  # Set the ID for the dropdown
                data=[{"label": opt, "value": opt} for opt in options],  # Set the options
                required=True,
                style={"marginBottom": "15px"}
            )
        ]
    )

# Function to create a group of checkboxes with a label
def create_checkbox_group(id_suffix, label, options):
    return html.Div(
        children=[
            label_with_red_asterisk(label),  # Add the label
            dmc.CheckboxGroup(
                id=id_suffix,  # Set the ID for the checkbox group
                orientation="vertical",
                children=[dmc.Checkbox(label=opt, value=opt) for opt in options],  # Create individual checkboxes
                style={"marginBottom": "15px"}
            )
        ]
    )

# Define the layout of the application
app.layout = html.Div([
    html.Div(children=[
        dmc.Container(
            sx={"backgroundColor": "#ffffff"},
            children=[
                dmc.Stack([
                    dmc.Group(
                        align="center",
                        children=[
                            dmc.Image(src="/assets/nasa-logo.png", width=100, height=0),
                            dmc.Text("NASA SkillBridge Application", size="30px", weight=20, style={"fontFamily": "Arial, sans-serif", "marginBottom": "20px"})
                        ]
                    ),
                    dmc.Text(
                        children=[
                            "This is a SkillBridge Application for a Transitioning Service Member."
                        ],
                        size="20px",
                        style={"fontFamily": "Arial, sans-serif", "marginBottom": "20px"}
                    ),
                    dmc.Text(
                        children=[
                            "NASA only collects the personally identifiable information (PII) that is necessary to provide you with the services you request. "
                        ],
                        size="15px",
                        style={"fontFamily": "Arial, sans-serif", "marginBottom": "10px"}
                    ),
                    dmc.Text(
                        children=[
                            "NASA SkillBridge opportunities are limited to 60-180 days."
                        ],
                        size="15px",
                        style={"fontFamily": "Arial, sans-serif", "marginBottom": "10px", "color": "red"}
                    ),
                    dmc.Checkbox(label="I have read and understand this information.", id="understand-info", style={"marginBottom": "20px"}),

                    # Section: Service Member Information
                    dmc.Text("Service Member Information", size="24px", weight=20, style={"fontFamily": "Arial, sans-serif", "marginBottom": "20px"}),
                    dmc.Grid([
                        dmc.Col(create_input("last-name", "Last Name:"), span=6),
                        dmc.Col(create_input("first-name", "First Name:"), span=6),
                        dmc.Col(create_input("phone-number", "Phone Number:", input_type="tel"), span=6),
                        dmc.Col(create_input("service-email", "Service Member Email:", input_type="email"), span=6),
                        dmc.Col(create_dropdown("branch-service", "Branch of Service:", [
                            "Army", "Army National Guard", "Air Force", "Air National Guard", 
                            "Navy", "Marine Corps", "Coast Guard", "Space Force"
                        ]), span=6),
                        dmc.Col(create_dropdown("grade", "Grade:", [
                            "E-1", "E-2", "E-3", "E-4", "E-5", "E-6", "E-7", "E-8", "E-9",
                            "W-1", "W-2", "W-3", "W-4", "W-5",
                            "O-1", "O-2", "O-3", "O-4", "O-5", "O-6", "O-7", "O-8", "O-9", "O-10"
                        ]), span=6),
                        dmc.Col(create_dropdown("years-of-service", "Years of Service:", [
                            "<5 years", "5-10 years", "11-18 years", "19+ years"
                        ]), span=6),
                        dmc.Col(create_input("duty-station", "Current Duty Station:"), span=6),
                        dmc.Col(create_input("job-specialty", "What is your Job Specialty? (Example: 15A Helicopter Pilot, IS Intelligence Specialist)", required=True), span=6),
                        dmc.Col(create_date_input("date-separation", "Est. Date of Separation:"), span=4),
                        dmc.Col(create_date_input("skillbridge-start-date", "Est. SkillBridge Start Date:"), span=4),
                        dmc.Col(create_date_input("skillbridge-end-date", "Est. SkillBridge End Date:"), span=4),
                    ]),

                    # Section: Service Member Unit Information
                    dmc.Text("Service Member Unit Information", size="24px", weight=20, style={"fontFamily": "Arial, sans-serif", "marginBottom": "20px"}),
                    dmc.Grid([
                        dmc.Col(create_input("supervisor-name", "First Line Supervisor:"), span=6),
                        dmc.Col(create_input("supervisor-email", "Supervisor Email:", input_type="email"), span=6),
                        dmc.Col(create_input("commanding-officer", "Commanding Officer:"), span=6),
                        dmc.Col(create_input("commanding-officer-email", "Commanding Officer Email:", input_type="email"), span=6),
                    ]),

                    # Section: NASA Area of Interest
                    dmc.Text("NASA Area of Interest", size="24px", weight=20, style={"fontFamily": "Arial, sans-serif", "marginBottom": "20px"}),
                    dmc.Grid([
                        dmc.Col(create_input("degrees", "List your degrees:"), span=6),
                        dmc.Col(create_input("certifications", "List your certifications:"), span=6),
                        dmc.Col(create_input("desired-career", "What are your desired career field interests at NASA?"), span=12),
                        dmc.Col(create_dropdown("opm-code", "OPM Occupational Group Code (Please select one or more OPM occupational group codes that correspond to the career fields you are interested in. This information will be used to connect you with the appropriate corresponding sponsors. )", [
                            "0000 – Environmental Protection, Emergency Management, Security, Safety",
                            "0100 – Social Science, Psychology, Welfare",
                            "0200 – Human Resource Management",
                            "0300 – General Administration, Communications, Clerical, Office Services",
                            "0400 – Biological Sciences",
                            "0500 – Accounting and Budget",
                            "0600 – Medical, Hospital, Public Health",
                            "0700 – Veterinary Medical Science",
                            "0800 – Engineering and Architecture",
                            "0900 – Legal",
                            "1000 – Information and Arts",
                            "1100 – Business",
                            "1200 – Copyright, Patent, Trademark",
                            "1300 – Physical Sciences",
                            "1400 – Library and Archives",
                            "1500 – Mathematics and Statistics",
                            "1600 – Facilities, Equipment, and Service",
                            "1700 – Education",
                            "1800 – Investigation, Inspection, Enforcement, and Compliance",
                            "1900 – Quality Assurance, Inspection and Grading",
                            "2000 – Logistics, Supply",
                            "2100 – Transportation",
                            "2200 – Information Technology Management"
                        ]), span=12),
                        dmc.Col(create_textarea("experience", "Explain your relevant professional experience and statement of interest for this program:"), span=12),
                        dmc.Col(create_dropdown("ethnicity", "Ethnicity (reflects USA Jobs member inputs):", [
                            "Hispanic or Latino", "Not Hispanic or Latino"
                        ]), span=6),
                        dmc.Col(create_dropdown("race", "Race (reflects USA Jobs member inputs):", [
                            "American Indian or Alaska Native", "Asian", "Black or African American", 
                            "Native Hawaiian or other Pacific Islander", "White"
                        ]), span=6),
                        dmc.Col(create_dropdown("sex", "Sex:", [
                            "Male", "Female"
                        ]), span=6),
                        dmc.Col(create_checkbox_group("nasa-centers", "What is your desired NASA Center? (Check all that apply)", [
                            "Ames Research Center (ARC)", "Armstrong Flight Research Center (AFRC)", "Glenn Research Center (GRC)",
                            "Johnson Space Center (JSC)", "Columbia Scientific Balloon Facility (CSBF)", "Goddard Institute for Space Studies (GISS)",
                            "Goddard Space Flight Center (GSFC)", "Kennedy Space Center (KSC)",
                            "Langley Research Center (LaRC)", "Michoud Assembly Facility (MAF)", "Marshall Space Flight Center (MSFC)",
                            "NASA Shared Services Center (NSSC)", "Stennis Space Center (SSC)",
                            "Wallops Flight Facility (WFF)", "White Sands Test Facility (WSTF)", "Remote"
                        ]), span=12),
                    ]),

                    # Add links to relevant documents
                    html.A("OPM Handbook of Occupational Groups and Families", href="https://www.opm.gov/policy-data-oversight/classification-qualifications/classifying-general-schedule-positions/occupationalhandbook.pdf", target="_blank", style={"fontFamily": "Arial, sans-serif", "fontSize": "12px", "marginBottom": "2px", "fontWeight": "normal"}),
                    html.A("Weblink to centers and facilities", href="https://science.nasa.gov/about-us/nasa-centers/", target="_blank", style={"fontFamily": "Arial, sans-serif", "fontSize": "12px", "marginBottom": "20px", "fontWeight": "normal"}),
                    
                    # Add checkboxes for understanding relocation info and TRS/TAPS completion
                    dmc.Checkbox(label="I understand NASA is not responsible for financing relocation to a NASA center or a supporting facility if I choose to participate in an onsite SkillBridge opportunity outside of my current military assignment location.", id="relocation-info", style={"marginBottom": "20px"}),
                    dmc.Checkbox(label="I have completed TRS/TAPS.", id="completed-trstaps", style={"marginBottom": "20px"}),
                    create_date_input("trstaps-completion-date", "Date of TRS/TAPS Completion:"),
                    
                    # Add a submit button
                    dmc.Button(id="submit-button", children=["Submit"], style={"width": "80vw", 'maxWidth': '600px', "marginTop": "20px", "backgroundColor": "#007bff", "color": "#fff"}),
                    
                    # Add a modal (popup) for submission confirmation
                    dmc.Modal(
                        id="modal",
                        centered=True,
                        children=[
                            dmc.Text("Thank you! Follow NASA", style={"textAlign": "center", "fontFamily": "Arial, sans-serif", "fontSize": "18px", "marginBottom": "40px", "fontWeight": "normal", "fontStyle": "italic"}),
                            dmc.Group(children=[
                                html.A(dmc.Tooltip(dmc.Avatar(src="/assets/icon-facebook.png", size="md", radius="md"), label="Facebook", position="bottom"), href="https://www.facebook.com/NASA", target="_blank"),
                                html.A(dmc.Tooltip(dmc.Avatar(src="/assets/icon-twitter.png", size="md", radius="md"), label="X", position="bottom"), href="https://twitter.com/NASAaero", target="_blank"),
                                html.A(dmc.Tooltip(dmc.Avatar(src="/assets/icon-instagram.png", size="md", radius="md"), label="Instagram", position="bottom"), href="https://www.instagram.com/NASAaero/", target="_blank"),
                                html.A(dmc.Tooltip(dmc.Avatar(src="/assets/icon-linkedin.png", size="md", radius="md"), label="LinkedIn", position="bottom"), href="https://www.linkedin.com/company/nasa", target="_blank")
                            ])
                        ]
                    )
                ],
                    sx={"padding": "5vw"}
                )
            ]
        )
    ],
        style={
            "position": "fixed",
            "top": "0",
            "width": "100%",
            "overflow": "auto",
            "height": "100%",
            "backgroundColor": "#f8f9fa"
        }
    ),
    dmc.Space(h=60)  # Add some space at the bottom of the form
])

# Define the callback function to handle form submission
@app.callback(
    [Output("submit-button", "disabled"),
     Output("submit-button", "loading"),
     Output("modal", "opened")],
    [Input("submit-button", "n_clicks")],
    [State("last-name", "value"),
    State("first-name", "value"),
    State("phone-number", "value"),
    State("service-email", "value"),
    State("branch-service", "value"),
    State("grade", "value"),
    State("years-of-service", "value"),
    State("duty-station", "value"),
    State("job-specialty", "value"),
    State("date-separation", "value"),
    State("skillbridge-start-date", "value"),
    State("skillbridge-end-date", "value"),
    State("supervisor-name", "value"),
    State("supervisor-email", "value"),
    State("commanding-officer", "value"),
    State("commanding-officer-email", "value"),
    State("degrees", "value"),
    State("certifications", "value"),
    State("desired-career", "value"),
    State("opm-code", "value"),
    State("experience", "value"),
    State("ethnicity", "value"),
    State("race", "value"),
    State("sex", "value"),
    State("nasa-centers", "value"),
    State("completed-trstaps", "checked"),
    State("trstaps-completion-date", "value"),
    State("understand-info", "checked"),
    State("relocation-info", "checked")]
)
def handle_submission(n_clicks, *args):
    ctx = callback_context  # Get the context of the callback (which input triggered it)
    if not ctx.triggered:
        return True, False, False
    
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    # Calculate the duration of the SkillBridge program
    start_date = datetime.strptime(args[10], '%Y-%m-%d')
    end_date = datetime.strptime(args[11], '%Y-%m-%d')
    duration = (end_date - start_date).days

    # Check if the duration is within the allowed range (60-180 days)
    if duration < 60 or duration > 180:
        return True, False, False  # Disable submit button if duration is not within 60-180 days

    # Create a dictionary with the submitted data
    submission_data = {
        "submission_uid": str(uuid.uuid4()),
        "last_name": args[0],
        "first_name": args[1],
        "phone_number": args[2],
        "service_email": args[3],
        "branch_service": args[4],
        "grade": args[5],
        "years_of_service": args[6],
        "duty_station": args[7],
        "job_specialty": args[8],
        "date_separation": args[9],
        "skillbridge_start_date": args[10],
        "skillbridge_end_date": args[11],
        "supervisor_name": args[12],
        "supervisor_email": args[13],
        "commanding_officer": args[14],
        "commanding_officer_email": args[15],
        "degrees": args[16],
        "certifications": args[17],
        "desired_career": args[18],
        "opm_code": args[19],
        "experience": args[20],
        "ethnicity": args[21],
        "race": args[22],
        "sex": args[23],
        "nasa_centers": ";".join(args[24]) if args[24] else None,
        "completed_trstaps": args[25],
        "trstaps_completion_date": args[26],
        "understand_info": args[27],
        "relocation_info": args[28],
        "ip_address": request.environ.get("REMOTE_ADDR"),
        "epoch_entry_time": int(pd.Timestamp.utcnow().timestamp())
    }

    # Convert the submission data to a DataFrame (for saving to a database, for example)
    df = pd.DataFrame(submission_data, index=[0])
    # Save to database (example)
    # utils_gcp_sql.append_to_table('dbo', 'skillbridge_applications', df)

    return False, True, True  # Disable submit button, show loading and modal

if __name__ == '__main__':
    app.run_server(debug=True)  # Run the app in debug mode
