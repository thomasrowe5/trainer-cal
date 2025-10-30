'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export default function DemoBookingPage() {
  const [slots, setSlots] = useState<{ start_time: string; end_time: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAvailability() {
      if (!API_BASE_URL) {
        setError('API URL is not configured');
        setLoading(false);
        return;
      }

      try {
        const res = await axios.get(`${API_BASE_URL}/availability`, {
          params: { user_id: 1 },
        });
        setSlots(res.data);
      } catch (err: any) {
        setError(err.message || 'Error loading availability');
      } finally {
        setLoading(false);
      }
    }
    fetchAvailability();
  }, []);

  async function handleBook(slot: { start_time: string; end_time: string }) {
    if (!API_BASE_URL) {
      alert('API URL is not configured');
      return;
    }

    try {
      const res = await axios.post(`${API_BASE_URL}/checkout`, {
        user_id: 1,
        start_time: slot.start_time,
        end_time: slot.end_time,
        price: 20,
      });
      window.location.href = res.data.url; // redirect to Stripe Checkout
    } catch (err: any) {
      alert('Error creating checkout session: ' + err.message);
    }
  }

  if (loading) return <p className="text-center mt-10">Loading slots...</p>;
  if (error) return <p className="text-center text-red-500 mt-10">{error}</p>;

  return (
    <main className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Book a Demo Session</h1>
      {slots.length === 0 ? (
        <p>No available slots right now.</p>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {slots.map((slot, i) => (
            <button
              key={i}
              onClick={() => handleBook(slot)}
              className="border rounded-lg p-3 hover:bg-blue-600 hover:text-white transition"
            >
              {new Date(slot.start_time).toLocaleString()} →{' '}
              {new Date(slot.end_time).toLocaleTimeString()}
            </button>
          ))}
        </div>
      )}
    </main>
  );
}
