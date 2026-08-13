"""
GUARDIAN GHANA - PROFESSIONAL EMAIL ASSAULT SYSTEM WEB APP
Version: 2.0 - Advanced Battle Station
Author: Chris Dela Yao Agbeke
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import re
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Guardian Ghana - Email Assault System",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for professional military styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3c72;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .battle-station {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .email-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1e3c72;
        margin-bottom: 1rem;
    }
    .success-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .warning-badge {
        background-color: #ffc107;
        color: black;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .export-btn {
        background-color: #1e3c72;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


class GuardianEmailGenerator:
    """Professional email generator - Web optimized"""

    def __init__(self):
        self.email_patterns = {
            'professional': [
                '{first}@{domain}',
                '{first}.{last}@{domain}',
                '{first}{last}@{domain}',
                '{first}.{initial}@{domain}',
                '{initial}.{last}@{domain}',
                '{last}.{first}@{domain}',
                '{first}-{last}@{domain}',
                '{first}_{last}@{domain}',
                '{initial}{last}@{domain}',
                '{last}{first}@{domain}',
            ],
            'position_prefix': {
                'owner': ['owner', 'proprietor', 'director', 'ceo'],
                'md': ['md', 'ceo', 'managing.director', 'executive.director', 'president'],
                'operations': ['operations', 'ops', 'site.manager', 'mine.manager', 'plant.manager'],
                'compliance': ['compliance', 'regulatory', 'environmental', 'ehs'],
                'sustainability': ['sustainability', 'esg', 'hos', 'head.sustainability', 'csr'],
                'hse': ['hse', 'safety', 'health.safety', 'environmental.manager', 'ehs.manager'],
                'finance': ['finance', 'cfo', 'financial.controller', 'accounts'],
                'technical': ['technical', 'chief.engineer', 'mine.engineer', 'engineering'],
                'hr': ['hr', 'human.resources', 'recruitment'],
                'marketing': ['marketing', 'pr', 'communications'],
            },
            'company_general': [
                'info@{domain}',
                'contact@{domain}',
                'enquiries@{domain}',
                'admin@{domain}',
                'hello@{domain}',
                'office@{domain}',
                'mining@{domain}',
                'compliance@{domain}',
                'environment@{domain}',
                'sustainability@{domain}',
                'hse@{domain}',
                'reception@{domain}',
            ]
        }

        self.templates = self._load_templates()

    def _load_templates(self):
        """Load all email templates"""
        return {
            'owner': {
                'subject': "EPA Compliance Solution for Your Small Scale Mining License",
                'intro': "As a fellow Ghanaian entrepreneur in the mining sector, I understand the challenges of maintaining EPA compliance while running operations.",
                'body': """
Guardian Ghana helps small scale mining license holders like yourself:

• Cut EPA reporting time from 2 weeks → 2 hours
• Avoid unexpected fines with AI-powered monitoring
• Generate professional EPA reports with one click
• Get 48-hour warnings before compliance issues arise

Simple question: Who currently handles your environmental reporting to EPA?

We offer a 30-day pilot at 50% discount (₵2,500 instead of ₵5,000) for the first 10 SSM license holders.
"""
            },
            'md': {
                'subject': "Strategic Compliance Technology for [COMPANY] Mining Operations",
                'intro': "For Restricted Mining Lease holders, operational continuity depends on consistent EPA compliance.",
                'body': """
Guardian Ghana provides enterprise-level monitoring specifically designed for RML holders:

• Real-time monitoring across all discharge points
• Predictive analytics to prevent violations before they occur
• Automated quarterly/annual EPA report generation
• Dashboard for management oversight of compliance status

We currently serve RML holders who have reduced compliance-related downtime by 70%.
"""
            },
            'operations': {
                'subject': "Streamlining EPA Reporting for [COMPANY] Operations Team",
                'intro': "Balancing production targets with EPA compliance requirements is a constant challenge for operations managers.",
                'body': """
Our AI monitoring platform helps operations teams:

• Monitor water quality 24/7 without manual testing
• Get early warnings (48-hour notice) of potential issues
• Automate compliance documentation
• Reduce environmental incident response time

The result: More time for production optimization, less time on compliance paperwork.
"""
            },
            'compliance': {
                'subject': "Technology Partnership for Mining Compliance Management",
                'intro': "As a compliance professional, you understand the importance of accurate, timely reporting and proactive monitoring.",
                'body': """
Guardian Ghana is built specifically for mining compliance teams:

• Centralized dashboard for all monitoring points
• Automated alert system for threshold breaches
• Audit-ready documentation with timestamps
• Predictive modeling for risk assessment

We're the technology partner that makes your job easier and your compliance program stronger.
"""
            },
            'sustainability': {
                'subject': "ESG & Environmental Monitoring Platform for [COMPANY]",
                'intro': "For mining companies committed to sustainability, transparent environmental monitoring is non-negotiable.",
                'body': """
Guardian Ghana supports sustainability leaders with:

• Real-time ESG reporting capabilities
• Predictive analytics for environmental risk management
• Automated compliance documentation for stakeholders
• Transparent monitoring accessible to regulators and communities

Our platform turns compliance from a cost center into a sustainability showcase.
"""
            },
            'hse': {
                'subject': "Integrated HSE Monitoring for Mining Operations",
                'intro': "Health, Safety, and Environmental management requires comprehensive monitoring and rapid response capabilities.",
                'body': """
Guardian Ghana supports HSE teams with:

• 24/7 water quality monitoring with instant alerts
• Historical data analysis for trend identification
• Automated compliance reporting
• Integration potential with other HSE systems

Our platform enables proactive HSE management rather than reactive response.
"""
            },
            'consultant': {
                'subject': "Partnership: Technology-Enabled Compliance Solutions",
                'intro': "Environmental consultants serving mining clients need robust tools to deliver value and ensure compliance.",
                'body': """
Guardian Ghana offers consulting firms:

• White-labeled monitoring platform for client projects
• 20% referral commission on closed business
• Joint proposal development support
• Technical partnership for complex compliance projects

We enhance your service delivery with technology while you maintain client relationships.
"""
            },
            'general': {
                'subject': "EPA Compliance Monitoring Platform for Ghana Mining Sector",
                'intro': "Guardian Ghana provides AI-powered environmental monitoring specifically designed for Ghana's mining sector.",
                'body': """
Our platform helps mining companies:

• Automate EPA compliance reporting
• Monitor water quality in real-time
• Predict and prevent pollution events
• Generate professional compliance reports

We're currently offering a 30-day pilot program at 50% discount (₵2,500) for the first 10 mining companies.
"""
            }
        }

    def generate_emails(self, first_name, last_name, domain, middle_name=None, position=None):
        """Generate possible email addresses"""
        first = first_name.lower().strip()
        last = last_name.lower().strip()
        initial = first[0] if first else ''
        middle_initial = middle_name[0].lower() if middle_name else ''

        emails = []

        # Basic patterns
        for pattern in self.email_patterns['professional']:
            try:
                email = pattern.format(
                    first=first,
                    last=last,
                    initial=initial,
                    domain=domain
                )
                emails.append(email)
            except:
                continue

        # Position-specific patterns
        if position and position in self.email_patterns['position_prefix']:
            for prefix in self.email_patterns['position_prefix'][position]:
                emails.append(f"{prefix}@{domain}")
                emails.append(f"{first}.{prefix}@{domain}")
                emails.append(f"{prefix}.{last}@{domain}")

        # Middle name variations
        if middle_initial:
            emails.append(f"{first}.{middle_initial}.{last}@{domain}")
            emails.append(f"{first}{middle_initial}{last}@{domain}")
            emails.append(f"{first}.{middle_initial}@{domain}")

        # Remove duplicates and sort
        return sorted(list(dict.fromkeys(emails)))

    def generate_company_emails(self, domain):
        """Generate general company emails"""
        return [pattern.format(domain=domain) for pattern in self.email_patterns['company_general']]

    def generate_email_content(self, template_key, first_name, company_name, position=None):
        """Generate complete email with signature"""
        template = self.templates.get(template_key, self.templates['general'])

        # Customize subject
        subject = template['subject'].replace('[COMPANY]', company_name)

        # Build body
        body = f"""Dear {first_name if first_name else 'Sir/Madam'},

{template['intro']}
{template['body']}

Would you be available for a 15-minute call next week to discuss how we can support {company_name}?

Best regards,

Chris Dela Yao Agbeke
Founder & CEO
Guardian Ghana
📞 [Your Number]
🌐 https://guardian-ghana-app.streamlit.app

---
Guardian Ghana - AI-Powered Environmental Intelligence
Protecting Ghana's water resources through technology
"""
        return subject, body


# Initialize generator
generator = GuardianEmailGenerator()

# Main UI
st.markdown('<h1 class="main-header">🎯 GUARDIAN GHANA</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="battle-station">
    <h2>PROFESSIONAL EMAIL ASSAULT SYSTEM</h2>
    <p>Generate targeted outreach emails for mining compliance prospects • Battlefield Ready v2.0</p>
</div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 🎯 TARGET INPUT")

    with st.form("email_generator"):
        first_name = st.text_input("First Name *", help="Contact person's first name")
        last_name = st.text_input("Last Name (Surname) *", help="Contact person's last name")
        middle_name = st.text_input("Middle Name", help="Optional - for better email variations")

        company_name = st.text_input("Company Name *", help="Full company name")
        domain = st.text_input("Company Domain *", help="e.g., company.com", placeholder="company.com")

        # Position selection
        position_options = [
            "Select Position (Optional)",
            "owner - Small Scale Mining Owner",
            "md - Managing Director/CEO",
            "operations - Operations Manager",
            "compliance - Compliance Manager",
            "sustainability - Sustainability/ESG Head",
            "hse - HSE Manager",
            "consultant - Environmental Consultant",
            "general - General Company Contact",
            "no_position - Generate Only Emails"
        ]

        position_choice = st.selectbox("Position / Target Role", position_options)

        submitted = st.form_submit_button("🚀 GENERATE EMAIL ASSAULT", use_container_width=True)

with col2:
    if submitted:
        if not first_name or not last_name or not company_name or not domain:
            st.error("⚠️ Please fill all required fields (*)")
        else:
            # Clean domain
            domain = domain.lower().replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]

            # Determine position key
            position_key = None
            template_key = 'general'

            if 'owner' in position_choice:
                position_key = 'owner'
                template_key = 'owner'
            elif 'md' in position_choice:
                position_key = 'md'
                template_key = 'md'
            elif 'operations' in position_choice:
                position_key = 'operations'
                template_key = 'operations'
            elif 'compliance' in position_choice:
                position_key = 'compliance'
                template_key = 'compliance'
            elif 'sustainability' in position_choice:
                position_key = 'sustainability'
                template_key = 'sustainability'
            elif 'hse' in position_choice:
                position_key = 'hse'
                template_key = 'hse'
            elif 'consultant' in position_choice:
                position_key = 'consultant'
                template_key = 'consultant'
            elif 'general' in position_choice:
                template_key = 'general'

            # Generate emails
            if position_key and position_key != 'general':
                emails = generator.generate_emails(first_name, last_name, domain, middle_name, position_key)
            else:
                emails = generator.generate_emails(first_name, last_name, domain, middle_name)

            # Generate company emails
            company_emails = generator.generate_company_emails(domain)

            # Generate email content
            if template_key == 'general':
                subject, body = generator.generate_email_content('general', 'Team', company_name)
            else:
                subject, body = generator.generate_email_content(template_key, first_name.split()[0], company_name)

            # Display results
            st.markdown("### 📧 GENERATED INTELLIGENCE")

            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["🎯 Target Emails", "🏢 Company Emails", "📨 Email Draft"])

            with tab1:
                st.markdown(f"**{len(emails)} email variations generated**")

                # Create DataFrame for better display
                email_df = pd.DataFrame({
                    'Priority': ['High'] * 5 + ['Medium'] * (len(emails) - 5) if len(emails) > 5 else ['High'] * len(
                        emails),
                    'Email': emails[:15] if len(emails) > 15 else emails
                })

                for idx, row in email_df.iterrows():
                    badge = "🟢 HIGH" if row['Priority'] == 'High' else "🟡 MEDIUM"
                    st.markdown(f"{badge} `{row['Email']}`")

                if len(emails) > 15:
                    st.info(f"... and {len(emails) - 15} more variations")

            with tab2:
                st.markdown(f"**{len(company_emails)} general company emails**")
                for email in company_emails[:10]:
                    st.markdown(f"🏢 `{email}`")

            with tab3:
                st.markdown("#### 📨 COMPLETE EMAIL DRAFT")

                # Email preview card
                st.markdown(f"""
                <div class="email-card">
                    <span class="success-badge">READY TO SEND</span>
                    <span class="warning-badge">{position_key.upper() if position_key else 'GENERAL'}</span>
                    <br><br>
                    <strong>TO:</strong> {emails[0] if emails else company_emails[0]}<br>
                    <strong>SUBJECT:</strong> {subject}<br><br>
                    {body.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

                # Export options
                col_exp1, col_exp2 = st.columns(2)

                with col_exp1:
                    # Copy to clipboard
                    full_email = f"TO: {emails[0] if emails else company_emails[0]}\nSUBJECT: {subject}\n\n{body}"
                    st.button("📋 Copy to Clipboard",
                              on_click=lambda: st.write(f"```\n{full_email}\n```"),
                              use_container_width=True)

                with col_exp2:
                    # Export as TXT
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"guardian_ghana_{company_name[:10]}_{timestamp}.txt"

                    export_data = f"""
GUARDIAN GHANA - EMAIL ASSAULT PACKAGE
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target: {company_name}
Contact: {first_name} {last_name}
Position: {position_key or 'General'}

{'=' * 60}

PRIORITY EMAIL ADDRESSES:
{chr(10).join([f'• {email}' for email in emails[:5]])}

{'=' * 60}

COMPANY EMAILS:
{chr(10).join([f'• {email}' for email in company_emails[:5]])}

{'=' * 60}

EMAIL DRAFT:
TO: {emails[0] if emails else company_emails[0]}
SUBJECT: {subject}

{body}

{'=' * 60}

ALL GENERATED EMAILS ({len(emails)}):
{chr(10).join([f'{i + 1}. {email}' for i, email in enumerate(emails)])}

{'=' * 60}
END OF REPORT
"""

                    st.download_button(
                        label="📥 Export as TXT",
                        data=export_data,
                        file_name=filename,
                        mime="text/plain",
                        use_container_width=True
                    )

            # Store in session state for batch export
            if 'email_batch' not in st.session_state:
                st.session_state.email_batch = []

            st.session_state.email_batch.append({
                'company': company_name,
                'contact': f"{first_name} {last_name}",
                'position': position_key or 'general',
                'emails': emails[:10],
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            })

            st.success(f"✅ Target acquired! {len(emails)} email variations generated.")

# Batch export section
if 'email_batch' in st.session_state and st.session_state.email_batch:
    st.markdown("---")
    st.markdown("### 📦 BATCH EXPORT")
    st.write(f"**{len(st.session_state.email_batch)} targets** in current session")

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        if st.button("💾 Export All as CSV", use_container_width=True):
            df = pd.DataFrame(st.session_state.email_batch)
            csv = df.to_csv(index=False)

            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="guardian_ghana_batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv">📥 Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Batch export ready")

    with col_b2:
        if st.button("🗑️ Clear Batch"):
            st.session_state.email_batch = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <strong>GUARDIAN GHANA - EMAIL ASSAULT SYSTEM v2.0</strong><br>
    Battlefield Ready • Mining Compliance Outreach • Generate. Target. Execute.
</div>
""", unsafe_allow_html=True)