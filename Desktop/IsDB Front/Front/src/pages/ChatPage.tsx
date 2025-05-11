import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Wand2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';
import { sendRequest } from '@/lib/api';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export function ChatPage() {
  const [context, setContext] = useState('');
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!context.trim()) {
      toast({
        title: "Context Required",
        description: "Please provide some context for your question.",
        variant: "destructive",
      });
      return;
    }
    
    if (!question.trim()) {
      toast({
        title: "Question Required",
        description: "Please enter a question.",
        variant: "destructive",
      });
      return;
    }

    const newMessageId = Date.now().toString();
    
    setMessages((prev) => [
      ...prev,
      {
        id: newMessageId,
        role: 'user',
        content: question,
      },
    ]);

    setLoading(true);
    
    const response = await sendRequest('/challenge_1', { context, question });
    
    if (response) {
      const { Analysis, suggestion, validation } = response;
      
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: `Analysis:\n${Analysis}\n\nSuggestion:\n${suggestion}\n\nValidation:\n${validation}`,
        },
      ]);
    }
    
    setLoading(false);
    setQuestion('');
  };

  const handleSampleQuestion = () => {
    setContext("The water cycle, also known as the hydrologic cycle, describes the continuous movement of water on, above and below the surface of the Earth. Water can change states among liquid, vapor, and ice at various places in the water cycle.");
    setQuestion("How does evaporation contribute to the water cycle?");
  };

  return (
    <div className="w-full max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold tracking-tight mb-4">Context Analysis</h1>
        <p className="text-muted-foreground">
          Provide context for more accurate responses to your questions.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="w-full"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="context" className="block text-sm font-medium">
                Context
              </label>
              <Textarea
                id="context"
                placeholder="Enter background information or context..."
                value={context}
                onChange={(e) => setContext(e.target.value)}
                className="min-h-[200px] resize-y"
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="question" className="block text-sm font-medium">
                Your Question
              </label>
              <Textarea
                id="question"
                placeholder="Ask your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="min-h-[100px] resize-none"
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
                disabled={loading || !context.trim() || !question.trim()}
                className="flex items-center gap-2"
              >
                <span>{loading ? 'Processing...' : 'Send'}</span>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="w-full"
        >
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Conversation</CardTitle>
              <CardDescription>
                Questions and answers will appear here
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
                {messages.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    Your conversation will appear here...
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
      </div>
    </div>
  );
}