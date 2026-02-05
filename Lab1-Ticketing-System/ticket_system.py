import json
import datetime
import os

class Ticket:
    def __init__(self, ticket_id, title, description, priority, category, requester):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.status = "Open"
        self.requester = requester
        self.assigned_to = None
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = self.created_at
        self.resolution = None
        self.notes = []

    def to_dict(self):
        return {
            'ticket_id': self.ticket_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'status': self.status,
            'requester': self.requester,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'resolution': self.resolution,
            'notes': self.notes
        }
    
class TicketingSystem:
    def __init__(self, filename='tickets.json'):
        self.filename = filename
        self.tickets = []
        self.load_tickets()

    def load_tickets(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tickets = data
        else:
            self.tickets = []

    def save_tickets(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tickets, f, indent=4)

    def create_ticket(self, title, description, priority, category, requester):
        ticket_id = len(self.tickets) + 1
        ticket = Ticket(ticket_id, title, description, priority, category, requester)
        self.tickets.append(ticket.to_dict())
        self.save_tickets()
        print(f"\n✓ Ticket #{ticket_id} created successfully!")
        return ticket_id

    def view_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                print("\n" + "="*60)
                print(f"Ticket #{ticket['ticket_id']}: {ticket['title']}")
                print("="*60)
                print(f"Status: {ticket['status']}")
                print(f"Priority: {ticket['priority']}")
                print(f"Category: {ticket['category']}")
                print(f"Requester: {ticket['requester']}")
                print(f"Assigned To: {ticket['assigned_to'] or 'Unassigned'}")
                print(f"Created: {ticket['created_at']}")
                print(f"\nDescription:\n{ticket['description']}")
                if ticket['notes']:
                    print(f"\nNotes:")
                    for note in ticket['notes']:
                        print(f"  - {note}")
                if ticket['resolution']:
                    print(f"\nResolution:\n{ticket['resolution']}")
                print("="*60 + "\n")
                return ticket
        print(f"\n✗ Ticket #{ticket_id} not found.")
        return None

    def list_tickets(self, status=None):
        filtered = self.tickets
        if status:
            filtered = [t for t in filtered if t['status'] == status]
        
        if not filtered:
            print("\nNo tickets found.")
            return
        
        print("\n" + "="*90)
        print(f"{'ID':<5} {'Title':<35} {'Priority':<12} {'Status':<12} {'Category':<15}")
        print("="*90)
        for ticket in filtered:
            print(f"{ticket['ticket_id']:<5} {ticket['title'][:33]:<35} "
                  f"{ticket['priority']:<12} {ticket['status']:<12} {ticket['category']:<15}")
        print("="*90 + "\n")
        
    def update_status(self, ticket_id, new_status):
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                ticket['status'] = new_status
                ticket['updated_at'] = datetime.datetime.now().isoformat()
                self.save_tickets()
                print(f"\n✓ Ticket #{ticket_id} status updated to '{new_status}'")
                return True
        print(f"\n✗ Ticket #{ticket_id} not found.")
        return False

    def assign_ticket(self, ticket_id, technician):
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                ticket['assigned_to'] = technician
                ticket['updated_at'] = datetime.datetime.now().isoformat()
                self.save_tickets()
                print(f"\n✓ Ticket #{ticket_id} assigned to {technician}")
                return True
        print(f"\n✗ Ticket #{ticket_id} not found.")
        return False

    def add_note(self, ticket_id, note):
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                ticket['notes'].append(f"[{timestamp}] {note}")
                ticket['updated_at'] = datetime.datetime.now().isoformat()
                self.save_tickets()
                print(f"\n✓ Note added to ticket #{ticket_id}")
                return True
        print(f"\n✗ Ticket #{ticket_id} not found.")
        return False

    def resolve_ticket(self, ticket_id, resolution):
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                ticket['resolution'] = resolution
                ticket['status'] = 'Resolved'
                ticket['updated_at'] = datetime.datetime.now().isoformat()
                self.save_tickets()
                print(f"\n✓ Ticket #{ticket_id} resolved!")
                return True
        print(f"\n✗ Ticket #{ticket_id} not found.")
        return False
    
def main():
    system = TicketingSystem()
    
    while True:
        print("\n╔════════════════════════════════════════╗")
        print("║   IT HELPDESK TICKETING SYSTEM        ║")
        print("╚════════════════════════════════════════╝")
        print("1. Create New Ticket")
        print("2. View Ticket")
        print("3. List All Tickets")
        print("4. Update Ticket Status")
        print("5. Assign Ticket")
        print("6. Add Note to Ticket")
        print("7. Resolve Ticket")
        print("8. Exit")
        print("─"*42)
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice == '1':
            print("\n--- Create New Ticket ---")
            title = input("Title: ")
            description = input("Description: ")
            print("\nPriority: 1=Low, 2=Medium, 3=High, 4=Critical")
            priority_input = input("Select priority (1-4): ")
            priority_map = {'1': 'Low', '2': 'Medium', '3': 'High', '4': 'Critical'}
            priority = priority_map.get(priority_input, 'Medium')
            
            print("\nCategory: 1=Hardware, 2=Software, 3=Network, 4=Access")
            category_input = input("Select category (1-4): ")
            category_map = {'1': 'Hardware', '2': 'Software', '3': 'Network', '4': 'Access'}
            category = category_map.get(category_input, 'General')
            
            requester = input("Requester name: ")
            system.create_ticket(title, description, priority, category, requester)
        
        elif choice == '2':
            try:
                ticket_id = int(input("\nEnter ticket ID: "))
                system.view_ticket(ticket_id)
            except ValueError:
                print("\n✗ Invalid ticket ID")
        
        elif choice == '3':
            print("\nFilter by status? (Leave blank for all)")
            print("Options: Open, In Progress, Resolved, Closed")
            status_filter = input("Status: ").strip() or None
            system.list_tickets(status=status_filter)
        
        elif choice == '4':
            try:
                ticket_id = int(input("\nEnter ticket ID: "))
                print("Status options: Open, In Progress, Resolved, Closed")
                new_status = input("New status: ")
                system.update_status(ticket_id, new_status)
            except ValueError:
                print("\n✗ Invalid ticket ID")
        
        elif choice == '5':
            try:
                ticket_id = int(input("\nEnter ticket ID: "))
                technician = input("Assign to: ")
                system.assign_ticket(ticket_id, technician)
            except ValueError:
                print("\n✗ Invalid ticket ID")
        
        elif choice == '6':
            try:
                ticket_id = int(input("\nEnter ticket ID: "))
                note = input("Note: ")
                system.add_note(ticket_id, note)
            except ValueError:
                print("\n✗ Invalid ticket ID")
        
        elif choice == '7':
            try:
                ticket_id = int(input("\nEnter ticket ID: "))
                resolution = input("Resolution: ")
                system.resolve_ticket(ticket_id, resolution)
            except ValueError:
                print("\n✗ Invalid ticket ID")
        
        elif choice == '8':
            print("\nThank you for using the IT Helpdesk Ticketing System!")
            break
        
        else:
            print("\n✗ Invalid option. Please select 1-8.")

if __name__ == "__main__":
    main()