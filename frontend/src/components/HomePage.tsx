import URLShortener from '@/components/CreateUrlForm.tsx';

export default function HomePage() {
  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-100 to-gray-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full mx-auto">
        <header className="text-center mb-16">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            Shorten Your Links
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Create short, memorable links in seconds. Perfect for social media, marketing campaigns, or personal use.
          </p>
        </header>

        <main className="flex justify-center w-full">
          <div className="w-full">
            <URLShortener />
          </div>
        </main>

        <footer className="mt-20 text-center">
          <p className="text-gray-500">&copy; 2024 Tinytrail. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
}
