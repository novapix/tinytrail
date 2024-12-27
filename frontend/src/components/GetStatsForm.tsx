import React, { useRef, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import axios from 'axios';
import { URLResponse, URLFormProps } from '@/types/types.ts';

export default function GetStatsForm({ isOpen }: URLFormProps) {
  const [shortCode, setShortCode] = useState('');
  const [stats, setStats] = useState<URLResponse | null>(null);
  const requestMade = useRef(false);

  const statsHandler = async (e: React.FormEvent) => {
    if (requestMade.current) return;
    requestMade.current = true;
    e.preventDefault();
    try {
      const response = await axios.get<URLResponse>(
        `http://127.0.0.1:8000/${shortCode}/stats`
      );
      if (response.status === 200 && response.data) {
        setStats(response.data);
        console.log(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };
  if (!isOpen) return null;

  return (
    <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-yellow-500 to-yellow-700 text-white shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-3xl font-bold text-center">
          Get URL Stats
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={statsHandler} className="space-y-6">
          <div>
            <label
              htmlFor="shortCode"
              className="block text-lg font-medium mb-2"
            >
              Enter Short Code
            </label>
            <Input
              id="shortCode"
              placeholder="Enter Short Code to Get Details"
              value={shortCode}
              onChange={(e) => setShortCode(e.target.value)}
              required
              className="mt-1 bg-white/20 text-white placeholder-white/60 border-white/40 focus:border-white focus:ring-white"
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-white text-yellow-600 hover:bg-yellow-100 transition-colors duration-300 text-lg py-6 rounded-full font-semibold flex items-center justify-center"
          >
            Get Stats
          </Button>
        </form>
        {stats && (
          <div className="mt-4 text-center text-black">
            <p>ID: {stats.id}</p>
            <p>URL: {stats.url}</p>
            <p>Short Code: {stats.shortCode}</p>
            <p>Created At: {stats.createdAt}</p>
            <p>Updated At: {stats.updatedAt}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
