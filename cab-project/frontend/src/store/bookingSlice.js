import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  pickup: '',
  destination: '',
  selectedCab: null,
  bookingStatus: 'idle',
};

export const bookingSlice = createSlice({
  name: 'booking',
  initialState,
  reducers: {
    setPickup: (state, action) => {
      state.pickup = action.payload;
    },
    setDestination: (state, action) => {
      state.destination = action.payload;
    },
    setSelectedCab: (state, action) => {
      state.selectedCab = action.payload;
    },
    setBookingStatus: (state, action) => {
      state.bookingStatus = action.payload;
    },
  },
});

export const { setPickup, setDestination, setSelectedCab, setBookingStatus } = bookingSlice.actions;
export default bookingSlice.reducer;