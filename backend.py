import csv
import tkinter as tk
import mysql.connector
import websockets
import asyncio
import json
import os

# Tkinter setup
root = tk.Tk()
root.title("Execution Results")
text_area = tk.Text(root)
text_area.pack()

def log(message):
    text_area.insert(tk.END, message + "\n")

def fetch_from_db(column_name):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Update with your credentials
            password="",      # Update with your password
            database="db"  # Match your DB name
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column_name} FROM test_table")
        return cursor.fetchall()
    except Exception as e:
        log(f"Database error: {str(e)}")
        return None

# WebSocket client
async def send_status(websocket, status_data):
    await websocket.send(json.dumps(status_data))

# CSV processing (without websocket parameter)
async def process_csv():
    statuses = []
    csv_path = os.path.join(os.path.dirname(__file__), 'csv_output', 'blocks.csv')
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row['type'] == 'database_fetch':
                    table = json.loads(row['params'])['TAG']
                    data = fetch_from_db(table)
                    log(f"Fetched {len(data)} rows from {table}")
                    statuses.append({'id': row['id'], 'status': 'success'})
                elif row['type'] == 'controls_if':
                    statuses.append({'id': row['id'], 'status': 'success'})
            except Exception as e:
                log(f"Error in block {row['id']}: {str(e)}")
                statuses.append({'id': row['id'], 'status': 'error'})
    return statuses

# Main execution
async def main():
    # Process the CSV file first
    statuses = await process_csv()
    
    # Then establish the WebSocket connection to send the statuses
    async with websockets.connect('ws://localhost:8765') as websocket:
        await send_status(websocket, statuses)
    
    root.mainloop()

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
