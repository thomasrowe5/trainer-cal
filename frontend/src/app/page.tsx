export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-gray-800">
      <h1 className="text-4xl font-bold mb-4">TrainerCal</h1>
      <p className="text-lg mb-8">
        Book. Pay. Train. — simple scheduling and payments for coaches.
      </p>
      <a href="/book" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Book a Demo
      </a>
    </main>
  );
}
