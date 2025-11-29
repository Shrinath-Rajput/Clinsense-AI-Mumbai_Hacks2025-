import streamlit as st
from sentence_transformers import SentenceTransformer, util

# ------------------- LOAD MODEL ONCE -------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

SPECIALIZATIONS = [
    "General Physician",
    "Pediatrician",
    "Dermatologist",
    "Cardiologist",
    "Neurologist",
    "Orthopedic Surgeon",
    "ENT Specialist",
    "Psychiatrist",
    "Pulmonologist",
    "Gastroenterologist",
    "Endocrinologist",
    "Gynecologist",
    "Ophthalmologist",
    "Dentist",
]

def show_smart_match():
    st.subheader("🤖 AI-based Doctor Recommendation")

    st.markdown(
        "Type your symptoms in your own words. The AI will suggest the **best doctor specialization** for you."
    )

    example_text = "fever, headache, cold since 2 days, body pain"
    symptoms = st.text_area(
        "📝 Describe your symptoms",
        value=example_text,
        height=120,
        help="Example: 'Fever and headache since 2 days, coughing at night'",
    )

    if st.button("🔍 Find Best Doctor"):
        if not symptoms.strip():
            st.warning("Please enter some symptoms first.")
            return

        with st.spinner("Analyzing your symptoms with AI..."):
            model = load_model()
            user_emb = model.encode(symptoms, convert_to_tensor=True)
            spec_embs = model.encode(SPECIALIZATIONS, convert_to_tensor=True)
            scores = util.cos_sim(user_emb, spec_embs)[0].cpu().tolist()

            ranked = sorted(
                zip(SPECIALIZATIONS, scores),
                key=lambda x: x[1],
                reverse=True,
            )

            best_spec, best_score = ranked[0]

        st.success(f"🏥 Suggested specialization: **{best_spec}**")
        st.caption(f"(similarity score: {best_score:.2f}, higher is better)")

        with st.expander("See other possible matches"):
            for spec, score in ranked[1:5]:
                st.write(f"- **{spec}** — score: `{score:.2f}`")

        st.info(
            "⚠ This is a **prototype AI helper**, not a medical diagnosis. "
            "Always consult a real doctor for serious issues."
        )
