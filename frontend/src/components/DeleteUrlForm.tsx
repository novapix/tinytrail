import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrashIcon } from '@heroicons/react/24/solid';
import { URLFormProps } from '@/types/types.ts';

export default function DeleteUrlForm({ isOpen }: URLFormProps) {
  const [deleteCode, setDeleteCode] = useState('');

  // Function to handle URL deletion
  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`/shorten/${deleteCode}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        alert('URL deleted successfully!');
        setDeleteCode('');
      } else {
        alert('Error deleting URL');
      }
    } catch (error) {
      alert('Failed to delete URL');
    }
  };
  if (!isOpen) return null;

  return (
    <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-red-500 to-red-700 text-white shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-3xl font-bold text-center">
          Delete URL
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleDelete} className="space-y-6">
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
              placeholder="Enter the short code to delete"
              value={deleteCode}
              onChange={(e) => setDeleteCode(e.target.value)}
              required
              className="mt-1 bg-white/20 text-white placeholder-white/60 border-white/40 focus:border-white focus:ring-white"
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-white text-red-600 hover:bg-red-100 transition-colors duration-300 text-lg py-6 rounded-full font-semibold flex items-center justify-center"
          >
            Delete URL
            <TrashIcon className="ml-2 h-5 w-5" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
