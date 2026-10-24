# TRAI and Compliance Design

## TRAI DND compliance

- Promotional and non-critical SMS are suppressed for users with DND enabled.
- Transactional, security, fraud, margin-call, and regulatory messages are classified as critical or service messages and are not suppressed by DND.
- Every suppression decision records a reason: `TRAI_DND`, `QUIET_HOURS`, `USER_OPT_OUT`, `CHANNEL_DISABLED`, or `FREQUENCY_CAP`.
- Sender IDs, templates, and consent records must be registered through the applicable DLT/communication-provider workflow before production use.

## Quiet hours

- Default quiet hours are 21:00 to 08:00 in the user's timezone.
- Quiet hours apply to SMS and WhatsApp.
- Critical financial and security events override quiet hours.
- In-app notifications may be created during quiet hours but should not trigger device wake or sound.

## Consent and preferences

- Users can enable or disable each channel.
- Users can opt out of non-critical categories.
- Critical security and regulatory notices cannot be fully opted out.
- Preference changes are auditable and versioned in production.

## Data protection

- Store only masked account numbers in notification payloads.
- Do not include full card numbers, passwords, OTPs, or secrets in templates.
- Encrypt notification content at rest and in transit.
- Retain delivery metadata according to the organisation's records-retention policy.
