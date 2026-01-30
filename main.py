#python3 -m streamlit run main.py
# UV python project manager 
import streamlit as st
import pandas as pd
from datetime import date
from manager import Manager

class App:
    def __init__(self):
        if "manager" not in st.session_state:
            st.session_state.page = "reserve"
            st.session_state.manager = Manager()
            st.session_state.manager.load("save.json")
        self._manager = st.session_state.manager

        if "reserve_start" not in st.session_state:
            st.session_state.reserve_start = date.today()
        if "reserve_end" not in st.session_state:
            st.session_state.reserve_end = date.today()
        if "reserve_location" not in st.session_state:
            st.session_state.reserve_location = None
        if "reserve_optionals" not in st.session_state:
            st.session_state.reserve_optionals = []

        if "locations_name" not in st.session_state:
            st.session_state.locations_name = None
        if "locations_price" not in st.session_state:
            st.session_state.locations_price = 0
        if "locations_requisites" not in st.session_state:
            st.session_state.locations_requisites = []
        if "locations_optionals" not in st.session_state:
            st.session_state.locations_optionals = []
        if "locations_location" not in st.session_state:
            st.session_state.locations_location = None

        st.set_page_config(
            page_title="Reservation Manager",   
            page_icon="📅",                     
            layout="wide",                      
            initial_sidebar_state="expanded"    
        )
        
    def render(self):
        st.sidebar.title("Navigation")
        if st.sidebar.button("Make reservation"):
            st.session_state.page = "reserve"
        if st.sidebar.button("Search details"):
            st.session_state.page = "inspect"
        if st.sidebar.button("Edit Locals"):
            st.session_state.page = "locations"
        if st.sidebar.button("Edit Resources"):
            st.session_state.page = "resources"
        if st.sidebar.button("Save and Load"):
            st.session_state.page = "data"

        if st.session_state.page == "reserve":
            self.reserve()
        elif st.session_state.page == "inspect":
            self.inspect()
        elif st.session_state.page == "locations":
            self.locations()
        elif st.session_state.page == "resources":
            self.resources()
        elif st.session_state.page == "data":
            self.data()

    def reserve(self):
        st.header("Make a new reservation")
        start = st.date_input("Start Date")
        end = st.date_input("End Date")
        location = st.selectbox(
                "Location",
                self._manager.locations,
            )
        if location:
            optionals = st.multiselect(
                    "Choose the optional resources",
                    self._manager.optionals[location]
                )
            st.write("Default Resources")
            for requisite in self._manager.requisites[location]:
                st.write(f"- {requisite}")
            price_value = self._manager.calculate_price(start, end, location, optionals)
            st.text_input("Total price", f"{price_value}", disabled=True)
            if st.button("Add Reservation"):
                succeeded, msg = self._manager.add_reservation(start, end, location, optionals)
                if succeeded:
                    st.success(msg)
                else:
                    st.error(msg)

    def inspect(self):
        st.header("Search details")
        if self._manager.reservations:
            df = pd.DataFrame(self._manager.reservations)
            st.dataframe(df)

            ids = []
            for r in self._manager.reservations:
                ids.append(r["ID"])

            selected_id = st.selectbox(
                "Select a reservation to view details",
                ids
            )
    
            selected = self._manager.id_map[selected_id]

            #start = st.date_input("Start Date", value=selected['start'])
            #end = st.date_input("End Date", value=selected['end'])

            if selected:
                st.subheader("Reservation Details")
                st.write(f"**ID:** {selected['ID']}")
                st.write(f"**Start Date:** {selected['start']}")
                st.write(f"**End Date** {selected['end']}")
                st.write(f"**Location** {selected['location']}")
                st.write(f"**Requires:** {", ".join(self._manager.requisites[selected['location']])}") 
                st.write(f"**Price:** : {self._manager.calculate_price(
                    selected["start"],
                    selected["end"],
                    selected["location"],
                    selected["optionals"]
                )}")

            if st.button("Delete Reservation"):
                self._manager.delete_reservation(selected_id)
                st.warning("Reservation deleted!")
                st.rerun()
        else:
            st.info("No reservations yet.")

    def locations(self):
        st.header("Edit locations")
        data = []
        for location in self._manager.locations:
            data.append(
                    {
                        "location": location,
                        "price": self._manager.price[location],
                    }
                )

        with st.form("Add location"):
            name = st.text_input("Location Name")
            price = st.number_input("Price", min_value=0, step=1)
            requisites = st.multiselect(
                "Requisites",
                self._manager.resources
            )
            optionals = st.multiselect(
                "Optionals",
                self._manager.resources
            )

            add = st.form_submit_button("Add location")
            if add:
                succeeded, msg = self._manager.add_location(name, price, requisites, optionals)
                if succeeded:
                    st.success(msg)
                else:
                    st.error(msg)
                st.rerun()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            location = st.selectbox(
                "Select a location to view details",
                self._manager.locations
            )

            price = st.number_input("Price", 0, step=1, value=self._manager.price[location])
            if price != self._manager.price[location]:
                self._manager.update_price(location, price)
                st.rerun()

            related = []
            for required in self._manager.requisites[location]:
                related.append( 
                        {
                            "resource" : required,
                            "relation" : "required"
                        }
                    )
            for optional in self._manager.optionals[location]:
                related.append(
                        {
                            "resource" : optional,
                            "relation" : "optional"
                        }
                    )
                
            df = pd.DataFrame(related)
            st.dataframe(df)

            if st.button("Delete location"):
                self._manager.delete_location(location)
                st.rerun()

    def resources(self):
        st.header("Edit resources")
        data = []
        for resource in self._manager.resources:
            data.append(
                    {
                        "resource": resource,
                        "quantity": self._manager.quantity[resource],
                        "price": self._manager.price[resource],
                    }
                )
        with st.form("Add resource"):
            name = st.text_input("Resource Name")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0, step=1)
            exclusions = st.multiselect("Exclusions", self._manager.resources)

            add = st.form_submit_button("Add resource")
            if add:
                succeeded, msg = self._manager.add_resource(name, quantity, price, exclusions)
                if succeeded:
                    st.success(msg)
                else:
                    st.error(msg)
                st.rerun()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            resource = st.selectbox(
                "Select a resource to view details",
                self._manager.resources
            )

            price = st.number_input("Price", 0, step=1, value=self._manager.price[resource])
            if price != self._manager.price[resource]:
                self._manager.update_price(resource, price)
                st.rerun()

            quantity = st.number_input("Quantity", 1, step=1, value=self._manager.quantity[resource])
            if quantity != self._manager.quantity[resource]:
                self._manager.update_quantity(resource, quantity)
                st.rerun()
            
            exclusions = []
            for exclusion in self._manager.exclusions[resource]:
                exclusions.append( 
                        {
                            "resource" : exclusion,
                            "relation" : "exclusion"
                        }
                    )
            if len(exclusions) > 0:
                df = pd.DataFrame(exclusions)
                st.dataframe(df)

            if st.button("Delete Resource"):
                self._manager.delete_resource(resource)
                st.rerun()

    def data(self):
        load_filename = st.text_input("Load filename", value="save.json")
        if st.button("Load file"):
            succeded = self._manager.load(load_filename)
            if succeded:
                st.success("Succeded to load file")
            else:
                st.error("Failed to load file")

        
        save_filename = st.text_input("Save filename", value="save.json")
        if st.button("Save to file"):
            succeded = self._manager.save(save_filename)
            if succeded:
                st.success("Succeded to save file")
            else:
                st.error("Failed to save file")

if __name__ == "__main__":
    app = App()
    app.render()
