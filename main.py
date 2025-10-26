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
        if st.session_state.page == "form":
            self.form()
        elif st.session_state.page == "details":
            self.details()

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



if __name__ == "__main__":
    app = App()
    app.render()
