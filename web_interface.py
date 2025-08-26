import streamlit as st
import pandas as pd
from data_analyst_mysql import DataAnalystAssistant
from enhanced_visualizer import EnhancedVisualizer
import os

st.set_page_config(page_title="LLM-Based Data Analyst Assistant", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .stExpander {
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .stExpander > div > div {
        background: white;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Add custom CSS for styling the expander
st.markdown("""
<style>
/* Style the expander title */
div[data-testid="stExpander"] > details > summary {
    background: linear-gradient(90deg, #12c2e9, #c471ed, #f64f59);
    color: white;
    font-weight: bold;
    padding: 0.8rem;
    border-radius: 8px;
    font-size: 16px;
}

/* Remove default triangle and add custom icon */
div[data-testid="stExpander"] > details > summary::-webkit-details-marker {
    display: none;
}

div[data-testid="stExpander"] > details > summary:after {
    content: " ▼";
    float: right;
    color: white;
    font-size: 14px;
}

/* Expander content box styling */
div[data-testid="stExpander"] > div {
    background: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 0.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = EnhancedVisualizer()
if 'current_table' not in st.session_state:
    st.session_state.current_table = None

st.markdown('<div class="main-header"><h1>🤖 LLM-Based Data Analyst Assistant</h1></div>', unsafe_allow_html=True)

# Sidebar for configuration
# Sidebar for configuration
with st.sidebar:
    # Stylized DRAKO title
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
        border-bottom: 2px solid #ccc;
        margin-bottom: 1rem;
    ">
        <h1 style="
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 2.8rem;
            background: linear-gradient(90deg, #12c2e9, #c471ed, #f64f59);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
            margin: 0;
        ">DRAKO</h1>
        <p style="
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.3rem;
            font-style: italic;
        ">Your AI-Powered Data Analyst</p>
    </div>
    """, unsafe_allow_html=True)

    # Configuration section
    st.markdown("""
<div style="text-align: center; font-size: 1.5rem; font-weight: bold; margin-top: 10px; margin-bottom: 10px;">
Configuration
</div>
""", unsafe_allow_html=True)


    # Add custom CSS
    st.markdown("""
    <style>
    .centered-text-input {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .centered-text-input input {
        text-align: center; /* Centers text inside input */
        width: 50%; /* Adjust width */
    }
    </style>
    """, unsafe_allow_html=True)

# Wrap your input inside a container with the custom class
    st.markdown('<div class="centered-text-input">', unsafe_allow_html=True)
    ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
    st.markdown('</div>', unsafe_allow_html=True)

    # Collapsible MySQL Database Settings
    with st.expander("MySQL Database Configuration", expanded=False):
        mysql_host = st.text_input("Host", value="localhost")
        mysql_port = st.number_input("Port", value=3306)
        mysql_user = st.text_input("Username")
        mysql_password = st.text_input("Password", type="password")
        mysql_database = st.text_input("Database Name")

        if st.button("Connect to MySQL"):
            if not all([mysql_host, mysql_user, mysql_password, mysql_database]):
                st.error("Please fill in all MySQL credentials")
            else:
                try:
                    mysql_config = {
                        'host': mysql_host,
                        'port': int(mysql_port),
                        'user': mysql_user,
                        'password': mysql_password,
                        'database': mysql_database
                    }
                    st.session_state.assistant = DataAnalystAssistant(ollama_url, mysql_config)
                    st.success("Connected to MySQL and initialized assistant!")
                except Exception as e:
                    st.error(f"Failed to connect: {str(e)}")

                    

    # Button for file-only mode
    if st.button("Work with Files Only") and not st.session_state.assistant:
        st.session_state.assistant = DataAnalystAssistant(ollama_url)
        st.success("Assistant initialized for file-only mode!")
    # Add a beautiful dashed horizontal line below the button
    st.markdown("""
<hr class="dashed-line">
<style>
.dashed-line {
    border: none;
    border-top: 2px dashed #c471ed; /* Purple dashed line */
    margin: 15px auto;
    width: 100%; /* Centered with reduced width */
}
</style>
""", unsafe_allow_html=True)
    
    
    st.markdown("""
<div style="text-align: center; font-size: 1.5rem; font-weight: bold; margin-top: 10px; margin-bottom: 10px;">
Upload Data
</div>
""", unsafe_allow_html=True)


    # File upload
    uploaded_files = st.file_uploader(
        "Upload Excel/CSV files", 
        type=['xlsx', 'xls', 'csv'], 
        accept_multiple_files=True
    )

    
    if uploaded_files:
        if not st.session_state.assistant:
            st.session_state.assistant = DataAnalystAssistant(ollama_url)
            st.info("Assistant auto-initialized for file uploads")
        
        for file in uploaded_files:
            # Ensure Excel folder exists
            excel_folder = "Excel"
            if not os.path.exists(excel_folder):
                os.makedirs(excel_folder)
            
            # Save uploaded file temporarily in Excel folder
            temp_path = os.path.join(excel_folder, f"temp_{file.name}")
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            
            # Load into assistant
            table_name = st.text_input(f"Table name for {file.name}", 
                                     value=os.path.splitext(file.name)[0])
            
            if st.button(f"Load {file.name}"):
                try:
                    result = st.session_state.assistant.load_file(temp_path, table_name)
                    st.success(result)
                    os.remove(temp_path)  # Clean up
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")

# Main interface
if st.session_state.assistant:
    # Show available tables
    if st.session_state.assistant.tables:
        st.subheader("Available Tables")
        
        # Dropdown to select table
        table_names = st.session_state.assistant.get_available_tables()
        if table_names:
            selected_table = st.selectbox("Select a table to view:", ["-- Select Table --"] + table_names)
            
            # Clear chat history when table changes
            if selected_table != st.session_state.current_table and selected_table != "-- Select Table --":
                st.session_state.chat_history = []
                st.session_state.current_table = selected_table
                st.rerun()
            
            if selected_table != "-- Select Table --":
                info = st.session_state.assistant.tables[selected_table]
                st.write(f"**Table:** {selected_table}")
                st.write(f"**Columns:** {', '.join(info['columns'])}")
                st.write("**Sample data:**")
                if info['sample_data']:
                    st.dataframe(pd.DataFrame(info['sample_data']))
                else:
                    st.write("No sample data available")
                
                # Show context indicator
                st.info(f"💬 Chat context: {selected_table} table")
        
        # Expandable view for all tables
        with st.expander("View All Tables Details"):
            for table_name, info in st.session_state.assistant.tables.items():
                st.write(f"**{table_name}**")
                st.write(f"Columns: {', '.join(info['columns'])}")
                if info['sample_data']:
                    st.dataframe(pd.DataFrame(info['sample_data'][:2]))
                st.write("---")
    
    # Chat interface
    st.subheader("Ask Questions About Your Data")
    
    # DML Operations help
    with st.expander("💡 Supported Operations"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Query Operations:**")
            st.write("• Show me all records")
            st.write("• Sort by column name")
            st.write("• Count total records")
            st.write("• Filter by conditions")
        with col2:
            st.write("**Data Operations:**")
            st.write("• Delete records where...")
            st.write("• Update column set value")
            st.write("• Add new record")
            st.write("• Modify existing data")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        
        with st.chat_message("assistant"):
            if chat['success']:
                st.write(chat['insights'])
                
                # Add visualization if possible
                if 'results' in chat and chat['results']:
                    results_df = pd.DataFrame(chat['results'])
                    
                    # Show table results right after insights
                    st.dataframe(results_df)
                    
                    # Clean data summary
                    data_summary = st.session_state.visualizer.get_chart_summary(results_df)
                    st.info(data_summary)
                    
                    # Create and display chart
                    chart = st.session_state.visualizer.create_visualization(
                        chat['question'], chat['sql_query'], results_df
                    )
                    if chart:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.plotly_chart(chart, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Optional: Show advanced details in collapsible section
                    with st.expander("🔧 Advanced Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Shape:** {results_df.shape}")
                            st.write(f"**Columns:** {list(results_df.columns)}")
                        with col2:
                            st.write(f"**Data Types:** {dict(results_df.dtypes)}")
                            st.write("**Sample Data:**")
                            st.dataframe(results_df.head(3))
                        
                        # Generated Plotly code
                        st.write("**Generated Plotly Code:**")
                        plotly_code = st.session_state.visualizer.generate_plotly_code(
                            chat['question'], chat['sql_query'], results_df
                        )
                        st.code(plotly_code, language='python')
                    
                    viz_explanation = st.session_state.visualizer.get_visualization_explanation(
                        chat['question'], chat['sql_query'], results_df
                    )
                    st.success(viz_explanation)
                
                with st.expander("View SQL Query"):
                    st.code(chat['sql_query'], language='sql')
            else:
                st.error(chat['error'])
    
    # Input for new question
    question = st.chat_input("Ask a question about your data...")
    
    if question:
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                result = st.session_state.assistant.analyze(question, st.session_state.current_table)
                st.session_state.chat_history.append(result)
                
                if result['success']:
                    st.write(result['insights'])
                    
                    # Add visualization if possible
                    if 'results' in result and result['results']:
                        results_df = pd.DataFrame(result['results'])
                        
                        # Show table results right after insights
                        st.dataframe(results_df)
                        
                        # Clean data summary
                        data_summary = st.session_state.visualizer.get_chart_summary(results_df)
                       
                        st.info(data_summary)
                        
                        # Create and display chart
                        chart = st.session_state.visualizer.create_visualization(
                            question, result['sql_query'], results_df
                        )
                        if chart:
                           # # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                            st.plotly_chart(chart, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Optional: Show advanced details in collapsible section
                        with st.expander("🔧 Advanced Details"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Shape:** {results_df.shape}")
                                st.write(f"**Columns:** {list(results_df.columns)}")
                            with col2:
                                st.write(f"**Data Types:** {dict(results_df.dtypes)}")
                                st.write("**Sample Data:**")
                                st.dataframe(results_df.head(3))
                            
                            # Generated Plotly code
                            st.write("**Generated Plotly Code:**")
                            plotly_code = st.session_state.visualizer.generate_plotly_code(
                                question, result['sql_query'], results_df
                            )
                            st.code(plotly_code, language='python')
                        
                        viz_explanation = st.session_state.visualizer.get_visualization_explanation(
                            question, result['sql_query'], results_df
                        )
                        st.success(viz_explanation)
                    
                    with st.expander("View SQL Query"):
                        st.code(result['sql_query'], language='sql')
                else:
                    st.error(result['error'])

else:
    st.warning("Please connect to MySQL database in the sidebar. Make sure Ollama is running with Llama 3 model.")
    st.info("💡 **Tip:** Once connected, you can use existing tables in your database or upload new files.")
    
 