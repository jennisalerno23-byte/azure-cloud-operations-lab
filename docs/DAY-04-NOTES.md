# Day 4 - Azure Monitor and Log Analytics

## Implemented

- Registered `Microsoft.Insights`
- Registered `Microsoft.OperationalInsights`
- Azure Monitor native VM CPU metric
- CPU metric alert: Average > 70%
- Evaluation: every 1 minute / 5-minute window
- Severity 2 - Warning
- Action Group with email notification
- Log Analytics Workspace
- Azure Monitor Agent
- Data Collection Rule for Linux Syslog
- DCR association with VM

## Validations

- Generated sustained CPU load
- Linux confirmed ~100% CPU usage
- Azure Monitor recorded ~99.7%
- CPU alert triggered
- Email notification received
- Alert automatically resolved after CPU recovery
- Recovery email received
- Syslog data received in Log Analytics
- Manual `daemon.info` event found with KQL
- Nginx stop/start events investigated centrally in Log Analytics

## Troubleshooting

- `Microsoft.Insights` provider was not registered
- `Microsoft.OperationalInsights` provider was not registered
- DCR required `streams = ["Microsoft-Syslog"]` inside the Syslog data source
- Log Analytics ingestion is not immediate

## KQL Practiced

- Filter by `Computer`
- Filter by `Facility`
- Filter by `SeverityLevel`
- Search text in `SyslogMessage`
- Order events by `TimeGenerated`

## Key Findings

- Azure Monitor metrics have ingestion and display latency compared with local Linux tools such as `top`.
- Metrics help detect that something is wrong. Logs help investigate what happened.
