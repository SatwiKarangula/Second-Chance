import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const sendEvent = async ({
  event_type,
  session_id,
  cart_value,
  event_key,
  source = "web",
  metadata = {},
}) => {
  const response = await api.post(
    "/api/events",
    {
      event_type,
      session_id,
      cart_value,
      event_key,
      source,
      metadata,
    }
  );

  return response.data;
};

export default api;