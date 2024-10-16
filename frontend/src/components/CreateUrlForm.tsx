import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRightIcon } from '@heroicons/react/24/solid';
import { URLFormProps } from '@/types/types.ts';

export default function URLShortener({ isOpen }: URLFormProps) {
  const [longURL, setLongURL] = useState('');

  const handleSubmit = (e: { preventDefault: () => void }) => {
    e.preventDefault();
    // API CALL PENDING
    console.log('Shortening URL:', longURL);
  };
  if (!isOpen) return null;

  return (
    <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-3xl font-bold text-center">
          URL Shortener
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
            <ArrowRightIcon className="ml-2 h-5 w-5" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
