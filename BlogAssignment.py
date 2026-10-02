import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# Load environment variables
load_dotenv()

# Page configuration for a professional wide layout
st.set_page_config(
    page_title="AI Blog Team Pro Studio",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for H1 and Tab font sizes
st.markdown("""
    <style>
    .main-desc { font-size: 1.05rem; color: #4B5563; margin-bottom: 20px; }
    
    /* Increase tab font size and padding */
    button[data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR: User Profile & Global API Configurations
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("## 👤 User Profile & Settings")
    
    # Profile Card Mock
    st.info("**Creator:** Ennash\n\n**Plan:** Pro Workspace\n\n⭐ **Points Earned:** 1,240 XP")
    
    st.divider()
    
    st.markdown("### 🔑 API & Credentials")
    openai_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    serper_key_input = st.text_input("Serper API Key", type="password", value=os.getenv("SERPER_API_KEY", ""))
    
    if st.button("Save Credentials", use_container_width=True):
        if openai_key_input:
            os.environ["OPENAI_API_KEY"] = openai_key_input
        if serper_key_input:
            os.environ["SERPER_API_KEY"] = serper_key_input
        st.success("Credentials updated!")
        
    st.markdown("---")
    st.caption("AI Blog Team v2.5 • Powered by CrewAI & Streamlit")

# -------------------------------------------------------------
# MAIN LAYOUT: Industry Standard Tabbed Dashboard
# -------------------------------------------------------------
# Updated to H1 Markdown heading
st.markdown("# 📝 Blog Team Studio")
st.markdown('<p class="main-desc">An advanced multi-agent workspace where autonomous AI teams research trending angles, draft engaging articles, and execute high-performance SEO optimizations automatically.</p>', unsafe_allow_html=True)

# Navigation Tabs
tab_home, tab_insights, tab_activity, tab_settings, tab_faq = st.tabs([
    "🏠 Home", 
    "📈 Insights", 
    "📁 Activity", 
    "⚙️ Settings", 
    "❓ FAQ"
])

# =============================================================
# TAB 1: HOME (Blog Team Studio Execution)
# =============================================================
with tab_home:
    col_main, col_side = st.columns([2.5, 1], gap="large")
    
    with col_main:
        st.subheader("🚀 Generate New SEO Blog Post")
        topic = st.text_input("Enter your core blog topic or niche:", "The Future of Artificial Intelligence Automation in 2026")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            model_choice = st.selectbox("Select LLM Architecture", ["gpt-4o-mini", "gpt-4o"])
        with col_opt2:
            word_count = st.slider("Target Word Count", 150, 600, 300)
            
        generate_btn = st.button("✨ Run AI Blog Team", type="primary", use_container_width=True)

        if generate_btn:
            current_openai = os.getenv("OPENAI_API_KEY")
            current_serper = os.getenv("SERPER_API_KEY")
            
            if not current_openai or not current_serper:
                st.error("⚠️ Please configure both OpenAI and Serper API keys in the sidebar.")
            else:
                try:
                    llm = LLM(model=model_choice)
                    search_tool = SerperDevTool()

                    # Agents
                    researcher = Agent(
                        role="Trend Researcher",
                        goal="Search the web and find one high-impact trending subtopic for the given topic",
                        backstory="You analyze online search trends to discover what audiences care about right now.",
                        tools=[search_tool],
                        llm=llm,
                        verbose=True
                    )
                    writer = Agent(
                        role="Content Writer",
                        goal=f"Write an engaging, simple, friendly blog post around {word_count} words",
                        backstory="You write clear, captivating blogs that beginners and tech enthusiasts alike enjoy reading.",
                        llm=llm,
                        verbose=True
                    )
                    seo = Agent(
                        role="SEO Specialist",
                        goal="Make the blog exceptionally optimized for search engines",
                        backstory="You add high-ranking catchy titles, optimal keyword targets, and precise meta descriptions.",
                        llm=llm,
                        verbose=True
                    )

                    # Tasks
                    research_task = Task(
                        description=f"Search the web and find ONE specific trending angle or subtopic for the core topic: {topic}.",
                        expected_output="One trending subtopic angle and a short data-backed justification.",
                        agent=researcher,
                    )
                    write_task = Task(
                        description=f"Write a short, clean blog post (~{word_count} words) based on the researched subtopic.",
                        expected_output="A well-formatted blog post body containing a title and neat paragraphs.",
                        agent=writer,
                    )
                    seo_task = Task(
                        description="Optimize the content for SEO. Provide a catchy title, 5 target search keywords, and a compelling 1-line meta description, followed by the final blog post.",
                        expected_output="Final structured output containing Title, Meta Description, Keywords, and the Body Text.",
                        agent=seo,
                    )

                    crew = Crew(
                        agents=[researcher, writer, seo],
                        tasks=[research_task, write_task, seo_task],
                    )

                    with st.spinner("🤖 Autonomous agents active: Scraping trends -> Writing copy -> Optimizing SEO..."):
                        result = crew.kickoff()

                    st.success("🎉 Blog Generated Successfully!")
                    st.markdown("---")
                    st.markdown(result.raw)

                except Exception as e:
                    st.error(f"Execution error: {e}")

    with col_side:
        st.markdown("### 📋 Studio Workflow")
        st.markdown("""
        1. **Trend Researcher:** Scrapes live search parameters.
        2. **Content Writer:** Formulates tailored drafts.
        3. **SEO Specialist:** Injects keywords & meta elements.
        """)
        st.markdown("---")
        st.info("💡 **Quick Tip:** Keep titles descriptive for better web-scraping yield.")

# =============================================================
# TAB 2: INSIGHTS (Points & Trends Usage Graph)
# =============================================================
with tab_insights:
    st.subheader("📊 Performance & Usage Analytics")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Points Earned", "1,240 XP", "+120 today")
    col_m2.metric("Blogs Published", "18 Posts", "+3 this week")
    col_m3.metric("SEO Average Score", "94 / 100", "+4.2%")
    
    st.divider()
    
    st.markdown("#### 📈 API & Generation Usage Trends")
    trend_filter = st.radio("Select timeframe for usage metrics:", ["Last 7 Days", "Last 30 Days", "Last 60 Days"], horizontal=True)
    
    days_count = 7 if "7" in trend_filter else (30 if "30" in trend_filter else 60)
    chart_data = pd.DataFrame(
        {
            "Day": [f"Day {i+1}" for i in range(days_count)],
            "Generations": [max(1, (i % 5) + 2) for i in range(days_count)]
        }
    ).set_index("Day")
    
    st.line_chart(chart_data)

# =============================================================
# TAB 3: ACTIVITY (Saved & Last 30 Days Generated Content)
# =============================================================
with tab_activity:
    st.subheader("📁 Content Archive & History")
    st.write("Review your generated output history over the past 30 days.")
    
    mock_history = [
        {"date": "2026-09-28", "title": "The Rise of Edge AI in Mobile Apps", "status": "Published", "words": 320},
        {"date": "2026-09-22", "title": "Sustainable Architecture Trends", "status": "Saved Draft", "words": 280},
        {"date": "2026-09-15", "title": "Remote Team Productivity Frameworks", "status": "Archived", "words": 410},
    ]
    
    for item in mock_history:
        with st.expander(f"📌 {item['date']} — {item['title']} ({item['status']})"):
            st.write(f"**Target Word Count:** {item['words']} words")
            st.write(f"**Status:** {item['status']}")
            st.button("View Full Content", key=item['title'])

# =============================================================
# TAB 4: SETTINGS (Preferences, External Integrations & Scheduler)
# =============================================================
with tab_settings:
    st.subheader("⚙️ App Preferences & Integrations")
    
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown("#### 🎯 Preferred Topic & Content Defaults")
        st.text_input("Default Author Style", value="Professional & Friendly")
        st.selectbox("Default Industry Niche", ["Technology & AI", "Health & Wellness", "Fintech", "Marketing"])
        st.checkbox("Auto-include bullet points", value=True)
        st.checkbox("Enable grammar auto-correction", value=True)
        
        if st.button("Save Preferences"):
            st.success("Preferences saved successfully!")

    with col_set2:
        st.markdown("#### 🔌 External App Connections")
        st.text_input("WordPress REST API URL", placeholder="https://yourwebsite.com/wp-json/...")
        st.text_input("Medium Integration Token", type="password")
        
        st.markdown("#### ⏰ Schedule Automated Job")
        st.selectbox("Frequency", ["Daily Draft", "Weekly Batch", "Custom Cron"])
        st.time_input("Execution Time", value=datetime.strptime("09:00:00", "%H:%M:%S").time())
        
        if st.button("Activate Schedule"):
            st.success("Automation job registered successfully!")

# =============================================================
# TAB 5: FAQ (Help Center)
# =============================================================
with tab_faq:
    st.subheader("❓ Frequently Asked Questions")
    
    with st.expander("How do the CrewAI agents collaborate?"):
        st.write("The system relies on a sequential framework: the Trend Researcher finds trending web points, passes context to the Content Writer to create a draft, which is finally polished by the SEO Specialist.")
    
    with st.expander("How are points calculated in Insights?"):
        st.write("Points accumulate dynamically based on successful generations, keywords optimized, and regular weekly tool usage.")
    
    with st.expander("Can I connect my WordPress blog directly?"):
        st.write("Yes! Head over to the **Settings tab**, enter your WordPress REST API endpoints and credentials, and your finalized articles can publish directly.")
    
    with st.expander("Where do I find my API keys?"):
        st.write("OpenAI keys can be retrieved from your OpenAI developer dashboard, and Serper search keys are available for free at Serper.dev.")