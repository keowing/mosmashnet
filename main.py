import json
from datetime import datetime

def process_tournament_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        keywords = ["ultimate singles", "ssbu singles"]
        regions = data.get("data", {})
        
        # Define table column widths
        w_name = 40
        w_slug = 25
        w_loc = 25
        w_date = 8
        w_entrants = 15
        
        # Table Header
        header = (f"{'Tournament Name':<{w_name}} | {'Slug':<{w_slug}} | "
                  f"{'Location':<{w_loc}} | {'Date':<{w_date}} | "
                  f"{'Entrants':<{w_entrants}} | {'Profile Image URL'}")
        print(header)
        print("-" * (len(header) + 50)) # Extra length for the URL
        
        for region_data in regions.values():
            for tournament in region_data.get("nodes", []):
                for event in tournament.get("events", []):
                    event_name = event.get("name", "").lower()
                    
                    if any(kw in event_name for kw in keywords):
                        # 1. Basic Data
                        name = tournament.get("name", "N/A")
                        slug = tournament.get("slug", "").replace('tournament', '')
                        location = f"{tournament.get('city')}, {tournament.get('addrState')}"
                        entrants = f"{event.get('numEntrants')} Entrants"
                        
                        # 2. Date Formatting
                        start_ts = tournament.get("startAt")
                        date_str = datetime.fromtimestamp(start_ts).strftime('%m/%d') if start_ts else "N/A"
                        
                        # 3. Profile Image Extraction
                        profile_url = "No Image"
                        for img in tournament.get("images", []):
                            if img.get("type") == "profile":
                                profile_url = img.get("url")
                                break
                        
                        # 4. Print aligned row
                        print(f"{name:<{w_name}} | {slug:<{w_slug}} | "
                              f"{location:<{w_loc}} | {date_str:<{w_date}} | "
                              f"{entrants:<{w_entrants}} | {profile_url}")
                        
                        break
                        
    except FileNotFoundError:
        print(f"Error: '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")

if __name__ == "__main__":
    process_tournament_data("json.txt")