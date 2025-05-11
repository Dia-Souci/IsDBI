import { motion } from 'framer-motion';
import { Home as HomeIcon, MessageSquare, List, MessageCircle, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Link } from 'react-router-dom';

export function HomePage() {
  const features = [
    {
      title: "Challenge Set 1",
      icon: <MessageSquare className="h-8 w-8 text-primary" />,
      description: "Ask questions with context for more accurate answers",
      path: "/chat",
      color: "bg-blue-500/10 dark:bg-blue-500/20",
    },
    {
      title: "Challenge Set 2",
      icon: <List className="h-8 w-8 text-primary" />,
      description: "Get organized list responses with percentages and explanations",
      path: "/question",
      color: "bg-green-500/10 dark:bg-green-500/20",
    },
    {
      title: "Challenge Set 3",
      icon: <MessageCircle className="h-8 w-8 text-primary" />,
      description: "Quick paragraph-based questions and answers",
      path: "/simple-chat",
      color: "bg-purple-500/10 dark:bg-purple-500/20",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center space-y-12">
      <section className="w-full max-w-5xl text-center space-y-4 pt-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            IsDBI Hack <span className="text-primary">RAG System</span>
          </h1>
          <p className="mt-6 text-lg text-muted-foreground max-w-3xl mx-auto">
            Ask questions in context and get intelligent, structured responses tailored to IsDBI needs.
          </p>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex flex-wrap justify-center gap-4 mt-8"
        >
          <Button asChild size="lg" className="gap-2">
            <Link to="/chat">
              Get Started <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link to="https://github.com/Dia-Souci/IsDBI.git" target="_blank" rel="noopener noreferrer">
              View on GitHub
            </Link>
          </Button>
        </motion.div>
      </section>

      <section className="w-full max-w-5xl py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Explore Features</h2>
          <p className="text-muted-foreground mt-2">
            Discover the different ways to interact with our chat system
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 * (index + 1) }}
            >
              <Card className="h-full flex flex-col">
                <CardHeader>
                  <div className={`p-2 rounded-md w-fit mb-4 ${feature.color}`}>
                    {feature.icon}
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
                <CardContent className="flex-grow">
                  {/* Additional content could go here */}
                </CardContent>
                <CardFooter>
                  <Button asChild className="w-full">
                    <Link to={feature.path}>
                      Try it now <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </CardFooter>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}