# examples = [
#     {
#         "input": "What were the fault statuses of the main actuator over the last 24 hours?",
#         "query": "SELECT `DATE-TIME`, `Main Act Fault St` FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 DAY;"
#     },
#     {
#         "input": "How many times did the actuator fault status change to 'Fault' in the last week?",
#         "query": "SELECT COUNT(*) FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 WEEK AND `Main Act Fault St` = 'Fault';"
#     },
#     {
#         "input": "What is the average turbidity recorded over the last month?",
#         "query": "SELECT AVG(Turbidity) AS AverageTurbidity FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 MONTH;"
#     },
#     {
#         "input": "What was the maximum chlorine level recorded in the last 24 hours?",
#         "query": "SELECT MAX(Chlorine) AS MaxChlorine FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 DAY;"
#     },
#     {
#         "input": "How many times did the DC Voltage drop below 5V in the last week?",
#         "query": "SELECT COUNT(*) FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 WEEK AND `DC Voltgae` < 5;"
#     },
#     {
#         "input": "What was the running spring level at the last recorded time?",
#         "query": "SELECT `Running Spring Level` FROM `{table}` ORDER BY `DATE-TIME` DESC LIMIT 1;"
#     },
#     {
#         "input": "What is the total flow measured over the last month?",
#         "query": "SELECT SUM(`Total Flow`) AS TotalFlow FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 MONTH;"
#     },
#     {
#         "input": "What is the average drawdown for the last 24 hours?",
#         "query": "SELECT AVG(Draw Down) AS AverageDrawDown FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 DAY;"
#     },
#     {
#         "input": "List all records where the current status was 'Open' in the last 48 hours.",
#         "query": "SELECT * FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 2 DAY AND `Current` = 'Open';"
#     },
#     {
#         "input": "Provide the count of entries for each status of the main actuator fault in the last month.",
#         "query": "SELECT `Main Act Fault St`, COUNT(*) AS Count FROM `{table}` WHERE `DATE-TIME` >= NOW() - INTERVAL 1 MONTH GROUP BY `Main Act Fault St`;"
#     }
# ]


examples = [
    {
        "input": "What was the minimum Spring Level recorded in June 2024?",
        "query": """
        SELECT MIN(`Spring Level`) AS min_spring_level
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2024-06-01' AND '2024-06-30';
        """
    },
    {
        "input": "What was the average TW Rh for each day last month?",
        "query": """
        SELECT DATE(`DATE-TIME`) AS day, AVG(`TW Rh`) AS avg_tw_rh
        FROM table_name
        WHERE `DATE-TIME` BETWEEN CURDATE() - INTERVAL 1 MONTH AND CURDATE()
        GROUP BY day;
        """
    },
    {
        "input": "How much total water flowed through the system in the first quarter of 2024?",
        "query": """
        SELECT SUM(`Total Flow`) AS total_flow
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2024-01-01' AND '2024-03-31';
        """
    },
    {
        "input": "What was the peak Motor Frequency during the last weekend?",
        "query": """
        SELECT MAX(`Motor Frequency`) AS peak_motor_frequency
        FROM table_name
        WHERE `DATE-TIME` BETWEEN CURDATE() - INTERVAL WEEKDAY(CURDATE()) + 2 DAY AND CURDATE() - INTERVAL WEEKDAY(CURDATE()) - 1 DAY;
        """
    },
    {
        "input": "What is the total chlorine level recorded every week in the last 6 months?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%u') AS week, SUM(Chlorine) AS total_chlorine
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 6 MONTH
        GROUP BY week;
        """
    },
    {
        "input": "What is the average turbidity level recorded per month over the past year?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%m') AS month, AVG(Turbidity) AS avg_turbidity
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 1 YEAR
        GROUP BY month;
        """
    },
    {
        "input": "What was the total output DC voltage in May 2024?",
        "query": """
        SELECT SUM(`Output DC Voltage`) AS total_output_dc_voltage
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2024-05-01' AND '2024-05-31';
        """
    },
    {
        "input": "What was the highest PT recorded on the last day of each month in 2023?",
        "query": """
        SELECT DATE(`DATE-TIME`) AS last_day, MAX(PT) AS highest_pt
        FROM table_name
        WHERE `DATE-TIME` = LAST_DAY(`DATE-TIME`) AND YEAR(`DATE-TIME`) = 2023
        GROUP BY last_day;
        """
    },
    {
        "input": "What was the average TW St value every week for the past three months?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%u') AS week, AVG(`TW St`) AS avg_tw_st
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 3 MONTH
        GROUP BY week;
        """
    },
    {
        "input": "What was the sum of Flow Rate during the first week of August 2024?",
        "query": """
        SELECT SUM(`Flow Rate`) AS sum_flow_rate
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2024-08-01' AND '2024-08-07';
        """
    },
    {
        "input": "What was the maximum OHT Level observed every day during December 2023?",
        "query": """
        SELECT DATE(`DATE-TIME`) AS day, MAX(`OHT Level`) AS max_oht_level
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2023-12-01' AND '2023-12-31'
        GROUP BY day;
        """
    },
    {
        "input": "What was the total Draw Down for each month in the last year?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%m') AS month, SUM(`Draw Down`) AS total_draw_down
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 1 YEAR
        GROUP BY month;
        """
    },
    {
        "input": "What was the lowest Static Spring Level recorded last week?",
        "query": """
        SELECT MIN(`Static Spring Level`) AS min_static_spring_level
        FROM table_name
        WHERE `DATE-TIME` BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE();
        """
    },
    {
        "input": "What was the average Current for each hour on July 15, 2024?",
        "query": """
        SELECT HOUR(`DATE-TIME`) AS hour, AVG(`Current`) AS avg_current
        FROM table_name
        WHERE DATE(`DATE-TIME`) = '2024-07-15'
        GROUP BY hour;
        """
    },
    {
        "input": "What is the total chlorine level for each day over the past month?",
        "query": """
        SELECT DATE(`DATE-TIME`) AS day, SUM(Chlorine) AS total_chlorine
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 1 MONTH
        GROUP BY day;
        """
    },
    {
        "input": "What was the maximum Turbidity recorded each week in 2023?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%u') AS week, MAX(Turbidity) AS max_turbidity
        FROM table_name
        WHERE YEAR(`DATE-TIME`) = 2023
        GROUP BY week;
        """
    },
    {
        "input": "What was the total Total Flow for each month in 2024?",
        "query": """
        SELECT DATE_FORMAT(`DATE-TIME`, '%Y-%m') AS month, SUM(`Total Flow`) AS total_flow
        FROM table_name
        WHERE YEAR(`DATE-TIME`) = 2024
        GROUP BY month;
        """
    },
    {
        "input": "What is the average Running Spring Level for the last 5 days?",
        "query": """
        SELECT AVG(`Running Spring Level`) AS avg_running_spring_level
        FROM table_name
        WHERE `DATE-TIME` >= CURDATE() - INTERVAL 5 DAY;
        """
    },
    {
        "input": "What is the minimum Output DC Voltage recorded each hour on August 1, 2024?",
        "query": """
        SELECT HOUR(`DATE-TIME`) AS hour, MIN(`Output DC Voltage`) AS min_output_dc_voltage
        FROM table_name
        WHERE DATE(`DATE-TIME`) = '2024-08-01'
        GROUP BY hour;
        """
    },
    {
        "input": "What was the highest Flow Rate recorded for each day during the first week of July 2024?",
        "query": """
        SELECT DATE(`DATE-TIME`) AS day, MAX(`Flow Rate`) AS max_flow_rate
        FROM table_name
        WHERE `DATE-TIME` BETWEEN '2024-07-01' AND '2024-07-07'
        GROUP BY day;
        """
    }
]

   
   
sys_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query.
The MySQL Table is named '{table}' and has the following columns: DATE-TIME, TW St, TW Ol St, TW L_R, By Act Fault St, By Act Opn St, By Act Close St, Main Act Fault St, Main Act Open St, Mani Act Close St, Current, DC Voltage, Output DC Voltage, TW Rh, Running Spring Level, Static Spring Level, Draw Down, Total Flow, Turbidity, Chlorine.

Column descriptions with example values:

- DATE-TIME (DATETIME): Date and time, e.g., 2024-04-01 04:05:13.000
- TW St (VARCHAR): Status of the TW, e.g., Off, Normal
- TW Ol St (VARCHAR): TW Oil Status, e.g., Remote
- TW L_R (VARCHAR): TW L_R Status, e.g., Fault
- By Act Fault St (VARCHAR): By Act Fault Status, e.g., Fault
- By Act Opn St (VARCHAR): By Act Open Status, e.g., -
- By Act Close St (VARCHAR): By Act Close Status, e.g., Close
- Main Act Fault St (VARCHAR): Main Act Fault Status, e.g., Fault
- Main Act Open St (VARCHAR): Main Act Open Status, e.g., Open
- Mani Act Close St (VARCHAR): Mani Act Close Status, e.g., -
- Current (FLOAT): Current value, e.g., 0.0
- DC Voltage (FLOAT): DC Voltage, e.g., 0.0
- Output DC Voltage (FLOAT): Output DC Voltage, e.g., 0
- TW Rh (FLOAT): TW Relative Humidity, e.g., 0.00
- Running Spring Level (FLOAT): Running Spring Level, e.g., 6.60
- Static Spring Level (FLOAT): Static Spring Level, e.g., 5.38
- Draw Down (FLOAT): Draw Down, e.g., 0.00
- Total Flow (FLOAT): Total Flow, e.g., 0.0
- Turbidity (FLOAT): Turbidity, e.g., 0.0
- Chlorine (FLOAT): Chlorine, e.g., 0.0

**Instructions:**

- Always include the DATE-TIME column in the SELECT statement.
- Default to today's information if no specific date or time is mentioned.
- Use max(DATE-TIME) to get the current day.
- When needed, use SQL DATE functions like DATE_SUB(), DATE_ADD(), and DATEDIFF() to calculate dates.
- Utilize subqueries, GROUP BY, ORDER BY, etc., as necessary.
- Generate a syntactically correct SQL query that can be directly executed in Python.

**Note:**
- If the question is unrelated to the database, reply with "I don't know."
- If the question involves modifying or deleting the SQL table, reply with "I can't do that." You only have read-only permissions.
- Return only the SQL query without formatting it as ```sql```.

Below are several examples of questions and their corresponding SQL queries.

"""
#**Always use All possible and required columns in sql query. for example if question is 'give me health scores of high risk devices' then consider column Asset_Names also because it is related.**
 
 
 
 
 
 
 
answer_prompt = """Your task is to take the output generated by an SQL query and transform it into a user-friendly, well-structured response. The response should be clear, concise, and easy to read, presenting the information in a logical and organized manner.

Guidelines:

1. **Summarize the SQL Result**: Summarize the SQL result in an easy-to-understand manner.
2. **Use Lists for Clarity**: Present the data in a structured format for readability, using bullet points or numbered lists.
3. **Highlight Important Information**: Use bold formatting for important details.
4. **Ensure Completeness and Accuracy**: Cover all relevant data points from the SQL result.
5. **Exclude SQL Information**: Do not include any SQL-related information in the final answer. Only provide the processed results.

Columns and Example Values:
- **DATE-TIME**: Date and time, e.g., 2024-04-01 04:05:13.000
- **TW St**: Status of the TW, e.g., Off, Normal
- **TW Ol St**: TW Oil Status, e.g., Remote
- **TW L_R**: TW L_R Status, e.g., Fault
- **By Act Fault St**: By Act Fault Status, e.g., Fault
- **By Act Opn St**: By Act Open Status, e.g., -
- **By Act Close St**: By Act Close Status, e.g., Close
- **Main Act Fault St**: Main Act Fault Status, e.g., Fault
- **Main Act Open St**: Main Act Open Status, e.g., Open
- **Mani Act Close St**: Mani Act Close Status, e.g., -
- **Current**: Current value, e.g., 0.0
- **DC Voltage**: DC Voltage, e.g., 0.0
- **Output DC Voltage**: Output DC Voltage, e.g., 0
- **TW Rh**: TW Relative Humidity, e.g., 0.00
- **Running Spring Level**: Running Spring Level, e.g., 6.60
- **Static Spring Level**: Static Spring Level, e.g., 5.38
- **Draw Down**: Draw Down, e.g., 0.00
- **Total Flow**: Total Flow, e.g., 0.0
- **Turbidity**: Turbidity, e.g., 0.0
- **Chlorine**: Chlorine, e.g., 0.0

**Example Response Structure**:
1. **For a List of Fault Statuses**:
    - Fault statuses of the main actuator over the last 24 hours:<br><br>
    1. **Date-Time**: 2024-06-15 23:59:59<br>
       ● **Main Act Fault Status**: Fault<br><br>
    2. **Date-Time**: 2024-06-15 23:58:00<br>
       ● **Main Act Fault Status**: Fault<br><br>
    ...<br><br>
    (Include as many entries as needed, summarizing or listing all available data points)

2. **For Count Queries**:
    - The actuator fault status changed to 'Fault' **X** times in the last week.

3. **For Average Values**:
    - The average turbidity recorded over the last month is **Y**.

4. **For Maximum Values**:
    - The maximum chlorine level recorded in the last 24 hours is **Z**.

5. **For Specific Values at Last Recorded Time**:
    - The running spring level at the last recorded time was **V**.

Use the above guidelines to generate responses based on the SQL results provided.

**Do not include the dates provided in the SQL query result if they are wrong. Exclude them from the final answer.**
**If the SQL result is too long, you can summarize it but make sure that every detail of the provided columns is covered in the answer.**
**If the SQL result is empty or not provided, simply reply 'I don't have information about this. Please provide a relevant and clear question!'**

Question: {input}
SQL Query: {query}
SQL Result: {result}
Answer: """
