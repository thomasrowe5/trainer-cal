'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_URL;
if (!API && typeof window !== 'undefined') {
  console.warn('NEXT_PUBLIC_API_URL is not defined. API calls will fail.');
}

interface Slot {
  start_time: string;
  end_time: string;
}

export default function BookPage() {
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSlots = async () => {
      if (!API) {
        setError('API URL is not configured');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`${API}/availability`, {
          params: { user_id: 1 },
        });
        setSlots(response.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load availability');
      } finally {
        setLoading(false);
      }
    };

    fetchSlots();
  }, []);

  const handleBook = async (slot: Slot) => {
    if (!API) {
      alert('API URL is not configured');
      return;
    }

    try {
      const response = await axios.post(`${API}/checkout`, {
        user_id: 1,
        start_time: slot.start_time,
        end_time: slot.end_time,
        price: 20,
      });
      window.location.href = response.data.url;
    } catch (err: any) {
      alert('Error creating checkout session: ' + err.message);
    }
  };

  if (loading) {
    return <p className="mt-10 text-center">Loading slots...</p>;
  }

  if (error) {
    return (
      <p className="mt-10 text-center text-red-500" role="alert">
        {error}
      </p>
    );
  }

  return (
    <main className="mx-auto max-w-xl p-6">
      <h1 className="mb-4 text-2xl font-semibold">Book a Session</h1>
      {slots.length === 0 ? (
        <p>No available slots right now.</p>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {slots.map((slot) => (
            <button
              key={slot.start_time}
              onClick={() => handleBook(slot)}
              className="rounded-lg border p-3 transition hover:bg-blue-600 hover:text-white"
              type="button"
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
