# Financial Event Catalog

The platform supports 28 financial event types across transaction, trading, investment, lending, compliance, account, and security categories.

| Event type | Category | Priority |
|---|---|---|
| transaction_alert | transaction | high |
| transaction_failure | transaction | high |
| upi_transaction | transaction | high |
| upi_failure | transaction | high |
| refund_processed | transaction | high |
| margin_call | trading | critical |
| price_alert | trading | medium |
| price_alert_triggered | trading | high |
| sip_reminder | investment | medium |
| sip_installment_due | investment | high |
| mutual_fund_purchase | investment | medium |
| mutual_fund_redemption | investment | medium |
| dividend_credit | investment | medium |
| corporate_action | investment | medium |
| fixed_deposit_maturity | investment | medium |
| portfolio_summary | investment | low |
| loan_disbursement | lending | high |
| loan_emi_due | lending | high |
| loan_emi_overdue | lending | critical |
| credit_card_statement | lending | medium |
| credit_card_payment_due | lending | high |
| kyc_status | compliance | high |
| regulatory_notice | compliance | critical |
| tax_statement_ready | compliance | medium |
| account_statement_ready | account | low |
| security_alert | security | critical |
| password_change | security | critical |
| login_from_new_device | security | critical |

Critical events override DND, quiet hours, user opt-outs, and frequency caps because they may be required for financial risk, fraud, security, or regulatory purposes.
