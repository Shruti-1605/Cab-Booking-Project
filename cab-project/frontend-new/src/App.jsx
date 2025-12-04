import React from 'react';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { store } from './store/store';
import SimpleBookingForm from './components/SimpleBookingForm';

const queryClient = new QueryClient();

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <div className="min-h-screen bg-gray-100 p-4">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-center mb-8">Cab Booking App</h1>
            <SimpleBookingForm />
          </div>
        </div>
      </QueryClientProvider>
    </Provider>
  );
}

export default App;