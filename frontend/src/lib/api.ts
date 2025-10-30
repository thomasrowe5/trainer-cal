import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_BASE_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not defined");
}

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getHealth = async () => {
  const response = await client.get("/health");
  return response.data;
};

export const getAvailability = async (userId: string) => {
  const response = await client.get("/availability", {
    params: { user_id: userId },
  });
  return response.data;
};

type CheckoutPayload = {
  user_id: string;
  start_time: string;
  end_time: string;
  price: string;
};

export const postCheckout = async (data: CheckoutPayload) => {
  const response = await client.post("/checkout", data);
  return response.data;
};

export const getBookings = async (userId: string) => {
  const response = await client.get("/bookings", {
    params: { user_id: userId },
  });
  return response.data;
};

export const cancelBooking = async (bookingId: string) => {
  const response = await client.post("/bookings/cancel", {
    booking_id: bookingId,
  });
  return response.data;
};
