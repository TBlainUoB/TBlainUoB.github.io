import streamlit as st
import json
import plotly.graph_objects as go
from collections import defaultdict
import os
import glob

# Function to extract intents and branches from JSON files
def extract_conversation_flow(json_data):
    sequence = []
    
    if "turns" not in json_data:
        return sequence
    
    for turn in json_data["turns"]:
        states = []
        
        if "events" in turn:
            for event in turn["events"]:
                # Check for intent events (IntRec*)
                if "name" in event and event["name"].startswith("IntRec") and "value" in event:
                    states.append(("Intent", event["value"]))
                
                # Check for branch events (BranchName*)
                if "name" in event and event["name"].startswith("BranchName") and "value" in event:
                    states.append(("Branch", event["value"]))
        
        # Add all states in this turn to the sequence
        sequence.extend(states)
    
    return sequence

# Build Sankey diagram data from all conversations
def build_sankey_data(all_sequences):
    # Track transitions between states
    transitions = defaultdict(int)
    all_nodes = set()
    
    for sequence in all_sequences:
        # Create pairs of consecutive states
        for i in range(len(sequence) - 1):
            source_type, source_value = sequence[i]
            target_type, target_value = sequence[i + 1]
            
            source = f"{source_type}: {source_value}"
            target = f"{target_type}: {target_value}"
            
            all_nodes.add(source)
            all_nodes.add(target)
            transitions[(source, target)] += 1
    
    # Convert to format needed for Plotly Sankey
    nodes = list(all_nodes)
    sources = []
    targets = []
    values = []
    
    for (source, target), value in transitions.items():
        sources.append(nodes.index(source))
        targets.append(nodes.index(target))
        values.append(value)
    
    return {
        "nodes": nodes,
        "sources": sources,
        "targets": targets,
        "values": values
    }

# Create Sankey diagram using Plotly
def create_sankey(data):
    if not data["nodes"]:
        return None
    
    # Set colors (green for intents, blue for branches)
    colors = ["rgba(44, 160, 44, 0.8)" if node.startswith("Intent") else "rgba(31, 119, 180, 0.8)" 
              for node in data["nodes"]]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=data["nodes"],
            color=colors
        ),
        link=dict(
            source=data["sources"],
            target=data["targets"],
            value=data["values"]
        )
    )])
    
    fig.update_layout(
        title_text="Conversation Flow",
        font_size=10,
        height=600
    )
    
    return fig

# Main Streamlit app
def main():
    st.title("Conversation Flow Visualization")
    
    # File uploader (allow multiple JSON files)
    uploaded_files = st.file_uploader("Upload conversation JSON files", 
                                     type=["json"], 
                                     accept_multiple_files=True)
    
    # Folder input option
    folder_path = st.text_input("Or enter folder path containing JSON files:")
    
    if st.button("Process Files"):
        all_sequences = []
        
        # Process uploaded files
        if uploaded_files:
            for file in uploaded_files:
                try:
                    json_data = json.load(file)
                    sequence = extract_conversation_flow(json_data)
                    if sequence:
                        all_sequences.append(sequence)
                        st.success(f"Processed {file.name}: found {len(sequence)} events")
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
        
        # Process files from folder
        if folder_path and os.path.isdir(folder_path):
            json_files = glob.glob(os.path.join(folder_path, "*.json"))
            for file_path in json_files:
                try:
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                    sequence = extract_conversation_flow(json_data)
                    if sequence:
                        all_sequences.append(sequence)
                        st.success(f"Processed {os.path.basename(file_path)}: found {len(sequence)} events")
                except Exception as e:
                    st.error(f"Error processing {file_path}: {e}")
        
        if all_sequences:
            # Build and display Sankey diagram
            sankey_data = build_sankey_data(all_sequences)
            
            if sankey_data["nodes"]:
                sankey_fig = create_sankey(sankey_data)
                st.plotly_chart(sankey_fig, use_container_width=True)
                
                # Display some statistics
                st.subheader("Statistics")
                st.write(f"Total conversations: {len(all_sequences)}")
                st.write(f"Unique states: {len(sankey_data['nodes'])}")
                st.write(f"Total transitions: {sum(sankey_data['values'])}")
            else:
                st.warning("Not enough data to create a flow diagram.")
        else:
            st.warning("No valid conversation data found in the files.")
    
    # Display instructions
    st.markdown("""
    ### How to use this app:
    1. Upload JSON files containing conversation data, or enter a folder path
    2. Click "Process Files" to generate the visualization
    3. The Sankey diagram shows how users flow through different intents and branches
    
    Green nodes represent intents (IntRec*) and blue nodes represent branches/turns (BranchName*).
    """)

if __name__ == "__main__":
    main()
