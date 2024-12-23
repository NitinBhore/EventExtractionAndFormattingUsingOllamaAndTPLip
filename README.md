# Event Extraction and Formatting

## Assignment Description:
You are tasked with extracting all events from an RFP content file that may be in **Excel**, **PDF**, or **DOCX** format. Each event must include the following details:  

- **Start date**  
- **Day of the week**  
- **Repeat count**  
- **Start time**  
- **End time**  
- **Event type**  
- **Setup style**  
- **Number of people**  
- **Additional comments**  

If any of the fields are missing, leave them blank.  

---

### Desired JSON Output Format:
```json
{
  "events": [
    ["MM/DD/YYYY", "day of the week", [
      ["Repeat Count (default value blank)", "Start time (default value blank)", "End time (default value blank)", "Event type (default value blank)", "Setup style (default value blank)", "Number of people (default value blank)", "Additional comments (default value blank)"]
    ]]
  ]
}
