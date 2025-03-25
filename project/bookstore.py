import streamlit as st
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import pandas as pd
import os

# ----- Domain Models -----
class State(ABC):
    @abstractmethod
    def status(self) -> str:
        pass

class Silver(State):
    def status(self) -> str:
        return "Silver"

class Gold(State):
    def status(self) -> str:
        return "Gold"

@dataclass
class Book:
    name: str
    price: float

@dataclass
class Customer:
    username: str
    password: str
    points: int = 0
    purchased_books: list[Book] = field(default_factory=list)

    @property
    def state(self) -> State:
        return Gold() if self.points >= 1000 else Silver()

    def buy(self, books: list[Book], redeem: bool = False) -> float:
        total_cost = sum(book.price for book in books)
        if redeem:
            redeem_value = min(self.points / 100, total_cost)
            total_cost -= redeem_value
            self.points -= int(redeem_value * 100)
        self.points += int(total_cost * 10)
        self.purchased_books.extend(books)
        return total_cost

@dataclass
class Owner:
    username: str = "admin"
    password: str = "admin"

    def login(self, user: str, pwd: str) -> bool:
        return self.username == user and self.password == pwd

# ----- Repository for Persistence -----
class Repository:
    def __init__(self, book_file: str, cust_file: str):
        self.book_file = book_file
        self.cust_file = cust_file
        self.books_df = pd.DataFrame(columns=["name", "price"])
        self.cust_df = pd.DataFrame(columns=["username", "password", "points"])
        self.load()

    def load(self):
        if os.path.exists(self.book_file):
            self.books_df = pd.read_csv(self.book_file, names=["name", "price"])
        if os.path.exists(self.cust_file):
            self.cust_df = pd.read_csv(self.cust_file, names=["username", "password", "points"])

    def save(self):
        self.books_df.to_csv(self.book_file, index=False, header=False)
        self.cust_df.to_csv(self.cust_file, index=False, header=False)

    def add_book(self, book: Book):
        new_row = pd.DataFrame([{"name": book.name, "price": book.price}])
        self.books_df = pd.concat([self.books_df, new_row], ignore_index=True)
        self.save()

    def delete_books(self, indices: list[int]):
        self.books_df = self.books_df.drop(indices).reset_index(drop=True)
        self.save()

    def add_customer(self, customer: Customer):
        new_row = pd.DataFrame([{"username": customer.username, "password": customer.password, "points": customer.points}])
        self.cust_df = pd.concat([self.cust_df, new_row], ignore_index=True)
        self.save()

    def delete_customers(self, indices: list[int]):
        self.cust_df = self.cust_df.drop(indices).reset_index(drop=True)
        self.save()

    def update_customer_points(self, username: str, points: int):
        idx = self.cust_df.index[self.cust_df.username == username]
        if not idx.empty:
            self.cust_df.at[idx[0], 'points'] = points
            self.save()

# ----- Streamlit Application -----
class BookstoreApp:
    def __init__(self):
        st.set_page_config(layout='wide')
        self.repo = Repository('books.txt', 'customers.txt')
        self.owner = Owner()
        self.current_customer: Customer | None = None
        self.run()

    def run(self):
        if 'page' not in st.session_state:
            st.session_state.page = 'login'
        # Call the function based on the current page.
        getattr(self, f"_{st.session_state.page}")()

    def _navigate(self, page: str):
        st.session_state.page = page
        # No explicit rerun needed; Streamlit will re-run on state change.

    def _login(self):
        st.title('Login')
        user = st.text_input('Username')
        pwd = st.text_input('Password', type='password')
        if st.button('Login'):
            if self.owner.login(user, pwd):
                self._navigate('owner_dashboard')
            else:
                match = self.repo.cust_df.query('username == @user and password == @pwd')
                if not match.empty:
                    points = int(match.points.iloc[0])
                    self.current_customer = Customer(user, pwd, points)
                    self._navigate('customer_dashboard')
                else:
                    st.error('Invalid credentials')

    def _owner_dashboard(self):
        st.title('Owner Dashboard')
        if st.button('Manage Books'):
            self._navigate('owner_books')
        if st.button('Manage Customers'):
            self._navigate('owner_customers')
        if st.button('Logout'):
            self._navigate('login')

    def _owner_books(self):
        st.title('Books Management')
        st.dataframe(self.repo.books_df)
        name = st.text_input('Name')
        price = st.number_input('Price', min_value=0.0)
        if st.button('Add Book'):
            self.repo.add_book(Book(name, price))
            # The script will re-run and show the updated table.
        sel = st.multiselect('Delete', list(self.repo.books_df.index))
        if st.button('Delete Book') and sel:
            self.repo.delete_books(sel)
        if st.button('Back'):
            self._navigate('owner_dashboard')

    def _owner_customers(self):
        st.title('Customers Management')
        st.dataframe(self.repo.cust_df)
        uname = st.text_input('Username')
        pwd = st.text_input('Password')
        if st.button('Add Customer'):
            self.repo.add_customer(Customer(uname, pwd))
        sel = st.multiselect('Delete', list(self.repo.cust_df.index))
        if st.button('Delete Customer') and sel:
            self.repo.delete_customers(sel)
        if st.button('Back'):
            self._navigate('owner_dashboard')

    def _customer_dashboard(self):
        cust = self.current_customer
        st.title(f"Welcome {cust.username} — Points: {cust.points}, Status: {cust.state.status()}")
        sel = st.multiselect('Select Books', list(self.repo.books_df.index), 
                             format_func=lambda i: f"{self.repo.books_df.at[i, 'name']} (${self.repo.books_df.at[i, 'price']})")
        if st.button('Buy'):
            self._finalize_purchase(sel, False)
        if st.button('Redeem & Buy'):
            self._finalize_purchase(sel, True)
        if st.button('Logout'):
            self._navigate('login')

    def _finalize_purchase(self, indices: list[int], redeem: bool):
        cust = self.current_customer
        books = [Book(row['name'], row['price']) for _, row in self.repo.books_df.loc[indices].iterrows()]
        cost = cust.buy(books, redeem)
        self.repo.delete_books(indices)
        self.repo.update_customer_points(cust.username, cust.points)
        st.write(f"Total Cost: ${cost:.2f}")
        st.write(f"Points: {cust.points}, Status: {cust.state.status()}")
        if st.button('Logout'):
            self._navigate('login')

if __name__ == '__main__':
    BookstoreApp()