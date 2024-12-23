import traceback

import streamlit as st
import pymongo
from datetime import date

# Set Streamlit page config
st.set_page_config(
    page_title="Merry Christmas, babi boo!",
    page_icon="🎄",
    layout="centered",
)

# Use session state to track login status
if "login_status" not in st.session_state:
    st.session_state["login_status"] = False


def show_login_form():
    cols = st.columns([1, 5, 1])
    with cols[1]:
        st.header('Log in to see something special!')
        st.image('./images/mystery.gif')
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("See it now!")

    if login_button:
        if username == st.secrets['USERNAME'] and password == st.secrets['PASSWORD']:
            st.session_state["login_status"] = True
            st.rerun()
        else:
            st.error("Oh no it's not correct :( Please try again.")


def get_giftcards() -> list:
    """Fetch all giftcards from MongoDB, sorted by _id (optional)."""
    client = None
    try:
        client = pymongo.MongoClient(st.secrets['CONN_STRING'])
        db = client[st.secrets['DB_NAME']]
        giftcards_collection = db["giftcards"]
        return list(giftcards_collection.find().sort("_id"))
    except:
        traceback.print_exc()
        return []
    finally:
        if client:
            client.close()


def mark_giftcard_redeemed(card_id) -> bool:
    """Set 'redeemed' field to True for the specified card."""
    client = None
    try:
        client = pymongo.MongoClient(st.secrets['CONN_STRING'])
        db = client[st.secrets['DB_NAME']]
        giftcards_collection = db["giftcards"]
        giftcards_collection.update_one(
            {"_id": card_id},
            {"$set": {"redeemed": True}}
        )
        return True
    except:
        traceback.print_exc()
        return False
    finally:
        if client:
            client.close()


# def get_wishlist():
#     """Fetch all wishlist items from MongoDB, sorted by _id (optional)."""
#     return list(wishlist_collection.find().sort("_id"))
#
#
# def add_wish_to_wishlist(wish_text):
#     """Insert a new wish document into the wishlist collection."""
#     new_wish = {
#         "wish": wish_text,
#         "date_added": date.today().strftime("%B %d, %Y")
#     }
#     wishlist_collection.insert_one(new_wish)


# ---------------------------------------
# 3. STREAMLIT UI
# ---------------------------------------

# --- Title / Header ---
if not st.session_state['login_status']:
    show_login_form()
else:
    st.title("Merry Christmas, babi boo! 🎁❤️")
    st.subheader("Some special gift cards just for you...")
    st.image('./images/gift.gif')
    st.write(
        """
        This page is a special Christmas gift dedicated to you. 
        Below you will find gift cards you can redeem **anytime**. 
        Just hit the **"Redeem"** button, and I will fulfill your wish!
        """
    )

    # --- Retrieve Gift Cards from MongoDB ---
    gift_cards = get_giftcards()

    st.write("### Your Gift Cards")

    # --- Display each card ---
    for card in gift_cards:
        card_col1, card_col2 = st.columns([3, 1])

        with card_col1:
            st.markdown(f"**{card.get('title', 'Untitled')}**")
            st.write(card.get("description", "No description provided."))

        with card_col2:
            if card.get("redeemed", False):
                # If card is already redeemed, show a success label
                st.success("Redeemed!")
            else:
                # If not redeemed yet, show a redeem button
                if st.button("Redeem", key=str(card["_id"])):
                    mark_giftcard_redeemed(card["_id"])
                    st.rerun()  # Refresh the app so redeemed state is visible

        st.markdown("---")

    # --- Custom Wish Section ---
    # st.write("### Request a Custom Wish")
    # st.write(
    #     """
    #     Is there something else you want?
    #     Let me know below, and I'll add it to your personal wishlist!
    #     """
    # )
    #
    # # A small form to capture custom wishes
    # with st.form("wish_form"):
    #     wish = st.text_area("Describe your wish here")
    #     submit_wish = st.form_submit_button("Add to Wishlist")
    #
    #     if submit_wish and wish.strip():
    #         add_wish_to_wishlist(wish.strip())
    #         st.success("Your wish has been added to the wishlist!")
    #         st.experimental_rerun()  # Refresh to show the newly added wish
    #
    # # --- Display the custom wishlist ---
    # wishlist_items = get_wishlist()
    # if wishlist_items:
    #     st.write("### Your Wishlist:")
    #     for w in wishlist_items:
    #         st.markdown(f"- **{w['wish']}** (added on {w['date_added']})")

    st.write(" ")
    st.image('./images/santa.gif', use_container_width=True)
    st.header("**Merry Christmas! I love you!** 🎄✨")
    st.snow()
