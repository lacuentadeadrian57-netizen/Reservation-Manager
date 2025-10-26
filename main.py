#python3 -m streamlit run script.py
# UV python project manager 
import streamlit as st
import pandas as pd
from datetime import date
from manager import Manager

class App:
    def __init__(self):
        if "manager" not in st.session_state:
            st.session_state.page = "form"
            st.session_state.manager = Manager()
            st.session_state.manager.load("save.json")
        self.manager = st.session_state.manager
        st.set_page_config(
            page_title="Reservation Manager",   
            page_icon="📅",                     
            layout="wide",                      
            initial_sidebar_state="expanded"    
        )
        
    def render(self):
        st.sidebar.title("Navigation")
        if st.sidebar.button("Make reservation"):
            st.session_state.page = "form"
        if st.sidebar.button("Search details"):
            st.session_state.page = "details"
        if st.sidebar.button("Edit Locals"):
            st.session_state.page = "locals"
        if st.sidebar.button("Edit Resources"):
            st.session_state.page = "resources"

        if st.session_state.page == "form":
            self.form()
        elif st.session_state.page == "details":
            self.details()
        elif st.session_state.page == "locals":
            self.locals()
        elif st.session_state.page == "resources":
            self.resources()

    def form(self):
        st.header("Make a new reservation")
        start = st.date_input("Start Date")
        end = st.date_input("End Date")
        location = st.selectbox("Location", self.manager.locations)
        optionals = st.multiselect("Choose the optional resources", self.manager.optionals[location])
        
        st.write("Default Resources")
        for requisite in self.manager.requisites[location]:
            st.write(f"- {requisite}")

        price_value = self.manager.calculate_price(start, end, location, optionals)
        st.text_input("Total price", f"{price_value}", disabled=True)

        if st.button("Add Reservation"):
            succeeded, msg = self.manager.add_reservation(start, end, location, optionals)
            if succeeded:
                st.success(msg)
            else:
                st.error(msg)
   
    def details(self):
        st.header("Search details")
        if self.manager.reservations:
            df = pd.DataFrame(self.manager.reservations)
            st.dataframe(df)

            ids = []
            for r in self.manager.reservations:
                ids.append(r["ID"])

            selected_id = st.selectbox(
                "Select a reservation to view details",
                ids
            )

            selected = self.manager.id_map[selected_id]
            if selected:
                st.subheader("Reservation Details")
                st.write(f"**ID:** {selected['ID']}")
                st.write(f"**Start Date:** {selected['start']}")
                st.write(f"**End Date** {selected['end']}")
                st.write(f"**Location** {selected['location']}")
                st.write(f"**Requires:** {", ".join(self.manager.requisites[selected['location']])}") 
                st.write(f"**Price:** : {self.manager.calculate_price(
                    selected["start"],
                    selected["end"],
                    selected["location"],
                    selected["optionals"]
                )}")

            if st.button("Delete Reservation"):
                self.manager.delete_reservation(selected_id)
                st.warning("Reservation deleted!")
                st.rerun()
        else:
            st.info("No reservations yet.")

    def locals(self):
        data = []
        for location in self.manager.locations:
            data.append(
                {
                    "location": location,
                    "price": self.manager.price[location],
                }
            )
        with st.form("Add location"):
            name = st.text_input("Location Name")
            price = st.number_input("Price", min_value=0, step=1)
            requisites = st.multiselect("Requisites", self.manager.resources)
            optionals = st.multiselect("Optionals", self.manager.resources)

            add = st.form_submit_button("Add location")
            if add:
                succeeded, msg = self.manager.add_location(name, price, requisites, optionals)
                if succeeded:
                    st.success(msg)
                else:
                    st.error(msg)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            location = st.selectbox(
                "Select a location to view details",
                self.manager.locations
            )

            related = []
            for required in self.manager.requisites[location]:
                related.append(
                    {
                        "resource" : required,
                        "relation" : "required"
                    }
                )
            for optional in self.manager.optionals[location]:
                related.append(
                    {
                        "resource" : optional,
                        "relation" : "optional"
                    }
                )
            df = pd.DataFrame(related)
            st.dataframe(df)

            if st.button("Delete location"):
                st.warning("⚠️ Warning: Deleting this location may also remove any reservations that depend on it.")
                if st.button("Confirm"):
                    self.manager.delete_location(location)

    def resources(self):
        data = []
        for resource in self.manager.resources:
            data.append(
                {
                    "resource": resource,
                    "quantity": self.manager.quantity[resource],
                    "price": self.manager.price[resource],
                }
            )
        with st.form("Add resource"):
            name = st.text_input("Resource Name")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0, step=1)

            add = st.form_submit_button("Add resource")
            if add:
                succeeded, msg = self.manager.add_resource(name, quantity, price)
                if succeeded:
                    st.success(msg)
                else:
                    st.error(msg)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            resource = st.selectbox(
                "Select a resource to view details",
                self.manager.resources
            )
            if st.button("Delete Resource"):
                st.warning("⚠️ Warning: Deleting this resource may also remove any reservations that depend on it.")
                if st.button("Confirm"):
                    self.manager.delete_resource(resource)
            
            



if __name__ == "__main__":
    app = App()
    app.render()
