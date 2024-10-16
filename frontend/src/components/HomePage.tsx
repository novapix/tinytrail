import { useState } from 'react';
import URLShortener from '@/components/CreateUrlForm.tsx';
import UpdateUrlForm from '@/components/UpdateUrlForm';
import DeleteUrlForm from '@/components/DeleteUrlForm';

export default function HomePage() {
  const [openCard, setOpenCard] = useState<'create' | 'update' | 'delete'>(
    'create'
  ); // Default to 'create'

  const handleToggle = (card: 'create' | 'update' | 'delete') => {
    setOpenCard(openCard === card ? 'create' : card); // reset to 'create' if the same card is clicked
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-100 to-gray-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full mx-auto">
        <header className="text-center mb-16">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            Shorten Your Links
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Create short, memorable links in seconds. Perfect for social media,
            marketing campaigns, or personal use.
          </p>
        </header>

        <main className="flex flex-col items-center space-y-12 w-full">
          <button
            onClick={() => handleToggle('create')}
            className="text-lg text-gray-700"
          >
            Create URL
          </button>
          <URLShortener isOpen={openCard === 'create'} />
          <button
            onClick={() => handleToggle('update')}
            className="text-lg text-gray-700"
          >
            Update URL
          </button>
          <UpdateUrlForm isOpen={openCard === 'update'} />
          <button
            onClick={() => handleToggle('delete')}
            className="text-lg text-gray-700"
          >
            Delete URL
          </button>

          <DeleteUrlForm isOpen={openCard === 'delete'} />
        </main>

        <footer className="mt-20 fixed text-center inset-x-0">
          <p className="text-gray-500">
            &copy; 2024 Tinytrail. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
}
