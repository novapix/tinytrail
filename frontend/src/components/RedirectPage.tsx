import { useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { URLResponse } from '@/types/types.ts';

export default function RedirectPage() {
  const { shortCode } = useParams<{ shortCode: string }>();
  const navigate = useNavigate();
  const requestMade = useRef(false);

  useEffect(() => {
    const fetchLongURL = async () => {
      if (requestMade.current) return;
      requestMade.current = true;

      try {
        console.log('Fetching long URL for short code:', shortCode);

        const response = await axios.get<URLResponse>(
          `http://127.0.0.1:8000/shorten/${shortCode}`
        );

        if (response.status === 200 && response.data.url) {
          console.log('Fetched long URL:', response.data.url);
          window.location.href = response.data.url;
        } else {
          console.error('Invalid response:', response);
          alert('Short code not found');
          navigate('/');
        }
      } catch (error) {
        console.error('Failed to fetch the long URL:', error);
        alert('Failed to fetch the long URL');
        navigate('/');
      }
    };

    fetchLongURL().catch((error) => {
      console.error('Unhandled error in fetchLongURL:', error);
    });
  }, [shortCode, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <h1 className="text-2xl font-bold">Redirecting...</h1>
    </div>
  );
}
