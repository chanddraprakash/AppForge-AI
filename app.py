import streamlit as st

if "generated" not in st.session_state:
    st.session_state.generated = False

if "code_explanation" not in st.session_state:
    st.session_state.code_explanation = ""

from ai_engine import ask_ai

st.set_page_config(
    page_title="AppForge AI",
    page_icon="🚀"
)

st.title("🚀 AppForge AI")
st.subheader("AI-Powered Application Development Assistant")

st.write(
    "Turn your app idea into a plan, code, explanation, and learning roadmap."
)

idea = st.text_area(
    "💡 What do you want to build?",
    placeholder="Example: I want to build a food delivery app for college students."
)

if st.button("🚀 Start Building"):

    if not idea:
        st.warning("Please enter an app idea first.")

    else:
        with st.spinner("🧠 Understanding your idea..."):

            prompt = f"""
            You are AppForge AI, an expert application development assistant.

            The user wants to build:

            {idea}

            Analyze this application idea and return EXACTLY these five sections.

            Use the following markers exactly:

            ===UNDERSTAND===
            Explain:
            - The problem being solved
            - Target users
            - Main objective
            - Important requirements

            ===PLAN===
            Explain:
            - Main features
            - Recommended technology stack
            - Application architecture
            - Database requirements
            - Development roadmap

            ===BUILD===
            Provide:
            - Suggested project structure
            - Important files
            - Starter code examples
            - Explain what the important files do

            ===EXPLAIN===
            Explain:
            - How the application works
            - What each major technology does
            - Explain the important generated code for a beginner

            ===LEARN===
            Provide:
            - Technologies the user should learn
            - Concepts to learn
            - Recommended learning order
            - Practical steps to continue development

            Important:
            - Keep everything beginner-friendly.
            - Do not use HTML <br> tags.
            - Use Markdown headings and bullet points.
            - Do not add anything before ===UNDERSTAND===.
            - Do not add anything after the ===LEARN=== section.
            """

            try:
                answer = ask_ai(prompt)
                st.session_state.generated = True
                st.session_state.answer = answer
                st.session_state.idea = idea


                def extract_section(text, start_marker, end_marker=None):
                    if start_marker not in text:
                        return "The AI did not return this section in the expected format."

                    section = text.split(start_marker, 1)[1]

                    if end_marker and end_marker in section:
                        section = section.split(end_marker, 1)[0]

                    return section.strip()


                understand = extract_section(
                    answer,
                    "===UNDERSTAND===",
                    "===PLAN==="
                )

                plan = extract_section(
                    answer,
                    "===PLAN===",
                    "===BUILD==="
                )

                build = extract_section(
                    answer,
                    "===BUILD===",
                    "===EXPLAIN==="
                )

                explain = extract_section(
                    answer,
                    "===EXPLAIN===",
                    "===LEARN==="
                )
                learn = ""

                if "===LEARN===" in answer:
                    learn = extract_section(
                        answer,
                        start_marker="===LEARN==="
                    )

                    # SAVE RESULTS
                    st.session_state.understand = understand
                    st.session_state.plan = plan
                    st.session_state.build = build
                    st.session_state.explain = explain
                    st.session_state.learn = learn
                    st.session_state.generated = True

                if not learn.strip() or "did not return" in learn:
                    learn = f"""
                ### 🎓 Learning Roadmap

                To build **{idea}**, follow this learning path:

                #### 1. Frontend Development
                - Learn HTML and CSS
                - Learn JavaScript basics
                - Learn React or React Native
                - Learn how to create screens and components

                #### 2. Backend Development
                - Learn Python or Node.js
                - Learn REST APIs
                - Learn authentication

                #### 3. Database
                - Learn SQL
                - Learn PostgreSQL
                - Learn tables and relationships

                #### 4. Application Development
                - Connect frontend and backend
                - Integrate APIs
                - Handle errors and validation

                #### 5. Testing
                - Test individual features
                - Test APIs
                - Test the complete application

                #### 6. Deployment
                - Learn Git and GitHub
                - Learn environment variables
                - Learn basic cloud deployment

                ### 🚀 Recommended Order

                **Frontend → Backend → Database → APIs → Integration → Testing → Deployment**
                """

                st.success("🎉 Your application plan is ready!")

                st.session_state.generated = True

                if st.session_state.generated:
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(
                        [
                            "🧠 Understand",
                            "📋 Plan",
                            "🛠 Build",
                            "💻 Explain",
                            "🎓 Learn"
                        ],
                        default="💻 Explain" if st.session_state.get("code_explanation") else "🧠 Understand"
                    )

                with tab1:
                    st.markdown("## 🧠 Understand")
                    st.markdown(understand)

                with tab2:
                    st.markdown("## 📋 Plan")
                    st.markdown(plan)

                with tab3:
                    st.markdown("## 🛠 Build")
                    st.markdown(build)

                with tab4:
                    st.markdown("## 📖 Explain")

                    st.markdown(explain)

                    st.divider()

                    st.markdown("### 💻 Understand Your Code")

                    code_to_explain = st.text_area(
                        "Paste code you want to understand:",
                        placeholder="Paste your code here..."
                    )

                    if st.button("💬 Explain This Code"):

                        if code_to_explain.strip():

                            with st.spinner("💬 Analyzing your code..."):

                                explanation_prompt = f"""
                    You are a friendly programming teacher.

                    Explain this code to a beginner:

                    {code_to_explain}

                    Explain:
                    1. What this code does
                    2. How it works
                    3. Important functions or concepts
                    4. Inputs and outputs
                    5. A simple real-world analogy
                    6. One thing the learner should remember

                    Keep the explanation simple and clear.
                    """

                                code_explanation = ask_ai(explanation_prompt)

                                st.session_state.code_explanation = code_explanation

                        else:
                            st.warning("Please paste some code first.")

                    # Show the explanation after Streamlit reruns
                    if st.session_state.code_explanation:
                        st.markdown("### 📖 Explanation")
                        st.markdown(st.session_state.code_explanation)
                with tab5:
                    st.markdown("## 🎓 Learn")
                    st.markdown(learn)

            except Exception as e:
                st.error("Something went wrong while connecting to the AI.")
                st.code(str(e))