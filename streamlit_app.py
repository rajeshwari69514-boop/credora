import streamlit as st
import requests


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="EduTrust AI",
    page_icon="📚",
    layout="wide"
)


# -----------------------------------------
# HEADER
# -----------------------------------------

st.title("📚 EduTrust AI")

st.subheader(
    "Source-Grounded Academic Assistant"
)

st.write(
    "Ask academic questions and receive "
    "source-supported, evidence-aware answers."
)

st.divider()


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.header("📖 EduTrust AI")

    st.write(
        "An academic assistant designed to "
        "reduce unsupported AI answers."
    )

    st.markdown("### ✨ Features")

    st.write("🔎 Semantic document retrieval")
    st.write("📚 Source-grounded answers")
    st.write("🎯 Evidence confidence")
    st.write("⚠️ Source conflict detection")
    st.write("🕒 Source freshness check")
    st.write("🧠 Misconception detection")

    st.divider()

    st.caption(
        "EduTrust AI — HACKNOVA 2026"
    )


# -----------------------------------------
# QUESTION INPUT
# -----------------------------------------

st.markdown("### 💬 Ask your academic question")

question = st.text_area(
    "Question",
    placeholder=(
        "Example: What is normalization in DBMS?"
    ),
    height=120,
    label_visibility="collapsed"
)


ask_button = st.button(
    "🚀 Ask EduTrust AI",
    use_container_width=True
)


# -----------------------------------------
# PROCESS QUESTION
# -----------------------------------------

if ask_button:

    if not question.strip():

        st.warning(
            "⚠️ Please enter an academic question."
        )

    else:

        with st.spinner(
            "🔍 Retrieving trusted academic information..."
        ):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/question/",
                    json={
                        "question": question
                    },
                    timeout=90
                )


                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                if response.status_code == 200:

                    data = response.json()


                    # -----------------------------------------
                    # TOP STATUS
                    # -----------------------------------------

                    st.success(
                        "✅ Answer generated successfully."
                    )


                    # -----------------------------------------
                    # ANSWER
                    # -----------------------------------------

                    st.markdown(
                        "## 🤖 AI Answer"
                    )

                    st.info(
                        data.get(
                            "answer",
                            "No answer available."
                        )
                    )


                    # -----------------------------------------
                    # SUMMARY METRICS
                    # -----------------------------------------

                    st.markdown(
                        "## 📊 Answer Summary"
                    )

                    col1, col2, col3, col4 = st.columns(4)


                    with col1:

                        st.metric(
                            "Confidence",
                            f"{data.get('confidence', 0)}%"
                        )


                    with col2:

                        st.metric(
                            "Confidence Level",
                            data.get(
                                "confidence_level",
                                "Unknown"
                            )
                        )


                    with col3:

                        st.metric(
                            "AI Provider",
                            data.get(
                                "provider",
                                "Unknown"
                            )
                        )


                    with col4:

                        st.metric(
                            "Answer Mode",
                            data.get(
                                "answer_mode",
                                "Unknown"
                            )
                        )


                    # -----------------------------------------
                    # EVIDENCE CONFIDENCE
                    # -----------------------------------------

                    st.markdown(
                        "## 🎯 Evidence Confidence"
                    )

                    confidence = data.get(
                        "confidence",
                        0
                    )

                    st.progress(
                        min(
                            max(
                                int(confidence),
                                0
                            ),
                            100
                        )
                    )

                    st.write(
                        f"Evidence relevance: "
                        f"**{confidence}%**"
                    )


                    # -----------------------------------------
                    # SOURCES
                    # -----------------------------------------

                    st.markdown(
                        "## 📚 Supporting Sources"
                    )

                    sources = data.get(
                        "sources",
                        []
                    )

                    if sources:

                        for source in sources:

                            source_name = source.get(
                                "source",
                                "Unknown Source"
                            )

                            source_id = source.get(
                                "source_id",
                                "SOURCE"
                            )

                            subject = source.get(
                                "subject",
                                "general"
                            )

                            relevance = source.get(
                                "relevance"
                            )

                            with st.expander(
                                f"📄 {source_id} — {source_name}"
                            ):

                                st.write(
                                    f"**Subject:** "
                                    f"{subject}"
                                )

                                if relevance is not None:

                                    st.write(
                                        f"**Relevance:** "
                                        f"{relevance}%"
                                    )

                                content = source.get(
                                    "content",
                                    ""
                                )

                                if content:

                                    st.markdown(
                                        "**Supporting Content:**"
                                    )

                                    st.write(
                                        content
                                    )

                    else:

                        st.info(
                            "No supporting source was found."
                        )


                    # -----------------------------------------
                    # SOURCE VALIDATION
                    # -----------------------------------------

                    st.markdown(
                        "## 🔐 Source Validation"
                    )

                    validation_col1, validation_col2 = st.columns(2)


                    # -----------------------------------------
                    # CONFLICT
                    # -----------------------------------------

                    with validation_col1:

                        st.markdown(
                            "### ⚠️ Conflict Check"
                        )

                        conflict = data.get(
                            "conflict_check",
                            {}
                        )

                        conflict_detected = conflict.get(
                            "conflict_detected",
                            False
                        )

                        if conflict_detected:

                            st.warning(
                                conflict.get(
                                    "message",
                                    "Potential source conflict detected."
                                )
                            )

                            conflicts = conflict.get(
                                "conflicts",
                                []
                            )

                            for item in conflicts:

                                st.write(
                                    f"• "
                                    f"{item.get('source_1', 'Source 1')}"
                                    f" ↔ "
                                    f"{item.get('source_2', 'Source 2')}"
                                )

                        else:

                            st.success(
                                conflict.get(
                                    "message",
                                    "No obvious source conflict detected."
                                )
                            )


                    # -----------------------------------------
                    # FRESHNESS
                    # -----------------------------------------

                    with validation_col2:

                        st.markdown(
                            "### 🕒 Freshness Check"
                        )

                        freshness = data.get(
                            "freshness_check",
                            {}
                        )

                        freshness_status = freshness.get(
                            "status",
                            "Unavailable"
                        )

                        if freshness_status == "Fresh":

                            st.success(
                                "✅ Sources are relatively fresh."
                            )

                        elif freshness_status == "Moderately Old":

                            st.warning(
                                "⚠️ Some sources are moderately old."
                            )

                        elif freshness_status == "Old":

                            st.warning(
                                "⚠️ Retrieved sources are old."
                            )

                        else:

                            st.info(
                                freshness.get(
                                    "message",
                                    "Freshness information unavailable."
                                )
                            )


                        freshness_sources = freshness.get(
                            "sources",
                            []
                        )

                        for source_info in freshness_sources:

                            source_name = source_info.get(
                                "source",
                                "Unknown Source"
                            )

                            status = source_info.get(
                                "status",
                                "Unknown"
                            )

                            last_modified = source_info.get(
                                "last_modified",
                                "Unknown"
                            )

                            st.write(
                                f"**{source_name}**"
                            )

                            st.caption(
                                f"{status} | "
                                f"Last modified: "
                                f"{last_modified}"
                            )


                    # -----------------------------------------
                    # MISCONCEPTION
                    # -----------------------------------------

                    st.markdown(
                        "## 🧠 Misconception Check"
                    )

                    misconception = data.get(
                        "misconception_check",
                        "Not available"
                    )

                    st.info(
                        misconception
                    )


                    # -----------------------------------------
                    # TECHNICAL DETAILS
                    # -----------------------------------------

                    with st.expander(
                        "⚙️ Technical Response Details"
                    ):

                        st.json(data)


                # -----------------------------------------
                # ERROR
                # -----------------------------------------

                else:

                    st.error(
                        "❌ Unable to get a response "
                        "from EduTrust AI."
                    )

                    st.write(
                        f"Status Code: "
                        f"{response.status_code}"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        pass


            # -----------------------------------------
            # CONNECTION ERROR
            # -----------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend is not running."
                )

                st.info(
                    "Start FastAPI first using:\n\n"
                    "python -m uvicorn app.main:app --reload"
                )


            # -----------------------------------------
            # TIMEOUT
            # -----------------------------------------

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The request took too long."
                )

                st.info(
                    "Please try the question again."
                )


            # -----------------------------------------
            # OTHER ERROR
            # -----------------------------------------

            except Exception as e:

                st.error(
                    "❌ Unexpected error occurred."
                )

                st.write(
                    str(e)
                )


# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "EduTrust AI | Source-Grounded Academic Assistant | "
    "HACKNOVA 2026"
)