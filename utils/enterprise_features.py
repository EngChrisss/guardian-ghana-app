"""
Enterprise features for government and corporate clients
"""
import streamlit as st
import pandas as pd
import numpy as np  # ADD THIS
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class EnterpriseDashboard:
    def __init__(self):
        self.client_tiers = {
            'government': {
                'features': ['real-time_monitoring', 'compliance_tracking', 'enforcement_tools',
                           'historical_analysis', 'multi_agency_access'],
                'data_retention': '7 years',
                'support_level': '24/7 priority'
            },
            'corporate': {
                'features': ['risk_assessment', 'compliance_alerts', 'custom_thresholds',
                           'api_access', 'sla_guarantee'],
                'data_retention': '3 years',
                'support_level': 'business hours'
            },
            'research': {
                'features': ['raw_data_access', 'custom_analytics', 'export_tools',
                           'api_access', 'collaboration_tools'],
                'data_retention': '10 years',
                'support_level': 'email'
            }
        }

    def generate_client_portal(self, client_type: str = 'government') -> Dict:
        """Generate a customized portal for different client types"""
        portal = {
            'welcome_message': f"Welcome to Guardian Ghana {client_type.title()} Portal",
            'features': self.client_tiers[client_type]['features'],
            'dashboard_sections': self._get_dashboard_sections(client_type),
            'reports': self._generate_standard_reports(client_type),
            'alerts': self._get_client_alerts(client_type)
        }
        return portal

    def _get_dashboard_sections(self, client_type: str) -> List[Dict]:
        """Get relevant dashboard sections for client type"""
        sections = []

        if client_type == 'government':
            sections = [
                {'title': 'National Water Security', 'type': 'map', 'priority': 'high'},
                {'title': 'Compliance Violations', 'type': 'table', 'priority': 'high'},
                {'title': 'Enforcement Actions', 'type': 'workflow', 'priority': 'medium'},
                {'title': 'Regional Analysis', 'type': 'charts', 'priority': 'medium'},
                {'title': 'Budget Impact', 'type': 'metrics', 'priority': 'low'}
            ]
        elif client_type == 'corporate':
            sections = [
                {'title': 'Risk Assessment', 'type': 'heatmap', 'priority': 'high'},
                {'title': 'Compliance Status', 'type': 'status', 'priority': 'high'},
                {'title': 'Operational Impact', 'type': 'metrics', 'priority': 'medium'},
                {'title': 'Regulatory Updates', 'type': 'feed', 'priority': 'low'}
            ]

        return sections

    def _generate_standard_reports(self, client_type: str) -> List[Dict]:
        """Generate standard reports for client type"""
        reports = []

        base_reports = [
            {'name': 'Daily Monitoring Summary', 'frequency': 'daily', 'format': 'PDF/Excel'},
            {'name': 'Weekly Compliance Report', 'frequency': 'weekly', 'format': 'PDF'},
            {'name': 'Monthly Risk Assessment', 'frequency': 'monthly', 'format': 'PDF/PPT'}
        ]

        if client_type == 'government':
            base_reports.extend([
                {'name': 'Quarterly EPA Submission', 'frequency': 'quarterly', 'format': 'Official'},
                {'name': 'Annual Water Security Report', 'frequency': 'annually', 'format': 'Book'}
            ])

        return base_reports

    def _get_client_alerts(self, client_type: str) -> List[str]:
        """Get alerts relevant to client type"""
        alerts = [
            "System Status: Operational",
            "Last Data Update: Today",
            "AI Model: 87% Accuracy"
        ]

        if client_type == 'government':
            alerts.append("Compliance Deadline: End of Quarter")
            alerts.append("Enforcement Actions: 3 pending")

        return alerts

    def generate_pricing_tier(self, tier_name: str) -> Dict:
        """Generate pricing structure for different tiers"""
        tiers = {
            'basic': {
                'price': '₵62,500/month',
                'features': ['5 rivers', 'basic_alerts', 'web_dashboard', 'email_support'],
                'limitations': ['no_api', 'no_customization', '24h_data_delay'],
                'best_for': 'Small mining companies'
            },
            'professional': {
                'price': '₵187,500/month',
                'features': ['20 rivers', 'ai_predictions', 'api_access', 'custom_alerts', 'priority_support'],
                'addons': ['mobile_app', 'additional_users', 'custom_reports'],
                'best_for': 'Medium enterprises, Local governments'
            },
            'enterprise': {
                'price': 'Custom (starts at ₵625,000/month)',
                'features': ['unlimited_rivers', 'full_ai_suite', 'dedicated_server', '24/7_support',
                           'custom_integration', 'sla_99.9%'],
                'implementation': ['6-8 weeks', 'dedicated_team', 'training_sessions'],
                'best_for': 'National governments, Large corporations'
            }
        }

        return tiers.get(tier_name, tiers['professional'])


class RevenueCalculator:
    def __init__(self):
        self.ghana_market_size = 500  # Estimated potential clients in Ghana

    def calculate_potential_revenue(self, client_distribution: Dict = None) -> Dict:
        """Calculate potential revenue based on client distribution - IN GHANA CEDIS"""
        if client_distribution is None:
            client_distribution = {
                'basic': 0.6,      # 60% of clients
                'professional': 0.3,  # 30% of clients
                'enterprise': 0.1     # 10% of clients
            }

        enterprise = EnterpriseDashboard()
        total_clients = self.ghana_market_size

        # Calculate in Ghana Cedis (1 USD = 12.5 GHS)
        revenue = {
            'basic': total_clients * client_distribution['basic'] * 62500,    # ₵62,500
            'professional': total_clients * client_distribution['professional'] * 187500,  # ₵187,500
            'enterprise': total_clients * client_distribution['enterprise'] * 625000,      # ₵625,000
        }

        monthly_revenue = sum(revenue.values())
        annual_revenue = monthly_revenue * 12

        return {
            'monthly_revenue': f"₵{monthly_revenue:,.0f}",
            'annual_revenue': f"₵{annual_revenue:,.0f}",
            'client_distribution': {
                'basic': int(total_clients * client_distribution['basic']),
                'professional': int(total_clients * client_distribution['professional']),
                'enterprise': int(total_clients * client_distribution['enterprise'])
            },
            'assumptions': {
                'market_size': self.ghana_market_size,
                'conversion_rate': '20% year 1'
            }
        }


# Create instances
enterprise_dashboard = EnterpriseDashboard()
revenue_calculator = RevenueCalculator()