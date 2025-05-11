import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Wand2, ArrowUp, ArrowDown } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { useToast } from '@/hooks/use-toast';

interface ListItem {
  id: string;
  name: string;
  percentage: number;
  description: string;
}

export function QuestionPage() {
  const [context, setContext] = useState('');
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ListItem[]>([]);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
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

    // Simulate API call
    setLoading(true);
    
    // Simulate a delay for the API response
    setTimeout(() => {
      // Generate a mock response with list items
      const mockResults = generateMockResults(context, question);
      setResults(mockResults);
      setLoading(false);
    }, 1500);
  };

  // Function to generate mock results
  const generateMockResults = (context: string, question: string): ListItem[] => {
    // Extract some words from context to use in results
    const contextWords = context
      .split(' ')
      .filter(word => word.length > 4)
      .map(word => word.replace(/[.,;:!?]/g, ''));
    
    // Default items if context doesn't have enough words
    const defaultItems = [
      "Analysis", "Recommendation", "Solution", "Approach", 
      "Method", "Framework", "Strategy", "Insight"
    ];
    
    // Generate 4-6 results
    const numResults = Math.floor(Math.random() * 3) + 4; // 4-6 results
    const results: ListItem[] = [];
    
    for (let i = 0; i < numResults; i++) {
      // Get a word from context or use default
      let name;
      if (contextWords.length > i) {
        name = contextWords[i].charAt(0).toUpperCase() + contextWords[i].slice(1);
      } else {
        name = defaultItems[i % defaultItems.length];
      }
      
      // Generate a percentage
      const percentage = Math.floor(Math.random() * 60) + 40; // 40-99%
      
      // Generate a description
      const description = `This ${name.toLowerCase()} appears to be related to your question about ${
        question.split(' ').slice(0, 3).join(' ')
      }... The analysis suggests a ${percentage}% correlation with the context provided.`;
      
      results.push({
        id: i.toString(),
        name,
        percentage,
        description
      });
    }
    
    // Sort by percentage (descending by default)
    return results.sort((a, b) => b.percentage - a.percentage);
  };

  const handleSort = () => {
    const newOrder = sortOrder === 'desc' ? 'asc' : 'desc';
    setSortOrder(newOrder);
    
    // Sort the results
    const sortedResults = [...results].sort((a, b) => {
      return newOrder === 'desc' 
        ? b.percentage - a.percentage 
        : a.percentage - b.percentage;
    });
    
    setResults(sortedResults);
  };

  const handleSampleQuestion = () => {
    setContext("Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention. Machine learning algorithms are often categorized as supervised, unsupervised, semi-supervised, or reinforcement learning.");
    setQuestion("What are the best machine learning methods for text classification?");
  };

  return (
    <div className="w-full max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold tracking-tight mb-4">Situation Analysis</h1>
        <p className="text-muted-foreground mb-8">
          Get ranked results with percentages and explanations.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left side - Input fields */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
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
                className="min-h-32 resize-y"
                rows={6}
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
                className="resize-none"
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
                disabled={loading || !context.trim() || !question.trim()}
                className="flex items-center gap-2"
              >
                <span>{loading ? 'Processing...' : 'Analyze'}</span>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </motion.div>
        
        {/* Right side - Results Display */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Results</CardTitle>
                <CardDescription>
                  Ranked analysis of your question
                </CardDescription>
              </div>
              
              {results.length > 0 && (
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={handleSort}
                  className="flex items-center gap-1"
                >
                  Sort 
                  {sortOrder === 'desc' ? (
                    <ArrowDown className="h-4 w-4" />
                  ) : (
                    <ArrowUp className="h-4 w-4" />
                  )}
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="py-12">
                  <div className="flex justify-center items-center gap-2 mb-4">
                    <div className="h-2 w-2 bg-primary rounded-full animate-bounce"></div>
                    <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                  <p className="text-center text-muted-foreground">Analyzing your question...</p>
                </div>
              ) : results.length > 0 ? (
                <div className="space-y-6">
                  {results.map((item, index) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: 0.1 * index }}
                      className="border rounded-lg p-4"
                    >
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="font-medium text-lg">{item.name}</h3>
                        <span className="font-bold text-lg">{item.percentage}%</span>
                      </div>
                      
                      <Progress 
                        value={item.percentage} 
                        className="h-2 mb-3"
                        // Add color based on percentage
                        color={
                          item.percentage > 80 ? "bg-green-500" :
                          item.percentage > 60 ? "bg-blue-500" :
                          item.percentage > 40 ? "bg-yellow-500" : "bg-red-500"
                        }
                      />
                      
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="py-12 text-center text-muted-foreground">
                  <p>Enter your context and question to see results.</p>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}