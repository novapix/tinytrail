import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CirclePlus } from 'lucide-react';
import { URLFormProps } from '@/types/types.ts';

export default function URLShortener({ isOpen }: URLFormProps) {
  const [longURL, setLongURL] = useState('');
  const [shortCode, setShortCode] = useState('');

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/shorten`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: longURL }),
      });

      if (response.ok) {
        const data = await response.json();
        setShortCode(data.shortCode);
        alert('URL created successfully!');
        setLongURL('');
      } else {
        alert('Error updating URL');
      }
    } catch (error) {
      alert('Failed to update URL');
    }
    // API CALL PENDING

    console.log('Shortening URL:', longURL);
  };
  if (!isOpen) return null;

  return (
    <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-3xl font-bold text-center">
          Create New URL
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="longLink"
              className="block text-lg font-medium mb-2"
            >
              Enter your long URL
            </label>
            <Input
              id="longLink"
              type="url"
              placeholder="https://example.com/my-long-url"
              value={longURL}
              onChange={(e) => setLongURL(e.target.value)}
              required
              className="mt-1 bg-white/20 text-white placeholder-white/60 border-white/40 focus:border-white focus:ring-white"
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-white text-blue-600 hover:bg-blue-100 transition-colors duration-300 text-lg py-6 rounded-full font-semibold flex items-center justify-center"
          >
            Shorten it
            <CirclePlus />
          </Button>
        </form>
        {shortCode && (
          <div className="mt-4 text-center">
            <p className="text-lg">
              Short URL : {window.location.href}
              {shortCode}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
