import streamlit as st
import pandas as pd
import io
from datetime import datetime

    # Configure the page with wider layout
st.set_page_config(
    page_title="Text Preference Tool",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Text Preference Selection Tool"
    }
)

# Apply custom CSS for better appearance
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    .main {
        padding: 1rem;
    }
    .comparison-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid transparent;
        height: 300px;
        overflow-y: auto;
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .comparison-box:hover {
        border-color: #bbdefb;
    }
    .original-text {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        max-height: 200px;
        overflow-y: auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #1976d2;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    /* Scrollbar styling for better UX */
    .comparison-box::-webkit-scrollbar, .original-text::-webkit-scrollbar {
        width: 8px;
    }
    .comparison-box::-webkit-scrollbar-track, .original-text::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .comparison-box::-webkit-scrollbar-thumb, .original-text::-webkit-scrollbar-thumb {
        background: #aaa;
        border-radius: 10px;
    }
    .comparison-box::-webkit-scrollbar-thumb:hover, .original-text::-webkit-scrollbar-thumb:hover {
        background: #888;
    }
    /* Indicator for scrollable content */
    .scroll-indicator {
        position: absolute;
        bottom: 10px;
        right: 10px;
        color: #1976d2;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.8rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        opacity: 0.8;
    }
    /* Layout options */
    .view-toggle {
        text-align: right;
        margin-bottom: 10px;
    }
    .header-container {
        text-align: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
        color: #757575;
        font-size: 0.9rem;
    }
    .variation-label {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .label-a {
        background-color: #e3f2fd;
        color: #1976d2;
        border: 1px solid #1976d2;
    }
    .label-b {
        background-color: #f3e5f5;
        color: #7b1fa2;
        border: 1px solid #7b1fa2;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    /* Fixed container for the comparison interface */
    .comparison-container {
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        bottom: 0;
        padding: 0 1rem;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        max-width: 900px;
        margin: 0 auto;
    }
    /* Make the page content area have proper spacing */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 900px;
    }
    .metric-card {
        text-align: center;
        padding: 1.5rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .metric-a {
        color: #1976d2;
    }
    .metric-b {
        color: #7b1fa2;
    }
    .instructions {
        background-color: #fffde7;
        border-left: 5px solid #fbc02d;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1.5rem;
    }
    .upload-section {
        border: 2px dashed #bdbdbd;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header section - more compact
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h1>Text Preference Tool</h1></div>", unsafe_allow_html=True)
    
    # Initialize session state variables if they don't exist
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'preferences' not in st.session_state:
        st.session_state.preferences = []
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    if 'file_extension' not in st.session_state:
        st.session_state.file_extension = None
    if 'comparison_complete' not in st.session_state:
        st.session_state.comparison_complete = False
    if 'text_size' not in st.session_state:
        st.session_state.text_size = 'medium' # Default text size
    
    # File upload section
    if st.session_state.data is None:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2>Upload Your Excel File</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='instructions'>", unsafe_allow_html=True)
        st.markdown("""
        <strong>Instructions:</strong>
        <ul>
            <li>Prepare an Excel file with at least 3 columns</li>
            <li>Column 1: Original text</li>
            <li>Column 2: Variation A</li>
            <li>Column 3: Variation B</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            try:
                # Show a spinner while loading
                with st.spinner("Processing your file..."):
                    # Read the file
                    df = pd.read_excel(uploaded_file)
                    
                    # Check if file has at least 3 columns
                    if len(df.columns) < 3:
                        st.error("Your Excel file must have at least 3 columns: original text, variation A, and variation B.")
                    else:
                        # Save the data without showing preview
                        st.session_state.data = df
                        # Extract file name and extension for later use
                        file_name_parts = uploaded_file.name.split('.')
                        st.session_state.file_name = '.'.join(file_name_parts[:-1])
                        st.session_state.file_extension = file_name_parts[-1]
                        # Initialize preferences list with None values for each row
                        st.session_state.preferences = [None] * len(df)
                        
                        # Display brief success message and automatically proceed
                        with st.spinner("Starting comparisons..."):
                            st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Comparison section (only show if data is loaded)
    elif not st.session_state.comparison_complete:
        # Get current data row
        data = st.session_state.data
        current_idx = st.session_state.current_index
        
        # Initialize view mode if not already set
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = "side_by_side"
        
        if current_idx < len(data):
            # Display progress at the top
            progress_text = f"Comparison {current_idx + 1} of {len(data)}"
            st.markdown(f"<div style='text-align: center;'><h3>{progress_text}</h3></div>", unsafe_allow_html=True)
            progress_value = (current_idx) / (len(data) - 1) if len(data) > 1 else 1.0
            progress_bar = st.progress(progress_value)
            
            # Display settings for text size
            col_size, col_toggle = st.columns([4, 1])
            
            # Add text size control
            with col_size:
                text_size_options = {
                    "Small": "small", 
                    "Medium": "medium", 
                    "Large": "large"
                }
                selected_size = st.select_slider(
                    "Text size:",
                    options=list(text_size_options.keys()),
                    value="Medium" if st.session_state.text_size == "medium" else 
                         "Small" if st.session_state.text_size == "small" else "Large"
                )
                st.session_state.text_size = text_size_options[selected_size]
                
                # Apply text size dynamically with JavaScript
                text_size_px = {
                    "small": "0.9rem",
                    "medium": "1.05rem",
                    "large": "1.3rem"
                }[st.session_state.text_size]
                
                st.markdown(f"""
                <script>
                    document.addEventListener('DOMContentLoaded', (event) => {{
                        const boxes = document.querySelectorAll('.comparison-box, .original-text');
                        boxes.forEach(box => {{
                            box.style.fontSize = '{text_size_px}';
                        }});
                    }});
                </script>
                """, unsafe_allow_html=True)
            
            # View toggle option
            with col_toggle:
                st.markdown("<div class='view-toggle'>", unsafe_allow_html=True)
                # Toggle between side-by-side and vertical views
                view_options = {"Side-by-side": "side_by_side", "Vertical": "vertical"}
                selected_view = st.radio("View Mode:", list(view_options.keys()), horizontal=True, 
                                         index=0 if st.session_state.view_mode == "side_by_side" else 1, 
                                         label_visibility="collapsed")
                st.session_state.view_mode = view_options[selected_view]
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Display original text
            st.markdown("<h4>Original Text</h4>", unsafe_allow_html=True)
            original_text = data.iloc[current_idx, 0]
            st.markdown(f"<div class='original-text'>{original_text}</div>", unsafe_allow_html=True)
            
            # Display variations for comparison based on view mode
            st.markdown("<h4>Which variation do you prefer?</h4>", unsafe_allow_html=True)
            
            if st.session_state.view_mode == "side_by_side":
                # Side-by-side view
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='variation-label label-a'>Variation A</div>", unsafe_allow_html=True)
                    variation_a = data.iloc[current_idx, 1]
                    
                    # Create a container for the text with scroll indicator
                    st.markdown(f"""
                    <div style="position: relative;">
                        <div class='comparison-box'>{variation_a}</div>
                        <div class='scroll-indicator'>Scroll for more ↓</div>
                    </div>
                    """, unsafe_allow_html=True)
                    choose_a = st.button("Choose A", type="primary", key="choose_a", use_container_width=True)
                
                with col2:
                    st.markdown("<div class='variation-label label-b'>Variation B</div>", unsafe_allow_html=True)
                    variation_b = data.iloc[current_idx, 2]
                    
                    # Create a container for the text with scroll indicator
                    st.markdown(f"""
                    <div style="position: relative;">
                        <div class='comparison-box'>{variation_b}</div>
                        <div class='scroll-indicator'>Scroll for more ↓</div>
                    </div>
                    """, unsafe_allow_html=True)
                    choose_b = st.button("Choose B", type="primary", key="choose_b", use_container_width=True)
            else:
                # Vertical view for better comparison of long text
                # Variation A
                st.markdown("<div class='variation-label label-a'>Variation A</div>", unsafe_allow_html=True)
                variation_a = data.iloc[current_idx, 1]
                
                # Create a container for the text with scroll indicator
                st.markdown(f"""
                <div style="position: relative;">
                    <div class='comparison-box'>{variation_a}</div>
                    <div class='scroll-indicator'>Scroll for more ↓</div>
                </div>
                """, unsafe_allow_html=True)
                choose_a = st.button("Choose A", type="primary", key="choose_a", use_container_width=True)
                
                # Variation B
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                st.markdown("<div class='variation-label label-b'>Variation B</div>", unsafe_allow_html=True)
                variation_b = data.iloc[current_idx, 2]
                
                # Create a container for the text with scroll indicator
                st.markdown(f"""
                <div style="position: relative;">
                    <div class='comparison-box'>{variation_b}</div>
                    <div class='scroll-indicator'>Scroll for more ↓</div>
                </div>
                """, unsafe_allow_html=True)
                choose_b = st.button("Choose B", type="primary", key="choose_b", use_container_width=True)
            
            # Handle selection
            if choose_a:
                st.session_state.preferences[current_idx] = 'A'
                st.session_state.current_index += 1
                st.rerun()
            
            elif choose_b:
                st.session_state.preferences[current_idx] = 'B'
                st.session_state.current_index += 1
                st.rerun()
        
        else:
            # All comparisons are done
            st.session_state.comparison_complete = True
            st.rerun()
    
    # Results and download section
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🎉 All Comparisons Completed! 🎉</h2>", unsafe_allow_html=True)
        
        # Update the dataframe with preferences
        result_df = st.session_state.data.copy()
        result_df['Preference'] = st.session_state.preferences
        
        # Prepare file for download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name='Results')
        
        buffer.seek(0)
        
        # Generate a timestamp for the file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_file_name = f"{st.session_state.file_name}_results_{timestamp}.{st.session_state.file_extension}"
        
        # Create centered download button with more prominent styling
        st.markdown("<div style='text-align: center; margin: 3rem 0;'>", unsafe_allow_html=True)
        st.markdown("<p>Your comparison selections have been saved. Download your results file below:</p>", unsafe_allow_html=True)
        st.download_button(
            label="Download Results Excel",
            data=buffer,
            file_name=download_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add button to start over
        st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
        if st.button("Start New Comparison", key="new_comparison"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<div class='footer'>Text Preference Tool</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()