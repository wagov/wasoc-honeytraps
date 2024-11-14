# WA HoneyTraps Program

This site contains technical information to onboard to WA HoneyTraps program.

## Onboarding Process (Technical)

1. Raise a ticket in <https://irp.dpc.wa.gov.au> to get onboard WA Honeytraps Program.
2. Verify that a Canary group has been provisioned for agency by WA SOC.
3. Deploy integration webhook logic-apps [send-canary-alert-webhook](arm-templates/send-canary-alert-webhook/README.md)
4. Deploy analytic rules for Microsoft Sentinel [analytic-rules](arm-templates/analytic-rules/README.md)
5. Ensure analytic rules and logic-apps were enabled
6. Initiate end-to-end test to generate alert

## Feedback
For questions or feedback, please contact cybersecurity@dpc.wa.gov.au