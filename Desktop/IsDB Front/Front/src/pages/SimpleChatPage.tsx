import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Wand2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export function SimpleChatPage() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!question.trim()) {
      toast({
        title: "Question Required",
        description: "Please enter a question.",
        variant: "destructive",
      });
      return;
    }

    // Generate a unique message ID
    const newMessageId = Date.now().toString();
    
    // Add the user's message
    setMessages((prev) => [
      ...prev,
      {
        id: newMessageId,
        role: 'user',
        content: question,
      },
    ]);

    // Simulate API call
    setLoading(true);
    
    // Simulate a delay for the API response
    setTimeout(() => {
      // Generate a mock response based on the question
      const response = generateMockResponse(question);
      
      // Add the assistant's response
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: response,
        },
      ]);
      
      setLoading(false);
      setQuestion(''); // Clear the question input
    }, 1500);
  };

  // Function to generate a mock response
  const generateMockResponse = (question: string) => {
    const questionLower = question.toLowerCase();
    
    // Some simple pattern matching for more realistic responses
    if (questionLower.includes('hello') || questionLower.includes('hi')) {
      return "Hello! How can I help you today?";
    } else if (questionLower.includes('how are you')) {
      return "I'm functioning well, thank you for asking! How can I assist you?";
    } else if (questionLower.includes('weather')) {
      return "I don't have access to real-time weather data, but I can help you find weather information if you provide a location and time frame.";
    } else if (questionLower.includes('help')) {
      return "I'd be happy to help! Please provide more details about what you need assistance with, and I'll do my best to provide relevant information.";
    } else if (questionLower.length < 10) {
      return "I need a bit more information to provide a helpful response. Could you please elaborate on your question?";
    } else {
      // Generic response for other questions
      return `Thank you for your question about "${question.substring(0, 30)}${question.length > 30 ? '...' : ''}". \n\nBased on my understanding, this relates to ${extractTopic(question)}. The answer would depend on several factors including ${generateFactors()}. \n\nWould you like me to elaborate on any specific aspect of this topic?`;
    }
  };

  // Helper function to extract a topic from the question
  const extractTopic = (question: string) => {
    const words = question.split(' ');
    // Find nouns (approximation - words with 4+ characters)
    const potentialTopics = words.filter(word => word.length > 4);
    
    if (potentialTopics.length > 0) {
      return potentialTopics[Math.floor(Math.random() * potentialTopics.length)]
        .replace(/[.,;:!?]/g, '');
    }
    return "the subject you mentioned";
  };

  // Helper function to generate random factors
  const generateFactors = () => {
    const factors = [
      "context", "specific conditions", "timeline", "resources available", 
      "underlying assumptions", "related systems", "historical precedents",
      "current technologies", "environmental constraints", "stakeholder requirements"
    ];
    
    // Randomly select 2-3 factors
    const numFactors = Math.floor(Math.random() * 2) + 2;
    const selectedFactors = [];
    
    for (let i = 0; i < numFactors; i++) {
      const randomIndex = Math.floor(Math.random() * factors.length);
      selectedFactors.push(factors[randomIndex]);
      factors.splice(randomIndex, 1); // Remove to avoid duplicates
    }
    
    return selectedFactors.join(", ");
  };

  const handleSampleQuestion = () => {
    setQuestion("Can you explain how machine learning works in simple terms?");
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold tracking-tight mb-4">Challenge 3</h1>
        <p className="text-muted-foreground mb-8">
          Ask questions and get straightforward answers.
        </p>
      </motion.div>

      <div className="flex flex-col space-y-8">
        {/* Chat message display */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Conversation</CardTitle>
              <CardDescription>
                Your chat history will appear here
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {messages.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    Start chatting to see your conversation here...
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={cn(
                        "p-4 rounded-lg",
                        message.role === "user"
                          ? "bg-primary/10 text-primary-foreground ml-auto max-w-[80%]"
                          : "bg-muted max-w-[80%]"
                      )}
                    >
                      <div className="font-semibold">
                        {message.role === "user" ? "You" : "Assistant"}:
                      </div>
                      <div className="mt-1 whitespace-pre-wrap">{message.content}</div>
                    </div>
                  ))
                )}
                {loading && (
                  <div className="bg-muted p-4 rounded-lg max-w-[80%]">
                    <div className="font-semibold">Assistant:</div>
                    <div className="mt-1">
                      <span className="inline-block w-2 h-2 bg-primary rounded-full animate-bounce"></span>
                      <span className="inline-block w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                      <span className="inline-block w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
        
        {/* Input area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="question" className="block text-sm font-medium">
                Your Question
              </label>
              <Textarea
                id="question"
                placeholder="Type your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="min-h-32"
                rows={4}
              />
            </div>
            
            <div className="flex items-center justify-between gap-4">
              <Button 
                type="button" 
                variant="outline"
                onClick={handleSampleQuestion}
                className="flex items-center gap-2"
              >
                <Wand2 className="h-4 w-4" />
                <span>Sample</span>
              </Button>
              
              <Button 
                type="submit" 
                disabled={loading || !question.trim()}
                className="flex items-center gap-2"
              >
                <span>{loading ? 'Processing...' : 'Send'}</span>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  );
}