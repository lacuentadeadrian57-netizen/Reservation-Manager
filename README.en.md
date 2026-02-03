***Python Reservation Manager***

Application developed in **Python 3** using **Streamlit** for managing reservations, resources and locations.
This project allows you to create, inspect, and manage reservations with restrictions and associated pricing

### Domain Chosen
The chosen domain is resource and location reservation management.
This domain was selected because it is widely applicable: from booking meeting rooms, coworking spaces, or sports facilities, to managing rentals of equipment or venues. It naturally involves time management, resource allocation, and pricing rules, making it ideal for demonstrating how Python can handle scheduling, restrictions, and persistence of data.

### Architecture
The Reservation Manager is centered on three pillars: events (reservations), resources (locations and resources), and restrictions. The restrictions are the most critical part of the system, ensuring that every reservation respects compatibility rules and resource availability.

1. Events (Reservations)
    Each reservation is an event that ties together:

        A location (e.g., “Conference Room A”).

        A time span (start and end dates).

        A set of resources: requisites (default) and optionals (chosen by the user).

    Reservations are validated against restrictions before being accepted.

Example:  
Reservation for Conference Room A from Jan 5–7 with requisites Table, Chairs and optional Projector.

2. Resources (Locations and Resources)

    Locations define:

        A base price.

        Corequisites: default resources that are always included.

        Optionals: resources that can be added by the user.

    Resources define:

        A name, quantity, and price.

        Exclusions: resources that cannot be combined with certain others.

Example:

    Location: Conference Room A → requisites: Table, Chairs; optionals: Projector, Speakers.

    Resource: Projector → price: $10/day; excludes: Outdoor Screen.

3. Restrictions (Core of the System)

Restrictions are the rules that guarantee valid reservations. They are actively managed by the system whenever a reservation is created, updated, or deleted.

    Mutual Exclusion Between Resources

        Certain resources cannot be used together.

        Example: Projector excludes Outdoor Screen.
        → If both are selected, the reservation is rejected.

    Corequisites Between Locations and Resources

        Each location requires specific resources by default.

        Example: Conference Room A always includes Table and Chairs.
        → These requisites are automatically added to every reservation for that location.

    Optional Resources With Restrictions

        Even optional resources can carry exclusions.

        Example: Speakers exclude Silent Mode Equipment.
        → If a user selects both, the reservation is invalid.

        This ensures that optional choices are flexible but still consistent with system rules.

    Date Validation

        Start date ≤ End date.

        Start date ≥ today.

        Example: Reserving from 2026‑01‑01 to 2025‑12‑31 → ❌ rejected.

    Resource Quantities

        Reservations cannot exceed available quantities.

        Example: Only 2 projectors exist; if 3 simultaneous reservations request them → ❌ rejected.

    Collision Handling

        Reservations for the same location cannot overlap.

        If overlap occurs, the system shifts the reservation forward to the next available slot.

        Example: Reservation A: Jan 5, 10:00–12:00. Reservation B requested for Jan 5, 11:00–13:00.
        → Reservation B is moved to start at 12:00.

### Prerequisites 
- Python 3.8+
- Libraries:
  - `streamlit`
  - `pandas`
  - `datetime` (comes with Python standard library, no installation needed)

### Features
- Create reservations with start/end dates
- Calculate total price automatically
- Inspect reservations in a table
- Edit locations and resources
- Delete reservations, locations, and resources
- Enforce restrictions (no overlaps, valid durations, capacity limits, opening hours)

### Installation and Execution

1. **Clone the repository**
   git clone https://github.com/lacuentadeadrian57-netizen/Reservation-Manager.git
   cd Reservation-Manager

2. **Create a virtual enviroment (recommended)**
    python3 -m venv enviroment
    source enviroment/bin/activate   # macOS/Linux
    enviroment\Scripts\activate      # Windows

3. **Install dependencies**
    pip install -r requirements.txt

4. **Run the application**
    python3 -m streamlit run main.py

5. **Open in browser**
    Streamlit will start a local server (default: http://localhost:8501).

    Navigate to the link to access the Reservation Manager interface


### Usage 
The Python Reservation Manager is a web application built with Streamlit that provides a simple interface for managing reservations, locations, and resources. The app is organized into five main sections, accessible from the sidebar navigation panel:

1. **Reservation Form**
    Allows users to create a new reservation by specifying:

        Start date and end date

        Location

        Optional resources

    Displays the default resources that are always included with the chosen location.

    Calculates and shows the total price, combining the base cost of the location with any optional resources selected.

    Each location has its own set of default resources and optional resources, ensuring flexibility in accommodations.

2. **Reservation Details**
    Provides a tabular view of all reservations created.

    Users can inspect reservation details such as ID, dates, location, resources, and price.

    Includes functionality to delete reservations when no longer needed.

3. **Edit Locations**
    Enables users to add new locations by specifying:

        Name

        Price

        Default resources (requisites)

        Optional resources

    Existing locations can be listed, inspected, updated (e.g., change price), or deleted.

    This section ensures that each location maintains a clear definition of what resources are required and what can be optionally added.

4. **Edit Resources**
    Allows users to manage the pool of resources available for reservations.

    Users can add new resources by specifying:

        Name

        Quantity available

        Price

        Exclusions (resources that cannot be combined with this one)

    Existing resources can be listed, inspected, updated (price and quantity), or deleted.

    The system enforces exclusion rules: if two resources that exclude each other are selected in the same reservation, the reservation cannot be created.

5. **Save and Load**
    Provides options to save the current state of the application (locations, resources, reservations) to a JSON file.

    Allows users to load data from a file to restore a previous state.

    This ensures persistence of data across sessions and makes it easy to share or back up configurations.



