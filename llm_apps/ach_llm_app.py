#!/usr/bin/env python3

import re
import streamlit as st
from dotenv import load_dotenv
from os import getenv
from openai import OpenAI


# Load environment variables
load_dotenv("./secret.env")

# Initialise API key and BASE_URL
API_KEY = getenv("OPENROUTER_API_KEY")
BASE_URL = getenv("OPENROUTER_BASE_URL")

# Set up OpenAI API key
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


# Function to generate initial hypotheses based on a given context
def generate_initial_hypotheses(context):
    prompt = f"""
    Based on the following threat context, generate plausible hypotheses for potential threats:

    Context: {context}

    List at least three hypotheses that could explain potential threats, considering different actors, methods, and motives.
    Return only the hypotheses, following strictly this schema:

    **H1:** Hypothesis 1 here.
    **H2:** Hypothesis 2 here.
    **H3:** Hypothesis 3 here.
    Et cetera.
    """
    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


# Function to generate evidence suggestions based on provided hypotheses
def generate_evidence_for_hypotheses(hypotheses):
    prompt = f"""
    Based on the following threat hypotheses, suggest relevant pieces of evidence that could either support or refute each hypothesis.

    Hypotheses:
    {hypotheses}

    Provide a list of evidence items relevant to each hypothesis.
    Do not say anything, just list the evidence.
    Please list each evidence item on a separate line, starting with a label (e.g., E1, E2, etc.). Return only the evidence items in this exact format:

    **H1**

    E1-1: Evidence 1 here.
    E1-2: Evidence 2 here.
    E1-3: Evidence 3 here.

    **H2**

    E2-1: Evidence 1 here.
    E2-2: Evidence 2 here.
    Et cetera.
    """
    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.6,
    )
    return response.choices[0].message.content.strip()


# Function for performing ACH analysis
def perform_ach_analysis(hypotheses, evidence_list, evidence_consistency):
    evidence_analysis = "\n".join(
        [f"- {e}: {c}" for e, c in zip(evidence_list, evidence_consistency)]
    )

    prompt = f"""
    Perform an Analysis of Competing Hypotheses (ACH) with the following inputs:

    Hypotheses:
    {hypotheses}

    Evidence and Consistency Ratings:
    {evidence_analysis}

    For each hypothesis, evaluate its consistency with the evidence, rank hypotheses based on overall consistency, and provide a summary for the most likely threat scenario.
    Be concise and straight to the point.
    """
    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.6,
    )
    return response.choices[0].message.content


# Streamlit Interface
st.title("ACH-Based Threat Modelling")

# Initialize session state variables
if "hypotheses" not in st.session_state:
    st.session_state.hypotheses = ""
if "generated_evidence" not in st.session_state:
    st.session_state.generated_evidence = ""
if "evidence_consistency" not in st.session_state:
    st.session_state.evidence_consistency = []

# Step 1: Input threat context and generate initial hypotheses
context = st.text_area(
    label="Provide Threat Context",
    placeholder="E.g., Recent increase in network traffic, potential indicators of insider threat, attempts to access sensitive information.",
)

if st.button("Generate Hypotheses"):
    if context:
        st.session_state.hypotheses = generate_initial_hypotheses(context)
        st.subheader("Generated Hypotheses")
        st.markdown(st.session_state.hypotheses)
    else:
        st.warning("Please provide a threat context to generate hypotheses.")

# Step 2: Generate or input evidence for each hypothesis
evidence_generation_option = st.radio(
    "Generate Evidence or Enter Manually?", ["Generate Evidence", "Enter Manually"]
)

if evidence_generation_option == "Generate Evidence" and st.session_state.hypotheses:
    st.session_state.generated_evidence = generate_evidence_for_hypotheses(
        st.session_state.hypotheses
    )
    st.subheader("Generated Evidence Suggestions")
    st.markdown(re.sub(r"(E\d+-\d+)", r"\r\1", st.session_state.generated_evidence))

evidence_list = st.text_area(
    label="Enter Additional Evidence",
    placeholder="E.g., Unusual access times, detected malware, specific user actions",
)
if st.session_state.generated_evidence:
    evidence_list += st.session_state.generated_evidence

# Step 3: Evidence consistency scoring
st.subheader("Rate Evidence Consistency with Hypotheses")
evidence_items = evidence_list.split("\n")
evidence_consistency = []

evidence_consistency = [
    (
        item.strip(),
        st.slider(
            f"Consistency for '{item.strip()}'",
            min_value=0,
            max_value=5,
            value=3,
            key=item,
        ),
    )
    for item in evidence_items
    if item.strip().startswith("E")
]

st.session_state.evidence_consistency = evidence_consistency

# Step 4: Perform ACH analysis
if st.button("Perform ACH Analysis"):
    if st.session_state.hypotheses and evidence_list:
        ach_output = perform_ach_analysis(
            st.session_state.hypotheses,
            evidence_items,
            [c for _, c in st.session_state.evidence_consistency],
        )
        st.subheader("ACH Analysis Output")
        st.write(ach_output)
    else:
        st.warning("Please provide both hypotheses and evidence for ACH analysis.")
