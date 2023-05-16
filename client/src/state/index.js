import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  mode: "dark",
  userId: "c34cb078-3bea-427c-bafc-49151ec53064",
};

export const globalSlice = createSlice({
  name: "global",
  initialState,
  reducers: {
    setMode: (state) => {
      state.mode = state.mode === "light" ? "dark" : "light";
    },
  },
});

export const { setMode } = globalSlice.actions;

export default globalSlice.reducer;
