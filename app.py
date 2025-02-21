import streamlit as st
import pandas as pd
import numpy as np
from puzzle import solve_calendar, BOARD_LAYOUT, ROWS, COLS

def create_streamlit_app():
    st.title("Calendar Puzzle Solver. Made by Thejas and Arya only for DSW")
    
    st.write("""
    This app solves the calendar puzzle by finding a way to cover all squares except for a chosen month and date.
    The pieces can be rotated and flipped to fit the puzzle.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        selected_month = st.selectbox("Select Month", months)
    
    with col2:
        days = [str(i) for i in range(1, 32)]
        selected_day = st.selectbox("Select Day", days)
    
    if st.button("Solve Puzzle"):
        solution = solve_calendar(selected_month, selected_day)
        
        if solution is None:
            st.error(f"No solution found for {selected_month} {selected_day}!")
        else:
            st.success(f"Solution found for {selected_month} {selected_day}!")
            
            st.write("### Solution Visualization")
            
            # Create a color mapping for pieces
            color_map = {
                "Red": "#FF0000",
                "Blue": "#0000FF",
                "Green": "#00FF00",
                "Yellow": "#FFFF00",
                "LightBlue": "#ADD8E6",
                "Purple": "#800080",
                "Pink": "#FFC0CB",
                "Box": "#8B4513"
            }
            
            # Create the display data
            display_data = []
            styles = []
            for r in range(ROWS):
                row_data = []
                row_styles = []
                for c in range(COLS):
                    label = BOARD_LAYOUT[r][c]
                    if label == "X":
                        row_data.append("")
                        row_styles.append('background-color: #D3D3D3')
                    elif (r, c) not in solution:
                        row_data.append(label)
                        if label in [selected_month, selected_day]:
                            row_styles.append('background-color: #FFFFFF; color: #000000; font-weight: bold')
                        else:
                            row_styles.append('background-color: #F0F0F0')
                    else:
                        piece_color = solution[(r, c)]
                        row_data.append("■")
                        row_styles.append(f'background-color: {color_map[piece_color]}')
                display_data.append(row_data)
                styles.append(row_styles)
            
            df = pd.DataFrame(display_data)
            
            # Create a style DataFrame with the same shape as the data
            style_df = pd.DataFrame(styles)
            
            # Apply styles using a function that references the pre-computed styles
            def style_cells(df):
                return style_df
            
            styled_df = df.style.apply(lambda _: style_df, axis=None)
            st.dataframe(styled_df, use_container_width=True)
            
            # Add legend
            st.write("### Piece Colors")
            legend_cols = st.columns(4)
            for idx, (piece, color) in enumerate(color_map.items()):
                col_idx = idx % 4
                with legend_cols[col_idx]:
                    st.markdown(
                        f'<div style="background-color: {color}; padding: 10px; '
                        f'margin: 5px; color: black; border-radius: 5px; '
                        f'text-align: center;">{piece}</div>', 
                        unsafe_allow_html=True
                    )

            # Add helpful note
            st.info("""
            In the visualization above:
            - Colored squares show the placement of each puzzle piece
            - White squares show the uncovered month and date
            - Gray squares are not part of the puzzle
            """)

if __name__ == "__main__":
    create_streamlit_app()