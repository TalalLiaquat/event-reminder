#!/usr/bin/env python3
import json
import os
from datetime import datetime

class EventReminder:
    def __init__(self):
        self.events = []
        self.next_id = 1

    def _parse_date(self, date_str):
        for fmt in ("%Y-%m-%d",): 
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt
            except ValueError:
                continue
        raise ValueError("Invalid date format! Please use YYYY-MM-DD")

    def add_event(self, title, date_str, description=""):
        dt = self._parse_date(date_str)
        event = {
            "id": self.next_id,
            "title": title.strip(),
            "date": dt.strftime("%Y-%m-%d"),
            "description": description.strip()
        }
        self.events.append(event)
        self.events.sort(key=lambda e: self._parse_date(e["date"]))
        self.next_id += 1
        return event

    def get_upcoming_events(self, now=None):
        if now is None:
            now = datetime.now()
        upcoming = [e for e in self.events if self._parse_date(e["date"]) >= now]
        upcoming.sort(key=lambda e: self._parse_date(e["date"]))
        return upcoming

    def delete_past_events(self, now=None):
        if now is None:
            now = datetime.now()
        self.events = [e for e in self.events if self._parse_date(e["date"]) >= now]

    def export_to_txt(self, path):
        with open(path, "w", encoding="utf-8") as f:
            if not self.events:
                f.write("No events.\n")
                return path
            f.write("Event List\n")
            f.write("="*60 + "\n")
            for e in self.events:
                f.write(f"ID: {e['id']}\n")
                f.write(f"Title: {e['title']}\n")
                f.write(f"Date: {e['date']}\n")
                f.write(f"Description: {e['description']}\n")
                f.write("-"*60 + "\n")
        return path

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
        return path

    def load_from_file(self, path):
        if not os.path.exists(path):
            return 0
        with open(path, "r", encoding="utf-8") as f:
            self.events = json.load(f)
        if self.events:
            self.next_id = max(e["id"] for e in self.events) + 1
        else:
            self.next_id = 1
        self.events.sort(key=lambda e: self._parse_date(e["date"]))
        return len(self.events)

    def remove_event_by_id(self, event_id):
        before = len(self.events)
        self.events = [e for e in self.events if str(e["id"]) != str(event_id)]
        return before - len(self.events)

    def pretty_print(self, events=None):
        if events is None:
            events = self.events
        if not events:
            print("No events found.")
            return
        print("\n{:<5} | {:<20} | {:<12} | {:<30}".format("ID", "Title", "Date", "Description"))
        print("-"*75)
        for e in events:
            print("{:<5} | {:<20} | {:<12} | {:<30}".format(
                e['id'], e['title'], e['date'], e['description']
            ))

def main():
    reminder = EventReminder()
    data_file = "events.json"
    reminder.load_from_file(data_file)

    while True:
        print("\nEvent Reminder Menu")
        print("1. Add event")
        print("2. Show upcoming events")
        print("3. Delete past events now")
        print("4. Export events to .txt")
        print("5. Save events to file")
        print("6. Load events from file")
        print("7. Delete an event by ID")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            while True: 
                title = input("Title: ").strip()
                date_str = input("Date (YYYY-MM-DD): ").strip()
                description = input("Description (optional): ").strip()

                try:
                    reminder.add_event(title, date_str, description)
                    print("Event added")
                except Exception as e:
                    print("Error:", e)
                    print("Please try again.\n")
                    continue 

                again = input("Would you like to add another event? (y/n): ").strip().lower()
                if again != "y":
                    break

        elif choice == "2":
            reminder.delete_past_events()
            upcoming = reminder.get_upcoming_events()
            print("\nUpcoming events:")
            reminder.pretty_print(upcoming)

        elif choice == "3":
            reminder.delete_past_events()
            print("Past events deleted (if any).")

        elif choice == "4":
            path = input("Enter filename (default: events_export.txt): ").strip() or "events_export.txt"
            reminder.export_to_txt(path)
            print("Exported to", path)

        elif choice == "5":
            path = input("Enter filename to save (default: events.json): ").strip() or "events.json"
            reminder.save_to_file(path)
            print("Saved to", path)

        elif choice == "6":
            path = input("Enter filename to load (default: events.json): ").strip() or "events.json"
            count = reminder.load_from_file(path)
            print(f"Loaded {count} events from", path)

        elif choice == "7":
            eid = input("Enter event ID to delete: ").strip()
            removed = reminder.remove_event_by_id(eid)
            print(f"Removed {removed} event(s).")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
