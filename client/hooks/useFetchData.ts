
import { useState, useEffect } from 'react';
import api from '../services/api';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

const useFetchData = <T,>(endpoint: string): FetchState<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get<T>(endpoint);
        setData(response.data);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'An unknown error occurred.');
        console.error('Fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endpoint]);

  return { data, loading, error };
};

export default useFetchData;
