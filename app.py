from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.form.to_dict()

    # Retrieve asset criticality from localStorage (simulated here)
    asset_criticality_json = request.form.get('asset_criticality', None)
    if asset_criticality_json:
        asset_criticality = json.loads(asset_criticality_json)
    else:
        # Default values if not provided
        asset_criticality = [
            {"criticality": "VITAL", "criteria": "Alternative services and/or facilities cannot be provided if asset is lost or severely damaged. Loss or compromise will result in abandonment or long-term cessation of the functions or core business practices. Loss or compromise will have a debilitating impact on the reputation of the organisation (international, permanent)."},
            {"criticality": "KEY", "criteria": "Major restrictions to core business practices will result if asset is lost or severely damaged. Loss or compromise will result in long-term cessation/disruption of core business. Loss or compromise will have a major, widespread impact on the organisation’s reputation (national, sustained)."},
            {"criticality": "IMPORTANT", "criteria": "Some minor restrictions to core business practices will result if asset is lost or severely damaged. Loss or compromise will result in short-term cessation/disruption of core business. Loss or compromise may have an impact on the organisation’s reputation (regional, short-term)."},
            {"criticality": "SUPPORTING", "criteria": "Business as usual services and/or facilities can be provided if asset is lost or severely damaged. Loss or compromise will not result in cessation/disruption of core business. Loss or compromise will have no discernible impact on the organisation’s reputation."}
        ]

    # Retrieve threat criteria from localStorage (simulated here)
    threat_criteria_json = request.form.get('threat_criteria', None)
    if threat_criteria_json:
        threat_criteria = json.loads(threat_criteria_json)
    else:
        # Default values if not provided
        threat_criteria = {
            "intent": [
                {"rating": "None", "description": "No desire - absence of drive and purpose. Threat actor would not believe they have the capacity and competence to perpetrate the Threat Act."},
                {"rating": "Implied", "description": "Motivated, but with some flexibility in terms of method and capacity for compromise. Threat actor would have reasonable expectations of successfully perpetrating the Threat Act attack based on their capacity and competence."},
                {"rating": "Expressed", "description": "Extreme motivations with few if any limitations on perpetrating the Threat Act and no room for compromise. Threat actor would have a very high expectation of successfully perpetrating the Threat Act."}
            ],
            "capability": [
                {"rating": "Extensive", "description": "Fully funded and resourced. Highly skilled and comprehensively trained."},
                {"rating": "Moderate", "description": "Moderate level of funding and/or resources. Moderate level of training and skills."},
                {"rating": "Low", "description": "Few if any resources and/or funding. No knowledge or training."}
            ],
            "threatTolerance": [
                {"tolerance": "High", "description": "Threat Acts rated at this level must appear within the Risk Register."},
                {"tolerance": "Medium", "description": "Threat Acts rated at this level (and higher) must appear within the Risk Register."},
                {"tolerance": "Low", "description": "Threat Acts rated at this level (and higher) must appear within the Risk Register."}
            ],
            "threatMatrix": [
                {"capability": "Extensive", "intent1": "", "intent2": "Medium", "intent3": "High"},
                {"capability": "Moderate", "intent1": "Low", "intent2": "Medium", "intent3": "High"},
                {"capability": "Low", "intent1": "Low", "intent2": "Low", "intent3": "Medium"}
            ]
        }

    # Retrieve hazard criteria from localStorage (simulated here)
    hazard_criteria_json = request.form.get('hazard_criteria', None)
    if hazard_criteria_json:
        hazard_criteria = json.loads(hazard_criteria_json)
    else:
        # Default values if not provided
        hazard_criteria = [
            {"rating": "Critical", "criteria": "Event would be of rigorous intensity. Event could materialise with minimal warning. Event would be prolonged. The event is within close proximity. The event would be highly volatile. The event would be highly persistent."},
            {"rating": "Emerging", "criteria": "Event would be of moderate intensity. Event could materialise with manageable warning. Event would be of moderate duration. The event is within intermediate proximity. The event would be of medium volatility. The event would be moderately persistent."},
            {"rating": "Benign", "criteria": "Event would be of low intensity. Event could materialise with ample warning. Event would be short-term. The event is distant. The event would be of low volatility. The event would not be persistent."},
            {"rating": "Critical", "criteria": "Hazard events rated at this level must appear within the Risk Register."},
            {"rating": "Emerging", "criteria": "Hazard events rated at this level (and higher) must appear within the Risk Register."},
            {"rating": "Benign", "criteria": "Hazard events rated at this level (and higher) must appear within the Risk Register."}
        ]

    # Retrieve control effectiveness criteria from localStorage (simulated here)
    control_effectiveness_criteria_json = request.form.get('control_effectiveness_criteria', None)
    if control_effectiveness_criteria_json:
        control_effectiveness_criteria = json.loads(control_effectiveness_criteria_json)
    else:
        # Default values if not provided
        control_effectiveness_criteria = [
            {"rating": "ADEQUATE", "criteria": "Control elements are well designed to address threats. Nothing more to be done except review and monitor control elements. There are no doubts that the controls are the most appropriate for the task."},
            {"rating": "MODERATE", "criteria": "Most control elements are designed correctly, in place and effective. Some more work should be considered to improve operational effectiveness. There may be doubts around operational effectiveness and reliability."},
            {"rating": "INADEQUATE", "criteria": "Controls do not address threats effectively. There are significant control flaws or no credible controls at all. There are obvious doubts that the controls will work as intended."}
        ]

    # Retrieve risk assessment criteria from localStorage (simulated here)
    risk_assessment_criteria_json = request.form.get('risk_assessment_criteria', None)
    if risk_assessment_criteria_json:
        risk_assessment_criteria = json.loads(risk_assessment_criteria_json)
    else:
        # Default values if not provided
        risk_assessment_criteria = {
            "consequenceCriteria": [
                {"rating": "Negligible", "criteria": "Minor injury or first aid treatment. Compromise of information otherwise available in the public domain. 1% of budget (organizational, division or project budget as relevant). Local mention only. Quickly forgotten. Freedom to operate unaffected. Self-improvement review required. Minor issues impact. Minimal impact on non-core operations. The impact can be dealt with by routine operations. Minor damage or vandalism to asset."},
                {"rating": "Minor", "criteria": "Injury requiring treatment by medical practitioner and/or lost time from workplace. Minor compromise of information sensitive to internal or sub-unit interest. 2-5% of annual budget. Scrutiny by executive, internal committees or internal audit to prevent escalation. Short-term local media concerns, some impact on local level activities. Some impact on organization capability in terms of delays, systems quality but able to be dealt with at operational level. Minor damage or loss of <5% of total assets."},
                {"rating": "Moderate", "criteria": "Major injury/hospitalisation. Compromise of information sensitive to organization operation. 5-10% of annual budget. Persistent internal concern. Scrutiny required by external agencies. Long term 'brand' impact. Impact on organization resulting in reduced performance such that targets are not met. Organization existence is not threatened, but could be subject to significant review. Damage or loss of 20% of assets."},
                {"rating": "Major", "criteria": "Single death or multiple major injuries. Compromise of information sensitive to organization interests. 10% of project or organizational annual budget. Persistent intense national public, political and media scrutiny. Long term 'brand' impact. Major operations severely restricted. Breakdown of key activities etc., leading to reduction in business performance (e.g. service delays, revenue loss, client dissatisfaction, legislative breaches). Extensive damage or loss of >50% of assets."},
                {"rating": "Catastrophic", "criteria": "Multiple deaths. Compromise of information with significant ongoing impact. >20% of project or organizational annual budget. Intense national concern, government inquiry or sustained adverse national/international media. 'Brand' significantly affects organization abilities. Protracted unavailability of critical skills/people. Critical failure(s) preventing core activities from being performed. Survival of the project/activity/organization is threatened. Destruction or complete loss of >50% of assets."}
            ],
            "likelihoodCriteria": [
                {"likelihoodRating": "Certain", "likelihoodDescriptor": "Occurs on an annual basis and will happen again in the short term."},
                {"likelihoodRating": "Likely", "likelihoodDescriptor": "Has occurred in last few years within the organization or something has occurred that will cause it to happen in the short term."},
                {"likelihoodRating": "Possible", "likelihoodDescriptor": "Has occurred at least once within the organization and is likely to occur again in the medium term."},
                {"likelihoodRating": "Unlikely", "likelihoodDescriptor": "Is possible but has not occurred to date and is considered to have less than 1% chance of occurring within the organization."},
                {"likelihoodRating": "Rare", "likelihoodDescriptor": "Has never occurred within the organization but has occurred infrequently elsewhere and it is possible that it could occur in the medium term."}
            ],
            "riskTolerance": [
                {"riskTolerance": "Extreme", "riskTreatmentRequirements": "Risk cannot be justified on any grounds - immediate risk treatment or avoidance is mandatory."},
                {"riskTolerance": "High", "riskTreatmentRequirements": "Risk exceeds the organization’s tolerance threshold and must be reduced."},
                {"riskTolerance": "Medium", "riskTreatmentRequirements": "Risk should be reduced if cost effective to do so. If not monitoring arrangements must be established and the risk must be reviewed periodically."},
                {"riskTolerance": "Low", "riskTreatmentRequirements": "Risk is within acceptable tolerances and should be monitored and reviewed for changes."}
            ],
            "riskMatrix": [
                {"likelihood": "Certain", "consequence1": "Medium", "consequence2": "Medium", "consequence3": "High", "consequence4": "Extreme", "consequence5": "Extreme"},
                {"likelihood": "Likely", "consequence1": "Low", "consequence2": "Medium", "consequence3": "High", "consequence4": "High", "consequence5": "Extreme"},
                {"likelihood": "Possible", "consequence1": "Low", "consequence2": "Low", "consequence3": "Medium", "consequence4": "High", "consequence5": "High"},
                {"likelihood": "Unlikely", "consequence1": "Low", "consequence2": "Low", "consequence3": "Medium", "consequence4": "Medium", "consequence5": "Medium"},
                {"likelihood": "Rare", "consequence1": "Low", "consequence2": "Low", "consequence3": "Low", "consequence4": "Medium", "consequence5": "Medium"}
            ]
        }

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    flowables = []

    # Title
    title = Paragraph("Risk Assessment Report", styles['Title'])
    flowables.append(title)
    flowables.append(Spacer(1, 12))

    # General Information
    flowables.append(Paragraph("General Information", styles['Heading2']))
    flowables.append(Spacer(1, 12))
    prepared_for = Paragraph(f"Prepared for: {data.get('prepared_for')}", styles['Normal'])
    prepared_by = Paragraph(f"Prepared By: {data.get('prepared_by')}", styles['Normal'])
    scope = Paragraph(f"Scope: {data.get('scope')}", styles['Normal'])
    flowables.extend([prepared_for, Spacer(1, 12), prepared_by, Spacer(1, 12), scope, Spacer(1, 12)])

    # Objectives and Risk Details
    flowables.append(Paragraph("Objectives and Risk Details", styles['Heading2']))
    flowables.append(Spacer(1, 12))
    objectives = Paragraph(f"Objectives: {data.get('objectives')}", styles['Normal'])
    risk_details = Paragraph(f"Risk Details: {data.get('risk_details')}", styles['Normal'])
    flowables.extend([objectives, Spacer(1, 12), risk_details, Spacer(1, 12)])

    # Asset Criticality Table
    flowables.append(Paragraph("Asset Criticality", styles['Heading2']))
    flowables.append(Spacer(1, 12))
    table_data = [["Criticality Rating", "Criteria"]]
    for item in asset_criticality:
        table_data.append([item["criticality"], item["criteria"]])
    table = Table(table_data, colWidths=[2 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(table)
    flowables.append(Spacer(1, 12))

    # Threat Criteria Tables
    flowables.append(Paragraph("Threat Criteria", styles['Heading2']))
    flowables.append(Spacer(1, 12))

    # Intent Table
    flowables.append(Paragraph("Intent", styles['Heading3']))
    intent_table_data = [["Intent Rating", "Intent Descriptor"]]
    for item in threat_criteria['intent']:
        intent_table_data.append([item["rating"], item["description"]])
    intent_table = Table(intent_table_data, colWidths=[2 * inch, 4 * inch])
    intent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(intent_table)
    flowables.append(Spacer(1, 12))

    # Capability Table
    flowables.append(Paragraph("Capability", styles['Heading3']))
    capability_table_data = [["Capability Rating", "Capability Descriptor"]]
    for item in threat_criteria['capability']:
        capability_table_data.append([item["rating"], item["description"]])
    capability_table = Table(capability_table_data, colWidths=[2 * inch, 4 * inch])
    capability_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(capability_table)
    flowables.append(Spacer(1, 12))

    # Threat Tolerance Table
    flowables.append(Paragraph("Threat Tolerance", styles['Heading3']))
    threat_tolerance_table_data = [["Threat Tolerance", "Threat Description"]]
    for item in threat_criteria['threatTolerance']:
        threat_tolerance_table_data.append([item["tolerance"], item["description"]])
    threat_tolerance_table = Table(threat_tolerance_table_data, colWidths=[2 * inch, 4 * inch])
    threat_tolerance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(threat_tolerance_table)
    flowables.append(Spacer(1, 12))

    # Threat Matrix Table
    flowables.append(Paragraph("Threat Matrix", styles['Heading3']))
    threat_matrix_table_data = [["Capability", "None", "Implied", "Expressed"]]
    for item in threat_criteria['threatMatrix']:
        threat_matrix_table_data.append([item["capability"], item["intent1"], item["intent2"], item["intent3"]])
    threat_matrix_table = Table(threat_matrix_table_data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])
    threat_matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(threat_matrix_table)
    flowables.append(Spacer(1, 12))

    # Hazard Criteria Tables
    flowables.append(Paragraph("Hazard Criteria", styles['Heading2']))
    flowables.append(Spacer(1, 12))

    # Event Rating Table
    flowables.append(Paragraph("Event Rating", styles['Heading3']))
    event_rating_table_data = [["Event Rating", "Criteria"]]
    for item in hazard_criteria[:3]:
        event_rating_table_data.append([item["rating"], item["criteria"]])
    event_rating_table = Table(event_rating_table_data, colWidths=[2 * inch, 4 * inch])
    event_rating_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(event_rating_table)
    flowables.append(Spacer(1, 12))

    # Event Tolerance Table
    flowables.append(Paragraph("Event Tolerance", styles['Heading3']))
    event_tolerance_table_data = [["Event Tolerance", "Criteria"]]
    for item in hazard_criteria[3:]:
        event_tolerance_table_data.append([item["rating"], item["criteria"]])
    event_tolerance_table = Table(event_tolerance_table_data, colWidths=[2 * inch, 4 * inch])
    event_tolerance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(event_tolerance_table)
    flowables.append(Spacer(1, 12))

    # Control Effectiveness Criteria Table
    flowables.append(Paragraph("Control Effectiveness Criteria", styles['Heading2']))
    flowables.append(Spacer(1, 12))
    control_effectiveness_table_data = [["Rating", "Criteria"]]
    for item in control_effectiveness_criteria:
        control_effectiveness_table_data.append([item["rating"], item["criteria"]])
    control_effectiveness_table = Table(control_effectiveness_table_data, colWidths=[2 * inch, 4 * inch])
    control_effectiveness_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(control_effectiveness_table)
    flowables.append(Spacer(1, 12))

    # Risk Assessment Criteria Tables
    flowables.append(Paragraph("Risk Assessment Criteria", styles['Heading2']))
    flowables.append(Spacer(1, 12))

    # Consequence Criteria Table
    flowables.append(Paragraph("Consequence Criteria", styles['Heading3']))
    consequence_criteria_table_data = [["Rating", "Criteria"]]
    for item in risk_assessment_criteria['consequenceCriteria']:
        consequence_criteria_table_data.append([item["rating"], item["criteria"]])
    consequence_criteria_table = Table(consequence_criteria_table_data, colWidths=[2 * inch, 4 * inch])
    consequence_criteria_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(consequence_criteria_table)
    flowables.append(Spacer(1, 12))

    # Likelihood Criteria Table
    flowables.append(Paragraph("Likelihood Criteria", styles['Heading3']))
    likelihood_criteria_table_data = [["Likelihood Rating", "Likelihood Descriptor"]]
    for item in risk_assessment_criteria['likelihoodCriteria']:
        likelihood_criteria_table_data.append([item["likelihoodRating"], item["likelihoodDescriptor"]])
    likelihood_criteria_table = Table(likelihood_criteria_table_data, colWidths=[2 * inch, 4 * inch])
    likelihood_criteria_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(likelihood_criteria_table)
    flowables.append(Spacer(1, 12))

    # Risk Tolerance Table
    flowables.append(Paragraph("Risk Tolerance", styles['Heading3']))
    risk_tolerance_table_data = [["Risk Tolerance", "Risk Treatment Requirements"]]
    for item in risk_assessment_criteria['riskTolerance']:
        risk_tolerance_table_data.append([item["riskTolerance"], item["riskTreatmentRequirements"]])
    risk_tolerance_table = Table(risk_tolerance_table_data, colWidths=[2 * inch, 4 * inch])
    risk_tolerance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(risk_tolerance_table)
    flowables.append(Spacer(1, 12))

    # Risk Matrix Table
    flowables.append(Paragraph("Risk Matrix", styles['Heading3']))
    risk_matrix_table_data = [["Likelihood", "Negligible", "Minor", "Moderate", "Major", "Catastrophic"]]
    for item in risk_assessment_criteria['riskMatrix']:
        risk_matrix_table_data.append([item["likelihood"], item["consequence1"], item["consequence2"], item["consequence3"], item["consequence4"], item["consequence5"]])
    risk_matrix_table = Table(risk_matrix_table_data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch, 2 * inch, 2 * inch])
    risk_matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    flowables.append(risk_matrix_table)
    flowables.append(Spacer(1, 12))

    # Recommendations
    flowables.append(Paragraph("Recommendations", styles['Heading2']))
    flowables.append(Spacer(1, 12))
    recommendations = Paragraph(f"Recommendations: {data.get('recommendations')}", styles['Normal'])
    flowables.append(recommendations)
    flowables.append(Spacer(1, 12))

    # Build PDF
    doc.build(flowables)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='risk_assessment_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
