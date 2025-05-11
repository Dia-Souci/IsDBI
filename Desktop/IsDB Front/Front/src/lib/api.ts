import { toast } from '@/hooks/use-toast';

interface ApiResponse {
  Analysis: string;
  suggestion: string;
  validation: string;
}

export async function sendRequest(endpoint: string, data: { context: string; question: string }): Promise<ApiResponse | null> {
  try {
    const response = await fetch(`http://localhost:8080${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('API request failed:', error);
    toast({
      title: "Error",
      description: "Failed to get response from the server. Make sure the Python backend is running.",
      variant: "destructive",
    });
    return null;
  }
}