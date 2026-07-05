import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* ===========================
GLOBAL
=========================== */

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

.stApp{
    background: linear-gradient(135deg,#0F172A,#111827);
    color:white;
}

/* ===========================
HERO
=========================== */

.hero{

background:linear-gradient(
90deg,
#16A34A,
#22C55E
);

padding:35px;

border-radius:20px;

box-shadow:0px 10px 25px rgba(0,0,0,.30);

margin-bottom:20px;

}

.hero h1{

font-size:48px;

font-weight:700;

color:white;

margin-bottom:8px;

}

.hero p{

font-size:18px;

color:white;

opacity:.9;

}


/* ===========================
METRIC CARDS
=========================== */

.metric-card{

background:#1E293B;

padding:22px;

border-radius:18px;

text-align:center;

border:1px solid #334155;

transition:.3s;

}

.metric-card:hover{

transform:translateY(-5px);

border:1px solid #22C55E;

box-shadow:0px 10px 20px rgba(34,197,94,.25);

}

.metric-title{

font-size:18px;

color:#CBD5E1;

}

.metric-value{

font-size:34px;

font-weight:bold;

color:white;

}


/* ===========================
RECOMMENDATION CARD
=========================== */

.food-card{

background:#1E293B;

padding:20px;

border-radius:20px;

margin-bottom:18px;

border-left:6px solid #22C55E;

box-shadow:0px 5px 18px rgba(0,0,0,.25);

}

.food-card:hover{

transform:scale(1.02);

transition:.3s;

}

.food-title{

font-size:28px;

font-weight:bold;

color:white;

margin-bottom:10px;

}

.food-info{

font-size:16px;

line-height:1.8;

color:#CBD5E1;

}


/* ===========================
SIDEBAR
=========================== */

section[data-testid="stSidebar"]{

background:#111827;

}


/* ===========================
BUTTON
=========================== */

.stButton>button{

width:100%;

height:55px;

font-size:18px;

font-weight:bold;

border-radius:14px;

background:#16A34A;

color:white;

border:none;

}

.stButton>button:hover{

background:#22C55E;

}


/* ===========================
FOOTER
=========================== */

.footer{

text-align:center;

padding:25px;

color:#94A3B8;

font-size:14px;

}


/* ===========================
HIDE STREAMLIT
=========================== */

#MainMenu{

visibility:hidden;

}

footer{

visibility:hidden;

}


</style>

""",
        unsafe_allow_html=True
    )