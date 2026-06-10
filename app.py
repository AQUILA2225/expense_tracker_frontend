import streamlit as st 
import requests
import pandas as pd 

server = "http://127.0.0.1:8000"

st.title("Expense Tracker App")

menu=st.sidebar.selectbox(
    "Select Option",
    [
        "Add Expense",
        "View Expense",
        "Update Expense",
        "Delete Expense",
        "Expense Summary"
    ]
)

if menu == "Add Expense":
    st.header("Add Expense")
    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=1.0)
    category = st.selectbox(
        "Category",
        [
            "Food", "Travel","Shopping","Bills","Entertainment","Others"
        ]
    )
    
    payment_method = st.selectbox(
        "Payment Method",
        ["Cash","UPI","Card","Net Banking"]
    )
    expense_date = st.date_input("Expense Date")
    description = st.text_input("Description")
    
    if st.button("Add Expense"):
        payload = {
            "title": title,
            "amount": amount,
            "category": category,
            "payment_method": payment_method,
            "expense_date": str(expense_date),
            "description": description
        }
        
        response = requests.post(f"{server}/add_expense",json=payload)
        
        st.success(response.json()["message"])
        
elif menu == "View Expense":
    st.header("All Expenses")
    
    response = requests.get(f"{server}/get_expenses")
    
    data = response.json()["expenses"]
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
        total=df["amount"].sum()
        st.subheader(f"Total Expenses: RS {total}")
    else:
        st.warning("No Expenses Found")
        

elif menu == "Update Expense":

    st.header("Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        step=1
    )

    title = st.text_input("New Title")

    amount = st.number_input(
        "New Amount",
        min_value=1
    )

    category = st.selectbox(
        "New Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    expense_date = st.date_input("New Expense Date")

    if st.button("Update Expense"):

        data = {
            "title": title,
            "amount": amount,
            "category": category,
            "expense_date": str(expense_date)
        }

        response = requests.put(
            f"{server}/update_expense/{expense_id}",
            json=data
        )

        st.success(response.json()["message"])
        
elif menu == "View Expenses":

    st.header("All Expenses")

    response = requests.get(
        f"{server}/get_expenses"
    )

    data = response.json()["expenses"] # list of dict 
    # st.write(data)
    if data:

        df = pd.DataFrame(data)

        st.dataframe(df)

        total = df["amount"].sum()

        st.subheader(f"Total Expense: ₹ {total}")

    else:
        st.warning("No Expenses Found")

elif menu == "Delete Expense":

    st.header("Delete Expense")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        response = requests.delete(
            f"{server}/delete_expense/{expense_id}"
        )

        st.success(response.json()["message"])
        
elif menu == "Expense Summary":

    st.header("Expense Summary By Category")

    try:

        response = requests.get(
            f"{server}/expense_summary"
        )

        data = response.json()["summary"]

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df)

            st.bar_chart(
                df.set_index("category")
            )

        else:

            st.warning("No Data Found")

    except Exception as e:

        st.error(str(e))