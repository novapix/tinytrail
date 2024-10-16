import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRightIcon } from '@heroicons/react/24/solid';
import { URLFormProps } from '@/types/types.ts';

export default function UpdateUrlForm({ isOpen }: URLFormProps) {
  const [shortCode, setShortCode] = useState('');
  const [newUrl, setNewUrl] = useState('');

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`/shorten/${shortCode}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ shortCode, newUrl }),
      });

      if (response.ok) {
        alert('URL updated successfully!');
        setShortCode('');
        setNewUrl('');
      } else {
        alert('Error updating URL');
      }
    } catch (error) {
      alert('Failed to update URL');
    }
  };
  if (!isOpen) return null;
  return (
    <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-green-500 to-teal-600 text-white shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-3xl font-bold text-center">
          Update URL
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleUpdate} className="space-y-6">
          <div>
            <label
              htmlFor="shortCode"
              className="block text-lg font-medium mb-2"
            >
              Enter Short Code
            </label>
            <Input
              id="shortCode"
              type="text"
              placeholder="Enter your short code"
              value={shortCode}
              onChange={(e) => setShortCode(e.target.value)}
              required
              className="mt-1 bg-white/20 text-white placeholder-white/60 border-white/40 focus:border-white focus:ring-white"
            />
          </div>
          <div>
            <label htmlFor="newUrl" className="block text-lg font-medium mb-2">
              Enter New URL
            </label>
            <Input
              id="newUrl"
              type="url"
              placeholder="https://example.com/my-new-url"
              value={newUrl}
              onChange={(e) => setNewUrl(e.target.value)}
              required
              className="mt-1 bg-white/20 text-white placeholder-white/60 border-white/40 focus:border-white focus:ring-white"
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-white text-green-600 hover:bg-green-100 transition-colors duration-300 text-lg py-6 rounded-full font-semibold flex items-center justify-center"
          >
            Update URL
            <ArrowRightIcon className="ml-2 h-5 w-5" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
