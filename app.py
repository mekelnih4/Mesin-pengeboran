import streamlit as st

# Title
st.title('Mesin Pengeboran')

# DB Section
L4_Xoffset = 0
L4_Yoffset = 0
L5_Xoffset = 0
L5_Yoffset = 0
L6_Xoffset = 0
L6_Yoffset = 0

# Example inputs
L4_value = st.slider('L4 Value', 0, 100)
L5_value = st.slider('L5 Value', 0, 100)
L6_value = st.slider('L6 Value', 0, 100)

# Output with offsets
st.write(f'L4 Output: {L4_value + L4_Xoffset}, Y Offset: {L4_Yoffset}')
st.write(f'L5 Output: {L5_value + L5_Xoffset}, Y Offset: {L5_Yoffset}')
st.write(f'L6 Output: {L6_value + L6_Xoffset}, Y Offset: {L6_Yoffset}')