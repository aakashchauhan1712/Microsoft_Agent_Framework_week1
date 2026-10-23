
import asyncio
import hashlib

import streamlit as st

from agent_logic import (
    create_agent,
    create_foundry_client,
    upload_pdf_to_foundry,
)

st.set_page_config(
    page_title="Week 1 AI Assistant",
    page_icon="🤖",
    layout="centered",
)

# ---------- Session state ----------

defaults = {
    "messages": [],
    "event_loop": None,
    "foundry_client": None,
    "agent": None,
    "agent_session": None,
    "indexed_pdf_hash": None,
    "indexed_filename": None,
    "file_id": None,
    "vector_store_id": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Keep one event loop for async Foundry operations.
if st.session_state.event_loop is None:
    st.session_state.event_loop = asyncio.new_event_loop()

loop = st.session_state.event_loop

# Create the Foundry client and initial agent only once per session.
if st.session_state.foundry_client is None:
    st.session_state.foundry_client = create_foundry_client()

if st.session_state.agent is None:
    st.session_state.agent = create_agent(
        client=st.session_state.foundry_client
    )


# ---------- Sidebar ----------

with st.sidebar:
    st.title("🤖 AI Assistant")
    st.caption("Week 1 milestone · Microsoft Agent Framework")
    st.divider()

    st.subheader("📄 PDF Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload a PDF and process it before asking document questions.",
    )

    current_pdf_hash = None
    pdf_bytes = None

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.getvalue()
        current_pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

        is_indexed = (
            current_pdf_hash == st.session_state.indexed_pdf_hash
            and st.session_state.vector_store_id is not None
        )

        if is_indexed:
            st.success(f"Ready: {uploaded_file.name}")
        else:
            st.info("Process this PDF before asking questions about it.")

            if st.button("Process PDF", use_container_width=True):
                try:
                    with st.spinner(
                        "Uploading PDF and creating searchable index..."
                    ):
                        file_id, vector_store_id = loop.run_until_complete(
                            upload_pdf_to_foundry(
                                client=st.session_state.foundry_client,
                                filename=uploaded_file.name,
                                pdf_bytes=pdf_bytes,
                            )
                        )

                        # Recreate the agent with File Search enabled.
                        new_agent = create_agent(
                            client=st.session_state.foundry_client,
                            vector_store_ids=[vector_store_id],
                        )

                    st.session_state.file_id = file_id
                    st.session_state.vector_store_id = vector_store_id
                    st.session_state.indexed_pdf_hash = current_pdf_hash
                    st.session_state.indexed_filename = uploaded_file.name
                    st.session_state.agent = new_agent
                    st.session_state.agent_session = None
                    st.session_state.messages = []

                    st.success("PDF indexed successfully!")
                    st.rerun()

                except Exception as exc:
                    st.error("Could not process the PDF.")
                    st.exception(exc)

    elif st.session_state.vector_store_id is not None:
        st.caption(
            f"Active indexed document: "
            f"{st.session_state.indexed_filename}"
        )
        st.caption(
            "Removing the upload from the widget does not delete "
            "the stored document."
        )

    st.divider()
    st.subheader("Available tools")

    st.markdown(
        "- Addition\n"
        "- Multiplication\n"
        "- Current date and time\n"
        "- Web search\n"
        "- Foundry File Search (after PDF processing)"
    )

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_session = None
        st.rerun()


# ---------- Main chat interface ----------

st.title("🤖 Week 1 AI Assistant")
st.caption("Powered by Microsoft Agent Framework and Azure AI Foundry")

if st.session_state.vector_store_id:
    st.info(
        f"PDF Q&A enabled for: {st.session_state.indexed_filename}"
    )
else:
    st.info(
        "General assistant mode is active. Upload and process a PDF "
        "from the sidebar to enable document Q&A."
    )

if not st.session_state.messages:
    st.markdown("### Welcome!")
    st.markdown(
        "Try asking:\n"
        "- What is 25 multiplied by 16?\n"
        "- What is the current date and time?\n"
        "- Search the web for the latest AI news.\n"
        "- Upload a PDF and ask: What are its main points?"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------- Process user messages ----------

prompt = st.chat_input("Ask your AI assistant...")

if prompt:
    # Prevent questions about a newly selected, unprocessed PDF
    # from accidentally using the previously indexed document.
    if (
        uploaded_file is not None
        and current_pdf_hash != st.session_state.indexed_pdf_hash
    ):
        st.warning("Please process the selected PDF before asking questions.")
        st.stop()

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = st.session_state.agent

                if st.session_state.agent_session is None:
                    st.session_state.agent_session = agent.create_session()

                response = loop.run_until_complete(
                    agent.run(
                        prompt,
                        session=st.session_state.agent_session,
                    )
                )

                answer = response.text or "The agent returned an empty response."
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception:
                st.error(
                    "The agent could not process your request. "
                    "Check the terminal for details."
                )
                st.exception(Exception("Agent request failed"))
